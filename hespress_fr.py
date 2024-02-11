from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time
import re
import os
import requests
import csv
from urllib.parse import urljoin
from google_drive_handle import authenticate_google_drive
drive = authenticate_google_drive()


# Set up Chrome WebDriver with options
options = ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('log-level=3')


# Initialize the Chrome WebDriver
wd = webdriver.Chrome(options=options)

def download_image(img_url):
    return img_url

def scroll_page(expected_article_count):
    scroll_pause_time = 2
    screen_height = wd.execute_script("return window.innerHeight;")
    scrolled_height = 0

    while True:
        scrolled_height += screen_height
        wd.execute_script(f"window.scrollTo(0, {scrolled_height});")
        time.sleep(scroll_pause_time)
        new_height = wd.execute_script("return document.body.scrollHeight")
        if scrolled_height >= new_height:
            break

        soup = BeautifulSoup(wd.page_source, 'html.parser')
        articles = soup.find_all('div', class_='overlay card')
        if len(articles) >= expected_article_count:
            break

def scrape_article_details(article_url):
    try:
        wd.get(article_url)
        WebDriverWait(wd, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'article-content')))
        soup = BeautifulSoup(wd.page_source, 'html.parser')
        content_tag = soup.find('div', class_='article-content')
        content = content_tag.get_text().strip() if content_tag else ""
        date_tag = soup.find('small', class_='text-muted time')
        date = date_tag.get_text().strip() if date_tag else ""
        image_tag = soup.find('img', class_='wp-post-image')
        image_url = image_tag['src'] if image_tag else None
        img_url = download_image(urljoin(article_url, image_url)) if image_url else None
        return content, date, img_url
    except TimeoutException:
        print("Timed out waiting for page elements to load")
        return "", "", None
    except Exception as e:
        print(f"An error occurred while scraping article details: {str(e)}")
        return "", "", None

def scrape_article_details(article_url):

    try:
        wd.get(article_url)
        WebDriverWait(wd, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'article-content')))  # Adjusted to wait for article content
        soup = BeautifulSoup(wd.page_source, 'html.parser')

        content_tag = soup.find('div', class_='article-content')
        content = content_tag.get_text().strip() if content_tag else ""

        date_tag = soup.find('small', class_='text-muted time')
        date = date_tag.get_text().strip() if date_tag else ""

        image_tag = soup.find('img', class_='wp-post-image')
        image_url = image_tag['src'] if image_tag else None

        img_url = download_image(urljoin(article_url, image_url)) if image_url else None

        return content, date, img_url

    except TimeoutException:
        print("Timed out waiting for page elements to load")
        return "", "", None, ""
    except Exception as e:
        print(f"An error occurred while scraping article details: {str(e)}")
        return "", "", None, ""

def sanitize_filename(filename):
    return re.sub(r'[^\w\s-]', '', filename).strip().lower().replace(' ', '_')

def scrape_category(category_url, num_articles):
    print("Attempting to scrape:", category_url)
    articles_data = []
    wd.get(category_url)
    scroll_page(num_articles)

    soup = BeautifulSoup(wd.page_source, 'html.parser')
    articles = soup.find_all('div', class_='overlay card')
    for article in articles[:num_articles]:
        link_tag = article.find('a', class_='stretched-link')
        link = link_tag['href'] if link_tag else ""
        title_tag = article.find('h3', class_='card-title')
        title = title_tag.get_text().strip() if title_tag else ""
        content, date, img_url = scrape_article_details(link)
        article_data = {
            "Title": title,
            "Date": date,
            "Category": category_url.split('/')[-1],
            "Content": content,
            "Link": link,
            "Image": img_url
        }
        print(f"Scraping article: {title}, Link: {link}")
        articles_data.append(article_data)


    # Save scraped data to a CSV file
    category_name = sanitize_filename(category_url.split("/")[-1])
    csv_file_path = os.path.join(os.getcwd(), f'{category_name}_data_fr.csv')
    file_mode = 'a' if os.path.exists(csv_file_path) else 'w'

    try:
            with open(csv_file_path, file_mode, newline='', encoding='utf-8') as file:
                fieldnames = ["Title", "Date", "Category", "Content", "Link", "Image"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                if file_mode == 'w':
                    writer.writeheader()
                for article in articles_data:
                    writer.writerow(article)
            print(f"CSV file saved successfully at {csv_file_path}")
    except IOError as e:
            print(f"Failed to save file at {csv_file_path}: {e}")
            return None  # Return None to indicate failure

    # Check if the file exists before uploading

    if os.path.exists(csv_file_path):
        print(f"File successfully created at {csv_file_path}")
        return csv_file_path

    else:
        print(f"Failed to create file for {category_url}")
        return None