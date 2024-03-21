import streamlit as st
import pandas as pd
# Assuming the necessary functions are defined in these modules
from hakufunktiot import get_publication_data
from datanmuokkausfunktiot import publication_table, fields_of_study_table

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>Datahaku julkaisuista</h1>", unsafe_allow_html=True)

# Displaying an image
image_url = 'https://raw.githubusercontent.com/XamkDataLab/lens_demo/main/DALL.jpg'
st.image(image_url)

# Input widgets for dates and terms
start_date = st.date_input('Alkaen', value=pd.to_datetime('2024-01-01'))
end_date = st.date_input('Päättyen', value=pd.to_datetime('2024-03-01'))
terms = st.text_area('Hakutermit (erota pilkulla, operaattori OR)', value='chatbot', height=300).split(',')

if st.button('Hae Data'):
    token = st.secrets["mytoken"]
    publication_data = get_publication_data(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"), [term.strip() for term in terms], token)
    
    if publication_data and publication_data['data']:
        st.write(f"Löytyi {publication_data['total']} julkaisua")

        # Generating DataFrames
        publications_df = publication_table(publication_data)
        fields_of_study_df = fields_of_study_table(publication_data)

        # Ensure DataFrame display for verification
        st.write("Publications DataFrame Preview:")
        st.dataframe(publications_df.head())
        st.write("Fields of Study DataFrame Preview:")
        st.dataframe(fields_of_study_df.head())

        # Selection box for fields of study
        unique_fields_of_study = fields_of_study_df['field_of_study'].unique().tolist()
        selected_field_of_study = st.selectbox('Select a Field of Study', ['All'] + unique_fields_of_study)

        if selected_field_of_study != 'All':
            # Ensure conversion to list is correct
            relevant_lens_ids = fields_of_study_df[fields_of_study_df['field_of_study'] == selected_field_of_study]['lens_id'].tolist()
            st.write(f"Debug: Relevant lens_ids {relevant_lens_ids}")  # Confirming the list content

            # Filtering based on the list
            if relevant_lens_ids:  # Checking if the list is not empty
                filtered_publications_df = publications_df[publications_df['lens_id'].isin(relevant_lens_ids)]

                if not filtered_publications_df.empty:
                    st.dataframe(filtered_publications_df)
                else:
                    st.write("Filtered DataFrame is empty. No publications found for the selected field of study.")
            else:
                st.write("No lens_ids found for the selected field of study.")
        else:
            st.dataframe(publications_df)
    else:
        st.error("No publication data fetched. Please check your inputs and try again.")
