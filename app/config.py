import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
KB_DIR = BASE_DIR / "knowledge_base"

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")
EMBED_MODEL = os.getenv("EMBED_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))
RETRIEVAL_K = int(os.getenv("RETRIEVAL_K", "5"))

COMPANY_NAME = "T&C AUTOS"
COMPANY_CITY = "Silicon Valley"
COMPANY_STATE = "California"
COMPANY_ADDRESS = "4200 Stevens Creek Blvd, San Jose, CA 95129"
COMPANY_PHONE = "(408) 555-0120"
COMPANY_EMAIL = "info@tcautos.com"

SUPPORTED_LANGUAGES = {
    "auto": "Auto Detect",
    "en": "English",
    "fr": "Fran\u00e7ais",
    "es": "Espa\u00f1ol",
    "de": "Deutsch",
    "nl": "Nederlands",
    "pt": "Portugu\u00eas",
    "ru": "\u0420\u0443\u0441\u0441\u043a\u0438\u0439",
    "hi": "\u0939\u093f\u0928\u094d\u0926\u0940",
    "bn": "\u09ac\u09be\u0982\u09b2\u09be",
    "zh-cn": "\u4e2d\u6587",
    "ar": "\u0627\u0644\u0639\u0631\u0628\u064a\u0629",
    "ur": "\u0627\u0631\u062f\u0648",
}

DEFAULT_LANGUAGE = "auto"

AGENTS = {
    "bob": {
        "embed_model": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        "label": "Bob",
        "speed": "Slow",
        "emoji": "\U0001f422",
        "color": "#9333ea",
        "collection_name": "bob_kb",
    },
    "june": {
        "embed_model": "sentence-transformers/all-MiniLM-L6-v2",
        "label": "June",
        "speed": "Fast",
        "emoji": "\u26a1",
        "color": "#22c55e",
        "collection_name": "june_kb",
    },
}
DEFAULT_AGENT = "june"
