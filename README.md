<div align="center">
  
# 🚀 PI Enterprise Resume Analyzer

**An Ultra-Premium, AI-Powered ATS & Resume Evaluation Engine**

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/Frontend-React_18-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![Vite](https://img.shields.io/badge/Bundler-Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev/)
[![TailwindCSS](https://img.shields.io/badge/Styling-Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![spaCy](https://img.shields.io/badge/NLP-spaCy-09A3D5?style=for-the-badge&logo=spacy&logoColor=white)](https://spacy.io/)

*Elevating the standard of recruitment through high-performance machine learning, semantic search, and jaw-dropping data visualization.*

</div>

---

## ⚡ Overview

The **PI (Pentaverse India) Enterprise Resume Analyzer** is a state-of-the-art, production-grade application designed to automate and augment the recruitment process. It bridges the gap between massive applicant pools and targeted talent acquisition by utilizing advanced Natural Language Processing (NLP), semantic similarity engines, and an ultra-premium visual framework.

Gone are the days of manually skimming messy PDFs. This platform ingests resumes, extracts critical entities, maps semantic relationships against targeted Job Descriptions (JDs), and displays the results in a stunning, interactive interface.

---

## ✨ Jaw-Dropping Features

*   **🧠 Deep Semantic Matching Algorithm:** Uses `sentence-transformers/all-MiniLM-L6-v2` to deeply understand the context of a candidate's experience rather than relying purely on noisy keyword mapping.
*   **📊 The "Candidate Duel" Mode:** A specialized visual mode that pits top candidates against each other via interactive Radar Charts and 3D Tilt Cards, allowing recruiters to visually dissect competency gaps instantly.
*   **🎭 The "Standard Array" Mode:** A beautiful, responsive grid system processing massive batches of candidates with incredibly smooth layout animations powered by **Framer Motion**.
*   **🤖 Neural Synthesizer (AI Suggestions):** Generates real-time architectural and skill-gap suggestions to identify exactly what a candidate is missing to be a perfect fit.
*   **🛡️ Robust Entity Extraction:** A hybrid NLP approach utilizing `spaCy` paired with aggressive Regex fallbacks to intelligently format and extract names, emails, phones, and academic backgrounds—even from horribly formatted PDFs.
*   **🏎️ High-Performance Asynchronous I/O:** Built on **FastAPI**, processing resumes strictly in-memory without expensive disk I/O, ensuring lightning-fast batch processing.
*   **🎨 Ultra-Premium UI/UX:** Dark-mode optimized, neon-glow glassmorphism, responsive grid layouts, and active faux-progress indicators designed to provide a television-ad quality SaaS experience.

---

## 🏗️ Technical Architecture

The architecture is split into a robust Python AI backend and a highly dynamic React frontend.

### ⚙️ Backend Core Modules (`/`)
*   `fastapi_app.py`: The asynchronous heart of the API serving the frontend using Uvicorn.
*   `analyzer.py`: The core orchestrator. Integrates parsing, NLP extraction, similarity scoring, and the mathematical ATS Evaluation algorithm (`Similarity * 50% + Skills * 30% + Experience * 20%`).
*   `nlp_engine.py`: Intelligent extraction engine. If `spaCy` fails to read a name due to technical jargon, it triggers a robust 3-tier fallback to parse the optimal candidate name.
*   `similarity_engine.py`: Loads the dense multi-layer `MiniLM` model for SBERT vector similarity matrix computation.
*   `generate_data.py` & `job_matcher.py`: A pre-configured PI Enterprise Role database that automatically infers the category of a candidate if no JD is provided.

### 💻 Frontend Application (`/frontend`)
*   **Framework:** React 18 + Vite for lightning-fast HMR builds.
*   **Styling:** TailwindCSS with customized `index.css` global animations (glass-panel effects, neon-glows, brand gradients).
*   **Animation Engine:** `framer-motion` for fluid grid swapping and `react-parallax-tilt` for interactive 3D elements.
*   **Visualizations:** `recharts` for dynamic radar capability indexing.

---

## 🛠️ Installation & Setup

### Prerequisites
*   **Python 3.9+**
*   **Node.js 18+** & `npm`

### 1. Backend Setup
Clone the repository and install the Python dependencies.
```bash
# Install required Python libraries
pip install -r requirements.txt

# Download the spaCy English NLP model (Required for Named Entity Recognition)
python -m spacy download en_core_web_sm
```

Start the FastAPI application:
```bash
python fastapi_app.py
```
*The backend will boot up on `http://127.0.0.1:8000`.*

### 2. Frontend Setup
Open a new terminal and navigate to the `frontend` directory.
```bash
cd frontend

# Install Node modules
npm install

# Start the Vite development server
npm run dev
```
*The frontend will boot up on `http://localhost:5173`.*

---

## 🚀 Usage Guide

1. **Access the Portal**: Navigate to `http://localhost:5173` in your web browser.
2. **Align Assets**: Drag and drop a batch of candidate PDFs into the secure upload zone.
3. **Target Parameters (Optional)**: Paste a custom Job Description (JD) into the alignment text box. If omitted, the engine will use generic role inference.
4. **Initiate Sequence**: Click the primary execution button. The UI's dynamic progress bar will activate while the asynchronous backend slices through the PDF text data.
5. **Analyze the Matrix**: 
    *   Toggle between **Standard Array** (to view the full candidate pool) and **Candidate Duel** (to put the Top 2 candidates into a head-to-head radar analysis).
    *   Review contextual Neural Syntheses for any given candidate.

---

## 🔮 Future Roadmap (v2.0)
*   [ ] Implement WebSockets for true real-time streaming progress logs.
*   [ ] Direct PDF/DOCX annotation exports highlighting exactly where skills were inferred.
*   [ ] LLM Integration (OpenAI/Ollama) for deeper qualitative analysis summaries.
*   [ ] Dashboard authentication and role-based access control (RBAC).

---
<div align="center">
  <i>Developed with ❤️ for Pentaverse OS / Enterprise Evaluator.</i>
</div>
