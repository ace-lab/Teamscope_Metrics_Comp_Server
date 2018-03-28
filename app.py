from flask import Flask, request, jsonify, redirect, url_for
import os
import socket
from tddchecker_comp import *
from metric_tddchecker import *
from github_comp_metric import github_comp
from travis_comp_metric import get_all_travis_data

app = Flask(__name__)

@app.route("/check_tdd_commits")
def check_tdd_commits():
    if request.args["preemptive"] == "True":
        return jsonify(premptive_calculations(request.args["repo"]))
    else:
        return jsonify(check_commits(request.args["repo"], request.args["branch"]))


@app.route("/compute_tdd_metric")
def compute_metric():
    compute_tdd_metric(request.args["repo"])
    return redirect(url_for("return_tdd_metric", repo=request.args["repo"]))

@app.route("/return_tdd_metric")
def return_tdd_metric():
    try:
        os.chdir(os.path.expanduser("~/repos"))
        matchObj = re.match(r'.*\/(.*)', request.args["repo"])
        short_name = matchObj.group(1)
        os.chdir("./{0}".format(short_name))
        json1_file = open("tddresults/result.json")
        json1_str = json1_file.read()
        data = json.loads(json1_str)
    except:
        data = {"success": False, "reason": "File does not exist"}
    return jsonify(data)

@app.route("/calc_gh_data")
def calc_gh_data():
    return jsonify(github_comp(request.args["repo"]))

@app.route("/calc_travis_data")
def calc_travis_data():
    return jsonify(get_all_travis_data(request.args["repo"]))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=43000)
