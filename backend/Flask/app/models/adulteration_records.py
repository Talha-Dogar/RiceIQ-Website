from datetime import datetime
from bson.json_util import dumps, loads
from .. import mongo
from bson import ObjectId
import json
from flask import jsonify

# def get_adulteration_records_grouped():
#     """
#     Endpoint to retrieve adulteration records grouped by seller.
#     Returns a list of sellers, each with their associated adulteration records.
#     """
#     try:        
#         pipeline = [
#             # Start with the Record collection where status is "adulteration"
#             {
#                 "$match": {
#                     "status": "adulteration"
#                 }
#             },
#             # Join with Result collection
#             {
#                 "$lookup": {
#                     "from": "Result",
#                     "localField": "resultID",
#                     "foreignField": "_id",
#                     "as": "record_data"
#                 }
#             },
#             # Unwind the record_data array
#             {
#                 "$unwind": "$record_data"
#             },
#             # Join with sellers collection
#             {
#                 "$lookup": {
#                     "from": "Seller",
#                     "localField": "sellerID",
#                     "foreignField": "_id",
#                     "as": "seller_data"
#                 }
#             },
#             # Unwind the seller_data array
#             {
#                 "$unwind": "$seller_data"
#             },
#             # Join with samples collection
#             {
#                 "$lookup": {
#                     "from": "Sample",
#                     "localField": "record_data.sampleID",
#                     "foreignField": "_id",
#                     "as": "sample_data"
#                 }
#             },
#             # Unwind the sample_data array
#             {
#                 "$unwind": "$sample_data"
#             },
#             # Project fields we need
#             {
#                 "$project": {
#                     "_id": 0,
#                     "seller_id": "$seller_data._id",
#                     "seller_name": "$seller_data.companyName",
#                     "seller_address": "$seller_data.address",
#                     "img_url": "$sample_data.imgUrl",
#                     "status": "$status",
#                     "date": "$record_data.obtainAt",
#                     "record_id": "$record_data._id"
#                 }
#             },
#             # Group by seller_id
#             {
#                 "$group": {
#                     "_id": "$seller_id",
#                     "seller_name": { "$first": "$seller_name" },
#                     "seller_address": { "$first": "$seller_address" },
#                     "records": {
#                         "$push": {
#                             "img_url": "$img_url",
#                             "status": "$status",
#                             "date": "$date",
#                             "record_id": "$record_id"
#                         }
#                     },
#                     "count": { "$sum": 1 }
#                 }
#             },
#             # Final projection to clean up the format
#             {
#                 "$project": {
#                     "_id": 0,
#                     "seller_id": "$_id",
#                     "seller_name": 1,
#                     "seller_address": 1,
#                     "records": 1,
#                     "count": 1
#                 }
#             },
#             # Sort by seller_id
#             {
#                 "$sort": {
#                     "seller_id": 1
#                 }
#             }
#         ]
        
#         # Execute the aggregation pipeline
#         print(mongo.db.list_collection_names())
#         print((mongo.db.Record.aggregate(pipeline)))
#         results = list(mongo.db.Record.aggregate(pipeline))
#         print("Results:", results)  # Debugging line
#         return results

#     except Exception as e:
#         print(f"Error retrieving grouped adulteration records: {e}")
#         return None



# def get_adulteration_records_grouped():
#     """
#     Endpoint to retrieve adulteration records grouped by seller.
#     Returns a list of sellers, each with their associated adulteration records.
#     """
#     try:
#         # Debug: Print all collection names
#         collection_names = mongo.db.list_collection_names()
#         print(f"Collections in database: {collection_names}")
        
#         # Check if relevant collections exist
#         required_collections = ["Record", "Result", "Seller", "Sample"]
#         for col in required_collections:
#             if col not in collection_names:
#                 print(f"Warning: Collection '{col}' not found in database")
        
#         # Debug: Check if there are any adulteration records
#         adulteration_count = mongo.db.Record.count_documents({"status": "adulteration"})
#         print(f"Found {adulteration_count} records with status='adulteration'")
        
#         if adulteration_count == 0:
#             print("No adulteration records found. Check the 'status' field value.")
#             return []
            
#         # First stage of pipeline to verify data structure
#         initial_records = list(mongo.db.Record.find({"status": "adulteration"}).limit(1))
#         if initial_records:
#             print(f"Sample record structure: {dumps(initial_records[0])}")
        
#         pipeline = [
#             # Start with the Record collection where status is "adulteration"
#             {
#                 "$match": {
#                     "status": "adulteration"
#                 }
#             },
#             # Join with Result collection
#             {
#                 "$lookup": {
#                     "from": "Result",
#                     "localField": "resultID",
#                     "foreignField": "_id",
#                     "as": "record_data"
#                 }
#             },
#             # Debug: Stop here and check intermediate results
#             {
#                 "$limit": 5
#             }
#         ]
        
#         # Execute a simplified pipeline to check initial lookup
#         initial_lookup = list(mongo.db.Record.aggregate(pipeline))
#         print(f"Initial lookup results (limited to 5): {dumps(initial_lookup)}")
        
#         # If initial lookup succeeded, proceed with full pipeline
#         if initial_lookup and len(initial_lookup[0].get("record_data", [])) > 0:
#             # Full pipeline as before
#             full_pipeline = [
#                 {"$match": {"status": "adulteration"}},
#                 {"$lookup": {
#                     "from": "Result",
#                     "localField": "resultID",
#                     "foreignField": "_id",
#                     "as": "record_data"
#                 }},
#                 {"$unwind": "$record_data"},
#                 {"$lookup": {
#                     "from": "Seller",
#                     "localField": "record_data.sellerID",
#                     "foreignField": "_id",
#                     "as": "seller_data"
#                 }},
#                 {"$unwind": "$seller_data"},
#                 {"$lookup": {
#                     "from": "Sample",
#                     "localField": "sampleID",
#                     "foreignField": "_id",
#                     "as": "sample_data"
#                 }},
#                 {"$unwind": "$sample_data"},
#                 {"$project": {
#                     "_id": 0,
#                     "seller_id": "$seller_data._id",
#                     "seller_name": "$seller_data.companyName",
#                     "seller_address": "$seller_data.address",
#                     "img_url": "$sample_data.imgUrl",
#                     "status": "$status",
#                     "date": "$record_data.obtainAt",
#                     "record_id": "$record_data._id"
#                 }},
#                 {"$group": {
#                     "_id": "$seller_id",
#                     "seller_name": {"$first": "$seller_name"},
#                     "seller_address": {"$first": "$seller_address"},
#                     "records": {
#                         "$push": {
#                             "img_url": "$img_url",
#                             "status": "$status",
#                             "date": "$date",
#                             "record_id": "$record_id"
#                         }
#                     },
#                     "count": {"$sum": 1}
#                 }},
#                 {"$project": {
#                     "_id": 0,
#                     "seller_id": "$_id",
#                     "seller_name": 1,
#                     "seller_address": 1,
#                     "records": 1,
#                     "count": 1
#                 }},
#                 {"$sort": {"seller_id": 1}}
#             ]
            
#             results = list(mongo.db.Record.aggregate(full_pipeline))
#             print(f"Final results count: {len(results)}")
#             return results
#         else:
#             # Check for ObjectId conversion issues
#             print("Lookup failed. Checking if resultID is correctly stored as ObjectId...")
#             sample_record = mongo.db.Record.find_one({"status": "adulteration"})
#             if sample_record and "resultID" in sample_record:
#                 print(f"resultID type: {type(sample_record['resultID'])}")
#                 print(f"resultID value: {sample_record['resultID']}")
                
#                 # Try alternative lookup if resultID is stored as string
#                 if isinstance(sample_record['resultID'], str):
#                     print("resultID is stored as string, trying string comparison...")
#                     alt_pipeline = [
#                         {"$match": {"status": "adulteration"}},
#                         {"$addFields": {
#                             "resultID_str": {"$toString": "$resultID"}
#                         }},
#                         {"$lookup": {
#                             "from": "Result",
#                             "localField": "resultID_str",
#                             "foreignField": "_id",
#                             "as": "record_data"
#                         }}
#                     ]
#                     alt_results = list(mongo.db.Record.aggregate(alt_pipeline))
#                     print(f"Alternative lookup results: {dumps(alt_results)}")
            
#             return []

#     except Exception as e:
#         print(f"Error retrieving grouped adulteration records: {e}")
#         import traceback
#         traceback.print_exc()
#         return None



from datetime import datetime
from bson.json_util import dumps, loads
from .. import mongo
from bson import ObjectId
import json

def get_adulteration_records_grouped():
    """
    Endpoint to retrieve adulteration records grouped by seller.
    Returns a list of sellers, each with their associated adulteration records.
    """
    try:        
        # Debug information
        # print("Collections:", mongo.db.list_collection_names())
        adulteration_count = mongo.db.Record.count_documents({"status": "adulteration"})
        # print(f"Found {adulteration_count} records with status='adulteration'")
        
        if adulteration_count == 0:
            print("No matching records found. Check if 'adulteration' is the correct status value.")
            return []
            
        # Based on your debug output, here is the corrected pipeline
        pipeline = [
            # Match adulteration records
            {
                "$match": {
                    "status": "adulteration"
                }
            },
            # Join with Result collection
            {
                "$lookup": {
                    "from": "Result",
                    "localField": "resultID",
                    "foreignField": "_id",
                    "as": "record_data"
                }
            },
            # Unwind the record_data array
            {
                "$unwind": {
                    "path": "$record_data",
                    "preserveNullAndEmptyArrays": False
                }
            },
            # Join with sellers collection using sellerID from Record (not from record_data)
            {
                "$lookup": {
                    "from": "Seller",
                    "localField": "sellerID",
                    "foreignField": "_id",
                    "as": "seller_data"
                }
            },
            # Unwind the seller_data array
            {
                "$unwind": {
                    "path": "$seller_data",
                    "preserveNullAndEmptyArrays": False
                }
            },
            # Join with samples collection using sampleID from record_data
            {
                "$lookup": {
                    "from": "Sample",
                    "localField": "record_data.sampleID",
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
                    "seller_id": "$seller_data._id",
                    "seller_name": "$seller_data.companyName",
                    "seller_address": "$seller_data.address",
                    "img_url": "$sample_data.imgUrl", 
                    "status": "$record_data.adulterationStatus",
                    "date": "$record_data.obtainAt",
                    "record_id": "$resultID"  # Using Record's _id as the record_id
                }
            },
            # Group by seller_id
            {
                "$group": {
                    "_id": "$seller_id",
                    "seller_name": { "$first": "$seller_name" },
                    "seller_address": { "$first": "$seller_address" },
                    "records": {
                        "$push": {
                            "img_url": "$img_url",
                            "status": "$status",
                            "date": "$date",
                            "record_id": "$record_id"
                        }
                    },
                    "count": { "$sum": 1 }
                }
            },
            # Final projection to clean up the format
            {
                "$project": {
                    "_id": 0,
                    "seller_id": { "$toString": "$_id" },
                    "seller_name": 1,
                    "seller_address": 1,
                    "records": {
                        "$map": {
                            "input": "$records",
                            "as": "rec",
                            "in": {
                                "img_url": "$$rec.img_url",
                                "status": "$$rec.status",
                                "date": "$$rec.date",
                                "record_id": { "$toString": "$$rec.record_id" }
                            }
                        }
                    },
                    "count": 1
                }
            },
            # Sort by seller_name
            {
                "$sort": {
                    "seller_name": 1
                }
            }
        ]
        
        # Execute the aggregation pipeline
        results = list(mongo.db.Record.aggregate(pipeline))
        # print(f"Final results count: {len(results)}")
        # print(f"Serialized results: {dumps(results)}")
        return results

    except Exception as e:
        print(f"Error retrieving grouped adulteration records: {e}")
        import traceback
        traceback.print_exc()
        return None
    


def delete_adulteration_record(record_id):
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
        
        # Find the record first to verify it exists and has status "adulteration"
        record = mongo.db.Record.find_one({"_id": record_id_obj, "status": "adulteration"})
        
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
        result_record = mongo.db.Result.find_one({"_id": result_id})
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
                result_delete = mongo.db.Result.delete_one(
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
        if record_delete.deleted_count == 1:
            return jsonify({
                "success": True,
                "message": "Adulteration record and associated data deleted successfully",
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

