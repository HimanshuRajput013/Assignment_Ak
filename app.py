import streamlit as st
import plotly.graph_objects as go
import time
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

num_articles = st.slider("Select the number of articles to fetch:", min_value=2, max_value=20, value=3)

if company_name:
    st.info(f"Fetching {num_articles} latest news articles for: {company_name}...")

    # Progress bar
    progress_bar = st.progress(0)

    # Start time tracking
    start_time = time.time()

    # Fetch articles
    st.write("⏳ **Fetching news articles...**")
    fetch_start = time.time()
    articles = extract_articles(company_name, num_articles=num_articles)
    fetch_time = time.time() - fetch_start
    progress_bar.progress(25)

    if not articles:
        st.error("No articles found. Try another company.")
    else:
        # Perform comparative analysis
        st.write("🔍 **Performing sentiment analysis...**")
        analysis_start = time.time()
        analysis_result = comparative_analysis(articles, company_name)
        analysis_time = time.time() - analysis_start
        progress_bar.progress(70)

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
                gauge_start_time = time.time()
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

    # Stop time tracking
    end_time = time.time()
    total_time = end_time - start_time
    progress_bar.progress(100)

    # Debugging Information
    st.subheader("⚙️ **Debugging & Execution Time**")
    st.write(f"⏳ **News Fetching Time:** {fetch_time:.2f} seconds")
    st.write(f"🔍 **Sentiment Analysis Time:** {analysis_time:.2f} seconds")
    st.write(f"🕒 **Total Execution Time:** {total_time:.2f} seconds")
