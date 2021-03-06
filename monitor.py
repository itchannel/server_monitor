import json
import docker
import psutil
from flask import Flask, request
import os


# Process Disk Stats for given mount points
def diskstats(disks):
    diskret = []
    for disk in disks:
        obj_Disk = psutil.disk_usage(disk["location"])
        total = obj_Disk.total / (1024.0 ** 3), "GB"
        used = obj_Disk.used / (1024.0 ** 3), "GB"
        free = obj_Disk.free / (1024.0 ** 3), "GB"
        percent = obj_Disk.percent
        diskret.append({
            "name": disk["location"],
            "total": total, "used": used,
            "free": free,
            "percent": percent
            })
    return diskret


# Get CPU Status
def cpustats():
    cpu_percent = psutil.cpu_percent(interval=1)
    data = {"cpu_usage_percent": cpu_percent}
    return data


# Docker containers

def dockerstats():
    client = docker.from_env()

    containers = client.containers.list()
    data = []
    for container in containers:
        data.append({
            "Name": container.attrs["Name"],
            "Status": container.attrs["State"]["Status"],
            "Attributes": container.attrs
        })
    return data


app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/stats', methods=["GET"])
def stats():
    disks = diskstats(config["disks"])
    cpu = cpustats()
    pc_powered = None
    if os.name == "nt":
        pc_powered = True
    docker = ""
    if "docker" in config:
        if config["docker"]["enabled"] is True:
            docker = dockerstats()
    data = {
        "disks": disks,
        "cpu": cpu,
        "pc_powered": pc_powered,
        "docker": docker
    }
    return json.dumps(data)


@app.route('/suspend', methods=["GET", "POST"])
def suspend():
    if request.method == "GET":
        if os.name == "nt":
            return {"pc_powered": True}
    else:
        data = request.get_json()
        print(data)
        if data["active"] == "false":
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")


with open('monitor.conf', 'r') as f:
    config = json.load(f)

print(os.name)
app.run(host="0.0.0.0", port=5001)
