import os
from dotenv import load_dotenv

load_dotenv("resources/doubtsovler_resources.env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
