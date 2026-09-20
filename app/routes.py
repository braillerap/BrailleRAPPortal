"""
  
\file            routes.py
\brief           Routes definition for the flask application


Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge,
publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS LICENSED UNDER
                GNU GENERAL PUBLIC LICENSE
                    Version 3, 29 June 2007

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE
AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

This file is part of BrailleRAPPortal software.

SPDX-FileCopyrightText: 2026 Stephane GODIN <stephane@braillerap.org>

SPDX-License-Identifier: GPL-3.0 
  
"""

import os
import json
import sys
import serial.tools.list_ports
from functools import wraps
from app import app
from app.local_if import PrintStatus, SerialPrint
from flask import render_template, flash, redirect, url_for, send_from_directory, request, abort
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)
from app.forms import LoginForm, RegisterForm, UserCreateForm, UserEditForm
from app.utils.ListProcess import ListProcess
from app.database.models import db, login_manager, User, USER_ROLE, ADMIN_ROLE


# main app user option for desktop braillerap
desktop_app_options = {
    "comport": "COM1",
    "brailletbl": "70",
    "lang": "en",
    "Paper": {"width": 210, "height": 297, "usablewidth": 190, "usableheight": 250},
    "stepvectormm": 2.4,
    "SvgInterpol":False,
    "ZigZagBloc":False,
    "Optimbloc":False,
    "OptimLevel":0,
    "Speed":6000,
    "Accel":1500,
    "VectorIndex":0,
    "VectorSteps":[
        {"name":"Paper", "step":2.4, "lock":True},
        {"name":"Aluminum Can", "step":1.8, "lock":True}
    ],
    "PaperUsableSize":[
        {"name":"A4 (BrailleRAP XL)","width":210, "height":250, "lock":True},
        {"name":"A3 (BrailleRAP XL)","width":297, "height":420-47, "lock":True},
        {"name":"A4 (BrailleRAP)","width":190, "height":250, "lock":True}
    ],
    "PaperSize":[
        { "name": "A4 (BrailleRAP)", "width": 210, "height": 297 , "lock":True},
        { "name": "A3 (BrailleRAP XL)", "width": 297, "height": 420 , "lock":True}
        
    ],
    "SizeIndex":0,
    "UsableSizeIndex":0,
    "louisfilecheck":""
}

# runtime option to automate some actions
desktop_run_options = {
    "path_patterns": "",
    "path_svg": "",
    "direct_print": "",
}

# runtime option for accessbrap
access_app_options = {
    "comport": "COM1",
    "nbcol": "31",
    "nbline": "24",
    "linespacing": "0",
    "brailletbl": "81",
    "lang": "",
    "theme": "light",
    "xmax":"200",
    "orientation":"0",
    "offsetx":"1",
    "offsety":"2.5",
    "fast":0,
    "louisfilecheck":"",
    "backtranslation":"back",
    "brailleblackalign":"guess",
    "braillerender":"black",
    "pagenumbering":"0"
}

openstreet_app_options = {
    
    "lang": "en",
    "osmiso639": "fr",
    "focuspolicy":False,
    "accesskey":False
}

desktopbrap_service = "desktopbraillerap"
accessbrap_service = "accessbraillerap"
openstreet_service = "openstreettouch"

print ("##################### SYS PATH ################")
#add python osm processing to python path
osmpath = os.path.abspath('./reactapp/OpenStreetTouch/')
sys.path.insert (0, osmpath)
print ("###############################################")
#import osm processing module

from app.osmbridge import OSMBridge


##########################################################
# test CAIRO availability
###########################################################
cairosvg_available = False
try:
    from cairosvg import svg2png
    cairosvg_available = True
except:
    print ("cairosvg not available")
local_ifx = SerialPrint ()
osmbridge = OSMBridge ()

# 
# Init flask app
#
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "You must be loggged in to access this page"

#
# Create DB if empty
#
with app.app_context():
        db.create_all()

   

def get_parameter_fname (service):
    return app.static_folder + "/param/" + service + ".json"

def save_parameters(service, paramdict):
        """Save parameters in local json file"""
        try:
            print("data", paramdict)
            print("json", json.dumps(paramdict))
            fpath = get_parameter_fname(service)
            with open(fpath, "w", encoding="utf-8") as of:
                json.dump(paramdict, of)

        except Exception as e:
            print(e)

##########################################################
# USER MANAGEMENT
##########################################################
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

def admin_required(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return view_func(*args, **kwargs)
    return wrapped

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.strip()).first()
        if user is None or not user.check_password(form.password.data):
            flash("Incorrect login /password .", "error")
        elif not user.is_active_account:
            flash("User is not active.", "error")
        else:
            login_user(user)
            flash(f"Bienvenue, {user.username} !", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("index"))

    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash("Ce nom d'utilisateur est déjà pris.", "error")
            return render_template("register.html", form=form)

        # first user is admin
        is_first_user = User.query.count() == 0
        user = User(
            username=form.username.data.strip(),
            
            role=ADMIN_ROLE if is_first_user else USER_ROLE,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash("Compte créé avec succès. Vous pouvez vous connecter.", "success")
        return redirect(url_for("login"))

    return render_template("register.html", form=form)

##############################################################
# portal API
##############################################################
@app.route('/local/ISO639_country_code')
@login_required
def api_country_code():
    listiso = osmbridge.GetISO639_country_code ()
    response = app.response_class(
                            response=json.dumps(listiso),
                            status=200,
                            mimetype='application/json'
                        )
    return response

@app.route('/local/cairosvg')
@login_required
def api_cairosvg_status():
    response = app.response_class(
                            response=json.dumps(cairosvg_available),
                            status=200,
                            mimetype='application/json'
                        )
    return response

@app.route('/local/readtransportdata', methods=['GET', 'POST'])
@login_required
def api_readtransportdata ():
    if request.method == "POST":
        print(request.json)
        print("request.json type", type(request.json))
        aparam = request.json
        print (aparam)
        ret = osmbridge.ReadTransportData (aparam['city'], aparam['type'], 
                                           aparam['iso639_city_code'], aparam['place_id'])
        
        response = app.response_class(
                                response=json.dumps(ret),
                                status=200,
                                mimetype='application/json'
                            )
                    
        return response
    return "error"

@app.route('/local/readstreetmapdata', methods=['GET', 'POST'])
def api_readstreetmapdata ():
    if request.method == "POST":
        print(request.json)
        print("request.json type", type(request.json))
        aparam = request.json
        print (aparam)
                
        svg = osmbridge.ReadStreetMapData (aparam['latitude'], aparam['longitude'], aparam['radius'], aparam['building'],
                aparam['footpath'], aparam['polygon'], aparam['includeWater'], aparam['clipping'])

        response = app.response_class(
                                response=svg,
                                status=200,
                                mimetype='image/svg+xml'
                            )
        return response
    return "error"

@app.route('/local/gcode_set_parameters', methods=['GET', 'POST'])
@login_required
def gcode_set_parameters():
    """Set parameters value"""
    if request.method == "POST":
        print(request.json)
        print("request.json type", type(request.json))
        aparam = request.json
        param = aparam["options"]

        print("parameters", aparam, type(aparam))
        if aparam['service'] == desktopbrap_service:
            try:
                for k, v in param.items():
                    if k in desktop_app_options:
                        desktop_app_options[k] = v

                save_parameters(aparam["service"], desktop_app_options)
            except Exception as e:
                print(e)
        elif aparam["service"] == accessbrap_service:
            try:
                for k, v in param.items():
                    if k in access_app_options:
                        access_app_options[k] = v

                save_parameters(aparam["service"], access_app_options)
            except Exception as e:
                print(e)
        status = PrintStatus ()
        response = app.response_class(
                        response=json.dumps(status.getjson()),
                        status=200,
                        mimetype='application/json'
                    )
            
        return response

@app.route('/local/gcode_print', methods=['GET', 'POST'])
@login_required
def gcode_print ():

    status = PrintStatus ()

    if request.method == "POST":
        print(request.json)
        print("request.json type", type(request.json))
        param = request.json
        status = local_ifx.PrintGcode (param['gcode'], param['port'])

    print ("print status ", json.dumps(status))
    response = app.response_class(
                response=json.dumps(status),
                status=200,
                mimetype='application/json'
            )
    

    return response        


@app.route('/local/gcode_cancelprint', methods=['GET', 'POST'])
@login_required
def gcode_cancelprint ():

    status = {"error":1}

    if request.method == "POST":
        gcode = request.json
        print (gcode)
        local_ifx.CancelPrint ()
        status = {"error":0}
        
    response = app.response_class(
                response=json.dumps(status),
                status=200,
                mimetype='application/json'
            )
    return response        

@app.route('/local/gcode_get_serial')
@login_required
def gcode_get_serial ():
    data = []
    try:
        ports = serial.tools.list_ports.comports()
        for port in ports:
           
            data.append(
                {
                    "device": port.device,
                    "description": port.description,
                    "name": port.name,
                    "product": port.product,
                    "manufacturer": port.manufacturer,
                }
            )
        print(data)
    except Exception as e:
        print(e)

    # check if com port in parameters is present in port enumeration
    if not any(d.get("device", "???") == desktop_app_options["comport"] for d in data):
        print("adding com port in parameters")
        data.append(
            {
                "device": desktop_app_options["comport"],
                "description": "????",
                "name": "????",
                "product": "????",
                "manufacturer": "????",
            }
        )

    # dump data in json format for frontend
    
    response = app.response_class(
            response=json.dumps(data),
            status=200,
            mimetype='application/json'
        )
    return response
    

@app.route('/desktopbrap/local/get_parameters')
@login_required
def desktop_get_parameters():
    try:
        fpath = get_parameter_fname(desktopbrap_service)
        print ("loading param from:", fpath)
        with open(fpath, "r", encoding="utf-8") as inf:
            data = json.load(inf)
            for k, v in data.items():
                if k in desktop_app_options:
                    desktop_app_options[k] = v

    except Exception as e:
        print(e)

    print ("backend get parameters: ", json.dumps(desktop_app_options)) 

    response = app.response_class(
        response=json.dumps(desktop_app_options),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/accessbrap/local/get_parameters')
@login_required
def access_get_parameters():
    try:
        fpath = get_parameter_fname(accessbrap_service)
        print ("loading param from:", fpath)
        with open(fpath, "r", encoding="utf-8") as inf:
            data = json.load(inf)
            for k, v in data.items():
                if k in access_app_options:
                    access_app_options[k] = v

    except Exception as e:
        print(e)

    print ("backend get parameters: ", json.dumps(access_app_options)) 

    response = app.response_class(
        response=json.dumps(access_app_options),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/openstreet/local/get_parameters')
@login_required
def openstreet_get_parameters():
    try:
        fpath = get_parameter_fname(openstreet_service)
        print ("loading param from:", fpath)
        with open(fpath, "r", encoding="utf-8") as inf:
            data = json.load(inf)
            for k, v in data.items():
                if k in access_app_options:
                    access_app_options[k] = v

    except Exception as e:
        print(e)

    print ("backend get parameters: ", json.dumps(openstreet_app_options)) 

    response = app.response_class(
        response=json.dumps(openstreet_app_options),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/desktopbrap/local/get_runtime_options')
@login_required
def desktop_get_options():

    print ("backend get options: ", json.dumps(desktop_run_options))
    response = app.response_class(
        response=json.dumps(desktop_run_options),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route ('/desktopbrap/parameter')
@app.route ('/desktopbrap/print')
@app.route ('/desktopbrap/file')
@app.route ('/desktopbrap/addsvg')
@app.route ('/desktopbrap/addtext')
@app.route ('/desktopbrap/position')
@app.route ('/desktopbrap/pattern')
@app.route ('/desktopbrap/data')
@login_required
def desktop_redirect_to_root():
    return redirect("/desktopbrap/index.html")

@app.route('/openstreet/static/media/<path>')
@app.route('/openstreet/static/css/<path>')
@app.route('/openstreet/static/js/<path>')
@app.route('/openstreet/<path:path>')
@app.route('/openstreet/')
@app.route('/accessbrap/static/media/<path>')
@app.route('/accessbrap/static/css/<path>')
@app.route('/accessbrap/static/js/<path>')
@app.route('/accessbrap/<path:path>')
@app.route('/accessbrap/')
@app.route('/desktopbrap/static/media/<path>')
@app.route('/desktopbrap/static/css/<path>')
@app.route('/desktopbrap/static/js/<path>')
@app.route('/desktopbrap/<path:path>')
@app.route('/desktopbrap/')
@login_required
def app_serve(path=""):
    print ("path=", path, "request ", request.path, "try folder ", app.static_folder + request.path)
    
    if path != "" and os.path.exists(app.static_folder + request.path):
        print ("file exist, serving ", app.static_folder + request.path)
        return send_from_directory(app.static_folder + request.path, "")
    else:
        return send_from_directory(app.static_folder + request.path, 'index.html')

@app.route ('/accessbrap/parameter')
@app.route ('/accessbrap/print')
@login_required
def access_redirect_to_root():
    return redirect("/accessbrap/index.html")

@app.route ('/openstreet/parameter')
@app.route ('/openstreet/transport')
@app.route ('/openstreet/cmap')
@login_required
def open_redirect_to_root():
    return redirect("/openstreet/index.html")


    
@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template ('index.html')


@app.route("/users")
@login_required
@admin_required
def users_list():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("users.html", users=users)

@app.route("/users/new", methods=["GET", "POST"])
@login_required
@admin_required
def user_create():
    form = UserCreateForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data.strip()).first():
            flash("User already exist.", "error")
            return render_template("user_create.html", form=form)
        

        user = User(
            username=form.username.data.strip(),
    
            role=form.role.data,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash(f"User « {user.username} » Created.", "success")
        return redirect(url_for("users_list"))

    return render_template("user_create.html", form=form)

@app.route("/users/<int:user_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def user_edit(user_id):
    
    user = db.session.get(User, user_id)
    print ("user edit", user)
    if user is None:
        abort(404)

    form = UserEditForm(obj=user)
    if form.validate_on_submit():
        duplicate_username = User.query.filter(
            User.username == form.username.data, User.id != user.id
        ).first()
        if duplicate_username:
            flash("User already exist.", "error")
            return render_template("user_form.html", form=form, user=user)
        

        user.username = form.username.data.strip()
        user.role = form.role.data
        user.is_active_account = form.is_active_account.data
        if form.new_password.data:
            user.set_password(form.new_password.data)

        db.session.commit()
        flash("User profile updated.", "success")
        return redirect(url_for("users_list"))

    return render_template("user_form.html", form=form, user=user)

@app.route("/users/<int:user_id>/delete", methods=["POST"])
@login_required
@admin_required
def user_delete(user_id):
    if user_id == current_user.id:
        flash("You can't delete your account.", "error")
        return redirect(url_for("users_list"))

    user = db.session.get(User, user_id)
    if user is None:
        abort(404)

    db.session.delete(user)
    db.session.commit()
    flash("User deleted.", "success")
    return redirect(url_for("users_list"))

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = UserEditForm(obj=current_user)
    form.role.render_kw = {"disabled": True}  # user can't change their role
    if form.validate_on_submit():
        duplicate_username = User.query.filter(
            User.username == form.username.data, User.id != current_user.id
        ).first()
        
        if duplicate_username:
            flash("User already exist.", "error")
            return render_template("user_form.html", form=form, user=current_user, is_self=True)
        
        current_user.username = form.username.data.strip()
        
        if form.new_password.data:
            current_user.set_password(form.new_password.data)
        db.session.commit()
        flash("User profile updated.", "success")
        return redirect(url_for("profile"))

    return render_template("user_form.html", form=form, user=current_user, is_self=True)


@app.route("/process")
def process ():
    return render_template ('process.html', plist=ListProcess())

@app.errorhandler(403)
def forbidden(_e):
    return render_template("error.html", code=403, message="Access denied."), 403

@app.errorhandler(404)
def not_found(_e):
    return render_template("error.html", code=404, message="Page does not exist."), 404