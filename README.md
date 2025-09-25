## Data-Sage
A Python application that searches the web, scrapes content from relevant sources, and generates AI-powered answers using the collected data.

## Features
Web search using Google Serper API
Content scraping and cleaning from multiple websites
AI-powered answers using Google Gemini
Simple Streamlit-based web interface
Token usage tracking for transparency
Organized logging with timestamped folders

## Project Structure  
```bash
Data Sage/
├── client.py # Streamlit interface
├── main.py # Command-line interface
├── get_links.py # Web search functionality
├── scrape.py # Scraping logic
├── cleaning.py # Content processing
├── llm.py # AI model integration
├── requirements.txt # Project dependencies
├── .env # Environment variables
└── logs/ # Saved content
```
## Required API Keys
- Serper.dev – for web search
- Google AI Studio – for Gemini AI
## How It Works
1. Searches the web for relevant links
2. Scrapes content from selected websites
3. Processes and merges the collected text
4. Uses Gemini AI to generate an answer
5. Displays the response and token usage
