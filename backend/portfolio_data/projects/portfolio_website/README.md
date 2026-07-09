---
title: RAG AI Portfolio Assistant & Website
category: project
tech: React, Tailwind CSS, Vite, FastAPI, ChromaDB, OpenRouter, Gemini API
tags: RAG, AI Assistant, Full-stack
github: https://github.com/imjeswar/portfolio
featured: true
---

# Personal Portfolio & AI RAG Chatbot

## Overview
This project is a premium personal portfolio website featuring a built-in AI Portfolio Assistant. Instead of requiring recruiters to read a static resume, the website allows them to converse with a custom-trained AI assistant that answers questions about Jeswar's projects, skills, education, and contact details.

## Core Features
- **RAG-based Chatbot**: Uses a FastAPI backend coupled with a ChromaDB vector database to index and search Jeswar's portfolio.
- **Dynamic Prompt Routing**: An Intent Classifier analyzes whether the user is asking about Jeswar (routes to strict RAG facts), general programming concepts (uses LLM knowledge with context linking), or a mix of both.
- **Glassmorphism UI**: Premium aesthetic design with dark mode styling, custom grid components, and a smooth cursor-following glow trail.
- **Certifications Preview**: Interactive grid displaying PDF credentials for verification.
