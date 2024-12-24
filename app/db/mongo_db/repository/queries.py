


get_sum_events_by_group_at_all_region_query = [
    {
        "$match": {}
    },
    {
        "$group": {
            "_id": {
                "region": "$location.region",
                "terrorist_group": "$terrorist_group.name"
            },
            "sum_events": {"$sum": 1}
        }
    },
    {
        "$project": {
            "_id": 0,
            "region": "$_id.region",
            "terrorist_group": "$_id.terrorist_group",
            "sum_events": 1
        }
    },
    {
        "$facet": {
            "grouped_by_region": [
                {
                    "$sort": {"sum_events": -1}
                },
                {
                    "$group": {
                        "_id": "$region",
                        "top_groups": {"$push": {"terrorist_group": "$terrorist_group", "sum_events": "$sum_events"}}
                    }
                },
                {
                    "$project": {
                        "top_groups": {"$slice": ["$top_groups", 5]}
                    }
                }
            ]
        }
    },
    {
        "$unwind": "$grouped_by_region"
    },
    {
        "$replaceRoot": {
            "newRoot": "$grouped_by_region"
        }
    },
    {
        '$limit': 5
    }
]



get_sum_events_by_group_at_region_query = [
    {
        "$match": {}
    },
    {
        "$group": {
            "_id": "$terrorist_group.name",
            "sum_events": {"$sum": 1}
        }
    },
    {
        "$project": {
            "_id": 0,
            "terrorist_group": "$_id",
            "sum_events": 1
        }
    },
    {
        "$sort": {"sum_events": -1}
    },
    {
        '$limit': 5
    }
]

get_attack_type_sort_by_most_deadly_query = [
    {
        "$match": {"casualties.deadly_grade": {"$ne": None}}
    },
    {
        "$unwind": "$attack.attack_type"
    },
    {
        "$group": {
            "_id": "$attack.attack_type",
            "total_deadly_grade": {"$sum": "$casualties.deadly_grade"}
        }
    },
    {
        "$match": {"total_deadly_grade": {"$ne": None}}
    },
    {
        "$sort": {"total_deadly_grade": -1},
    }
]

get_avg_deadly_grade_by_region_query = [
    {
        "$match": {
            "casualties.deadly_grade": {"$ne": None}
        }
    },
    {
        "$group": {
            "_id": "$location.region",
            "average_deadly_grade": {"$avg": "$casualties.deadly_grade"}
        }
    },
    {
        "$project": {
            "_id": 1,
            "average_deadly_grade": {"$round": ["$average_deadly_grade", 2]}
        }
    },
    {
        "$sort": {"average_deadly_grade": -1},
    }
]

get_five_groups_with_the_biggest_casualties_query = [
    {
      '$match': {
          'terrorist_group.name': {'$ne': None},
          'casualties.deadly_grade': {'$ne': None}
      }
    },
    {
        "$group": {
            "_id": "$terrorist_group.name",
            "sum_deadly_grade": {"$sum": "$casualties.deadly_grade"}
        }
    },
    {
        "$sort": {"sum_deadly_grade": -1},
    },
    {
        '$limit': 5
    }
]

get_attacks_and_targets_query = [
    {
        "$match": {
            "attack.attack_type": {"$ne": None},
            "attack.target_type": {"$ne": None}
        }
    },
    {
        "$unwind": "$attack.attack_type"
    },
    {
        "$project": {
            "attack_type": "$attack.attack_type",
            "target_type": "$attack.target_type"
        }
    }
]

sum_events_by_year_query = [
    {
        "$match": {
            "date.year": {"$ne": None}
        }
    },
    {
        "$group": {
            "_id": "$date.year",
            "sum_events": {"$sum": 1}
        }
    },
    {
        "$project": {
            "_id": 0,
            "year": "$_id",
            "sum_events": 1
        }
    }
]

sum_events_by_month_query = [
    {
        "$group": {
            "_id": "$date.month",
            "sum_events": {"$sum": 1}
        }
    },
    {
        "$project": {
            "_id": 0,
            "month": "$_id",
            "sum_events": 1
        }
    },
    {
        "$sort": {"month": 1}
    }
]

get_sum_events_by_year_at_all_regions_query = [
    {
        "$match": {
            "location.region": {"$ne": None},
            "terrorist_group.name": {'$ne': None}
        }
    },
    {
        "$group": {
            "_id": {
                "region": "$location.region",
                "year": "$date.year"
            },
            "sum_events": {"$sum": 1}
        }
    },
    {
        "$sort": {
            "_id.region": 1,
            "_id.year": 1
        }
    },
    {
        "$group": {
            "_id": "$_id.region",
            "first_year_sum_events": {"$first": {"year": "$_id.year", "sum_events": "$sum_events"}},
            "last_year_sum_events": {"$last": {"year": "$_id.year", "sum_events": "$sum_events"}}
        }
    },
    {
        "$project": {
            "_id": 0,
            "region": "$_id",
            "first_year_sum_events": 1,
            "last_year_sum_events": 1
        }
    }
]


get_number_of_unique_group_query = [
    {
        "$match": {}
    },
    {
        "$group": {
            "_id": None,
            "unique_groups": {"$addToSet": "$terrorist_group.name"}
        }
    },
    {
        "$project": {
            "_id": 1,
            "unique_count": {"$size": "$unique_groups"},
            "unique_group_names": "$unique_groups"

        }
    },
    {
        "$sort": {"unique_count": -1}
    }
]


get_groups_with_shared_targets_query = [
    {
        "$match": {}
    },
    {
        "$group": {
            "_id": {
                "region": "$location.region",
                "target": "$attack.target",
                "terrorist_group": "$terrorist_group.name"
            },
            "count": {"$sum": 1},
            "coordinates": {
                "$first": {
                    "lat": "$location.latitude",
                    "lng": "$location.longitude"
                }
            }
        }
    },
    {
        "$group": {
            "_id": {
                "region": "$_id.region",
                "target": "$_id.target"
            },
            "terrorist_groups": {"$push": "$_id.terrorist_group"},
            "total_attacks": {"$sum": "$count"},
            "coordinates": {"$first": "$coordinates"}
        }
    },
    {
        "$match": {
            "terrorist_groups.1": {"$exists": True}
        }
    },
    {
        "$group": {
            "_id": "$_id.region",
            "shared_targets": {
                "$push": {
                    "target": "$_id.target",
                    "terrorist_groups": "$terrorist_groups",
                    "total_attacks": "$total_attacks",
                    "coordinates": "$coordinates"
                }
            }
        }
    },
    {
        "$project": {
            "_id": 0,
            "region": "$_id",
            "shared_targets": {
                "$sortArray": {
                    "input": "$shared_targets",
                    "sortBy": {"total_attacks": -1}
                }
            }
        }
    },
    {
        "$sort": {"region": 1}
    }
]

get_groups_with_shared_attack_strategies_query = [
  {
    "$match": {}
  },
  {
    "$group": {
      "_id": {
        "region_or_country": "$location.region",
        "attack_type": "$attack.attack_type",
        "terrorist_group": "$terrorist_group.name"
      },
      "count": { "$sum": 1 }
    }
  },
  {
    "$group": {
      "_id": {
        "region_or_country": "$_id.region_or_country",
        "attack_type": "$_id.attack_type"
      },
      "unique_groups_count": { "$sum": 1 },
      "total_groups": { "$push": "$_id.terrorist_group" }
    }
  },
  {
    "$sort": { "unique_groups_count": -1 }
  },
  {
    "$group": {
      "_id": "$_id.region_or_country",
      "attack_type": { "$first": "$_id.attack_type" },
      "unique_groups_count": { "$first": "$unique_groups_count" },
      "total_groups": { "$first": "$total_groups" }
    }
  },
  {
    "$project": {
      "_id": 0,
      "region_or_country": "$_id",
      "attack_type": 1,
      "unique_groups_count": 1,
      "total_groups": 1
    }
  }
]



find_groups_with_repeated_attacks_on_same_target_types_query = [
    {
        "$match": {
            "terrorist_group.name": {"$ne": None},
            "attack.target_type": {"$ne": None}
        }
    },
    {
        "$group": {
            "_id": {
                "target_type": "$attack.target_type",
                "terrorist_group": "$terrorist_group.name"
            },
            "attack_count": {"$sum": 1}
        }
    },
    {
        "$match": {
            "attack_count": {"$gt": 1}
        }
    },
    {
        "$group": {
            "_id": "$_id.target_type",
            "terrorist_groups": {
                "$push": {
                    "group_name": "$_id.terrorist_group",
                    "attack_count": "$attack_count"
                }
            },
            "total_attacks": {"$sum": "$attack_count"}
        }
    },
    {
        "$sort": {"total_attacks": -1}
    },
    {
        "$project": {
            "_id": 0,
            "target_type": "$_id",
            "terrorist_groups": 1,
            "total_attacks": 1
        }
    }
]


find_groups_with_shared_targets_in_same_year_query = [
    {
        "$match": {
            "terrorist_group.name": {"$ne": None},
            "attack.target": {"$ne": None},
            "date.year": {"$ne": None}
        }
    },
    {
        "$group": {
            "_id": {
                "target": "$attack.target",
                "year": "$date.year"
            },
            "terrorist_groups": {"$addToSet": "$terrorist_group.name"}
        }
    },
    {
        "$match": {
            "terrorist_groups.1": {"$exists": True}
        }
    },
    {
        "$project": {
            "_id": 0,
            "target": "$_id.target",
            "year": "$_id.year",
            "terrorist_groups": 1
        }
    },
    {
        "$sort": {"year": 1, "target": 1}
    }
]
