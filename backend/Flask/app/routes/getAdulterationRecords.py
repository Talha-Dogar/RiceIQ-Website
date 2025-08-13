from flask import  jsonify, Blueprint
from bson.json_util import dumps, loads
import json
from ..models.adulteration_records import ( get_adulteration_records_grouped, delete_adulteration_record)


adulteration_records_bp = Blueprint('adulteration_records', __name__)
delete_adulteration_subrecord_bp = Blueprint('delete_adulteration_subrecord/<id>', __name__)



@adulteration_records_bp.route('/adulteration_records', methods=['GET'])
def get_adulteration_records():
    try:
        results = get_adulteration_records_grouped()
        # Convert MongoDB documents to JSON serializable format
        serialized_results = json.loads(dumps(results))
        print("Serialized results:", serialized_results)  # Debugging line
        return jsonify({
            "status": "success",
            "data": serialized_results
            # "total_samples": len(serialized_results)
        }), 200
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500



@delete_adulteration_subrecord_bp.route('/delete_adulteration_subrecord/<id>', methods=['DELETE'])
def delete_adulteration_record_route(id):
    return delete_adulteration_record(id)