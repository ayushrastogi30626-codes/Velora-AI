from dotenv import load_dotenv
import os
from tavily import TavilyClient

# load .env file
load_dotenv()

# get API key
api_key = os.getenv("TAVILY_API_KEY")

# check if key exists
if not api_key:
    print("❌ API key not found in .env file")
    exit()

# create client
client = TavilyClient(api_key=api_key)

# test search 1
print("\n🔍 Searching: Elon Musk")
result1 = client.search("Who is Elon Musk?")

print("\n📌 Elon Musk Results:")
for i, r in enumerate(result1["results"][:3]):
    print(f"\nResult {i+1}")
    print("Title:", r["title"])
    print("Summary:", r["content"])
    print("Link:", r["url"])


# test search 2
print("\n🔍 Searching: Prime Minister of India")
result2 = client.search("Who is the Prime Minister of India?")

print("\n📌 PM of India Results:")
for i, r in enumerate(result2["results"][:3]):
    print(f"\nResult {i+1}")
    print("Title:", r["title"])
    print("Summary:", r["content"])
    print("Link:", r["url"])