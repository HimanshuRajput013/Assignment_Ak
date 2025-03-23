import streamlit as st
import requests
import time
import plotly.graph_objects as go
from utils import extract_articles, comparative_analysis

# Function to create a sentiment gauge
def create_gauge(value, title, color):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": title},
        gauge={"axis": {"range": [0, 100]}, "bar": {"color": color}}
    ))
    return fig

# Function to render sentiment gauges
def render_gauges(pos_pct, neg_pct, neu_pct):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.plotly_chart(create_gauge(pos_pct, "Positive Sentiment", "#4CAF50"), use_container_width=True)
    with col2:
        st.plotly_chart(create_gauge(neg_pct, "Negative Sentiment", "#f44336"), use_container_width=True)
    with col3:
        st.plotly_chart(create_gauge(neu_pct, "Neutral Sentiment", "#2196F3"), use_container_width=True)

# Streamlit Page Configuration
st.set_page_config(page_title="News Sentiment Analyzer", layout="wide")

# App Title
st.title("📊 News Sentiment Analyzer")

# User Input: Company Name
company_name = st.text_input("Enter a company name to analyze:", "")

if company_name:
    st.info(f"Fetching latest news articles for: {company_name}...")

    # Fetch articles
    articles = extract_articles(company_name)
    
    if not articles:
        st.error("No articles found. Try another company.")
    else:
        # Perform comparative analysis
        analysis_result = comparative_analysis(articles, company_name)

        # 📌 Show Raw Output
        st.subheader("📜 Raw Output")
        with st.expander("🔍 Click to View Raw Extracted Articles & Analysis"):
            st.json(analysis_result)

        # Play Hindi Summary (if available)
        if "Hindi_audio" in analysis_result and st.button("🔊 Play Hindi Summary"):
            st.audio(analysis_result["Hindi_audio"], format="audio/mp3")

        # Display Summary of Each Article
        if "Articles" in analysis_result:
            st.subheader("📰 Extracted Articles & Sentiment")
            for article in analysis_result["Articles"]:
                st.markdown(f"**[{article.get('Title', 'Unknown Title')}]({article.get('URL', '#')})**")
                st.write(f"**Summary:** {article.get('Summary', 'No summary available.')}")
                st.write(f"**Sentiment:** {article['Sentiment'].get('label', 'Unknown')} ({article['Sentiment'].get('score', 0):.2f})")
                st.write("---")

        # Display Sentiment Distribution
        if "Comparative Sentiment Score" in analysis_result:
            st.subheader("📊 Sentiment Distribution")
            sentiment_counts = analysis_result["Comparative Sentiment Score"].get("Sentiment Distribution", {})
            total = sum(sentiment_counts.values())

            if total > 0:
                pos_pct = (sentiment_counts.get("POSITIVE", 0) / total) * 100
                neg_pct = (sentiment_counts.get("NEGATIVE", 0) / total) * 100
                neu_pct = (sentiment_counts.get("NEUTRAL", 0) / total) * 100
                render_gauges(pos_pct, neg_pct, neu_pct)

        # Display Coverage Differences
        if "Coverage Differences" in analysis_result["Comparative Sentiment Score"]:
            st.subheader("🔍 Coverage Differences")
            for comparison in analysis_result["Comparative Sentiment Score"]["Coverage Differences"]:
                st.write(f"📌 {comparison['Comparison']}")
                st.write(f"➡️ {comparison['Impact']}")
                st.write("---")

        # Display Topic Overlap
        if "Topic Overlap" in analysis_result["Comparative Sentiment Score"]:
            st.subheader("📌 Topic Overlap")
            topic_overlap = analysis_result["Comparative Sentiment Score"]["Topic Overlap"]
            common_topics = topic_overlap.get("Common Topics", [])
            unique_topics = topic_overlap.get("Unique Topics per Article", {})

            if common_topics:
                st.write(f"**Common Topics:** {', '.join(common_topics)}")
            else:
                st.write("No common topics found.")

            if unique_topics:
                st.write("### Unique Topics per Article:")
                for title, topics in unique_topics.items():
                    st.write(f"📌 **{title}:** {', '.join(topics)}")

        # Display Final Sentiment Conclusion
        if "Final Sentiment Analysis" in analysis_result:
            st.success(f"**🔹 Final Sentiment Analysis:** {analysis_result['Final Sentiment Analysis']}")

# Footer
st.write("---")
st.caption("Developed with ❤️ using Streamlit.")
