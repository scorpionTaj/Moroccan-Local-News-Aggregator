import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from google_drive_handle import authenticate_google_drive
drive = authenticate_google_drive()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def scrape_article(article_url):
    response = requests.get(article_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    title_tag = soup.find('h1')
    title = title_tag.get_text(strip=True) if title_tag else 'No Title'

    content_div = soup.find('div', id='article_holder')  # Ensure this is the correct ID
    if content_div:
        content = ' '.join(p.get_text(strip=True) for p in content_div.find_all('p'))
    else:
        content = 'Content not found'

    return {
        'Title': title,
        'Content': content
    }

def scrape_category(category_url, num_articles):
    articles_scraped = 0
    all_articles = []
    page_num = 1

    # Extract site and category from the URL
    site_name = category_url.split('/')[2]  # This gets 'www.akhbarona.com' from the URL
    site_name = site_name.replace('www.', '')
    category_name = category_url.split('/')[-1]  # This gets the category name from the URL

    while articles_scraped < num_articles:
        paginated_url = f"{category_url}/index.{page_num}.html"

        response = requests.get(paginated_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        article_links = soup.find_all('h2', class_='article_title')
        for article_link in article_links:
            a_tag = article_link.find('a')
            if a_tag and 'href' in a_tag.attrs:
                full_article_url = a_tag['href']
                if not full_article_url.startswith('http'):
                    full_article_url = f"{category_url}/{full_article_url}"
                article_data = scrape_article(full_article_url)

                all_articles.append(article_data)
                articles_scraped += 1

                if articles_scraped >= num_articles:
                    break

        if articles_scraped >= num_articles:
            break

        print(f"Going to next page: {paginated_url}")
        page_num += 1  # Increment the page number


    #csv_file_path = os.path.join(os.getcwd(), f'{category_name}_data_en.csv')
    df = pd.DataFrame(all_articles)
    csv_file_name = f"{site_name}_{category_name}_articles.csv"
    csv_file_path = os.path.join(os.getcwd(), csv_file_name)  # Full file path
    df.to_csv(csv_file_path, index=False)
    print(f"Articles saved to {csv_file_path}")

    return csv_file_path




