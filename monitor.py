import json
import psutil
import flask
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
            "name": disk,
            "total": total, "used": used,
            "free": free,
            "percent": percent
            })
    return diskret


# Get CPU Status
def cpustats():
    print("Coming Soon")


app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/stats', methods=["GET"])
def stats():
    disks = diskstats(config["disks"])
    data = {"disks": disks}
    return json.dumps(data)


@app.route('/suspend', methods=["GET"])
def suspend():
    if os.name == "nt":
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")


with open('monitor.conf', 'r') as f:
    config = json.load(f)

print(os.name)
app.run(host="0.0.0.0", port=5001)
