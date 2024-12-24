from app.db.mongo_db.database import terrorist_attacks_collection
from app.db.mongo_db.repository.queries import get_sum_events_by_group_at_all_region_query, \
    get_attack_type_sort_by_most_deadly_query, \
    get_avg_deadly_grade_by_region_query, get_five_groups_with_the_biggest_casualties_query, \
    get_attacks_and_targets_query, sum_events_by_year_query, sum_events_by_month_query, \
    get_sum_events_by_year_at_all_regions_query, get_number_of_unique_group_query, get_groups_with_shared_targets_query, \
    get_groups_with_shared_attack_strategies_query, find_groups_with_repeated_attacks_on_same_target_types_query, \
    find_groups_with_shared_targets_in_same_year_query


def get_all_data():
    return terrorist_attacks_collection.find()


def get_attack_type_sort_by_most_deadly(num: int = 0):
    pipeline_query = get_attack_type_sort_by_most_deadly_query

    if num:
        pipeline_query.append({"$limit": num})

    res = terrorist_attacks_collection.aggregate(pipeline_query)

    return list(res)


def get_avg_deadly_grade_by_region(area: str):
    pipeline_query = get_avg_deadly_grade_by_region_query

    if area == 'area':
        pipeline_query.append({"$limit": 5})

    result = terrorist_attacks_collection.aggregate(pipeline_query)

    return list(result)


def get_five_groups_with_the_biggest_casualties():
    pipeline_query = get_five_groups_with_the_biggest_casualties_query

    result = terrorist_attacks_collection.aggregate(pipeline_query)

    return list(result)


def get_attacks_and_targets():
    pipeline_query = get_attacks_and_targets_query

    results = terrorist_attacks_collection.aggregate(pipeline_query)

    return list(results)


def sum_events_by_year():
    pipeline_query = sum_events_by_year_query

    results = terrorist_attacks_collection.aggregate(pipeline_query)

    return list(results)


def sum_events_by_month(year: int):
    pipeline_query = sum_events_by_month_query

    match =  { "$match": { "date.year": year, "date.month": {"$ne": None} } }

    pipeline_query.append(match)

    results = terrorist_attacks_collection.aggregate(pipeline_query)

    return list(results)


def get_sum_events_by_year_at_all_regions():
    pipeline_query = get_sum_events_by_year_at_all_regions_query

    results = terrorist_attacks_collection.aggregate(pipeline_query)

    return list(results)


def get_sum_events_by_group_at_region_or_all_regions(region: str):
    match_stage = {
        "location.region": {"$ne": None},
        "terrorist_group.name": {"$ne": None}
    }

    if region != 'all':
        match_stage["location.region"] = region

    pipeline_query = get_sum_events_by_group_at_all_region_query
    pipeline_query[0]["$match"] = match_stage

    results = terrorist_attacks_collection.aggregate(pipeline_query)

    return list(results)


def get_number_of_unique_group_by_country_or_region(region_or_country: str):
    match_stage = {
        f"location.{region_or_country}": {"$ne": None},
        "terrorist_group.name": {"$ne": None}
    }

    pipeline_query = get_number_of_unique_group_query

    pipeline_query[0]["$match"] = match_stage

    pipeline_query[1]["$group"]["_id"] = f"$location.{region_or_country}"

    results = terrorist_attacks_collection.aggregate(pipeline_query)

    return list(results)

def get_groups_with_shared_targets(region_or_country: str):
    match_stage = {
        "terrorist_group.name": {"$ne": None},
        "attack.target": {"$ne": None},
        f"location.{region_or_country}": {"$ne": None},
        "location.latitude": {"$ne": None},
        "location.longitude": {"$ne": None},
    }

    pipeline_query = get_groups_with_shared_targets_query

    pipeline_query[0]["$match"] = match_stage
    pipeline_query[1]["$group"]["_id"][region_or_country] = f"$location.{region_or_country}"

    results = terrorist_attacks_collection.aggregate(pipeline_query)

    return list(results)


def get_groups_with_shared_attack_strategies(region_or_country: str):
    match_stage = {
        "terrorist_group.name": {"$ne": None},
        "attack.attack_type": {"$ne": None},
        f"location.{region_or_country}": {"$ne": None}
    }

    pipeline_query = get_groups_with_shared_attack_strategies_query

    pipeline_query[0]["$match"] = match_stage

    results = terrorist_attacks_collection.aggregate(pipeline_query)

    return list(results)


def find_groups_with_repeated_attacks_on_same_target_types():
    pipeline_query = find_groups_with_repeated_attacks_on_same_target_types_query

    results = terrorist_attacks_collection.aggregate(pipeline_query)

    return list(results)


def find_groups_with_shared_targets_in_same_year():
    pipeline_query = find_groups_with_shared_targets_in_same_year_query

    results = terrorist_attacks_collection.aggregate(pipeline_query)

    return list(results)
