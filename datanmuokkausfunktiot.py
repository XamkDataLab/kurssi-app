import pandas as pd

def fields_of_study_table(json_data):
    table_data = []

    for record in json_data['data']:
        lens_id = record.get('lens_id', None)
        fields_of_study = record.get('fields_of_study', [])

        for field in fields_of_study:
            row = {
                'lens_id': lens_id,
                'field_of_study': field
            }
            table_data.append(row)

    df = pd.DataFrame(table_data)
    return df

def publication_table(json_data):
    data_list = json_data['data']

    columns = ["lens_id", "title", "publication_type", "year_published", 
               "date_published_parts", "created", 
               "references_count", "start_page", "end_page", "author_count", 
               "abstract", "source", "source_urls", "external_ids", "is_open_access"]  

    data = [{key: item[key] if key in item else None for key in columns} for item in data_list]

    df = pd.DataFrame(data)

    df["source_title"] = df["source"].apply(lambda x: x.get("title") if x else None)
    df["source_publisher"] = df["source"].apply(lambda x: x.get("publisher") if x else None)
    df = df.drop(columns="source")

    df["url"] = df["source_urls"].apply(lambda x: x[0]["url"] if x else None)

    df = df.drop(columns="source_urls")

    def extract_doi(external_ids):
        if external_ids:
            for eid in external_ids:
                if eid['type'] == 'doi':
                    return eid['value']
        return None

    df['DOI'] = df['external_ids'].apply(extract_doi)
    df['link'] = 'https://doi.org/' + df['DOI']
    df = df.drop(columns="external_ids")

    return df
