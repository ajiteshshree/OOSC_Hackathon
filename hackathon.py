import requests
from bs4 import BeautifulSoup
import json

def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True)]
    return links

def save_content(url, filepath):
    response = requests.get(url)
    with open(filepath, 'w') as file:
        json.dump({'url': url, 'content': response.text}, file)

# Example usage
website_url = "https://www.wsj.com/"
links = scrape_website(website_url)
for i, link in enumerate(links):
    save_content(link, f'page_content_{i}.json')


