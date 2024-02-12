# Moroccan News Aggregator

The Moroccan News Aggregator is a simple web scraping project designed to extract news articles from popular Moroccan news websites. The goal is to provide users with a convenient way to access and categorize news content from different sources.

## Features

- **Streamlit Interface**: Streamlit provides an intuitive and interactive user interface for accessing aggregated news data. Users can conveniently browse through categorized news articles and explore the latest updates from Moroccan news sources.

- **Google Drive Integration**: Google Drive serves as the backend storage solution for managing and storing extracted news articles and related data. PyDrive, a wrapper library for Google Drive API, facilitates seamless integration with Google Drive.

- **Selenium Web Scraping**: Selenium automates the process of navigating through various Moroccan news websites, extracting relevant information, and categorizing the articles. It handles tasks such as logging in, navigating through pages, and extracting data from dynamic web elements.

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


## Usage

Once the Streamlit app is running, you can access the Moroccan News Aggregator through your web browser. Browse through the categorized news articles, explore the latest updates, and enjoy a streamlined news browsing experience tailored for Moroccan news content.

## Contributing

Contributions to the Moroccan News Aggregator project are welcome! If you have suggestions for improvements, new features, or bug fixes, feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

The Moroccan News Aggregator project relies on the contributions of various open-source libraries and tools. Special thanks to the developers and maintainers of Streamlit, Selenium, Google Drive API, and other dependencies used in this project.

---

Feel free to explore and customize the project for your needs. If you encounter any issues or have suggestions for improvements, please let us know!
