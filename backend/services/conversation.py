from typing import List, Dict, Any

class ConversationService:
    @staticmethod
    def trim_history(history: List[Dict[str, str]], limit: int = 10) -> List[Dict[str, str]]:
        """Filters and trims conversation history to the last N turns, excluding empty, invalid or error messages, adjacent duplicates, and placeholders."""
        if not history:
            return []
            
        cleaned_history = []
        for msg in history:
            role = msg.get("role")
            content = msg.get("content")
            
            # Skip invalid inputs, empty messages or placeholder values
            if not role or not content or not isinstance(content, str):
                continue
            
            role_clean = role.strip().lower()
            if role_clean not in ["user", "assistant"]:
                continue
                
            content_clean = content.strip()
            
            # Skip error prefixes to keep history clean and avoid confusing the assistant
            if content_clean.startswith("⚠️") or "API Error" in content_clean:
                continue
                
            # Filter out unfinished streaming placeholder content
            if not content_clean or content_clean == "..." or content_clean == "..":
                continue
                
            cleaned_history.append({
                "role": role_clean,
                "content": content_clean
            })
            
        # Deduplicate adjacent messages of the same role (keep the latest one)
        deduplicated = []
        for msg in cleaned_history:
            if deduplicated and deduplicated[-1]["role"] == msg["role"]:
                deduplicated[-1] = msg
            else:
                deduplicated.append(msg)
                
        return deduplicated[-limit:]
