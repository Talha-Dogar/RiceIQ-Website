from flask import jsonify, Blueprint
from bson.objectid import ObjectId
from datetime import datetime
from .. import mongo


dashboard_recent_records_bp = Blueprint('dashboard/recent_records', __name__)

@dashboard_recent_records_bp.route('/dashboard/recent_records/<user_id>', methods=['GET'])
def get_dashboard_data(user_id):
    """
    Get recent 5 rows each from Result and IdentificationResult collections for a user
    """
    try:
        # Convert user_id to ObjectId if needed
        try:
            user_id_obj = ObjectId(user_id)
        except:
            # If user_id is not in ObjectId format, use as is
            user_id_obj = user_id
        
        # Get recent 5 adulteration results
        adulteration_pipeline = [
            # Match records for this user with adulteration status
            {"$match": {"userID": user_id_obj, "status": "adulteration"}},
            
            # Join with Seller collection
            {"$lookup": {
                "from": "Seller",
                "localField": "sellerID",
                "foreignField": "_id",
                "as": "seller_info"
            }},
            
            # Join with Result collection
            {"$lookup": {
                "from": "Result",
                "localField": "resultID",
                "foreignField": "_id",
                "as": "result_info"
            }},
            
            # Unwind the arrays created by lookup
            {"$unwind": "$seller_info"},
            {"$unwind": "$result_info"},
            
            # Project only the fields we need
            {"$project": {
                "_id": 1,
                "sellerName": "$seller_info.companyName",
                "date": "$result_info.obtainAt",
                "adulterationStatus": "$result_info.adulterationStatus"
            }},
            
            # Sort by date (newest first)
            {"$sort": {"date": -1}},
            
            # Limit to 5 results
            {"$limit": 5}
        ]
        
        # Get recent 5 identification results
        identification_pipeline = [
            # Match records for this user with identification status
            {"$match": {"userID": user_id_obj, "status": "identification"}},
            
            # Join with IdentificationResult collection
            {"$lookup": {
                "from": "IdentificationResult",
                "localField": "resultID",
                "foreignField": "_id",
                "as": "identification_result"
            }},
            
            # Unwind the array created by lookup
            {"$unwind": "$identification_result"},
            
            # Project only the fields we need
            {"$project": {
                "_id": 1,
                "varietyName": "$identification_result.varietyName",
                "date": "$identification_result.obtainAt",
                "confidenceScore": "$identification_result.confidenceScore"
            }},
            
            # Sort by date (newest first)
            {"$sort": {"date": -1}},
            
            # Limit to 5 results
            {"$limit": 5}
        ]
        
        # Execute the aggregation pipelines
        adulteration_results = list(mongo.db.Record.aggregate(adulteration_pipeline))
        identification_results = list(mongo.db.Record.aggregate(identification_pipeline))
        
        # Format dates for JSON serialization
        for result in adulteration_results:
            if isinstance(result.get('date'), datetime):
                result['date'] = result['date'].isoformat()
        
        for result in identification_results:
            if isinstance(result.get('date'), datetime):
                result['date'] = result['date'].isoformat()
        
        # Return the results
        return jsonify({
            'adulteration_results': adulteration_results,
            'identification_results': identification_results
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

