from flask import Blueprint, jsonify
from ..models.sample_result import getIdentResultByID

result_identification_bp = Blueprint('result/identification', __name__)

@result_identification_bp.route('/result/identification/<resultID>', methods=['GET'])
def get_result(resultID):
    print("result_identification_bp api")
    try:
        if not resultID:
            return jsonify({'error': 'resultID is required'}), 400

        result = getIdentResultByID(resultID)

        if not result:
            return jsonify({'error': 'Result not found'}), 404
        
        confidence_score = result.get('confidenceScore', '0%')
        if isinstance(confidence_score, str) and confidence_score.endswith('%'):
            confidence_score = float(confidence_score.strip('%'))
        else:
            confidence_score = 0.0  # Default value if invalid

        response = {
            'variety': result.get('varietyName', 'Unknown'),
            'confidence': confidence_score,
            "total_grains": result.get('total_grains', ''),
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

