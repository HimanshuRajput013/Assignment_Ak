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
  "company": "Tata_Motor"
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
  "Company": "Tata Motors",
  "Articles": [
    {
      "Title": "Planning to buy car? Maruti, Tata, Kia to get pricier from this date: Details",
      "Summary": "Kia India has announced a price hike of up to 3% across its entire range, set to take effect from April 1. Tata Motors and Maruti Suzuki have also confirmed price increases on their vehicles. Maruti had previously raised prices on January 1 and again on February 1, making this the third hike in four months.",
      "Sentiment": {
        "label": "POSITIVE",
        "score": 0.9007
      },
      "URL": "https://timesofindia.indiatimes.com/auto/cars/planning-to-buy-car-maruti-tata-kia-to-get-pricier-from-this-date-details/articleshow/119190768.cms",
      "Topics": [
        "price hike",
        "price increases",
        "kia india",
        "kia",
        "raised prices"
      ]
    },
    {
      "Title": "Hyundai Creta, Exter, Verna & more to get expensive from this date: Here's why",
      "Summary": "Hyundai Motor India Limited has announced a price hike of up to 3%, set to take effect from April 2025. The automaker cited rising input costs, higher commodity prices, and increased operational expenses as key reasons for the revision. Kia India has also announced a 3% hike effective from April 1, while Maruti Suzuki and Tata Motors have also announced their decision to increase prices.",
      "Sentiment": {
        "label": "NEGATIVE",
        "score": 0.7824
      },
      "URL": "https://timesofindia.indiatimes.com/auto/cars/hyundai-creta-exter-verna-more-to-get-expensive-from-this-date-heres-why/articleshow/119213772.cms",
      "Topics": [
        "price hike",
        "kia india",
        "kia",
        "prices increased",
        "increase prices"
      ]
    }
  ],
  "Comparative Sentiment Score": {
    "Sentiment Distribution": {
      "POSITIVE": 1,
      "NEGATIVE": 1,
      "NEUTRAL": 0
    },
    "Coverage Differences": [
      {
        "Comparison": "Planning to buy car? Maruti, Tata, Kia to get pricier from this date: Details vs Hyundai Creta, Exter, Verna & more to get expensive from this date: Here's why",
        "Impact": "Planning to buy car? Maruti, Tata, Kia to get pricier from this date: Details discusses POSITIVE news, whereas Hyundai Creta, Exter, Verna & more to get expensive from this date: Here's why focuses on NEGATIVE coverage."
      }
    ],
    "Topic Overlap": {
      "Common Topics": [
        "kia",
        "price hike",
        "kia india"
      ],
      "Unique Topics per Article": {
        "Planning to buy car? Maruti, Tata, Kia to get pricier from this date: Details": [
          "raised prices",
          "price increases"
        ],
        "Hyundai Creta, Exter, Verna & more to get expensive from this date: Here's why": [
          "increase prices",
          "prices increased"
        ]
      }
    }
  },
  "Final Sentiment Analysis": "Tata Motors' latest news coverage is mostly POSITIVE. Potential stock growth expected.",
  "Hindi_audio": "complete_analysis.mp3"
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

