from flask import Flask, request, jsonify, render_template
import openai
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Access the API key
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/answer', methods=['POST'])
def question_answering():
    if request.method == 'POST':
        url = request.json.get('url')
        question = request.json.get('question')

        if not url or not question:
            return jsonify({'error': 'Missing required fields: url and question'}), 400

        try:
            # Fetch webpage content
            response = requests.get(url)
            response.raise_for_status()  # Raise exception for non-2xx status codes

            # Parse HTML content
            soup = BeautifulSoup(response.content, 'html.parser')

            # Customize answer extraction based on webpage structure (consider using libraries like scrapy for complex sites)
            answer_elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'li'])  # Adjust selectors as needed

            # Extract text from relevant elements
            extracted_text = ' '.join([element.get_text(strip=True) for element in answer_elements[:2]])

            # Use OpenAI to refine and summarize potential answers (consider cost implications)
            openai_response = openai.Completion.create(
                engine="gpt-3.5-turbo-instruct",  # Adjust engine as needed

                # prompt=f"Question: {question}. Webpage Content: {extracted_text}. Can you summarize the most relevant answer in given {extracted_text} ? if relevant answer not found in {extracted_text} say 'I don’t know the answer'",
                prompt = f'''**Given the question:** {question}. **Can you identify the factual information in the provided text that directly addresses the question?**
                **Context:** {extracted_text} If no relevant information is found in the {extracted_text}, please respond with "I don't know the answer".
                **... directly related to the question WITHOUT creating new information or going beyond the provided context...**''',
                max_tokens=100,  # Adjust max tokens for cost and conciseness
                n=1,
                stop=None,
                temperature=0.7,  # Adjust temperature for creativity vs. accuracy
            )

            print(openai_response)

            final_answer = openai_response.choices[0].text.strip()

            return jsonify({'answer': final_answer})
        except requests.exceptions.RequestException as e:
            return jsonify({'error': f"Error fetching webpage: {e}"}), 500
        except openai.error.OpenAIError as e:
            return jsonify({'error': f"Error with OpenAI API: {e}"}), 500

    return jsonify({'message': 'Use POST request with JSON data: {"url": "...", "question": "..."}'}), 405

if __name__ == '__main__':
    app.run(debug=True)
