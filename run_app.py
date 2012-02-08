from subprocess import Popen
import json

from flask import Flask
from flask import render_template, render_template_string
from flask import request

app = Flask(__name__)

@app.route('/')
def try_sed():
    kwargs = {}
    return render_template('index.html', **kwargs)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.data
    response = {"success": False}
    input = request.form.get("input")
    if input:
        if ";" in input or "$" in input or "|" in input:
            response["error"] = "Response cannot contain ; $ or |"
        elif not input.startswith("sed"):
            response["error"] = "Response must be a valid sed command."
        else:
            response = {"success": True}
            results = Popen(input.split(" "))
            print results.__dict__
    else:
        response["error"] = "Must enter a command."
    response = json.dumps(response)
    return render_template_string(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
