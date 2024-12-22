from flask import Blueprint, jsonify
from app.db.repository.terrorist_attacks_repository import get_attack_type_sort_by_most_deadly




analyze_attacks_blueprint = Blueprint('statistics', __name__)


@analyze_attacks_blueprint.route('/get_attack_type_sort_by_most_deadly_route/<int:num>', methods=['GET'])
def get_attack_type_sort_by_most_deadly_route(num: int):
    try:
        attack = get_attack_type_sort_by_most_deadly(num)
        return jsonify(attack), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500