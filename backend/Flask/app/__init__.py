from flask import Flask
from flask_pymongo import PyMongo
from .config.config import Config
from flask_cors import CORS  # Import CORS
mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    # Initialize MongoDB
    mongo.init_app(app)
 # Check MongoDB connection
    try:
        mongo.cx.server_info()  # Test MongoDB connection
        print("✅ MongoDB connection successful!")
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")

    # # Register Blueprints
    from .routes.predict_route import predict_bp
    from .routes.getResult import result_bp
    from .routes.predict_mult import predictmul_bp
    from .routes.predict_mult_2 import predictmul_v2_bp
    from .routes.predict_combine import predictmul_v3_bp
    from .routes.dashboard_cards import dashboard_cards_bp
    from .routes.dashboard_recent_records import dashboard_recent_records_bp
    from .routes.getAdulterationRecords import adulteration_records_bp, delete_adulteration_subrecord_bp
    from .routes.getIdentificationRecords import identification_records_bp, delete_identification_record_bp
    from .routes.getIdentificationResult import result_identification_bp
    from .routes.predict_adult import predict_adult_bp
    app.register_blueprint(predict_bp)
    app.register_blueprint(result_bp)
    # app.register_blueprint(predictmul_bp)
    # app.register_blueprint(predictmul_v2_bp)
    app.register_blueprint(predictmul_v3_bp)
    app.register_blueprint(dashboard_cards_bp)
    app.register_blueprint(dashboard_recent_records_bp)
    app.register_blueprint(adulteration_records_bp)
    app.register_blueprint(identification_records_bp)
    app.register_blueprint(result_identification_bp)
    app.register_blueprint(delete_adulteration_subrecord_bp)
    app.register_blueprint(delete_identification_record_bp)
    app.register_blueprint(predict_adult_bp)


    return app