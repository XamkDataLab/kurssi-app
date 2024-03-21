import streamlit as st
import pandas as pd
from hakufunktiot import *
from datanmuokkausfunktiot import *

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>Datahaku julkaisuista</h1>", unsafe_allow_html=True)

main_row = st.columns([2, 1, 2])

with main_row[0]:
    image_url = 'https://raw.githubusercontent.com/XamkDataLab/lens_demo/main/DALL.jpg'
    st.image(image_url)

with main_row[1]:
    start_date = st.date_input('Alkaen', value=pd.to_datetime('2024-01-01'))
    end_date = st.date_input('Päättyen', value=pd.to_datetime('2024-03-01'))

with main_row[2]:
    terms = st.text_area('Hakutermit (erota pilkulla, operaattori OR)', 
                        value='chatbot', 
                        height=300).split(',')

token = st.secrets["mytoken"]

if st.button('Hae Data'):
    try:
        publication_data = get_publication_data(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"), [term.strip() for term in terms], token)
        if publication_data and publication_data['data']:
            st.write(f"Löytyi {publication_data['total']} julkaisua")

            publications_df = publication_table(publication_data)
            fields_of_study_df = fields_of_study_table(publication_data)

            st.write(f"Publications DataFrame size: {publications_df.shape}, Type of lens_id: {publications_df['lens_id'].dtype}")
            st.write(f"Fields of Study DataFrame size: {fields_of_study_df.shape}, Type of lens_id: {fields_of_study_df['lens_id'].dtype}")

            unique_fields_of_study = fields_of_study_df['field_of_study'].unique().tolist()
            selected_field_of_study = st.selectbox('Select a Field of Study', ['All'] + unique_fields_of_study)

            if selected_field_of_study != 'All':
                relevant_lens_ids = fields_of_study_df[fields_of_study_df['field_of_study'] == selected_field_of_study]['lens_id'].tolist()
                filtered_publications_df = publications_df[publications_df['lens_id'].isin(relevant_lens_ids)]

                if not filtered_publications_df.empty:
                    st.dataframe(filtered_publications_df)
                else:
                    st.write("No publications found for the selected field of study. This may indicate an issue with the data or the selection.")
            else:
                st.dataframe(publications_df)
        else:
            st.write("No publication data fetched. Please check your inputs and try again.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
