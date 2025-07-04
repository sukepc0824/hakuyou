from flask import Flask, render_template, request, redirect, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)
DATA_DIR = "data"
BOOTH_FILE = os.path.join(DATA_DIR, "booths.json")
NOTIFY_FILE = os.path.join(DATA_DIR, "notifications.json")


def load_booths():
    with open(BOOTH_FILE, encoding="utf-8") as f:
        return json.load(f)


def save_booths(data):
    with open(BOOTH_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_notifications():
    with open(NOTIFY_FILE, encoding="utf-8") as f:
        return json.load(f)


def save_notifications(data):
    with open(NOTIFY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@app.route("/")
def index():
    booths = load_booths()
    notifs = load_notifications()
    return render_template("index.html", booths=booths, notifications=notifs)


@app.route("/admin")
def admin():
    booths = load_booths()
    return render_template("admin.html", booths=booths)


@app.route("/admin/<class_id>")
def admin_class(class_id):
    booths = load_booths()
    target = next((b for b in booths if b["class"] == class_id), None)
    if target:
        return render_template("admin.html", class_id=class_id, booth_name=target["booth_name"], status=target["status"])
    else:
        return render_template("admin.html", class_id=class_id, booth_name="", status=1)


@app.route("/update_status", methods=["POST"])
def update_status():
    cls = request.form["class"]
    new_status = int(request.form["status"])
    new_booth_name = request.form["booth_name"]
    booths = load_booths()
    for booth in booths:
        if booth["class"] == cls:
            booth["status"] = new_status
            booth["booth_name"] = new_booth_name
            break
    else:
        booths.append({"class": cls, "booth_name": new_booth_name, "status": new_status})
    save_booths(booths)
    return redirect(f"/admin/{cls}")



@app.route("/notify", methods=["GET", "POST"])
def notify():
    if request.method == "POST":
        msg = request.form["message"]
        notifs = load_notifications()
        notifs.insert(0, {
            "time": datetime.now().strftime("%H:%M"),
            "message": msg
        })
        save_notifications(notifs)
        return redirect("/notify")
    notifs = load_notifications()
    return render_template("notify.html", notifications=notifs)

#HTML側
@app.route("/api/booths")
def api_booths():
    return jsonify(load_booths())

@app.route("/api/notifications")
def api_notifications():
    return jsonify(load_notifications())


if __name__ == "__main__":
    app.run(debug=True)
