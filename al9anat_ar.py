from typing_extensions import Self
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from bs4 import BeautifulSoup
import time
import os
import re
import requests
import json
import csv
from urllib.parse import urljoin




# Set up Chrome WebDriver with options
options = ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Initialize the Chrome WebDriver
wd = webdriver.Chrome(options=options)

def download_image(img_url):
    return img_url

def sanitize_filename(filename):
    return re.sub(r'[^\w\s-]', '', filename).strip().lower().replace(' ', '_')

def scroll_page(wd, max_scrolls=7, articles_per_load=6, max_attempts=5):
    scroll_pause_time = 5
    attempts = 0

    for _ in range(max_scrolls):
        current_articles = len(wd.find_elements(By.CSS_SELECTOR, "article.l-post"))
        wd.execute_script("window.scrollBy(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)

        try:
            load_more_button = WebDriverWait(wd, 10).until(
                EC.presence_of_element_located((By.XPATH, '//a[@class="ts-button load-button load-button-a ts-button-alt" and @href="#"]'))
            )
            wd.execute_script("arguments[0].scrollIntoView();", load_more_button)
            wd.execute_script("arguments[0].click();", load_more_button)
            attempts = 0  # Reset attempts after successful button click
        except TimeoutException:
            attempts += 1
            if attempts >= max_attempts:
                print("Maximum attempts reached without new articles. Exiting.")
                return False  # Exit the function

        new_article_count = len(wd.find_elements(By.CSS_SELECTOR, "article.l-post"))
        if new_article_count > current_articles:
            attempts = 0  # Reset attempts after successfully loading new articles
        else:
            attempts += 1
            if attempts >= max_attempts:
                print("No new articles found after several attempts. Exiting.")
                return False  # Exit the function

    return True



def scrape_article_details(article_url, wd):
    try:
        # Validate the URL
        if not article_url.startswith("http"):
            article_url = "https://" + article_url
        print("Navigating to:", article_url)

        wd.get(article_url)
        WebDriverWait(wd, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'the-post-tags')))  # Wait for a specific element to ensure the page has loaded

        soup = BeautifulSoup(wd.page_source, 'html.parser')
        content_tag = soup.find('div', class_='post-content cf entry-content content-spacious')
        content = content_tag.get_text().strip() if content_tag else ""

        category_tag = soup.find('span', class_='meta-item cat-labels')
        category_from_article = category_tag.get_text().strip() if category_tag else "Uncategorized"

        title_tag = soup.find('h1', class_='is-title post-title')
        art_title = title_tag.get_text().strip() if title_tag else ""

        date_tag = soup.find('span', class_='meta-item has-next-icon date')
        date = date_tag.get_text().strip() if date_tag else ""

        image_tag = soup.find('a', class_='image-link')
        image_url = image_tag['href'] if image_tag else None
        img_url = urljoin(article_url, image_url)
        image_path = download_image(img_url) if image_url else None

        return content, date, image_path, art_title, category_from_article
    except TimeoutException:
        print("Timed out waiting for page elements to load for URL:", article_url)
        return "", "", None, "", ""
    except Exception as e:
        print(f"An error occurred while scraping article details at {article_url}: {str(e)}")
        return "", "", None, "", ""


def scrape_category(category_url, category_name, wd,num_articles):
    print("Attempting to scrape:", category_url)
    articles_data = []
    articles_count = 0
    wd.get(category_url)

    scroll_page(num_articles)

    soup = BeautifulSoup(wd.page_source, 'html.parser')
    articles = soup.find_all('article', class_='l-post grid-base-post grid-post')

    for article in articles:
        link_tag = article.find('a', class_='image-link media-ratio ratio-16-9')
        link = link_tag['href'] if link_tag else ""
        if link :
            wd.get(link)
            article_data = scrape_article_details(link, wd)
            if article_data[0]:  # Check if content is non-empty
                articles_data.append({
                    "art_id": articles_count,
                    "Title": article_data[3],
                    "Date": article_data[1],
                    "Category": article_data[4],
                    "Content": article_data[0],
                    "Link": link,
                    "Image": article_data[2],
                })
                articles_count += 1
                print(f"Article #{articles_count} scraped: {article_data[3]}")

    category_name = sanitize_filename(category_url.split("/")[-1])
    csv_file_path = os.path.join(os.getcwd(), f'{category_name}_data_ar.csv')
    file_mode = 'a' if os.path.exists(csv_file_path) else 'w'
    try:
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ["art_id", "Title", "Date", "Category", "Content", "Link", "Image"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for article in articles_data:
                writer.writerow(article)
        print(f"Data written to {csv_file_path} successfully.")
    except Exception as e:
        print(f"Error writing data to file: {e}")

    print(f"Total articles scraped for {category_name}: {len(articles_data)}")

    # Check if the file exists before uploading
    
    if os.path.exists(csv_file_path):
        print(f"File successfully created at {csv_file_path}")
        return csv_file_path
        
    else:
        print(f"Failed to create file for {category_url}")
        return None