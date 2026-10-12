"""Thin wrapper around the Google Gemini API (google-genai SDK)."""
from google import genai

# Model parameters for long outputs (meeting minutes, summaries)
LONG_OUTPUT_CONFIG = {
    "temperature": 1,  # Temperature controls the randomness of the generated text
    "top_p": 0.95,  # Top_p controls the diversity of the generated text
    "top_k": 40,  # Top_k controls the number of possible next words considered
    "max_output_tokens": 65536,  # Maximum number of tokens allowed in the generated text
    "response_mime_type": "text/plain",  # Response format
}

# Model parameters for short outputs (Telegram captions)
SHORT_OUTPUT_CONFIG = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 4096,  # Leaves room for the model's thinking tokens; captions are trimmed to Telegram's limit
    "response_mime_type": "text/plain",
}

# Safety settings for the Gemini model
SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

TIMEOUT_MS = 1000 * 1000  # Request timeout in milliseconds


class Gemini:
    """Uploads files to Gemini and generates text with one model."""

    def __init__(self, api_key, model):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def upload(self, path, display_name):
        """Uploads a file and returns the file object to use in prompts."""
        return self.client.files.upload(file=path, config={'display_name': display_name})

    def delete(self, name):
        """Deletes an uploaded file."""
        self.client.files.delete(name=name)

    def generate(self, contents, generation_config, system_instruction=None):
        """Calls the Gemini model and returns the generated text."""
        config = dict(generation_config, safety_settings=SAFETY_SETTINGS, http_options={"timeout": TIMEOUT_MS})
        if system_instruction:
            config["system_instruction"] = system_instruction
        response = self.client.models.generate_content(model=self.model, contents=contents, config=config)
        if response.text is None:
            raise ValueError(f"Empty response from Gemini (finish reason: {response.candidates[0].finish_reason if response.candidates else None})")
        return response.text
