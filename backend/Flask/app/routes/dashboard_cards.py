


# from flask import jsonify, Blueprint
# from bson.json_util import dumps, loads
# import json
# from .. import mongo
# from bson import ObjectId

# dashboard_cards_bp = Blueprint('dashboard_cards/<user_id>', __name__)

# @dashboard_cards_bp.route('/dashboard_cards/<user_id>', methods=['GET'])
# def get_analysis(user_id):
    
#     try:
#         # Convert user_id to appropriate format if necessary
#         user_id = ObjectId(user_id) if isinstance(user_id, str) else user_id
        
#         records_collection = mongo.db.Record
#         results_collection = mongo.db.Result
        
#         # Get total records count for this user
#         total_records = records_collection.count_documents({"userID": user_id})
        
#         # Get adulteration records count
#         adulteration_records = records_collection.count_documents({
#             "userID": user_id,
#             "status": "adulteration"
#         })
        
#         # Get identification records count
#         identification_records = records_collection.count_documents({
#             "userID": user_id,
#             "status": "identification"
#         })
        
#         # Get distinct count of sellers for this user
#         distinct_sellers_pipeline = [
#             {"$match": {"userID": user_id}},
#             {"$group": {"_id": "$sellerID"}},
#             {"$count": "distinct_sellers"}
#         ]
        
#         distinct_sellers_result = list(records_collection.aggregate(distinct_sellers_pipeline))
#         distinct_sellers_count = distinct_sellers_result[0]["distinct_sellers"] if distinct_sellers_result else 0
        
#         # Get adulterated and pure records counts by joining Record and Result tables
#         # For adulterated records
#         adulterated_pipeline = [
#             {"$match": {"userID": user_id, "status": "adulteration"}},
#             {"$lookup": {
#                 "from": "Result",
#                 "localField": "resultID",
#                 "foreignField": "_id",
#                 "as": "result"
#             }},
#             {"$unwind": "$result"},
#             {"$match": {"result.adulterationStatus": "True"}},
#             {"$count": "adulterated_count"}
#         ]
        
#         adulterated_result = list(records_collection.aggregate(adulterated_pipeline))
#         adulterated_count = adulterated_result[0]["adulterated_count"] if adulterated_result else 0
        
#         # For pure records
#         pure_pipeline = [
#             {"$match": {"userID": user_id, "status": "adulteration"}},
#             {"$lookup": {
#                 "from": "Result",
#                 "localField": "resultID",
#                 "foreignField": "_id",
#                 "as": "result"
#             }},
#             {"$unwind": "$result"},
#             {"$match": {"result.adulterationStatus": "False"}},
#             {"$count": "pure_count"}
#         ]
        
#         pure_result = list(records_collection.aggregate(pure_pipeline))
#         pure_count = pure_result[0]["pure_count"] if pure_result else 0
        
#         # Prepare and return response
#         response = {
#             "total_analysis": total_records,
#             "adulteration_analysis": adulteration_records,
#             "identification_analysis": identification_records,
#             "distinct_sellers": distinct_sellers_count,
#             "adulterated_count": adulterated_count,
#             "pure_count": pure_count
#         }
        
#         return jsonify(response), 200
        
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


from flask import jsonify, Blueprint
from bson.json_util import dumps, loads
import json
from .. import mongo
from bson import ObjectId
from datetime import datetime

dashboard_cards_bp = Blueprint('dashboard_cards/<user_id>', __name__)

@dashboard_cards_bp.route('/dashboard_cards/<user_id>', methods=['GET'])
def get_analysis(user_id):
    
    try:
        # Convert user_id to appropriate format if necessary
        user_id = ObjectId(user_id) if isinstance(user_id, str) else user_id
        
        records_collection = mongo.db.Record
        results_collection = mongo.db.Result
        
        # Get total records count for this user
        total_records = records_collection.count_documents({"userID": user_id})
        
        # Get adulteration records count
        adulteration_records = records_collection.count_documents({
            "userID": user_id,
            "status": "adulteration"
        })
        
        # Get identification records count
        identification_records = records_collection.count_documents({
            "userID": user_id,
            "status": "identification"
        })
        
        # Get distinct count of sellers for this user
        distinct_sellers_pipeline = [
            {"$match": {"userID": user_id}},
            {"$group": {"_id": "$sellerID"}},
            {"$count": "distinct_sellers"}
        ]
        
        distinct_sellers_result = list(records_collection.aggregate(distinct_sellers_pipeline))
        distinct_sellers_count = distinct_sellers_result[0]["distinct_sellers"] if distinct_sellers_result else 0
        
        # Get adulterated and pure records counts by joining Record and Result tables
        # For adulterated records
        adulterated_pipeline = [
            {"$match": {"userID": user_id, "status": "adulteration"}},
            {"$lookup": {
                "from": "Result",
                "localField": "resultID",
                "foreignField": "_id",
                "as": "result"
            }},
            {"$unwind": "$result"},
            {"$match": {"result.adulterationStatus": "True"}},
            {"$count": "adulterated_count"}
        ]
        
        adulterated_result = list(records_collection.aggregate(adulterated_pipeline))
        adulterated_count = adulterated_result[0]["adulterated_count"] if adulterated_result else 0
        
        # For pure records
        pure_pipeline = [
            {"$match": {"userID": user_id, "status": "adulteration"}},
            {"$lookup": {
                "from": "Result",
                "localField": "resultID",
                "foreignField": "_id",
                "as": "result"
            }},
            {"$unwind": "$result"},
            {"$match": {"result.adulterationStatus": "False"}},
            {"$count": "pure_count"}
        ]
        
        pure_result = list(records_collection.aggregate(pure_pipeline))
        pure_count = pure_result[0]["pure_count"] if pure_result else 0
        
 # Get monthly data for adulteration analyses
        adulteration_monthly_pipeline = [
            # Match adulteration records from this user
            {"$match": {"userID": user_id, "status": "adulteration"}},
            # Join with Result collection
            {"$lookup": {
                "from": "Result",
                "localField": "resultID",
                "foreignField": "_id",
                "as": "result"
            }},
            # Unwind the result array (skip records with no result)
            {"$unwind": {"path": "$result", "preserveNullAndEmptyArrays": False}},
            # Extract month from obtainAt date
            {"$project": {
                "month": {
                    "$month": {
                        "$cond": [
                            {"$eq": [{"$type": "$result.obtainAt"}, "string"]},
                            {"$dateFromString": {"dateString": "$result.obtainAt"}},
                            "$result.obtainAt"
                        ]
                    }
                },
                "status": "$status"
            }},
            # Group by month
            {"$group": {
                "_id": {"month": "$month"},
                "count": {"$sum": 1}
            }},
            # Sort by month
            {"$sort": {"_id.month": 1}}
        ]
        
        # Get monthly data for identification analyses
        identification_monthly_pipeline = [
            # Match identification records from this user
            {"$match": {"userID": user_id, "status": "identification"}},
            # Join with IdentificationResult collection
            {"$lookup": {
                "from": "IdentificationResult",
                "localField": "resultID",
                "foreignField": "_id",
                "as": "result"
            }},
            # Unwind the result array (skip records with no result)
            {"$unwind": {"path": "$result", "preserveNullAndEmptyArrays": False}},
            # Extract month from obtainAt date
            {"$project": {
                "month": {
                    "$month": {
                        "$cond": [
                            {"$eq": [{"$type": "$result.obtainAt"}, "string"]},
                            {"$dateFromString": {"dateString": "$result.obtainAt"}},
                            "$result.obtainAt"
                        ]
                    }
                },
                "status": "$status"
            }},
            # Group by month
            {"$group": {
                "_id": {"month": "$month"},
                "count": {"$sum": 1}
            }},
            # Sort by month
            {"$sort": {"_id.month": 1}}
        ]
        
        # Execute both pipelines
        adulteration_monthly_data = list(records_collection.aggregate(adulteration_monthly_pipeline))
        identification_monthly_data = list(records_collection.aggregate(identification_monthly_pipeline))
        
        # Create monthly data structure
        month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        monthly_data = []
        
        # Initialize data structure for all months
        for i, month_name in enumerate(month_names):
            monthly_data.append({
                "name": month_name,
                "identification": 0,
                "adulteration": 0
            })
        
        # Fill in adulteration data
        for item in adulteration_monthly_data:
            month_index = item["_id"]["month"] - 1  # Adjust for 0-based array
            monthly_data[month_index]["adulteration"] = item["count"]
        
        # Fill in identification data
        for item in identification_monthly_data:
            month_index = item["_id"]["month"] - 1  # Adjust for 0-based array
            monthly_data[month_index]["identification"] = item["count"]
        
        # Prepare and return response
        response = {
            "total_analysis": total_records,
            "adulteration_analysis": adulteration_records,
            "identification_analysis": identification_records,
            "distinct_sellers": distinct_sellers_count,
            "adulterated_count": adulterated_count,
            "pure_count": pure_count,
            "monthly_data": monthly_data
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500