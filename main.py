import sys
sys.path.append("py")

from flask import Flask, render_template, request, jsonify, redirect, send_from_directory
# from instance import *
import json
import os
import uuid
import datetime
import random
import string
import shutil
import importlib

def randomStringDigits(stringLength = 10):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

def get_setting(pid):
    setting = "./project/"+str(pid)+"/setting.json"
    if os.path.exists(setting):
        with open(setting) as json_file:
            data = json.load(json_file)
        return data
    else:
        return None

def get_function(pid=""):
    file = "./project/"+str(pid)+"/functions.py"
    if not os.path.exists(file):
        file = "./py/functions_default.py"
    data = {}
    keys = ["workermodel","taskmodel","workerslt","taskgen","taskassign","others"]
    cur_key = ""
    f = open(file)
    for line in f:
        if len(line) > 0 and line[0]=="#" and line[1:].replace("\n","") in keys:
            cur_key = line[1:].replace("\n","")
            data[cur_key] = ""
        elif cur_key != "":
            data[cur_key] += line
    return data

default_setting = {"title": "", "pid": "", "file": "", "price": "10", "n_judgements": "3", "worker_arrival_interval": "30", "dropout_time": "1800", "worker_classification": 3, "worker_property_names": ["class_name", "distribution", "execution_time"], "worker_properties": [["class1", "class2", "class3"], ["0.333", "0.333", "0.333"], ["100", "200", "300"]], "runtime": "3600", "time_stamp": "600", "repeat_times": "5", "n_data_rows": "3", "created": "", "modified": "", "data_selection": "default", "task_assignment": "default", "worker_selection": "none"}

default_function = get_function()

app = Flask(__name__, static_url_path='')


@app.route('/')
@app.route('/index.html')
def index():
    pids = []
    titles = []
    created = []
    modified =[]
    for root, dirs, files in os.walk("./project", topdown=False):
        for name in dirs:
            if "archived_" in name: continue
            data = get_setting(name)
            if data is not None:
                pids.append(name)
                titles.append(data["title"])
                created.append(data["created"])
                modified.append(data["modified"])

    # sort according to modified time
    for i in range(1, len(pids)):
        key = datetime.datetime.strptime(modified[i], '%Y-%m-%d %H:%M:%S').timestamp()
        pids_tmp = pids[i]
        titles_tmp = titles[i]
        created_tmp = created[i]
        modified_tmp = modified[i]

        j = i-1
        while j >= 0 and key > datetime.datetime.strptime(modified[j], '%Y-%m-%d %H:%M:%S').timestamp():
                pids[j+1] = pids[j]
                titles[j+1] = titles[j]
                created[j+1] = created[j]
                modified[j+1] = modified[j]
                j -= 1

        pids[j+1] = pids_tmp
        titles[j+1] = titles_tmp
        created[j+1] = created_tmp
        modified[j+1] = modified_tmp

    return render_template('index.html', len=len(titles), pids=pids, titles=titles, created=created, modified=modified)


@app.route('/new')
def newsettings():
    title = request.args.get('title')
    if len(title) > 0:
        data = default_setting
        data["title"] = title
        data["pid"] = randomStringDigits()
        data["created"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data["modified"] = data["created"]
        return render_template('settings.html', data=data)
    else:
        return "Page Not Found!"


@app.route('/settings')
def settings():
    pid = request.args.get('pid')
    data = get_setting(pid)
    if data is not None:
        return render_template('settings.html', data=data)
    else:
        return "Page Not Found!"


@app.route('/plugins')
def plugins():
    pid = request.args.get('pid')
    data = get_setting(pid)
    function = get_function(pid)
    if data is not None:
        return render_template('plugins.html', data=data, function=function)
    else:
        return "Page Not Found!"


@app.route('/results')
def results():
    pid = request.args.get('pid')
    data = get_setting(pid)
    data["output"] = []
    if os.path.exists("./output/"+pid+"/fig"):
        for root, dirs, files in os.walk("./output/"+pid+"/fig", topdown=False):
            for name in files:
                data["output"].append(name)
    if data is not None:
        return render_template('results.html', data=data)
    else:
        return "Page Not Found!"


@app.route('/fig')
def data():
    pid = request.args.get('pid')
    prop  = request.args.get('prop')
    print("./output/"+pid+"/fig/"+prop+".png")
    return send_from_directory('.', "output/"+pid+"/fig/"+prop+".png")


@app.route('/save',methods=['POST'])
def save():
    data = request.get_json(force=True)
    data["modified"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if not os.path.exists("project"):
        os.makedirs("project")
    if not os.path.exists("project/"+data["pid"]):
        os.makedirs("project/"+data["pid"])
    f = open("project/"+data["pid"]+"/setting.json","w")
    f.write(json.dumps(data))
    f.close()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


@app.route('/savefunc',methods=['POST'])
def savefunc():
    data = request.get_json(force=True)
    pid = data["pid"]
    if not os.path.exists("project"):
        os.makedirs("project")
    if not os.path.exists("project/"+data["pid"]):
        os.makedirs("project/"+data["pid"])
        f = open("project/"+pid+"/setting.json","w")
        f.write(json.dumps(default_setting))
        f.close()
    # update modified time
    data2 = get_setting(pid)
    data2["modified"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    f = open("project/"+pid+"/setting.json","w")
    f.write(json.dumps(data2))
    f.close()
    # save functions
    f = open("project/"+data["pid"]+"/functions.py","w")
    for key in data.keys():
        if key != "pid":
            f.write("#"+key+"\n"+data[key])
            if data[key][-1] != "\n": f.write("\n")
    f.close()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


@app.route('/del')
def delete():
    pid = request.args.get('pid')
    if os.path.exists("project/"+pid):
        if not os.path.exists("project/archived"):
            os.makedirs("project/archived")
        shutil.move("project/"+pid,"project/archived/"+pid)
    return redirect("/")


@app.route('/dup')
def duplicate():
    pid = request.args.get('pid')
    if os.path.exists("project/"+pid):
        newpid = randomStringDigits()
        os.makedirs("project/"+newpid)
        src_files = os.listdir("project/"+pid)
        for file_name in src_files:
            full_file_name = os.path.join("project/"+pid, file_name)
            if os.path.isfile(full_file_name):
                shutil.copy(full_file_name, "project/"+newpid+"/"+file_name)
        data = get_setting(newpid)
        data["pid"] = newpid
        data["title"] += " Copy"
        data["created"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data["modified"] = data["created"]
        f = open("project/"+newpid+"/setting.json","w")
        f.write(json.dumps(data))
        f.close()
    return redirect("/")


@app.route('/run')
def run():
    pid = request.args.get('pid')
    if os.path.exists("project/"+pid+"/functions.py"):
        shutil.copyfile("project/"+pid+"/functions.py","py/functions.py")
    else:
        shutil.copyfile("py/functions_default.py","py/functions.py")

    Ins = __import__("instance")
    importlib.reload(Ins)
    i = Ins.Instance("project/"+pid+"/setting.json")
    i.run()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

if __name__ == '__main__':
    app.run()
