---
title: AI Resume Analyzer
category: project
tech: Python, FastAPI, PyMuPDF, spaCy, React
tags: NLP, Resume Parsing, AI, ATS
featured: true
---

# AI Resume Analyzer

## Overview
Jeswar built the AI Resume Analyzer to solve a major issue encountered by students: resumes getting rejected by automated Applicant Tracking Systems (ATS) due to poor formatting or missing keywords. This app parses resumes, extracts structural sections, and compares them against target job descriptions.

## Core Features
- **PDF Text Parsing**: Fast text extraction from PDF files using PyMuPDF.
- **NLP Skill Extraction**: Extracts skills and experience metrics using spaCy's Named Entity Recognition (NER) and rule-based extractors.
- **ATS Compatibility Score**: Scores the resume against the target job description based on keyword matching and content alignment.
- **Keyword Gap Analysis**: Highlights essential tech skills and qualifications that are in the job description but missing from the resume.
- **AI Improvement Suggestions**: Generates suggestions to improve the resume text, structured by section (Summary, Skills, Work Experience).
