from flask import Flask, request, redirect, abort
from hashlib import md5
import db_manager
from datetime import datetime
from constants import SLUG_LENGTH

db = db_manager.DbManager()

app = Flask(__name__)

@app.route("/shorten", methods=["GET"])
def shorten():
    url = request.args.get("url")
    expiry_str = request.args.get("expiry", default="")
    expiry_date = datetime.strptime(expiry_str, "%Y%m%d%H%M") if expiry_str else None
    if not url:
        abort(400), "Empty URL"
    slug = md5((url+expiry_str).encode("utf-8")).hexdigest()[:SLUG_LENGTH]
    db.insert_slug(url, slug, expiry_date)
    return f"{request.host}/{slug}"

@app.route("/<slug>", methods=["GET"])
def expand(slug):
    url = db.get_url_from_slug(slug)
    if not url:
        abort(404), "Unknown slug"
    return redirect(url)