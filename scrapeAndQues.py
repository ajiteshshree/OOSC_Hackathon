import requests
from bs4 import BeautifulSoup
import json

# Function to scrape the website and retrieve all links
def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True)]
    return links

# Function to save webpage content and generate questions
def save_content_and_generate_questions_separately(url, content_filepath, questions_filepath, api_key):
    response = requests.get(url)
    content = response.text

    # Save the content to a JSON file
    with open(content_filepath, 'w') as file:
        json.dump({'url': url, 'content': content}, file)

    # Generate questions using the Gemini API
    questions = generate_questions(content, api_key)
    
    # Save the questions to a separate JSON file
    with open(questions_filepath, 'w') as file:
        json.dump({'url': url, 'questions': questions}, file)

# Function to generate questions using Gemini API
def generate_questions(content, api_key, n=10):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'gemini',  # Replace with the correct model name if applicable
        'prompt': f"Generate {n} concise questions under 80 characters from the following content:\n{content}\n",
        'max_tokens': 100  # Adjust if necessary
    }
    
    response = requests.post('https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=AIzaSyBo7AOHMyMBxgd_P53yN1ufpnydEsSKU9Q', headers=headers, json=data)
    response.raise_for_status()  # Ensure we notice bad responses

    # Extract questions from the response
    result = response.json()
    text = result['choices'][0]['text'].strip()
    questions = [q.strip() for q in text.split('\n') if q.strip()]
    
    return questions

# Example usage
api_key = "AIzaSyBo7AOHMyMBxgd_P53yN1ufpnydEsSKU9Q"
website_url = "https://kwajrockets.blogspot.com/2008/"

# Scrape the website to get all links
links = scrape_website(website_url)

# For each link, save the content and generate questions in separate files
for i, link in enumerate(links):
    # if i>10: 
    #     break
    try:
        content_filepath = f'data/page_content_{i}.json'
        questions_filepath = f'data/page_questions_{i}.json'
        save_content_and_generate_questions_separately(link, content_filepath, questions_filepath, api_key)
    except Exception as e:
        print(f"Error processing {link}: {e}")
