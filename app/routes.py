import os
import json
import time
import serial.tools.list_ports
from functools import wraps
from app import app
from app.local_if import PrintStatus, SerialPrint
from flask import render_template, flash, redirect, url_for, send_from_directory, request
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

desktopbrap_service = "desktopbraillerap"

local_ifx = SerialPrint ()
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Merci de vous connecter pour accéder à cette page."

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
            flash("Identifiants invalides.", "error")
        elif not user.is_active_account:
            flash("Ce compte a été désactivé.", "error")
        else:
            login_user(user)
            flash(f"Bienvenue, {user.username} !", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("index"))

    return render_template("login.html", form=form)

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

@app.route('/local/gcode_set_parameters', methods=['GET', 'POST'])
def gcode_set_parameters():
    """Set parameters value"""
    if request.method == "POST":
        print(request.json)
        print("request.json type", type(request.json))
        aparam = request.json
        param = aparam["options"]

        print("parameters", aparam, type(aparam))
        if aparam['service'] == "desktopbraillerap":
            try:
                for k, v in param.items():
                    if k in desktop_app_options:
                        desktop_app_options[k] = v

                save_parameters(aparam["service"], desktop_app_options)
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

@app.route('/desktopbrap/local/get_runtime_options')
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
def desktop_redirect_to_root():
    return redirect("/desktopbrap/index.html")

@app.route('/desktopbrap/static/media/<path>')
@app.route('/desktopbrap/static/css/<path>')
@app.route('/desktopbrap/static/js/<path>')
@app.route('/desktopbrap/<path:path>')
@app.route('/desktopbrap/')
def desktop_serve(path=""):
    print ("path=", path, "request ", request.path, "try folder ", app.static_folder + request.path)
    
    if path != "" and os.path.exists(app.static_folder + request.path):
        print ("file exist, serving ", app.static_folder + request.path)
        return send_from_directory(app.static_folder + request.path, "")
    else:
        return send_from_directory(app.static_folder + request.path, 'index.html')

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

@app.route("/users/<int:user_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def user_edit(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        abort(404)

    form = UserEditForm(obj=user)
    if form.validate_on_submit():
        duplicate_username = User.query.filter(
            User.username == form.username.data, User.id != user.id
        ).first()
        
        if duplicate_username:
            flash("Ce nom d'utilisateur est déjà pris.", "error")
            return render_template("user_form.html", form=form, user=user)

        user.username = form.username.data.strip()
        user.role = form.role.data
        user.is_active_account = form.is_active_account.data
        if form.new_password.data:
            user.set_password(form.new_password.data)

        db.session.commit()
        flash("Utilisateur mis à jour.", "success")
        return redirect(url_for("users_list"))

    return render_template("user_form.html", form=form, user=user)

@app.route("/users/<int:user_id>/delete", methods=["POST"])
@login_required
@admin_required
def user_delete(user_id):
    if user_id == current_user.id:
        flash("Vous ne pouvez pas supprimer votre propre compte.", "error")
        return redirect(url_for("users_list"))

    user = db.session.get(User, user_id)
    if user is None:
        abort(404)

    db.session.delete(user)
    db.session.commit()
    flash("Utilisateur supprimé.", "success")
    return redirect(url_for("users_list"))

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = UserEditForm(obj=current_user)
    form.role.render_kw = {"disabled": True}  # un utilisateur ne peut pas changer son propre rôle
    if form.validate_on_submit():
        duplicate_username = User.query.filter(
            User.username == form.username.data, User.id != current_user.id
        ).first()
        if duplicate_username:
            flash("Ce nom d'utilisateur est déjà pris.", "error")
            return render_template("user_form.html", form=form, user=current_user, is_self=True)
        
        current_user.username = form.username.data.strip()
        if form.new_password.data:
            current_user.set_password(form.new_password.data)
        db.session.commit()
        flash("Profil mis à jour.", "success")
        return redirect(url_for("profile"))

    return render_template("user_form.html", form=form, user=current_user, is_self=True)


@app.route("/process")
def process ():
    return render_template ('process.html', plist=ListProcess())
