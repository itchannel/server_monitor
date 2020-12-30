import psutil
import flask
import json

def diskstats(disk):
	obj_Disk = psutil.disk_usage(disk)

	total = obj_Disk.total / (1024.0 ** 3),"GB"
	used = obj_Disk.used / (1024.0 ** 3),"GB"
	free = obj_Disk.free / (1024.0 ** 3),"GB"
	percent = obj_Disk.percent
	return {"name":disk, "total":total, "used":used,"free":free,"percent":percent}

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/stats', methods=["GET"])
def stats():
	test = diskstats('/')
	data = { "disks":test}
	
	return json.dumps(data)


with open('monitor.conf', 'r') as f:
        config = json.load(f)


app.run(host="0.0.0.0", port=5001)
