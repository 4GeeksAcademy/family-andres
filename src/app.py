"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

jackson_family.add_member({
                "first_name": "John",
                "age": 33,
                "lucky_numbers": [7, 13, 22]
            })
jackson_family.add_member({
                "first_name": "Jane",
                "age": 35,
                "lucky_numbers": [10, 14, 3]
            })
jackson_family.add_member({
                "first_name": "Jimmy",
                "age": 5,
                "lucky_numbers": [1]
            })

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    if members is None:
        return jsonify({"error": "Members not found"}), 400
    return jsonify(members), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    print(member)
    if member is None:
        return jsonify({"error": "Member not found"}), 400
    return jsonify(member), 200

@app.route('/member', methods=['POST'])
def add_member():
    member_data = request.get_json()
    first_name = member_data.get("first_name", None)
    age = member_data.get("age", None)
    lucky_numbers = member_data.get("lucky_numbers", None)

    if first_name is None:
        return jsonify({"error": "first_name is required"}), 400
    if age is None:
        return jsonify({"error": "age is required"}), 400
    if lucky_numbers is None:
        return jsonify({"error": "lucky_numbers are required"}), 400
    
    jackson_family.add_member(member_data)
    return jsonify(member_data), 200

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    result = jackson_family.delete_member(member_id)
    if result["done"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 400

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)

