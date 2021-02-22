from flask import Flask, request, jsonify, json
from flask_pymongo import PyMongo
from marshmallow import Schema, fields, ValidationError
from bson.json_util import dumps
from json import loads
from datetime import datetime

with open('store.txt') as f:
    upass = f.readline().strip()

uri_update1 = "mongodb+srv://{}:{}@ecse3038-cluster.renxl.mongodb.net/LAB3?retryWrites=true&w=majority".format(
    upass, upass)

app = Flask(__name__)
app.config["MONGO_URI"] = uri_update1
mongo = PyMongo(app)

profile_obj = {}


class TonKschema(Schema):
    location = fields.String(required=True)
    lat = fields.String(required=True)
    long = fields.String(required=True)
    percentage_full = fields.Integer(required=True)

# GET /profile


@app.route("/profile")
def get_profile():
    return profile_obj

# POST /profile


@app.route("/profile", methods=["POST"])
def post_profile():
    profile_obj["username"] = request.json["username"]
    profile_obj["role"] = request.json["role"]
    profile_obj["color"] = request.json["color"]
    profile_obj["last_updated"] = datetime.now()

    return {
        "success": True,
        "data": profile_obj
    }

# PATCH /profile


@app.route("/profile", methods=["PATCH"])
def update_profile():
    if "username" in request.json:
        profile_obj["username"] = request.json["username"]

    if "role" in request.json:
        profile_obj["role"] = request.json["role"]

    if "color" in request.json:
        profile_obj["color"] = request.json["color"]

    profile_obj["last_updated"] = datetime.now()

    return {
        "success": True,
        "data": profile_obj
    }

# GET /data


@app.route("/data")
def data_get():
    TonKs = mongo.db.TonKs.find()
    return jsonify(loads(dumps(TonKs)))


# POST /data
@app.route("/data", methods=["POST"])
def data_post():
    try:
        TonKer = TonKschema().load(request.json)
        TonKerID = mongo.db.TonKs.insert_one(TonKer).inserted_id
        TonKerRET = mongo.db.TonKs.find_one(TonKerID)
        return loads(dumps(TonKerRET))
    except ValidationError as ve:
        return ve.messages, 400


# PATCH /data/:id
@app.route('/data/<ObjectId:id>', methods=["PATCH"])
def data_patch(id):
    mongo.db.TonKs.update_one({"_id": id}, {"$set": request.json})
    TonK = mongo.db.TonKs.find_one(id)
    return loads(dumps(TonK))


# DELETE /data/:id
@app.route('/data/<ObjectId:id>', methods=["DELETE"])
def data_delete(id):
    tank_result = mongo.db.TonKs.delete_one({"_id": id})
    if tank_result.deleted_count == 1:
        return {
            "success": True
        }
    else:
        return {
            "success": False
        }, 400


if __name__ == "__main__":
    app.run(debug=True)
