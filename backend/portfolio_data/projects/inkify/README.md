---
title: Inkify – Text to Handwriting Converter
category: project
tech: React, Tailwind CSS, handwriting web fonts, HTML5 Canvas API
tags: Font Rendering, Frontend, Canvas
---

# Inkify – Text to Handwriting Converter

## Overview
Inkify is a creative side project built by Jeswar to explore font rendering and typography. The application allows users to convert digital text into realistic, organic handwriting styles, which can be customized and downloaded as images to personalize cards, homework assignments, or notes.

## Core Features
- **Font Variety**: Multiple realistic handwriting web font styles to choose from.
- **Customizable Styling**: Adjust font size, line spacing, text width, and ink colors (blue, black, red).
- **Downloadable Output**: Exports the rendered text as high-resolution images.
- **Live Preview**: Real-time canvas rendering as the user types.

## Engineering Challenges & Solutions
- **Canvas Word Wrapping**:
  - *Challenge*: HTML5 Canvas API does not support multi-line word wrapping by default.
  - *Solution*: Developed a custom paragraph rendering algorithm that splits text into words, checks total line width on the fly, and inserts line breaks dynamically to preserve natural-looking boundaries.
