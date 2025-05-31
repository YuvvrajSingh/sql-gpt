# Available Groq Models (as of May 2025)
# Updated list of supported models

AVAILABLE_MODELS = {
    "llama-3.1-70b-versatile": {
        "name": "Llama 3.1 70B Versatile",
        "description": "Best for complex reasoning and SQL generation",
        "context_length": 131072,
        "recommended": True
    },
    "llama-3.1-8b-instant": {
        "name": "Llama 3.1 8B Instant", 
        "description": "Faster responses, good for simple queries",
        "context_length": 131072,
        "recommended": False
    },
    "llama-3.2-11b-vision-preview": {
        "name": "Llama 3.2 11B Vision Preview",
        "description": "Multimodal model with vision capabilities",
        "context_length": 128000,
        "recommended": False
    },
    "llama-3.2-90b-vision-preview": {
        "name": "Llama 3.2 90B Vision Preview", 
        "description": "Large multimodal model",
        "context_length": 128000,
        "recommended": False
    },
    "gemma2-9b-it": {
        "name": "Gemma 2 9B IT",
        "description": "Google's instruction-tuned model",
        "context_length": 8192,
        "recommended": False
    },
    "llama3-70b-8192": {
        "name": "Llama 3 70B 8192",
        "description": "High performance model for SQL generation",
        "context_length": 8192,
        "recommended": True
    },
    "deepseek-r1-distill-llama-70b": {
        "name": "DeepSeek R1 Distill Llama 70B",
        "description": "Distilled version of Llama 70B for efficiency",
        "context_length": 8192,
        "recommended": False
    },
}

# Default model for SQL generation
DEFAULT_MODEL = "llama3-70b-8192"
# Fallback models if default fails
FALLBACK_MODELS = [
    "llama-3.1-70b-versatile"
    "llama-3.1-8b-instant",
    "gemma2-9b-it"
]
