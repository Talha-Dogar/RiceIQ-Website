from datetime import datetime
from bson.json_util import dumps, loads
from .. import mongo
from bson import ObjectId
from flask import Blueprint, jsonify
import json
from ..models.identification_records import get_identification_records, delete_identification_record
# Create a blueprint for identification routes
identification_records_bp = Blueprint('identification/records', __name__)
delete_identification_record_bp = Blueprint('delete_identification_record/<id>', __name__)

@identification_records_bp.route('/identification/records', methods=['GET'])
def get_records():
    """
    Endpoint to retrieve identification records.
    Returns a list of identification records with data from Record, IdentificationResult, and Sample collections.
    """
    try:
        results = get_identification_records()
        response = {
            "status": "success",
            "data": results
        }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@delete_identification_record_bp.route('/delete_identification_record/<id>', methods=['DELETE'])
def delete_identification_record_route(id):
    return delete_identification_record(id)