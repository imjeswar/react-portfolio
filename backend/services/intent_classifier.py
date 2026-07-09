import re
import logging

logger = logging.getLogger(__name__)

class IntentClassifier:
    PORTFOLIO_KEYWORDS = {
        "jeswar", "you", "your", "yours", "me", "my", "i", "portfolio", "resume", "cv",
        "internship", "experience", "work", "job", "career", "contact", "email", "phone",
        "whatsapp", "number", "github", "linkedin", "college", "university", "cgpa",
        "grades", "study", "studying", "degree", "btech", "education", "courses",
        "certifications", "certificate", "certificates", "credentials", "credential",
        "project", "projects", "built", "made", "created", "designed", "developed",
        "achievements", "achievement", "hackathon", "hackathons", "award", "awards"
    }

    TECH_KEYWORDS = {
        "react", "fastapi", "python", "javascript", "typescript", "mongodb", "node",
        "express", "rag", "embeddings", "chromadb", "ai", "nlp", "streamlit", "nextjs",
        "next.js", "tailwind", "git", "github", "vscode", "postman", "render", "railway",
        "vercel", "jwt", "html", "css", "sql", "database", "sqlite"
    }

    @classmethod
    def classify(cls, question: str) -> str:
        """
        Classifies user query into 'portfolio', 'general', or 'mixed'.
        """
        q_lower = question.lower()
        # Find all words (alphanumeric tokens)
        tokens = set(re.findall(r'\b[\w\.-]+\b', q_lower))
        
        has_portfolio_context = not tokens.isdisjoint(cls.PORTFOLIO_KEYWORDS)
        has_tech_context = not tokens.isdisjoint(cls.TECH_KEYWORDS)
        
        if has_portfolio_context and has_tech_context:
            logger.info(f"[Intent] Classified as 'mixed' for query: '{question}'")
            return "mixed"
        elif has_portfolio_context:
            logger.info(f"[Intent] Classified as 'portfolio' for query: '{question}'")
            return "portfolio"
        else:
            logger.info(f"[Intent] Classified as 'general' for query: '{question}'")
            return "general"
