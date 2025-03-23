---
license: apache-2.0
title: News Scrapper
sdk: streamlit
emoji: 📚
colorFrom: red
colorTo: yellow
short_description: News Scrapper
---

# News Summarization and Text-to-Speech Application

A web-based application that extracts key details from multiple news articles related to a given company, performs sentiment analysis, conducts a comparative analysis, and generates a text-to-speech (TTS) output in Hindi.

## Overview

This application allows users to input a company name and receive a structured sentiment report along with an audio output. The tool extracts information from at least 10 unique news articles, analyzes sentiment, compares coverage across sources, and provides an audio summary in Hindi.

## Features

- **News Extraction**: Extracts the title, summary, and metadata from 10+ news articles related to the input company. News data is scraped from the Times of India website using `BeautifulSoup4`
- **Sentiment & Summarization Analysis**: Sentiment analysis is performed using the `distilbert-base-uncased-finetuned-sst-2-english` model. Summarization is done with the `sshleifer/distilbart-cnn-12-6 open-source model`.Topic extraction is handled using `KeyBERT`.
- **Comparative Analysis**: Analyzes sentiment distribution across multiple articles to identify differences in coverage.
- **Text-to-Speech**: Converts the summarized content into Hindi speech.Translation is done using `GoogleTranslator`.Hindi audio is generated using `gTTS`.
- **User Interface**: Simple web interface built with `Streamlit`
- **API Integration**: Communication between frontend and backend via `RESTful APIs`

## Live Demo

[Access the application on Hugging Face Spaces](https://huggingface.co/spaces/Himanshu0013/Akaike_News_Scrapper)

## Project Structure

```
news-summarization-tts/
├── app.py                 # Main Streamlit application
├── api.py                 # API endpoints
├── utils.py               # Utility functions
├── requirements.txt       # Dependencies
├── .gitignore             # Git ignore file
└── README.md              # Project documentation
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/HimanshuRajput013/Assignment_Ak.git
   cd Assignment_Ak
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running Locally

1. Start the API server:
   ```bash
   uvicorn api:app --host 0.0.0.0 --port 8000
   ```
   # Accessing the API via Postman
   1.Choose `POST` as the request type.

   2.Set the API Endpoint `URL` : `http://127.0.0.1:8000/analyze/`

   3.Configure the Request Body:  In Postman, navigate to the `Body` tab and select `raw`. Choose `JSON` format and enter the following request body:
       ```json
      {
        "company": "Tesla"
      }
      ``
      
   4.Response: Returns a `JSON` object containing extracted news articles and analysis as shown in the example output format.


3. In a separate terminal, run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

4. Open your browser and navigate to `http://localhost:8501`

## Technologies Used

### Libraries and Frameworks

- **BeautifulSoup (bs4)**: For web scraping news articles
- **NLTK/Transformers**: For sentiment analysis
- **Hugging Face**: For summariztion models
- **Streamlit**: For the user interface
- **FastAPI**: For API developments

**Example API Request**

```json
{
  "company": "Tesla"
}
```

**Response:**

Returns a JSON object containing extracted news articles and analysis as shown in the example output format.

### 3. POST /api/tts

Generates Hindi text-to-speech audio from the analysis.

**Response:**
Returns an audio file in base64 encoding.

## Example Output

```json
{
  "Company": "Tesla",
  "Articles": [
    {
      "Title": "Tesla's New Model Breaks Sales Records",
      "Summary": "Tesla's latest EV sees record sales in Q3...",
      "Sentiment": "Positive",
      "Topics": ["Electric Vehicles", "Stock Market", "Innovation"]
    },
    {
      "Title": "Regulatory Scrutiny on Tesla's Self-Driving Tech",
      "Summary": "Regulators have raised concerns over Tesla's self-driving software...",
      "Sentiment": "Negative",
      "Topics": ["Regulations", "Autonomous Vehicles"]
    }
  ],
  "Comparative Sentiment Score": {
    "Sentiment Distribution": {
      "Positive": 1,
      "Negative": 1,
      "Neutral": 0
    },
    "Coverage Differences": [
      {
        "Comparison": "Article 1 highlights Tesla's strong sales, while Article 2 discusses regulatory issues.",
        "Impact": "The first article boosts confidence in Tesla's market growth, while the second raises concerns about future regulatory hurdles."
      },
      {
        "Comparison": "Article 1 is focused on financial success and innovation, whereas Article 2 is about legal challenges and risks.",
        "Impact": "Investors may react positively to growth news but stay cautious due to regulatory scrutiny."
      }
    ],
    "Topic Overlap": {
      "Common Topics": ["Electric Vehicles"],
      "Unique Topics in Article 1": ["Stock Market", "Innovation"],
      "Unique Topics in Article 2": ["Regulations", "Autonomous Vehicles"]
    }
  },
  "Final Sentiment Analysis": "Tesla's latest news coverage is mostly positive. Potential stock growth expected.",
  "Audio": "[Play Hindi Speech]"
}
```

## Assumptions and Limitations

- **News Sources**: The application focuses on accessible, non-JavaScript news sources that can be scraped with BeautifulSoup.
- **Language**: Primary analysis is done in English before translation to Hindi for TTS.
- **Company Coverage**: Assumes the input company has at least 10 recent news articles available.
- **Rate Limiting**: Web scraping respects rate limits to avoid being blocked by news sites.
- **Processing Time**: Due to the comprehensive analysis, results may take 20-25 seconds to generate.

## Future Improvements

- Add support for more languages
- Implement more sophisticated topic modeling
- Expand company database with historical data
- Add visualization components for sentiment trends

