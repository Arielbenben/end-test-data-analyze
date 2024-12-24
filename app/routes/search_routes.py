from flask import request, Blueprint, jsonify
from app.service.search_service import search_keyword_in_all_indexes_and_return_map, \
    search_keywords_in_current_news_and_return_map, search_keyword_in_all_indexes_by_dates_and_return_map, \
    search_keywords_in_historic_news_and_return_map


search_keywords_blueprint = Blueprint('search_keywords', __name__)


@search_keywords_blueprint.route('/search/keywords/<int:limit>', methods=['POST'])
def search_keywords_in_all_database_route(limit: int):
    try:
        keywords = request.get_json()
        result = search_keyword_in_all_indexes_and_return_map(keywords, limit)
        return jsonify({"news with the given keywords": result}), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500


@search_keywords_blueprint.route('/search/news/<int:limit>', methods=['POST'])
def search_keywords_in_current_news_route(limit: int):
    try:
        keywords = request.get_json()
        result = search_keywords_in_current_news_and_return_map(keywords, limit)
        return jsonify({"current news with the given keywords": result}), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500


@search_keywords_blueprint.route('/search/historic/<int:limit>', methods=['POST'])
def search_keywords_in_historic_news_route(limit: int):
    try:
        keywords = request.get_json()
        result = search_keywords_in_historic_news_and_return_map(keywords, limit)
        return jsonify({"historic news with the given keywords": result}), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500


@search_keywords_blueprint.route('/search/combined/<int:limit>', methods=['POST'])
def search_keywords_sort_dates_in_all_database_route(limit: int):
    try:
        dates_and_keywords = request.get_json()
        result = search_keyword_in_all_indexes_by_dates_and_return_map(dates_and_keywords, limit)
        return jsonify({"news with the given keywords": result}), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500