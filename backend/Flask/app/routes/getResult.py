# from flask import Blueprint, request, jsonify
# from ..models.sample_result import getResultByID

# result_bp = Blueprint('result', __name__)

# @result_bp.route('/result/<resultID>', methods=['GET'])
# def get_result(resultID):
#     print("result api")
#     try:
#         # resultID = request.args.get('resultID')  # Fetch resultID from query params
#         if not resultID:
#             return jsonify({'error': 'resultID is required'}), 400

#         result = getResultByID(resultID)
        
#         if not result:
#             return jsonify({'error': 'Result not found'}), 404
#         response = {
            
#             'variety': result.get('varietyNames'),
#             'confidence': float(result.get('confidenceScore').strip('%')) / 100,
#             "adulteration": result.get('adulterationStatus') == "High Adulteration",
#             'percentage': result.get('percentageComposition')
#         }
#         return jsonify(response)

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

from flask import Blueprint, jsonify
from ..models.sample_result import getResultByID

result_bp = Blueprint('result', __name__)

@result_bp.route('/result/<resultID>', methods=['GET'])
def get_result(resultID):
    print("result api")
    try:
        if not resultID:
            return jsonify({'error': 'resultID is required'}), 400

        result = getResultByID(resultID)

        if not result:
            return jsonify({'error': 'Result not found'}), 404
        
        confidence_score = result.get('confidenceScore', '0%')
        if isinstance(confidence_score, str) and confidence_score.endswith('%'):
            confidence_score = float(confidence_score.strip('%')) 
        else:
            confidence_score = 0.0  # Default value if invalid

        response = {
            'variety': result.get('varietyNames', 'Unknown'),
            'confidence': confidence_score,
            "adulteration": result.get('adulterationStatus'),
            # 'percentage': result.get('percentageComposition', 0)
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

