from flask import Blueprint, jsonify
from app.db.mongo_db.repository.terrorist_attacks_repository import get_attack_type_sort_by_most_deadly, \
    get_five_groups_with_the_biggest_casualties, find_groups_with_shared_targets_in_same_year, \
    find_groups_with_repeated_attacks_on_same_target_types
from app.service.statistics_service import get_sum_events_by_group_at_region_or_all_regions_at_map, \
    get_avg_deadly_grade_by_region_at_map, calculate_yearly_attack_percentage_change_by_region_at_map, get_groups_with_shared_targets_at_map, \
    get_number_of_unique_group_by_country_or_region_at_map, get_groups_with_shared_attack_strategies_at_map


analyze_attacks_blueprint = Blueprint('statistics', __name__)


@analyze_attacks_blueprint.route('/get_attack_type_sort_by_most_deadly/<int:num>', methods=['GET'])
def get_attack_type_sort_by_most_deadly_route(num: int):
    try:
        attack = get_attack_type_sort_by_most_deadly(num)
        return jsonify(attack), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500


@analyze_attacks_blueprint.route('/get_avg_deadly_grade_by_region_at_map/<string:area>', methods=['POST'])
def get_avg_deadly_grade_by_region_at_map_route(area: str):
    try:
        print(area)
        result = get_avg_deadly_grade_by_region_at_map(area)
        return jsonify({"html" : result}), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500


@analyze_attacks_blueprint.route('/calculate_yearly_attack_percentage_change_by_region_at_map/<string:area>', methods=['GET'])
def calculate_yearly_attack_percentage_change_by_region_at_map_route(area: str):
    try:
        result = calculate_yearly_attack_percentage_change_by_region_at_map(area)
        return jsonify({"html": result}), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500


@analyze_attacks_blueprint.route('/get_sum_events_by_group_at_region_or_all_regions_at_map/<string:region>', methods=['GET'])
def get_sum_events_by_group_at_region_or_all_regions_route(region: str):
    try:
        result = get_sum_events_by_group_at_region_or_all_regions_at_map(region)
        return jsonify({"html": result}), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500


@analyze_attacks_blueprint.route('/get_groups_with_shared_targets_at_map/<string:region_or_country>', methods=['GET'])
def get_groups_with_shared_targets_at_map_route(region_or_country: str):
    try:
        result = get_groups_with_shared_targets_at_map(region_or_country)
        return jsonify({"html": result}), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500


@analyze_attacks_blueprint.route('/get_number_of_unique_group_by_country_or_region_at_map/<string:region_or_country>', methods=['GET'])
def get_number_of_unique_group_by_country_or_region_at_map_route(region_or_country: str):
    try:
        result = get_number_of_unique_group_by_country_or_region_at_map(region_or_country)
        return jsonify({"html": result}), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500


@analyze_attacks_blueprint.route('/get_groups_with_shared_attack_strategies_at_map/<string:region_or_country>', methods=['GET'])
def get_groups_with_shared_attack_strategies_at_map_route(region_or_country: str):
    try:
        result = get_groups_with_shared_attack_strategies_at_map(region_or_country)
        return jsonify({"html": result}), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500


@analyze_attacks_blueprint.route('/get_five_groups_with_the_biggest_casualties', methods=['GET'])
def get_five_groups_with_the_biggest_casualties_route():
    try:
        result = get_five_groups_with_the_biggest_casualties()
        return jsonify({"five groups with the biggest casualties": result}), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500


@analyze_attacks_blueprint.route('/find_groups_with_shared_targets_in_same_year', methods=['GET'])
def find_groups_with_shared_targets_in_same_year_route():
    try:
        result = find_groups_with_shared_targets_in_same_year()
        return jsonify({"groups with shared targets in same year": result}), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500


@analyze_attacks_blueprint.route('/find_groups_with_repeated_attacks_on_same_target_types', methods=['GET'])
def find_groups_with_repeated_attacks_on_same_target_types_route():
    try:
        result = find_groups_with_repeated_attacks_on_same_target_types()
        return jsonify({"groups with repeated attacks on same target types": result}), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500


