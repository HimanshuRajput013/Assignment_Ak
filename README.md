# News Summarization and Text-to-Speech Application

A web-based application that extracts key details from multiple news articles related to a given company, performs sentiment analysis, conducts a comparative analysis, and generates a text-to-speech (TTS) output in Hindi.

## Overview

This application allows users to input a company name and receive a structured sentiment report along with an audio output. The tool extracts information from at least 10 unique news articles, analyzes sentiment, compares coverage across sources, and provides an audio summary in Hindi.

## Features

- **News Extraction**: Extracts title, summary, and metadata from 10+ news articles related to the input company for this we scrap data from Times of India news website and use BeautifulSoup4 for scrapping data.
- 
- **Sentiment Analysis**: Performs sentiment analysis on article content (positive, negative, neutral) using `distilbert-base-uncased-finetuned-sst-2-english`
- **Comparative Analysis**: Conducts comparative sentiment analysis across multiple articles
- **Text-to-Speech**: Converts summarized content into Hindi speech
- **User Interface**: Simple web interface built with Streamlit
- **API Integration**: Communication between frontend and backend via RESTful APIs

## Live Demo

[Access the application on Hugging Face Spaces](https://huggingface.co/spaces/YOUR_USERNAME/news-summarization-tts)

## Project Structure

```
news-summarization-tts/
├── app.py                 # Main Streamlit application
├── api.py                 # API endpoints
├── utils.py               # Utility functions
├── requirements.txt       # Dependencies
├── Dockerfile             # For containerization
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
   git clone https://github.com/YOUR_USERNAME/news-summarization-tts.git
   cd news-summarization-tts
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
   python api.py
   ```

2. In a separate terminal, run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

3. Open your browser and navigate to `http://localhost:8501`

## Technologies Used

### Libraries and Frameworks

- **BeautifulSoup (bs4)**: For web scraping news articles
- **NLTK/Transformers**: For sentiment analysis
- **Hugging Face**: For text-to-speech models
- **Streamlit**: For the user interface
- **FastAPI**: For API development
- **Pandas**: For data manipulation and analysis

### Models

- **Sentiment Analysis**: DistilBERT fine-tuned on financial news
- **Text-to-Speech**: AI4Bharat/TTS-Hindi model from Hugging Face

## API Documentation

The application exposes the following API endpoints:

### 1. GET /api/companies

Returns a list of available companies for the dropdown.

**Response:**
```json
{
  "companies": ["Tesla", "Apple", "Microsoft", "Google", "Amazon"]
}
```

### 2. POST /api/news

Fetches news articles for a specified company.

**Request:**
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

## Implementation Details

### News Extraction

- Uses BeautifulSoup to scrape non-JavaScript web links
- Extracts title, content, publication date, and source
- Focuses on financial news sources and company press releases

### Sentiment Analysis

- Employs a fine-tuned DistilBERT model for financial sentiment analysis
- Classifies articles as positive, negative, or neutral
- Calculates confidence scores for sentiment classification

### Comparative Analysis

- Identifies common and unique topics across articles
- Analyzes sentiment distribution
- Highlights contradictions or agreements between sources
- Provides impact assessment on overall company perception

### Text-to-Speech

- Translates the final English summary to Hindi using a translation model
- Generates natural-sounding Hindi speech using AI4Bharat's TTS model
- Provides audio playback in the web interface

## Assumptions and Limitations

- **News Sources**: The application focuses on accessible, non-JavaScript news sources that can be scraped with BeautifulSoup.
- **Language**: Primary analysis is done in English before translation to Hindi for TTS.
- **Company Coverage**: Assumes the input company has at least 10 recent news articles available.
- **Rate Limiting**: Web scraping respects rate limits to avoid being blocked by news sites.
- **Processing Time**: Due to the comprehensive analysis, results may take 10-15 seconds to generate.

## Future Improvements

- Add support for more languages
- Implement more sophisticated topic modeling
- Expand company database with historical data
- Add visualization components for sentiment trends
- Improve scraping capabilities to handle JavaScript-rendered content

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
