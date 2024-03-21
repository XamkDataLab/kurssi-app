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
            unique_fields_of_study = fields_of_study_df['field_of_study'].unique().tolist()
            
            selected_field_of_study = st.selectbox('Select a Field of Study', ['All'] + unique_fields_of_study)
            
            if selected_field_of_study != 'All':
                filtered_fields_of_study = fields_of_study_df[fields_of_study_df['field_of_study'] == selected_field_of_study]
                filtered_publications_df = pd.merge(publications_df, filtered_fields_of_study, on='lens_id')
            else:
                filtered_publications_df = publications_df
            
            st.dataframe(filtered_publications_df)
    
        else:
            st.write("No publication data fetched. Please check your inputs and try again.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

