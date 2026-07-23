from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import spacy

nlp = spacy.load("en_core_web_sm")   # load once at startup, not every call

# We store the model in a variable so it loads only once
_semantic_model = None

def get_semantic_model():
    global _semantic_model
    if _semantic_model is None:
        # Downloads ~80MB model first time, then uses local cache
        _semantic_model = SentenceTransformer('all-MiniLM-L6-v2')
    return _semantic_model


# ─────────────────────────────────────────────
# APPROACH 1: TF-IDF Matching
# ─────────────────────────────────────────────

def tfidf_match_score(resume_text: str, jd_text: str) -> float:
    """
    TF-IDF = Term Frequency × Inverse Document Frequency
    
    TF  = how often a word appears in THIS document
    IDF = how rare that word is across ALL documents
    
    "Python" appearing in both resume and JD → high score
    "the", "and" → appear everywhere → IDF makes them near-zero weight
    
    Result: each document becomes a vector of numbers.
    We then measure the angle between the two vectors (cosine similarity).
    Angle = 0° → identical → score = 1.0
    Angle = 90° → nothing in common → score = 0.0
    """
    vectorizer = TfidfVectorizer(
        stop_words='english',    # ignore "the", "is", "at", etc.
        ngram_range=(1, 2)       # consider single words AND two-word phrases
                                 # so "machine learning" is one feature, not two
    )
    
    # fit_transform learns the vocabulary from BOTH texts, then converts them
    tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
    
    # Compare row 0 (resume) vs row 1 (JD)
    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    
    return round(float(score) * 100, 2)   # convert to 0-100 percentage


# ─────────────────────────────────────────────
# APPROACH 2: Semantic Matching
# ─────────────────────────────────────────────

def semantic_match_score(resume_text: str, jd_text: str) -> float:
    """
    Semantic matching UNDERSTANDS meaning, not just word overlap.
    
    TF-IDF would say:
      "built ML models" and "developed machine learning solutions" = LOW match
      (different words)
    
    Semantic model says:
      "built ML models" and "developed machine learning solutions" = HIGH match
      (same meaning)
    
    How? The model (all-MiniLM-L6-v2) was trained on millions of sentences.
    It converts text to a 384-dimensional vector where similar meanings
    land near each other in that space.
    
    We then use cosine similarity on those vectors, same as TF-IDF.
    """
    model = get_semantic_model()
    
    # Truncate to avoid memory issues with very long resumes
    resume_truncated = resume_text[:3000]
    jd_truncated = jd_text[:3000]
    
    embeddings = model.encode([resume_truncated, jd_truncated])
    score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    
    return round(float(score) * 100, 2)


# ─────────────────────────────────────────────
# KEYWORD GAP ANALYSIS
# ─────────────────────────────────────────────

def extract_keywords(text: str) -> set:
    """
    Uses spaCy's NLP pipeline to find meaningful words.
    
    spaCy does:
    1. Tokenization → splits "Python developer" into ["Python", "developer"]
    2. POS tagging → labels each word: NOUN, VERB, ADJ, etc.
    3. Lemmatization → "running" → "run", "databases" → "database"
    
    We keep only NOUNs, PROPER NOUNs, and ADJECTIVEs — these carry meaning.
    We skip STOPs (the, is, at) and PUNCTuation.
    We also grab noun phrases (multi-word skills like "data pipeline").
    """
    doc = nlp(text.lower())
    keywords = set()
    
    for token in doc:
        if (
            not token.is_stop        # not a filler word
            and not token.is_punct   # not punctuation
            and token.pos_ in ['NOUN', 'PROPN', 'ADJ']
            and len(token.text) > 2  # skip 1-2 letter words like "AI" get caught by PROPN
        ):
            keywords.add(token.lemma_)   # add the root form
    
    # Add noun phrases: "machine learning", "deep learning", "project management"
    for chunk in doc.noun_chunks:
        phrase = chunk.text.strip()
        if 1 < len(phrase.split()) <= 3:   # 2-3 word phrases only
            keywords.add(phrase)
    
    return keywords


def keyword_gap(resume_text: str, jd_text: str) -> dict:
    """
    Compares keywords in the JD against keywords in the resume.
    Returns what's missing, what's matched, and a coverage percentage.
    """
    resume_kw = extract_keywords(resume_text)
    jd_kw = extract_keywords(jd_text)
    
    missing = jd_kw - resume_kw           # in JD but NOT in resume
    matched = jd_kw & resume_kw           # in BOTH (intersection)
    
    coverage = round(len(matched) / len(jd_kw) * 100, 1) if jd_kw else 0
    
    return {
        "matched_keywords": sorted(matched),
        "missing_keywords": sorted(missing),
        "keyword_coverage": coverage,
        "total_jd_keywords": len(jd_kw)
    }