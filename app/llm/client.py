from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('GITHUB_TOKEN')

client = ChatOpenAI(base_url="https://models.github.ai/inference",
                      model="openai/gpt-4o-mini")

