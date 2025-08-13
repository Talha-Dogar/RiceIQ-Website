from flask import Flask
from app import create_app, mongo
from app.models.sample_result import insert_sample_and_result

# Initialize Flask App
app = create_app()

# Ensure the app context is set
with app.app_context():
    sample_data = {
        "createdAt": "2025-02-07T12:30:00.000Z",
        "imgUrl": "/uploads/rice_sample_1.jpg"
    }

    result_data = {
        "obtainAt": "2025-02-07T12:35:00.000Z",
        "confidenceScore": "92%",
        "varietyNames": ["Basmati", "IR64"],
        "adulterationStatus": "High Adulteration",
        "percentageComposition": {"Basmati": 60, "IR64": 40}
    }

    sample_id = insert_sample_and_result(sample_data, result_data)
    print(f"Inserted Sample ID: {sample_id}")
