# -*- coding: utf-8 -*-


from flask import Flask, url_for, request, json, jsonify #,Response
from functools import wraps
from flask import send_file

app = Flask(__name__)

#for welcome screen
@app.route('/')
def api_root():
    return 'Welcome!!!'

#example for checking all methods
@app.route('/echo', methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def api_echo():
    if request.method == 'GET':
        return "ECHO: GET\n"

    elif request.method == 'POST':
        return "ECHO: POST\n"

    elif request.method == 'PATCH':
        return "ECHO: PACTH\n"

    elif request.method == 'PUT':
        return "ECHO: PUT\n"

    elif request.method == 'DELETE':
        return "ECHO: DELETE"

#overriding error method
@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

@app.route('/get_image/<id>')
def get_image(id):
    return send_file('{}.jpg'.format(id), mimetype='image/jpg')
    
if __name__ == '__main__':
    app.run(debug=True)