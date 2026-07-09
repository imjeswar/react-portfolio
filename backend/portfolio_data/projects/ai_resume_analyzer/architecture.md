---
title: AI Resume Analyzer Architecture & Challenges
category: project
tech: Python, FastAPI, PyMuPDF, spaCy
---

# AI Resume Analyzer Technical Architecture & Challenges

## System Architecture
- **Backend API**: FastAPI backend exposed via REST endpoints.
- **NLP & Parsing**: PyMuPDF handles initial text stream extraction. spaCy handles word tokenization, POS tagging, and entity extraction.
- **Match Engine**: Custom scoring algorithms evaluate text similarities and keyword density ratios.

## Key Challenges & Solutions
1. **PDF Formatting Variance**:
   - *Challenge*: Resumes come in multi-column layouts, tables, and varying font decoders, which mix up text reading order.
   - *Solution*: Utilized coordinate-based text extraction blocks in PyMuPDF to restructure column text sequentially before parsing.
2. **Synonym Matching**:
   - *Challenge*: Job description might list "JS" or "ReactJS" while the resume lists "JavaScript" or "React", causing false negative mismatches.
   - *Solution*: Implemented a normalization mapping database and lemmatization filters to resolve technical synonyms to a common base word.
