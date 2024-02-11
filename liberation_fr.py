# Import required libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import timeit

# Headers for simulating a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def faire_requete(url):
    """
    Effectuer une requête HTTP avec gestion des erreurs
    Args:
        url (str): l'URL de la requête HTTP

    Returns:
        bytes or None: Le contenu de la réponse si la requête est réussie, sinon None.
    """
    try:
        with requests.get(url, headers=headers) as reponse:
            reponse.raise_for_status()
            return reponse.content
    except requests.RequestException as e:
        print(f"Erreur de requête HTTP: {e}")
        return None

def extract_articles(category_url, num_articles):
    temps_debut = timeit.default_timer()
    liens_articles = []
    current_count = 0

    while current_count < num_articles:
        time.sleep(2)
        contenu = faire_requete(category_url + f"?start={current_count}&order=")

        if contenu:
            soup = BeautifulSoup(contenu, "html.parser")
            liens = soup.find_all("h3", {"class":"titre_article"})
            for lien in liens:
                if current_count >= num_articles:
                    break
                liens_articles.append("https://www.libe.ma" + lien.a["href"])
                current_count += 1

    lignes = []
    for lien in liens_articles:
        time.sleep(2)
        contenu = faire_requete(lien)
        if contenu:
            soup = BeautifulSoup(contenu, "html.parser")
            try:
                titre = soup.find("h1", {"class":"access"}).text.replace("\n", "").strip()
            except:
                titre = None
            try:
                description = soup.find("div", {"class":"access firstletter"}).text.replace("\n", "").strip()
            except:
                description = None
            try:
                date = soup.find("div", {"class":"date"}).text.replace("\n", "").strip()
            except:
                date = None
            lignes.append([titre, description, date])

    return lignes

def scrape_category(category_url, num_articles):
    article_data = extract_articles(category_url, num_articles)

    colonnes = ["titre", "content", "date"]
    articles_df = pd.DataFrame(article_data, columns=colonnes)

    csv_file_path = "liberation_art.csv"
    articles_df.to_csv(csv_file_path, index=False)

    return csv_file_path
'''
if __name__ == "__main__":
    category_url = "https://www.libe.ma/Economie_r10.html"
    num_articles = 10  # Number of articles to scrape
    csv_file_path = scrape_category(category_url, num_articles)
    # Now, csv_file_path can be used in Streamlit for uploading
'''