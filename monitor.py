import psutil
import flask
import json


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


app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/stats', methods=["GET"])
def stats():
    test = diskstats(config["disks"])
    data = {"disks": test}
    return json.dumps(data)


with open('monitor.conf', 'r') as f:
    config = json.load(f)


app.run(host="0.0.0.0", port=5001)
