from datetime import datetime
from bson.json_util import dumps, loads
from .. import mongo
from bson import ObjectId
from flask import Blueprint, jsonify

def get_identification_records():
    """
    Endpoint to retrieve identification records.
    Returns a list of identification records with data from Record, IdentificationResult, and Sample collections.
    """
    try:
        # Debug information
        print("Collections:", mongo.db.list_collection_names())
        identification_count = mongo.db.Record.count_documents({"status": "identification"})
        print(f"Found {identification_count} records with status='identification'")
        
        if identification_count == 0:
            print("No matching records found. Check if 'identification' is the correct status value.")
            return jsonify([])
        
        # Pipeline for retrieving identification records
        pipeline = [
            # Match identification records
            {
                "$match": {
                    "status": "identification"
                }
            },
            # Join with IdentificationResult collection
            {
                "$lookup": {
                    "from": "IdentificationResult",
                    "localField": "resultID",
                    "foreignField": "_id",
                    "as": "identification_data"
                }
            },
            # Unwind the identification_data array
            {
                "$unwind": {
                    "path": "$identification_data",
                    "preserveNullAndEmptyArrays": False
                }
            },
            # Join with Sample collection using sampleID from identification_data
            {
                "$lookup": {
                    "from": "Sample",
                    "localField": "identification_data.sampleID",
                    "foreignField": "_id",
                    "as": "sample_data"
                }
            },
            # Unwind the sample_data array
            {
                "$unwind": {
                    "path": "$sample_data",
                    "preserveNullAndEmptyArrays": False
                }
            },
            # Project fields we need
            {
                "$project": {
                    "_id": 0,
                    "record_id": { "$toString": "$resultID" },
                    "img_url": "$sample_data.imgUrl",
                    "total_grains": "$identification_data.total_grains",
                    "varietyName": "$identification_data.varietyName",
                    "confidence": "$identification_data.confidenceScore",
                    "obtainAt": "$identification_data.obtainAt"
                }
            },
            # Sort by obtainAt date (newest first)
            {
                "$sort": {
                    "obtainAt": -1
                }
            }
        ]
        
        # Execute the aggregation pipeline
        results = list(mongo.db.Record.aggregate(pipeline))
        print(f"Final results count: {len(results)}")
        
        return results

    except Exception as e:
        print(f"Error retrieving identification records: {e}")
        return jsonify({"error": str(e)}), 500


def delete_identification_record(record_id):
    """
    Endpoint to delete a specific adulteration record by ID.
    Also deletes the associated Result and Sample records.
    
    Args:
        record_id (str): The ID of the record to delete
        
    Returns:
        JSON response with deletion status
    """
    try:
        # Convert string ID to ObjectId
        record_id_obj = ObjectId(record_id)
        
        # Find the record first to verify it exists and has status "identification"
        record = mongo.db.Record.find_one({"_id": record_id_obj, "status": "identification"})
        
        if not record:
            return jsonify({
                "success": False,
                "message": "Record not found or is not an adulteration record"
            }), 404
        
        # Get the resultID from the record to find associated Result
        result_id = record.get("resultID")
        if not result_id:
            return jsonify({
                "success": False,
                "message": "Record has no associated resultID"
            }), 400
            
        # Find the Result record to get the sampleID
        result_record = mongo.db.IdentificationResult.find_one({"_id": result_id})
        if not result_record:
            return jsonify({
                "success": False,
                "message": "Associated Result record not found"
            }), 404
            
        # Get the sampleID from the Result record
        sample_id = result_record.get("sampleID")
        
        # Start a session for transaction
        with mongo.cx.start_session() as session:
            with session.start_transaction():
                # Delete the Record first
                record_delete = mongo.db.Record.delete_one(
                    {"_id": record_id_obj},
                    session=session
                )
                
                # Delete the Result record
                result_delete = mongo.db.IdentificationResult.delete_one(
                    {"_id": result_id},
                    session=session
                )
                
                # Delete the Sample record if sampleID exists
                sample_delete = {"deleted_count": 0}
                if sample_id:
                    sample_delete = mongo.db.Sample.delete_one(
                        {"_id": sample_id},
                        session=session
                    )
        
        # Prepare response with deletion counts
        deletion_results = {
            "record": record_delete.deleted_count, 
            "result": result_delete.deleted_count,
            "sample": sample_delete.deleted_count if hasattr(sample_delete, 'deleted_count') else 0
        }
        
        # Check if the main record was deleted
        if record_delete.deleted_count == 1 and result_delete.deleted_count == 1 and deletion_results["sample"] > 0:
            return jsonify({
                "success": True,
                "message": "Identification record and associated data deleted successfully",
                "deleted_id": record_id,
                "deletion_counts": deletion_results
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "Failed to delete record",
                "deletion_counts": deletion_results
            }), 500
    
    except Exception as e:
        print(f"Error deleting adulteration record: {e}")
        return jsonify({
            "success": False,
            "message": f"Error deleting record: {str(e)}"
        }), 500

