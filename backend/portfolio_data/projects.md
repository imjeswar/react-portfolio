# Projects - Jeswar A M

Jeswar has designed and built 7 core projects using a variety of frameworks, AI tools, and full-stack utilities. Each project reflects a real problem he identified and solved from scratch.

---

## 1. FITZONE – Gym Management Platform

- **Why He Built It**: Jeswar noticed that most small gym owners in India were still managing members using WhatsApp messages and paper registers. He built FITZONE to replace that chaos with a clean, modern dashboard.
- **What It Does**: A complete gym management system that handles member registration, attendance tracking, membership renewal, billing records, and gym analytics — all in one place.
- **Key Features**:
  - Member dashboard with profile management
  - Live attendance tracking
  - Automated billing and membership status
  - Business metrics and usage insights
  - Fully responsive for mobile use by gym staff
- **Tech Stack**: Next.js, React, TypeScript, Tailwind CSS, Vercel
- **Challenges Solved**: Designing a data model that handles recurring membership cycles, partial payments, and attendance streaks. Also optimized for low-bandwidth mobile networks.
- **Live Demo**: https://gym-management-seven-liard.vercel.app/
- **GitHub Repository**: https://github.com/imjeswar/gym-management-.git

---

## 2. Portfolio Website

- **Why He Built It**: To showcase his work professionally and demonstrate his frontend engineering skills to recruiters and collaborators.
- **What It Does**: A premium personal portfolio with animated sections for skills, education, journey, projects, certifications, and an AI-powered chatbot assistant (the one you're talking to right now).
- **Key Features**:
  - Custom animated cursor with glow trail effect
  - Glassmorphism UI with dark theme
  - Interactive certifications grid with viewable PDFs
  - Embedded RAG-based AI Portfolio Assistant (FastAPI + ChromaDB backend)
  - Smooth scroll navigation with section-specific animations
- **Tech Stack**: React, Tailwind CSS, Vite, FastAPI (backend), ChromaDB (vector database), OpenRouter (LLM)
- **GitHub Repository**: https://github.com/imjeswar/portfolio

---

## 3. Inkify – Text to Handwriting Converter

- **Why He Built It**: As a creative side project, Jeswar wanted to explore typography and font rendering by converting typed text into realistic handwriting styles — useful for personalizing notes, cards, and posters.
- **What It Does**: Users type any text and select from multiple handwriting font styles. The app renders the text as if written by hand, with options to customize line spacing, font size, and ink color.
- **Key Features**:
  - Multiple handwriting font styles
  - Adjustable font size, line height, and ink color
  - Download output as an image
  - Live real-time preview as the user types
- **Tech Stack**: React, Tailwind CSS, handwriting web fonts, HTML5 Canvas API
- **Challenges Solved**: Handling multi-line text rendering on canvas with proper word wrapping that preserves the handwriting aesthetic.

---

## 4. AI Resume Analyzer

- **Why He Built It**: Jeswar observed that many students and job seekers submit resumes that get rejected by ATS (Applicant Tracking Systems) before a human even reads them. He built this tool to help people understand how their resume performs against job descriptions.
- **What It Does**: Users upload a resume (PDF) and paste a job description. The system parses the resume, extracts skills and experience, and uses NLP to score resume-to-job-description alignment, highlight missing keywords, and suggest improvements.
- **Key Features**:
  - PDF resume parsing and text extraction
  - ATS compatibility score (0–100)
  - Keyword gap analysis: skills in job description but missing from resume
  - AI-generated improvement suggestions powered by an LLM
  - Section-by-section breakdown (Summary, Skills, Experience, Education)
- **Tech Stack**: Python, FastAPI, PyMuPDF (PDF parsing), spaCy (NLP), React (frontend)
- **Challenges Solved**: Extracting clean structured data from poorly formatted PDF resumes. Normalizing skill synonyms (e.g. "JS" vs "JavaScript") for accurate matching.

---

## 5. Chatbot App

- **Why He Built It**: As an early exploration into conversational AI, Jeswar built a general-purpose chatbot to understand how to wire an LLM API to a chat interface.
- **What It Does**: A Streamlit-based conversational interface that connects to the Gemini API, maintaining multi-turn conversation context.
- **Key Features**:
  - Multi-turn conversation with message history
  - Clean Streamlit chat UI
  - Gemini API integration for natural language responses
- **Tech Stack**: Python, Streamlit, Gemini API (Google AI)

---

## 6. AI Health Assistant

- **Why He Built It**: Inspired by the lack of accessible health guidance for non-English speakers and rural users in India, Jeswar built a health Q&A chatbot that gives evidence-based wellness advice in plain language.
- **What It Does**: Users ask health and wellness questions. The assistant uses the Gemini API to respond with clear, plain-language guidance — not medical diagnosis, but practical wellness information.
- **Key Features**:
  - Conversational health Q&A
  - Symptom description → general advice flow
  - Responsible disclaimers (not a substitute for a doctor)
  - Clean and accessible UI
- **Tech Stack**: Python, Gemini API, Streamlit

---

## 7. E-commerce Platform

- **Why He Built It**: To practice building a production-grade full-stack web application with a real database, authentication, and AI-powered product recommendations.
- **What It Does**: A complete online shopping platform with product listings, cart, checkout, and an AI recommendation engine that suggests products based on browsing history and preferences.
- **Key Features**:
  - Product catalog with category filtering and search
  - Shopping cart and checkout flow
  - User authentication (register/login)
  - AI-powered product recommendations
  - Admin panel for product management
- **Tech Stack**: React, Node.js, Express, MongoDB, AI recommendation engine
