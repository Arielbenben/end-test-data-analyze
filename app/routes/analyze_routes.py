from flask import Blueprint

from app.service.mongo_service import get_all_sort_by_most_deadly

analyze_attacks_blueprint = Blueprint('statistic', __name__)


@analyze_attacks_blueprint.route('/get_most_deadly_attacks/<int:num>', methods=['GET'])
def init_data_db_route():
    try:
        get_all_sort_by_most_deadly()
        return jsonify({'message': 'database and indexes created successfully'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500