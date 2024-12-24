from app.db.elastic_search_db.database import elastic_client
import toolz as t



def search_keywords_in_all_indexes(keywords: str, limit: int = 1000):
    try:
        query = {
            "query": {
                "query_string": {
                    "query": keywords,
                    "fields": ["*"],
                    "default_operator": "AND"
                }
            },
            "size": limit
        }

        response = elastic_client.search(index="_all", body=query)

        hits = response.get("hits", {}).get("hits", [])
        results = [
            {"index": hit["_index"], "id": hit["_id"], "source": hit["_source"], "score": hit["_score"]}
            for hit in hits
        ]
        return results

    except Exception as e:
        return {"Error": str(e)}


def search_keyword_in_index(index: str, keyword: str, limit: int = 1000):
    query = {
        "query": {
            "multi_match": {
                "query": keyword,
                "fields": ["*"]
            }
        },
        "size": limit
    }

    response = elastic_client.search(index=index, body=query)

    return t.pipe(
        response['hits']['hits'],
        lambda hits: [hit['_source'] for hit in hits]
    )


def search_keyword_in_all_indexes_between_dates(keyword: str, start_date: str, end_date: str, limit: int):
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "multi_match": {
                            "query": keyword,
                            "fields": ['*']

                        }
                    },
                    {
                        "range": {
                            "date.full_date": {
                                "gte": start_date,
                                "lte": end_date
                            }
                        }
                    }
                ]
            }
        },
        "size": limit
    }

    response = elastic_client.search(index="_all", body=query)

    return [hit['_source'] for hit in response['hits']['hits']]