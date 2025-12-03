from flask import jsonify
from app.services.mysql_service import MySQLClass


def get_homepage_data():
    db = MySQLClass.getInstance()
    results = db.select_query("SELECT * FROM User")
    print(results, flush=True)
    return jsonify({"status": "ok", "data": results})
