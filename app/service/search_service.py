from app.db.elastic_search_db.database import current_terrorist_attacks_index, terrorist_attacks_history_index
from app.db.elastic_search_db.repository.terrorist_attack_repository import search_keywords_in_all_indexes, \
    search_keyword_in_index, search_keyword_in_all_indexes_between_dates
from app.service.map_service import create_map_object, add_a_marker_to_map


def search_keyword_in_all_indexes_and_return_map(keywords: str, limit: int):
    search_results = search_keywords_in_all_indexes(keywords, limit)
    map_object = create_map_object()

    for event in search_results:
        event_data = event['source']
        latitude = event_data.get('location', {}).get('latitude')
        longitude = event_data.get('location', {}).get('longitude')

        if latitude and longitude:
            map_object = add_a_marker_to_map(
                map_object,
                latitude,
                longitude,
                'terror_attack',
                event_data
            )
    return map_object._repr_html_()


def search_keywords_in_current_news_and_return_map(keywords: str, limit: int):
    search_results = search_keyword_in_index(current_terrorist_attacks_index, keywords, limit)
    map_object = create_map_object()

    for event in search_results:
        latitude = event.get('location', {}).get('latitude')
        longitude = event.get('location', {}).get('longitude')

        if latitude and longitude:
            map_object = add_a_marker_to_map(
                map_object,
                latitude,
                longitude,
                'current terror_attack',
                event
            )

    return map_object._repr_html_()


def search_keywords_in_historic_news_and_return_map(keywords: str, limit: int):
    search_results = search_keyword_in_index(terrorist_attacks_history_index, keywords, limit)
    map_object = create_map_object()

    for event in search_results:
        latitude = event.get('location', {}).get('latitude')
        longitude = event.get('location', {}).get('longitude')

        if latitude and longitude:
            map_object = add_a_marker_to_map(
                map_object,
                latitude,
                longitude,
                'current terror_attack',
                event
            )

    return map_object._repr_html_()


def search_keyword_in_all_indexes_by_dates_and_return_map(limit: int, keywords: str, start_date: str, end_date: str):
    search_results = search_keyword_in_all_indexes_between_dates(keywords, start_date, end_date, limit)
    map_object = create_map_object()

    for event in search_results:
        latitude = event.get('location', {}).get('latitude')
        longitude = event.get('location', {}).get('longitude')

        if latitude and longitude:
            map_object = add_a_marker_to_map(
                map_object,
                latitude,
                longitude,
                'terror_attack',
                event
            )

    return map_object._repr_html_()

dictu = {
    'keywords': 'israel',
    'start_date': '1970-01-01',
    'end_date': '2024-01-01'
}
# print(search_keyword_in_all_indexes_by_dates_and_return_map(dictu, 10))