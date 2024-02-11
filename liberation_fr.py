# Importation des bibliotiques
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import timeit


# En-têtes pour simuler une requête du navigateur
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


def convert(secondes):
    """
    Convertit un nombre de secondes en heures, minutes et secondes.

    Args:
        secondes (int): Le nombre total de secondes à convertir.

    Returns:
        list: Liste contenant la chaîne de caractères représentant le temps au format HH:MM:SS.
    """
    heures = secondes // 3600
    secondes %= 3600
    minutes = secondes // 60
    secondes %= 60

    return ["%d:%02d:%02d" % (heures, minutes, secondes)]

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


def extraire_articles(start_page, final_page):
    """
    Extraction des liens des articles.
    Args:
        nombre_pages: présente le nombre de page dans la catégorie de l'économie
    """

    temps_debut = timeit.default_timer()

    liens_articles = []

    lien_page = f"https://www.libe.ma/Economie_r10.html?start=1&order="
    time.sleep(2)
    contenu = faire_requete(lien_page)

    if contenu:
        soup = BeautifulSoup(contenu, "html.parser")
        liens = soup.find_all("div", {"class":"jl_clist_layout"})
        liens_articles.extend([lien.a["href"] for lien in liens])

    for page in range(start_page, final_page + 1):
        lien_page = f"https://www.libe.ma/Economie_r10.html?start={6*page}&order="
        time.sleep(2)
        contenu = faire_requete(lien_page)

        if contenu:
            soup = BeautifulSoup(contenu, "html.parser")
            liens = soup.find_all("h3", {"class":"titre_article"})
            liens_articles.extend(["https://www.libe.ma" + lien.a["href"] for lien in liens])

    #liens_df = pd.DataFrame(liens_articles, columns=["liens"])
    #liens_df.to_csv(f"liberation_urls.csv", index=False)

    colonnes = ["titre", "description", "date"]
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

    articles_df = pd.DataFrame(lignes, columns=colonnes)
    articles_df.to_csv(f"liberation_art.csv", index=False)

    duree = timeit.default_timer() - temps_debut
    duree_extraction = pd.DataFrame(convert(duree), columns=["durée d'extration"])
    duree_extraction.to_csv(f"duree_ext.txt")

    return liens_articles, articles_df, duree_extraction

if __name__ == "__main__":
    liens_articles, articles_df, duree_extraction = extraire_articles(start_page=1, final_page=1)
