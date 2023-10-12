import requests
from bs4 import BeautifulSoup as bs
import csv
from urllib.parse import urljoin

# Constants
BASE_URL = "https://pergikuliner.com/restaurants?default_search=&search_name_cuisine=&search_place=&page="
TIMEOUT = 30
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
}

# Function to extract and clean text from an element
def extract_text(element):
    return element.text.strip() if element else ''

def extract_ratings(soup):
    ratings = soup.find_all('div', class_='rate-box-bottom')
    return [extract_text(e) for e in ratings]

def extract_contact_info(soup):
    contact_info = soup.find_all('p', class_='small-screen-toggle')
    return [extract_text(e) for e in contact_info]

def extract_hours(soup):
    hours = soup.find_all('p', class_='small-screen-toggle')[-1].find_all('span', class_='left')[-1]
    return extract_text(hours)

def extract_payment_methods(soup):
    for e in soup.find('div', class_='info-list').find_all('li'):
        if 'Pembayaran' in extract_text(e):
            payment_method = extract_text(e).replace('Pembayaran', '')
            return payment_method
    return ''

def extract_facilities(soup):
    facilities = ''.join([extract_text(e) for e in soup.find('div', class_='facility-list').find_all('label', class_='checked')])
    return facilities

def fetch_restaurant_data(session, url, resto):
    html = session.get(url, timeout=TIMEOUT, headers=HEADERS).content
    soup = bs(html, 'html.parser')
    restaurant_data = {
        'Nama': extract_text(soup.find('div', class_='heading')),
        'Lokasi': '',
        'Tipe Kuliner': '',
        'Rasa': '',
        'Suasana': '',
        'Harga : Rasa': '',
        'Pelayanan': '',
        'Kebersihan': '',
        'Jam Buka': '',
        'Pembayaran': '',
        'Fasilitas': '',
        'Alamat': '',
        'Telepon': '',
        'Price per Person': '',
        'URL': url,
    }

    try:
        location_cuisine = extract_text(resto.find('div', class_='item-group').find('div')).split('|')
        restaurant_data['Lokasi'], restaurant_data['Tipe Kuliner'] = location_cuisine
    except:
        pass

    try:
        ratings = extract_ratings(soup)
        restaurant_data['Rasa'], restaurant_data['Suasana'], restaurant_data['Harga : Rasa'], restaurant_data['Pelayanan'], restaurant_data['Kebersihan'] = ratings
    except:
        pass

    try:
        contact_info = extract_contact_info(soup)
        restaurant_data['Telepon'], _ = contact_info
    except:
        pass

    try:
        restaurant_data['Jam Buka'] = extract_hours(soup)
    except:
        pass

    try:
        restaurant_data['Alamat'] = ''.join([e.strip() for e in soup.find('p', class_=None).find('span').text.split('\n')])
    except:
        pass

    try:
        restaurant_data['Pembayaran'] = extract_payment_methods(soup)
    except:
        pass

    try:
        restaurant_data['Price per Person'] = extract_text(soup.find('span', {'id': 'avg-price'}))
    except:
        pass

    try:
        restaurant_data['Fasilitas'] = extract_facilities(soup)
    except:
        pass

    return restaurant_data

def main():
    session = requests.Session()
    with open('data_pergikuliner.csv', 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['Nama', 'URL', 'Lokasi', 'Tipe Kuliner', 'Rasa', 'Suasana', 'Harga : Rasa',
                      'Pelayanan', 'Kebersihan', 'Jam Buka', 'Pembayaran',
                      'Fasilitas', 'Alamat', 'Telepon', 'Price per Person']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(1, 126):
            url = f"{BASE_URL}{i}"
            html = session.get(url, timeout=TIMEOUT, headers=HEADERS).content
            soup = bs(html, 'html.parser')
            for resto in soup.find_all('div', 'restaurant-result-wrapper best-rating'):
                resto_url = urljoin(url, resto.find('a', href=True)['href'])
                restaurant_data = fetch_restaurant_data(session, resto_url, resto)
                writer.writerow(restaurant_data)
                f.flush()

if __name__ == '__main__':
    main()
