from flask import Flask, request, jsonify, redirect, url_for,  render_template
from bs4 import BeautifulSoup
import requests
import openai

app = Flask(__name__)

# openai.api_key = "sk-mwpBfLq2RMSL5JpDPvW3T3BlbkFJyrzsBTZtRlaRnjbOOQ5Xv"

# def get_answer_from_openai(question, context):
#     response = openai.Answer.create(
#         search_model="davinci",
#         model="davinci",
#         question=question,
#         context=context
#     )
#     return response["answers"][0]["text"]

# def get_answer_from_web(url, question):
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, 'html.parser')
#     paragraphs = soup.find_all('p')
#     for paragraph in paragraphs:
#         if question.lower() in paragraph.text.lower():
#             return paragraph.text.strip()
#     return "I don't know the answer"

@app.route('/')
def welcome():
    return "welcome"

# @app.route('/answer', methods=['POST'])
# def answer_question():
#     data = request.json
#     url = data['url']
#     question = data['question']

#     try:
#         answer = get_answer_from_web(url, question)
#     except:
#         answer = "I don't know the answer"

#     if answer == "I don't know the answer":
#         context = " ".join([p.text for p in BeautifulSoup(requests.get(url).content, 'html.parser').find_all('p')])
#         answer = get_answer_from_openai(question, context)

#     return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)