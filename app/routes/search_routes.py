from flask import request, Blueprint, jsonify
from app.service.search_service import search_keyword_in_all_indexes_and_return_map, \
    search_keywords_in_current_news_and_return_map, search_keyword_in_all_indexes_by_dates_and_return_map, \
    search_keywords_in_historic_news_and_return_map


search_keywords_blueprint = Blueprint('search_keywords', __name__)


@search_keywords_blueprint.route('/search/keywords/<int:limit>/<string:keywords>', methods=['GET'])
def search_keywords_in_all_database_route(limit: int, keywords: str):
    try:
        result = search_keyword_in_all_indexes_and_return_map(keywords, limit)
        return jsonify({"html": result}), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500


@search_keywords_blueprint.route('/search/news/<int:limit>/<string:keywords>', methods=['GET'])
def search_keywords_in_current_news_route(limit: int, keywords: str):
    try:
        result = search_keywords_in_current_news_and_return_map(keywords, limit)
        return jsonify({"html": result}), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500


@search_keywords_blueprint.route('/search/historic/<int:limit>/<string:keywords>', methods=['GET'])
def search_keywords_in_historic_news_route(limit: int, keywords: str):
    try:
        result = search_keywords_in_historic_news_and_return_map(keywords, limit)
        return jsonify({"html": result}), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500


@search_keywords_blueprint.route('/search/combined/<int:limit>/<string:keywords>/<string:start_date>/<string:end_date>', methods=['GET'])
def search_keywords_sort_dates_in_all_database_route(limit: int, keywords: str, start_date: str, end_date: str):
    try:
        result = search_keyword_in_all_indexes_by_dates_and_return_map(limit, keywords, start_date, end_date)
        return jsonify({"html": result}), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500