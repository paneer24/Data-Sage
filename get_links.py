import requests
import json
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse
import re

load_dotenv()

def get_links(topic):
    topic = topic.replace(" ", "+")
    api_key = os.getenv("SERPER_API_KEY")

    url = f"https://google.serper.dev/search?q={topic}&apiKey={api_key}"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    json_data = json.loads(response.text)

    links = []

    for item in json_data["organic"]:
        links.append(item['link'])
        if "sitelinks" in item:
            for sub in item["sitelinks"]:
                links.append(sub['link'])

    return links

def save_page_content(links, topic):
    # Create logs folder if it doesn't exist
    log_folder = "logs"
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    
    # Create topic-specific subfolder
    topic_folder = os.path.join(log_folder, re.sub(r'[^\w\s-]', '', topic).strip())
    if not os.path.exists(topic_folder):
        os.makedirs(topic_folder)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for i, link in enumerate(links):
        try:
            print(f"Fetching content from: {link}")
            
            # Get page content
            response = requests.get(link, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Parse HTML and extract text
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Create filename from URL
            parsed_url = urlparse(link)
            filename = f"{i+1:02d}_{parsed_url.netloc}_{parsed_url.path.replace('/', '_')}.txt"
            filename = re.sub(r'[^\w\s-]', '', filename).strip()[:100]  # Limit filename length
            
            filepath = os.path.join(topic_folder, filename)
            
            # Save content to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"URL: {link}\n")
                f.write("=" * 80 + "\n\n")
                f.write(text)
            
            print(f"Saved: {filename}")
            
            # Add delay to be respectful to servers
            time.sleep(1)
            
        except Exception as e:
            print(f"Error fetching {link}: {str(e)}")
            continue

# Usage example
if __name__ == "__main__":
    topic = "artificial intelligence"
    links = get_links(topic)
    save_page_content(links, topic)