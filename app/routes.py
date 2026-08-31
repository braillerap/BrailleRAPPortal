import os
import json
import time
import serial.tools.list_ports
from app.local_if import PrintStatus, SerialPrint
from app import app

from flask import render_template, flash, redirect, url_for, send_from_directory, request
from app.myform import MyForm
from app.utils.ListProcess import ListProcess


# main app user option
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

local_ifx = SerialPrint ()

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

    print ("backend get parameters: ", json.dumps(desktop_app_options))
    response = app.response_class(
        response=json.dumps(desktop_app_options),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/desktopbrap/local/get_runtime_options')
def desktop_get_optons():

    print ("backend get options: ", json.dumps(desktop_run_options))
    response = app.response_class(
        response=json.dumps(desktop_run_options),
        status=200,
        mimetype='application/json'
    )
    return response

    

@app.route('/desktopbrap/static/media/<path>')
@app.route('/desktopbrap/static/css/<path>')
@app.route('/desktopbrap/static/js/<path>')
@app.route('/desktopbrap/<path:path>')
@app.route('/desktopbrap/')
def serve(path=""):
    print ("path=", path, "request ", request.path, "try folder ", app.static_folder + request.path)
    
    if path != "" and os.path.exists(app.static_folder + request.path):
        print ("file exist, serving ", app.static_folder + request.path)
        return send_from_directory(app.static_folder + request.path, "")
    else:
        return send_from_directory(app.static_folder + request.path, 'index.html')

@app.route('/')
@app.route('/index')
def index():
    return render_template ('index.html')



@app.route("/process")
def process ():
    return render_template ('process.html', plist=ListProcess())
