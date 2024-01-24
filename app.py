#web interface

import streamlit as st
import pandas as pd
import json
import importlib
import google_drive_handle as gdrive
from dotenv import load_dotenv
import os

# Load config.json
with open('config.json') as f:
    config = json.load(f)

drive = gdrive.authenticate_google_drive()
processed_files = set()
st.markdown(
    """
    <style>
        .centered {
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 class='centered'>Moroccan News Aggregator</h1>", unsafe_allow_html=True)

selected_websites = {}
selected_categories = {}

def save_file_id_mapping(file_id_mapping):
    with open("file_id_mapping.json", "w") as file:
        json.dump(file_id_mapping, file)

def load_file_id_mapping():
    try:
        with open("file_id_mapping.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}  # Return an empty dictionary if the file doesn't exist

file_id_mapping = load_file_id_mapping()

for website, details in config.items():
    if st.checkbox(website, key=website):
        # Language selection
        languages = details.get("languages", {})
        if languages and len(languages) > 1:
            language = st.selectbox(f'Choose language for {website}', list(languages.keys()), key=f'lang_{website}')
            selected_websites[website] = f"{website}_{language}"  # like: hespress_en
        else:
            selected_websites[website] = website  # like: akhbarona

        # Category selection
        categories = languages.get(language, {})
        if categories:
            categories = st.multiselect(f'Select categories for {website}', list(categories.keys()), key=f'{website}_categories')
            selected_categories[website] = categories

# Number of articles input
num_articles = st.number_input('Number of Articles', min_value=1, max_value=10000, step=1)

# Start scraping button
if st.button('Start Scraping'):
    with st.spinner('Scraping in progress...'):
        progress_bar = st.progress(0)
        total_tasks = sum(len(categories) for categories in selected_categories.values())
        completed_tasks = 0
        for website, module_name in selected_websites.items():
            scraper_module = importlib.import_module(module_name)
            for category in selected_categories.get(website, []):
                category_url = config[website]['languages'][language][category]
               
                file_path = scraper_module.scrape_category(category_url, num_articles)

                if file_path:
                    if file_path not in file_id_mapping:
                        file_id = gdrive.upload_file_to_drive(drive, file_path)
                        print(f"Uploading file: {file_path}, File ID: {file_id}")
                        file_id_mapping[file_path] = file_id
                        save_file_id_mapping(file_id_mapping)
                    else:
                        file_id = file_id_mapping[file_path]
                        print(f"File already uploaded. Using existing File ID: {file_id}")
            
                    if file_id:
                        download_link = gdrive.get_drive_download_link(drive, file_id)
                        if download_link:
                            #st.markdown(f"[Download {website} - {category} data]({download_link})", unsafe_allow_html=True)

                            df = pd.read_csv(file_path)
                            st.write(f"{website} - {category} Data:")
                            st.dataframe(df)
                        else:
                            st.error(f"Failed to retrieve download link for file ID: {file_id}")
                    else:
                        st.error(f"Failed to upload file for {website} - {category}")
                else:
                    st.error(f"File not created for {website} - {category}")

        st.success('Scraping Completed!')
