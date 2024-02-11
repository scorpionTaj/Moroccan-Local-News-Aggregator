# Moroccan News Aggregator

The Moroccan News Aggregator is a simple web scraping project designed to extract news articles from popular Moroccan news websites. The goal is to provide users with a convenient way to access and categorize news content from different sources.

## Features

- **Multi-Language Support:** Choose news articles in English, Arabic, or French languages from websites such as Hespress, Akhbarona, and Le360.
  
- **Category Selection:** Select specific categories within each language to filter news articles based on your interests.

- **Data Storage:** The scraped data is uploaded to Google Drive, ensuring easy access and sharing.

## Setup Instructions

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/scorpionTaj/news-scraper
    ```

2. **Install Dependencies In Terminal Using PIP:**

    ```bash
    pip install streamlit pandas selenium google_drive_handle python-dotenv
    ```

3. **Run the App:**

    ```bash
    streamlit run app.py
    ```

4. Follow the on-screen instructions to choose websites, languages, categories, and start scraping news articles.

## Configuration

Adjust settings in the `config.json` file to customize supported websites, languages, and categories.

## License

This project is licensed under the [MIT License](LICENSE).

---

Feel free to explore and customize the project for your needs. If you encounter any issues or have suggestions for improvements, please let us know!
