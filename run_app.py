import json

from flask import Flask
from flask import render_template, render_template_string
from flask import request, session

import command_execute
from command_execute import CommandException
from progress import Progress

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHZ!jmN]LWX/,?RT'

@app.route('/')
def try_sed():
    render_dict = {}
    if "progress" not in session:
        session["progress"] = Progress()
    render_dict["dialog"] = session["progress"].get_dialog()
    return render_template('index.html', **render_dict)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.data
    response = {"success": False}
    command = request.form.get("input")
    entry_check = {"success": False}
    result_check = {"success": False}
    if "progress" not in session:
        print "new session"
        session["progress"] = Progress()
    print session["progress"].get_step()
    if command:
        progress = session["progress"]
        entry_check = progress.check_entry(command)
        if entry_check["continue"]:
            try:
                result = command_execute.execute(command)
            except CommandException, error:
                response["error"] = "Error: %s" %error
            else:
                response = {"success": True, "result": result}
                result_check = progress.check_result(result)
        else:
            response = {"success": True, "result": ""}
    else:
        response["error"] = "Must enter a command."
    if entry_check["success"] or result_check["success"]:
        print "next step"
        progress.next_step()
    dialog = progress.get_dialog()
    response["dialog"] = dialog
    response = json.dumps(response)
    return render_template_string(response)

@app.route('/reset_step', methods=['POST'])
def reset_step():
    session["progress"] = Progress()
    return "success"

@app.route('/get_step', methods=['POST'])
def reset_step():
    step = session["progress"].get_step()
    return str(step)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
