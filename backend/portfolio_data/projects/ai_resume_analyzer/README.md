---
title: AI Resume Screening Simulator — ATS Optimizer
category: project
tech: Python, FastAPI, PyMuPDF, spaCy, React
tags: NLP, Resume Parsing, AI, ATS, ATS Optimizer
featured: true
live_demo: https://ats-resume-rho.vercel.app/
---

# AI Resume Screening Simulator — ATS Optimizer

## Overview
Jeswar built the AI Resume Screening Simulator & ATS Optimizer to solve a major issue encountered by job seekers: resumes getting rejected by automated Applicant Tracking Systems (ATS) due to poor formatting or missing keywords. This app parses resumes, extracts structural sections, and compares them against target job descriptions.

## Live Demo
- [Live Demo](https://ats-resume-rho.vercel.app/)

## Core Features
- **PDF Text Parsing**: Fast text extraction from PDF files using PyMuPDF.
- **NLP Skill Extraction**: Extracts skills and experience metrics using spaCy's Named Entity Recognition (NER) and rule-based extractors.
- **ATS Compatibility Score**: Scores the resume against the target job description based on keyword matching and content alignment.
- **Keyword Gap Analysis**: Highlights essential tech skills and qualifications that are in the job description but missing from the resume.
- **AI Improvement Suggestions**: Generates suggestions to improve the resume text, structured by section (Summary, Skills, Work Experience).
