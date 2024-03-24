import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Function to preprocess text
def preprocess_text(text):
    # Tokenization
    tokens = nltk.word_tokenize(text.lower())
    # Remove stop words and non-alphanumeric tokens
    stop_words = set(nltk.corpus.stopwords.words('english'))
    tokens = [token for token in tokens if token.isalnum() and token not in stop_words]
    return ' '.join(tokens)

# Function to calculate cosine similarity
def calculate_similarity(text1, text2):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    return cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]

# Function to deduplicate articles
def deduplicate_articles(news, prev_notes):
    SIMILARITY_THRESHOLD = 0.6
    processed_news = preprocess_text(news)
    is_duplicate = False
    for note in prev_notes:
        processed_note = preprocess_text(note)  # Assuming 'text' contains the article content
        similarity_score = calculate_similarity(processed_news, processed_note)
            
        if similarity_score > SIMILARITY_THRESHOLD:
            is_duplicate = True
            break
        else:
            continue

    return is_duplicate
