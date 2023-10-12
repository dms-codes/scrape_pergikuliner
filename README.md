## Restaurant Data Scraper

This Python script is a web scraper designed to extract and collect information about restaurants from the [Pergi Kuliner](https://pergikuliner.com) website. It utilizes the `requests` library to fetch web pages, `BeautifulSoup` for parsing HTML, and writes the collected data to a CSV file. The script scrapes data such as restaurant name, location, cuisine type, ratings, contact information, opening hours, accepted payment methods, facilities, address, price per person, and more.

### Prerequisites

Before running this script, you need to have Python installed on your system. Additionally, install the required Python packages using the following command:

```bash
pip install requests beautifulsoup4
```

### Usage

1. Clone or download the repository from the following link: [Pergi Kuliner Scraper](https://github.com/yourusername/pergi-kuliner-scraper).

2. Navigate to the project directory:

```bash
cd pergi-kuliner-scraper
```

3. Run the script:

```bash
python pergi_kuliner_scraper.py
```

The script will start scraping restaurant data from multiple pages on the Pergi Kuliner website.

### Output

The collected restaurant data will be saved to a CSV file named `data_pergikuliner.csv` in the project directory.

### Disclaimer

Please ensure that you have the necessary permissions and follow ethical scraping practices when using this script. Respect the website's terms of service, privacy policy, and robots.txt file.
