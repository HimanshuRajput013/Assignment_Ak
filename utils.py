import requests
from bs4 import BeautifulSoup
import logging
from transformers import pipeline
import re
import logging
from keybert import KeyBERT
from typing import Dict,List,Set
import os
from deep_translator import GoogleTranslator
from gtts import gTTS

log_file = "app.log"

# Ensure log file exists
if not os.path.exists(log_file):
    open(log_file, "w").close()

# Remove previous handlers to allow reconfiguration
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename=log_file,
    filemode="a",
    force=True
)

# Load Summary model 
summary_pipeline = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
# Load Sentiment model 
sentiment_pipeline = pipeline(
                                "sentiment-analysis",
                                model="distilbert/distilbert-base-uncased-finetuned-sst-2-english",
                                )
#Load keyBERT for Topic Modelling for every articale
kw_model = KeyBERT()



def extract_articles(company: str, num_articles: int = 10) -> List[Dict[str, str]]:
    """Extracts the latest news articles for a given company."""
    logging.info(f"Starting article extraction for company: {company}, fetching {num_articles} articles")
    
    headers = {
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                       '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    }
    url = f"https://timesofindia.indiatimes.com/topic/{company}"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Failed to fetch the main page: {e}")
        return []
    
    soup = BeautifulSoup(response.content, "html.parser")
    articles = []
    article_divs = soup.select('div.uwU81')[:num_articles]  # Now uses user-defined number
    
    for div in article_divs:
        a_tag = div.find('a')
        if not a_tag or 'href' not in a_tag.attrs:
            continue
        
        article_url = a_tag['href']
        
        try:
            request_internal = requests.get(article_url, headers=headers)
            request_internal.raise_for_status()
        except requests.RequestException as e:
            logging.warning(f"Skipping article due to request error: {e}")
            continue
        
        soup_internal = BeautifulSoup(request_internal.content, "html.parser")
        title_tag = soup_internal.find('h1')
        title = title_tag.get_text(strip=True) if title_tag else "No Title Found"
        
        content_div = soup_internal.find('div', class_=re.compile(r'_s30J\s*clearfix'))
        content = ''
        if content_div:
            paragraphs = content_div.find_all('p')
            content = '\n'.join([p.text.strip() for p in paragraphs]) if paragraphs else content_div.text.strip()
        
        if not content:
            logging.info(f"Skipping article '{title}' due to missing content.")
            continue
        
        summary_text = summary_pipeline(content, max_length=80, min_length=20, do_sample=False)
        summary = summary_text[0]['summary_text']
        
        label = sentiment_pipeline(summary)[0] if summary else {'label': "NEUTRAL", 'score': 0.5}
        
        topics = kw_model.extract_keywords(summary, keyphrase_ngram_range=(1, 2), stop_words='english')
        topic_list = [topic[0] for topic in topics]
        
        articles.append({
            "Title": title,
            "Summary": summary,
            "Sentiment": label,
            "URL": article_url,
            "Topics": topic_list
        })
    
    return articles

def _generate_audio(text, filename):
    """Converts text to Hindi speech using gTTS and saves the file."""
    hindi_text = GoogleTranslator(source='auto', target='hi').translate(text)
    tts = gTTS(text=hindi_text, lang='hi')
    tts.save(filename)
    return filename

def comparative_analysis(articles: List[Dict[str, any]], company_name: str) -> Dict[str, any]:
    logging.info(f" comparative analysis of news articles related to: {company_name}")
    all_topic_sets: List[Set[str]] = [set(article["Topics"]) for article in articles]
    common_topics: Set[str] = set.intersection(*all_topic_sets) if all_topic_sets else set()

    comparisons = []
    for i in range(len(articles) - 1):
        for j in range(i + 1, len(articles)):
            art1, art2 = articles[i], articles[j]
            comparisons.append({
                "Comparison": f"{art1['Title']} vs {art2['Title']}",
                "Impact": (
                    f"{art1['Title']} discusses {art1['Sentiment']['label']} news, whereas "
                    f"{art2['Title']} focuses on {art2['Sentiment']['label']} coverage."
                )
            })
    
    topic_overlap = {
        "Common Topics": list(common_topics),
        "Unique Topics per Article": {
            art["Title"]: list(set(art["Topics"]) - common_topics) for art in articles
        }
    }
    
    sentiment_counts = {"POSITIVE": 0, "NEGATIVE": 0, "NEUTRAL": 0}
    for art in articles:
        sentiment_counts[art['Sentiment']['label']] += 1
    
    dominant_sentiment = max(sentiment_counts, key=sentiment_counts.get)
    sentiment_message = {
        "POSITIVE": "Potential stock growth expected.",
        "NEGATIVE": "Caution advised for investors.",
        "NEUTRAL": "Mixed coverage; no strong sentiment trend."
    }

    final_sentiment_text = f"{company_name}'s latest news coverage is mostly {dominant_sentiment}. {sentiment_message[dominant_sentiment]}"

    # Combine all article summaries and final sentiment into one text
    combined_text = "\n".join([
        f"Title: {article['Title']}. Summary: {article['Summary']}. Sentiment: {article['Sentiment']['label']}."
        for article in articles
    ])
    combined_text += f"\n\nFinal Sentiment Analysis: {final_sentiment_text}"

    # Generate a single audio file for everything
    final_audio_filename = f"complete_analysis.mp3"
    _generate_audio(combined_text, final_audio_filename)
    
    return {
        "Company": company_name,
        "Articles": articles,
        "Comparative Sentiment Score": {
            "Sentiment Distribution": sentiment_counts,
            "Coverage Differences": comparisons,
            "Topic Overlap": topic_overlap
        },
        "Final Sentiment Analysis": final_sentiment_text,
        "Hindi_audio": final_audio_filename
    }
