from app.api.location_api import get_lot_and_lan_for_location
from app.db.mongo_db.repository.terrorist_attacks_repository import get_sum_events_by_year_at_all_regions, \
    get_attacks_and_targets, \
    get_avg_deadly_grade_by_region, get_sum_events_by_group_at_region_or_all_regions, get_groups_with_shared_targets, \
    get_number_of_unique_group_by_country_or_region, get_groups_with_shared_attack_strategies
import pandas as pd
from app.service.map_service import create_map_object, add_a_marker_to_map
from app.utils.statistics_utils import get_color_to_casualties_grade, sort_top_percentage_change, \
    calculate_percent_change


def get_attack_target_correlation():
    results = get_attacks_and_targets()
    df = pd.DataFrame(results)

    df_encoded = pd.get_dummies(df[['attack_type', 'target_type']])

    correlation = df_encoded.corr()

    attack_target_correlation = correlation.iloc[:len(df_encoded.columns) // 2, len(df_encoded.columns) // 2:]

    return attack_target_correlation


def calculate_yearly_attack_percentage_change_by_region_at_map(area: str):
    events_by_year = get_sum_events_by_year_at_all_regions()
    map_object = create_map_object()

    areas = [
        {**area, 'coordinates': get_lot_and_lan_for_location(area.get('region')),
         'percentage_change': calculate_percent_change(area)}
        for area in events_by_year
    ]

    if area == 'area':
        areas = sort_top_percentage_change(areas)

    for area in areas:
        map_object = add_a_marker_to_map(map_object, area['coordinates']['lat'], area['coordinates']['lng'],
                                         area['region'], f'{area["percentage_change"]}%')
    return map_object._repr_html_()


def get_avg_deadly_grade_by_region_at_map(area: str):
    avg_deadly = get_avg_deadly_grade_by_region(area)
    map_object = create_map_object()

    for area in avg_deadly:
        coordinates = get_lot_and_lan_for_location(area['_id'])
        color = get_color_to_casualties_grade(area['average_deadly_grade'])
        map_object = add_a_marker_to_map(map_object, coordinates['lat'], coordinates['lng'], area['_id'],
                                         area['average_deadly_grade'], color)

    return map_object._repr_html_()


def get_sum_events_by_group_at_region_or_all_regions_at_map(region: str):
    sum_events = get_sum_events_by_group_at_region_or_all_regions(region)
    map_object = create_map_object()

    for area in sum_events:
        coordinates = get_lot_and_lan_for_location(area['_id'])
        map_object = add_a_marker_to_map(map_object, coordinates['lat'], coordinates['lng'], area['_id'],
                                         [area['terrorist_group'] for area in area['top_groups']])
    return map_object._repr_html_()


def get_groups_with_shared_targets_at_map(region_or_country: str):
    if region_or_country not in ["region", "country"]:
        return {"message": "Please choose either 'region' or 'country'"}

    groups = get_groups_with_shared_targets(region_or_country)
    map_object = create_map_object()

    for area in groups:
        len_area = len(area['shared_targets'])

        for i in range(len_area):
            color = None
            if i == 0:
                color = 'red'

            map_object = add_a_marker_to_map(
                map_object,
                area['shared_targets'][i]['coordinates']['lat'],
                area['shared_targets'][i]['coordinates']['lng'],
                area['region'],
                area['shared_targets'][i]['terrorist_groups'],
                color
            )

    return map_object._repr_html_()


def get_number_of_unique_group_by_country_or_region_at_map(region_or_country: str):
    if region_or_country not in ["region", "country"]:
        return {"message": "Please choose either 'region' or 'country'."}

    unique_groups = get_number_of_unique_group_by_country_or_region(region_or_country)
    map_object = create_map_object()

    for area in unique_groups:
        coordinates = get_lot_and_lan_for_location(area['_id'])
        map_object = add_a_marker_to_map(map_object, coordinates['lat'], coordinates['lng'], area['_id'],
                                         area['unique_group_names'])
    return map_object._repr_html_()


def get_groups_with_shared_attack_strategies_at_map(region_or_country: str):
    if region_or_country not in ["region", "country"]:
        return {"message": "Please choose either 'region' or 'country'."}

    groups = get_groups_with_shared_attack_strategies(region_or_country)
    map_object = create_map_object()

    for area in groups:
        coordinates = get_lot_and_lan_for_location(area['region_or_country'])
        map_object = add_a_marker_to_map(map_object, coordinates['lat'], coordinates['lng'], area['unique_groups_count'],
                                         area['total_groups'])
    return map_object._repr_html_()

