import streamlit as st
from parser import extract_text_from_pdf
from matcher import tfidf_match_score, semantic_match_score, keyword_gap

# ── Page config (must be first Streamlit call) ──
st.set_page_config(
    page_title="Resume–JD Matcher",
    page_icon="📄",
    layout="wide"
)

st.title("Resume–JD Matcher")
st.caption("Upload your resume and paste a job description to see how well you match.")

# ── Two column input layout ──
col1, col2 = st.columns(2)

with col1:
    st.subheader("Your resume")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    
    resume_text = ""
    if uploaded_file is not None:
        resume_text = extract_text_from_pdf(uploaded_file)
        with st.expander("Preview extracted text"):
            st.text(resume_text[:800] + "...")

with col2:
    st.subheader("Job description")
    jd_text = st.text_area(
        "Paste the full job description here",
        height=280,
        placeholder="Copy-paste from LinkedIn, Naukri, etc."
    )

# ── Method selector ──
st.divider()
method = st.radio(
    "Choose matching method:",
    ["TF-IDF — fast, keyword-based", "Semantic — slower, understands meaning"],
    horizontal=True,
    help="TF-IDF is great for ATS-style matching. Semantic catches synonyms."
)

# ── Analyze button ──
analyze = st.button("Analyze my match", type="primary", use_container_width=True)

if analyze:
    # Validation
    if not uploaded_file:
        st.warning("Please upload your resume PDF.")
        st.stop()
    if not jd_text.strip():
        st.warning("Please paste a job description.")
        st.stop()
    if len(resume_text) < 50:
        st.error("Resume text is too short — the PDF may not have extractable text.")
        st.stop()

    # ── Run analysis ──
    with st.spinner("Analyzing... (first run may take 30s to download the model)"):
        if "TF-IDF" in method:
            score = tfidf_match_score(resume_text, jd_text)
        else:
            score = semantic_match_score(resume_text, jd_text)
        
        gap = keyword_gap(resume_text, jd_text)

    st.divider()

    # ── Score metrics ──
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Match score", f"{score}%")
    m2.metric("JD keywords", gap["total_jd_keywords"])
    m3.metric("You have", len(gap["matched_keywords"]))
    m4.metric("You're missing", len(gap["missing_keywords"]))

    # ── Visual score bar ──
    st.progress(min(int(score), 100))

    # ── Score interpretation ──
    if score >= 75:
        st.success(f"Strong match ({score}%). You're a competitive candidate for this role.")
    elif score >= 55:
        st.warning(f"Moderate match ({score}%). Adding the missing keywords below could push you over 70%.")
    else:
        st.error(f"Low match ({score}%). Consider tailoring your resume significantly — or reconsider the fit.")

    st.divider()

    # ── Keyword breakdown ──
    kw_col1, kw_col2 = st.columns(2)

    with kw_col1:
        st.subheader("Missing from your resume")
        st.caption("Add these naturally to your resume bullet points")
        missing_kw = list(gap["missing_keywords"])[:25]
        if missing_kw:
            # Display as pills using markdown
            pills = "  ".join([f"`{kw}`" for kw in missing_kw])
            st.markdown(pills)
        else:
            st.success("No major keywords missing!")

    with kw_col2:
        st.subheader("Already in your resume")
        matched_kw = list(gap["matched_keywords"])[:25]
        if matched_kw:
            pills = "  ".join([f"✓ `{kw}`" for kw in matched_kw])
            st.markdown(pills)

    # ── Tips ──
    st.divider()
    st.subheader("How to use these results")
    st.markdown("""
    1. Look at the **missing keywords** — don't stuff them in randomly
    2. For each missing keyword, ask: *"Have I actually done this?"*
    3. If yes → rewrite a bullet point to include it naturally
    4. If no → this role might require skills you haven't built yet
    5. Re-upload your updated resume and re-run to track improvement
    """)