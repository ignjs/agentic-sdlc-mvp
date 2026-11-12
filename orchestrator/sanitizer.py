import re
from pathlib import Path

PROMPT_INJECTION_PATTERNS = [
    r"ignore previous instructions",
    r"system prompt",
    r"developer prompt",
    r"override policy",
    r"act as admin",
    r"forget all previous",
    r"bypass security",
    r"ignore safety",
]


class InputSanitizer:
    """Validates and strips malicious content before agent execution."""

    @staticmethod
    def sanitize_text(raw_text: str) -> str:
        cleaned = raw_text.strip()
        for pattern in PROMPT_INJECTION_PATTERNS:
            if re.search(pattern, cleaned, flags=re.IGNORECASE):
                raise ValueError(f"Prompt injection pattern detected: {pattern}")

        suspicious_tokens = ["<script>", "javascript:", "DROP TABLE", "base64,"]
        for token in suspicious_tokens:
            if token.lower() in cleaned.lower():
                raise ValueError(f"Suspicious token detected: {token}")

        return cleaned

    @classmethod
    def sanitize_file(cls, path: str | Path) -> str:
        file_path = Path(path)
        raw_text = file_path.read_text(encoding="utf-8")
        return cls.sanitize_text(raw_text)
