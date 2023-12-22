import justext  # Make sure to import justext
import matplotlib.pyplot as plt
import pandas as pd
import requests
import streamlit as st
import yake
from PyPDF2 import PdfReader
from pytube import YouTube
from wordcloud import WordCloud
from youtube_transcript_api import YouTubeTranscriptApi


class WebApp:
    def extract_keywords(
        self, text, num_keywords, visualize_wordcloud=True, visualize_barchart=True
    ):
        # Extract keywords from the text and visualize in a word cloud and/or bar chart
        kw_extractor = yake.KeywordExtractor()
        language = "french"
        max_ngram_size = 3
        deduplication_threshold = 0.9
        custom_kw_extractor = yake.KeywordExtractor(
            lan=language,
            n=max_ngram_size,
            dedupLim=deduplication_threshold,
            top=num_keywords,
            features=None,
        )
        keywords = custom_kw_extractor.extract_keywords(text)

        # Get the specified number of keywords
        top_keywords = [keyword[0] for keyword in keywords[:num_keywords]]

        # Create a DataFrame for bar chart visualization
        df_keywords = pd.DataFrame(
            {"Keyword": top_keywords, "Score": [keyword[1] for keyword in keywords[:num_keywords]]}
        )

        # Visualize word cloud if selected
        if visualize_wordcloud:
            # Display a dynamic subheader for word cloud visualization
            st.subheader(f"Word Cloud for Top {num_keywords} Keywords")

            # Display the word cloud
            fig_wc, ax_wc = plt.subplots(figsize=(20, 20))
            wordcloud = WordCloud(
                stopwords=None, background_color="white", width=800, height=400
            ).generate(" ".join(top_keywords))
            ax_wc.imshow(wordcloud, interpolation="bilinear")
            ax_wc.axis("off")
            st.pyplot(fig_wc)

        # Visualize bar chart if selected
        if visualize_barchart:
            # Display a dynamic subheader for bar chart visualization
            st.subheader(f"Bar Chart for Top {num_keywords} Keywords")

            # Display the bar chart
            fig_bc, ax_bc = plt.subplots(figsize=(10, 6))
            df_keywords.plot(
                kind="barh", x="Keyword", y="Score", ax=ax_bc, color="skyblue", rot=0
            )  # Adjust the rotation angle as needed
            ax_bc.set_ylabel("Score")
            ax_bc.set_title(f"Top {num_keywords} Keywords and Their Scores")
            # st.pyplot(fig_bc)

        # Display the top keywords
        # st.subheader(f"Top {num_keywords} Keywords:")
        # st.write(top_keywords)

        # Count occurrences of the specified word
        # List of words to count and visualize
        words_to_count = [
            "numérique",
            "Société",
            "Révolution",
            "Développement",
        ]  # Add more words as needed

        # Count occurrences of each specified word
        word_counts = {word: text.lower().split().count(word.lower()) for word in words_to_count}

        # Plot bar chart for each specified word
        if visualize_barchart:
            df_word_counts = pd.DataFrame(list(word_counts.items()), columns=["Word", "Count"])
            st.subheader("Bar Chart for Word Occurrences")

            # Display the bar chart
            fig_word_counts, ax_word_counts = plt.subplots(figsize=(10, 6))
            df_word_counts.plot(
                kind="bar", x="Word", y="Count", ax=ax_word_counts, colormap="viridis"
            )
        #  ax_word_counts.set_ylabel("Count")
        #  ax_word_counts.set_title("Occurrences of Words in the Text")
        # st.pyplot(fig_word_counts)

    def download_transcript(self, video_url, num_keywords):
        # Download the transcription from YouTube using the video URL
        try:
            video_id = YouTube(video_url).video_id
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["fr"])
            transcript_text = "\n".join([entry["text"] for entry in transcript])
            keywords = self.extract_keywords(transcript_text, num_keywords)

            # Display the transcript
            st.subheader("YouTube Transcript:")
            st.write(transcript_text)

            if keywords:
                # Pass the number of keywords to the extract_keywords method
                self.extract_keywords(transcript_text, num_keywords)

        except Exception as e:
            st.error(f"Error downloading transcript: {str(e)}")

    def scrape_content_url(self, url, num_keywords):
        # Scrape content from a given URL using requests and justext
        try:
            response = requests.get(url)
            paragraphs = justext.justext(response.content, justext.get_stoplist("French"))
            total_paragraphs = len(paragraphs)
            scraped_content = []

            with st.progress(0):
                for i, paragraph in enumerate(paragraphs):
                    if not paragraph.is_boilerplate:
                        scraped_content.append(paragraph.text)

                    # Update overall progress bar
                    progress = (i + 1) / total_paragraphs
                    st.progress(progress)

            content_text = " ".join(scraped_content)
            keywords = self.extract_keywords(content_text, num_keywords)

            return content_text, keywords
        except Exception as e:
            st.error(f"Error scraping content: {str(e)}")
            return None, None

    def scrape_content_pdf(self, pdf_file, num_keywords):
        # Extract text from a PDF document
        try:
            pdf_reader = PdfReader(pdf_file)
            total_pages = len(pdf_reader.pages)
            extracted_text = []

            with st.progress(0):
                for i in range(total_pages):
                    page = pdf_reader.pages[i]
                    extracted_text.append(page.extract_text())

                    # Update overall progress bar
                    progress = (i + 1) / total_pages
                    st.progress(progress)

            content_text = " ".join(extracted_text)
            keywords = self.extract_keywords(content_text, num_keywords)

            return content_text, keywords
        except Exception as e:
            st.error(f"Error extracting text from PDF: {str(e)}")
            return None, None

    def run(self):
        st.markdown(
            "<h1 style='font-size:1.5em;'>Institut des Algorithmes du Sénégal - Diangat Web App</h1>",
            unsafe_allow_html=True,
        )

        # Choose between URL, PDF, or YouTube
        option = st.sidebar.radio("Choose data source:", ("URL", "PDF", "YouTube"))

        # Add an input for the number of keywords
        num_keywords = st.number_input(
            "Number of Keywords (up to 20):", min_value=1, max_value=200, value=20
        )

        # Sidebar buttons
        action_button = st.sidebar.button("Run Analysis")

        if option == "URL":
            # Input URL
            url = st.text_input("Enter the URL to scrape:", "")
            if action_button or st.button("Scrape Content"):
                if url:
                    st.info("Scraping content... Please wait.")
                    scraped_content, keywords = self.scrape_content_url(url, num_keywords)

                    if scraped_content:
                        st.subheader("Scraped Content:")
                        st.write(scraped_content)

                        if keywords:
                            # Pass the number of keywords to the extract_keywords method
                            self.extract_keywords(scraped_content, num_keywords)
                    else:
                        st.warning("Failed to scrape content. Check the URL and try again.")

        elif option == "PDF":
            # Upload PDF file
            pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])
            if action_button or st.button("Extract Text"):
                if pdf_file:
                    st.info("Extracting text... Please wait.")
                    extracted_text, keywords = self.scrape_content_pdf(pdf_file, num_keywords)

                    if extracted_text:
                        st.subheader("Extracted Text:")
                        if keywords:
                            # Pass the number of keywords to the extract_keywords method
                            self.extract_keywords(extracted_text, num_keywords)
                    else:
                        st.warning(
                            "Failed to extract text from PDF. Check the file and try again."
                        )

        elif option == "YouTube":
            # Input YouTube URL
            youtube_url = st.text_input("Enter the YouTube URL:", "")
            if action_button or st.button("Download Transcript"):
                if youtube_url:
                    st.info("Downloading transcript... Please wait.")
                    self.download_transcript(youtube_url, num_keywords)
                else:
                    st.warning("Please enter a valid YouTube URL.")


if __name__ == "__main__":
    web_app = WebApp()
    web_app.run()
