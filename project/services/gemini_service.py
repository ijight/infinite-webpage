import os
import json
import time
import requests
from dotenv import load_dotenv

load_dotenv() # For local development

class GeminiService:
    def __init__(self):
        self.api_key = os.environ.get('GEMINI_API_KEY') or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        
    def clean_response(self, text):
        """Remove markdown code blocks from the response"""
        # Remove ```html at start and ``` at end
        text = text.strip()
        if text.startswith('```html'):
            text = text[7:]
        if text.endswith('```'):
            text = text[:-3]
        return text.strip()
        
    def generate_content(self, prompt):
        url = f"{self.base_url}?key={self.api_key}"
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        try:
            for progress in range(0, 90, 10):
                yield f"data: {json.dumps({'token': '', 'progress': progress, 'status': 'thinking'})}\n\n"
                time.sleep(0.1)

            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            data = response.json()
            if 'candidates' in data:
                text = data['candidates'][0]['content']['parts'][0]['text']
                # Clean the response before sending
                text = self.clean_response(text)
                yield f"data: {json.dumps({'token': text, 'progress': 90, 'status': 'generating'})}\n\n"
                time.sleep(0.1)
                yield f"data: {json.dumps({'token': '', 'progress': 100, 'status': 'complete'})}\n\n"
            else:
                print(f"Unexpected response structure: {data}")
                        
        except Exception as e:
            print(f"Error during generation: {str(e)}")
            yield f"data: {json.dumps({'error': str(e), 'progress': 0, 'status': 'error'})}\n\n"

    def get_initial_page(self):
        print("\n=== Generating random initial page ===")
        prompt = """Generate a static html page for an interesting random topic, like wikipedia. 
        Choose any topic that would make for an engaging article.
        Include at least 4 links to related topics in the body. 
        Format it as clean HTML without any styling. 
        Make sure links are formatted as <a href="/topic/Topic-Name">Topic Name</a>.
        Wrap the entire content in <article> tags.
        Don't include <html>, <head>, or <body> tags."""
        
        return self.generate_content(prompt)

    def get_topic_page(self, topic):
        print(f"\n=== Generating page for topic: {topic} ===")
        prompt = f"""Generate a detailed static webpage about {topic}.
        Format it like a Wikipedia article with sections and content.
        Include a minumum of 4 links (but target 10) to topics throughout the document.
        Make it informative and engaging.
        Format it as clean HTML without any styling.
        Make sure links are formatted as <a href="/topic/Topic-Name">Topic Name</a>.
        Wrap the entire content in <article> tags.
        Don't include <html>, <head>, or <body> tags."""
        
        return self.generate_content(prompt) 