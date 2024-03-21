def get_publication_data(start_date, end_date, phrases, token):
    url = 'https://api.lens.org/scholarly/search'
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

    should_clauses = []
    for phrase in phrases:
        should_clauses.extend([
            {"match_phrase": {"title": phrase}},
            {"match_phrase": {"abstract": phrase}},
            {"match_phrase": {"full_text": phrase}},
        ])

    query_body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "bool": {
                            "should": should_clauses
                        }
                    },
                    {
                        "range": {
                            "date_published": {
                                "gte": start_date,
                                "lte": end_date
                            }
                        }
                    }
                ]
            }
        },
        "size": 500,
        "scroll": "1m"
    }

    publications = []
    scroll_id = None

    while True:
        if scroll_id is not None:
            query_body = {"scroll_id": scroll_id}

        response = requests.post(url, json=query_body, headers=headers)

        if response.status_code == requests.codes.too_many_requests:
            print("TOO MANY REQUESTS, waiting...")
            time.sleep(8)
            continue

        if response.status_code != requests.codes.ok:
            print("ERROR:", response)
            break

        response_data = response.json()
        publications += response_data['data']
        
        print(f"{len(publications)} / {response_data['total']} publications read...")

        if response_data['scroll_id'] is not None:
            scroll_id = response_data['scroll_id']
        
        if len(publications) >= response_data['total'] or len(response_data['data']) == 0:
            break

    data_out = {"total": len(publications), "data": publications}
    return data_out
