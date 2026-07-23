# 📄 Resume JD Matcher

A Resume JD Matcher is an AI-powered tool that helps job seekers compare their resume against a job description and understand how well their profile matches the role. It uses Natural Language Processing (NLP), semantic similarity, and keyword extraction to calculate a match score, identify missing skills, and provide actionable suggestions to improve resume relevance.

The application analyzes both the resume and the job description, highlights matched and missing keywords, and helps users tailor their resume for better ATS compatibility and job alignment.

## ✨ Features

* 📄 Upload Resume (PDF)
* 📋 Upload Job Description
* 🎯 Resume–JD Match Score
* 🔍 Keyword and Skill Gap Analysis
* 💡 Resume Improvement Suggestions
* 📊 Semantic Similarity Matching
* 🗂 Analysis History (SQLite)
* 📑 Export Match Report

## 🛠 Tech Stack

* Python
* Streamlit
* NLP
* Sentence Transformers
* spaCy
* Scikit-learn
* SQLite
* pdfplumber

## 📂 Project Structure

```text
Resume-JD-Matcher/
│── app/
│── models/
│── sample_data/
│── reports/
│── database/
│── requirements.txt
│── README.md
```

## 🚀 Installation

```bash
git clone https://github.com/your-username/Resume-JD-Matcher.git

cd Resume-JD-Matcher

python -m venv venv

# Windows
venv\Scripts\activate

pip install -r requirements.txt

python -m spacy download en_core_web_sm

streamlit run app/main.py
```

## 🔄 Workflow

1. Upload your resume (PDF).
2. Paste or upload a job description.
3. The application extracts and cleans text from both documents.
4. NLP and semantic models compare the resume with the job description.
5. The system calculates a match score.
6. Missing keywords and skills are identified.
7. The application provides suggestions to improve resume alignment.
8. Export the analysis as a report.

## 📌 Future Enhancements

* Multi-resume comparison
* Cover Letter Generator
* Resume Version Tracking
* Recruiter Dashboard
* LinkedIn Profile Analyzer
* Job Recommendation System
* Multi-language Resume Support

## 👩‍💻 Author

**Shravani Welzile**

If you find this project useful, consider giving it a ⭐ on GitHub!
