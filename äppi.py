import streamlit as st
import pandas as pd
from hakufunktiot import get_publication_data
from datanmuokkausfunktiot import publication_table, fields_of_study_table

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>Datahaku julkaisuista</h1>", unsafe_allow_html=True)

# Initialize session state variables if they don't exist
if 'publications_df' not in st.session_state:
    st.session_state.publications_df = pd.DataFrame()
if 'fields_of_study_df' not in st.session_state:
    st.session_state.fields_of_study_df = pd.DataFrame()

image_url = 'https://raw.githubusercontent.com/XamkDataLab/lens_demo/main/DALL.jpg'
st.image(image_url)

start_date = st.date_input('Alkaen', value=pd.to_datetime('2024-01-01'))
end_date = st.date_input('Päättyen', value=pd.to_datetime('2024-03-01'))
terms = st.text_area('Hakutermit (erota pilkulla, operaattori OR)', value='chatbot', height=300).split(',')

if st.button('Hae Data'):
    token = st.secrets["mytoken"]
    publication_data = get_publication_data(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"), [term.strip() for term in terms], token)
    
    if publication_data and publication_data['data']:
        st.write(f"Löytyi {publication_data['total']} julkaisua")
        st.session_state.publications_df = publication_table(publication_data)
        st.session_state.fields_of_study_df = fields_of_study_table(publication_data)

# Always display the DataFrames if they exist
if not st.session_state.publications_df.empty:
    st.dataframe(st.session_state.publications_df.head())
if not st.session_state.fields_of_study_df.empty:
    st.dataframe(st.session_state.fields_of_study_df.head())

# Dropdown for selecting field of study - outside of 'Hae Data' button condition
if not st.session_state.fields_of_study_df.empty:
    unique_fields_of_study = st.session_state.fields_of_study_df['field_of_study'].unique().tolist()
    selected_field_of_study = st.selectbox('Select a Field of Study', ['All'] + unique_fields_of_study)
    
    if selected_field_of_study != 'All':
        relevant_lens_ids = st.session_state.fields_of_study_df[st.session_state.fields_of_study_df['field_of_study'] == selected_field_of_study]['lens_id'].tolist()
        
        if relevant_lens_ids:
            filtered_publications_df = st.session_state.publications_df[st.session_state.publications_df['lens_id'].isin(relevant_lens_ids)]
            
            if not filtered_publications_df.empty:
                st.dataframe(filtered_publications_df)
            else:
                st.write("No publications found for the selected field of study.")
        else:
            st.write("No lens_ids found for the selected field of study.")
