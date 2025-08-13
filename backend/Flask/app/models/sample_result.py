from bson import ObjectId
from pymongo.errors import PyMongoError

from .. import mongo

def insert_sample_and_result(sample_data, result_data, status):
    print("I am here")
    session = mongo.cx.start_session()
    try:
        with session.start_transaction():
            sample_id = mongo.db.Sample.insert_one(sample_data, session=session).inserted_id
            result_data["sampleID"] = ObjectId(sample_id)
            result_id=mongo.db.Result.insert_one(result_data, session=session).inserted_id
            record_data = {
            "userID": ObjectId("67a705177eb78cad4999384d") ,
            "resultID":result_id ,
            "sellerID": ObjectId("67a72bba265ff005a9aff548") ,
            "status": status,
                }
            mongo.db.Record.insert_one(record_data, session=session)
        session.commit_transaction()
        return result_id
    except PyMongoError as e:
        session.abort_transaction()
        print(f"Transaction aborted: {e}")
        return None
    finally:
        session.end_session()


def getResultByID(resultID):
    result = mongo.db.Result.find_one({"_id": ObjectId(resultID)})
    if not result:
        return None
    return result



def insert_sample_and_identification_result(sample_data, result_data, status):
    session = mongo.cx.start_session()
    try:
        with session.start_transaction():
            sample_id = mongo.db.Sample.insert_one(sample_data, session=session).inserted_id
            result_data["sampleID"] = ObjectId(sample_id)
            result_id=mongo.db.IdentificationResult.insert_one(result_data, session=session).inserted_id
            record_data = {
            "userID": ObjectId("67a705177eb78cad4999384d") ,
            "resultID":result_id ,
            "sellerID": ObjectId("67a72bba265ff005a9aff548") ,
            "status": status,
                }
            mongo.db.Record.insert_one(record_data, session=session)
        session.commit_transaction()
        return result_id
    except PyMongoError as e:
        session.abort_transaction()
        print(f"Transaction aborted: {e}")
        return None
    finally:
        session.end_session()



def getIdentResultByID(resultID):
    result = mongo.db.IdentificationResult.find_one({"_id": ObjectId(resultID)})
    if not result:
        return None
    return result