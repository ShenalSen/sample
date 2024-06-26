# -*- coding: utf-8 -*-
"""ChatbotSHENZEN.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1FUVDJX0xlWfNwFZAnNqW-XvuH5GkMV2M
"""

# This notebook demonstrates the creation of a chatbot using Python. The chatbot utilizes natural language processing (NLP) techniques to understand and respond to user input.
# It leverages machine learning models and libraries such as TensorFlow, PyTorch, or Hugging Face's Transformers for implementing conversational AI.
# The notebook covers data preprocessing, model training, and deployment aspects to build an interactive chatbot application.

# Install the required libraries
!pip install nltk
!pip install newspaper3k

# Import necessary libraries
import nltk
from newspaper import Article

# Additional imports for chatbot development
import random
import string
import numpy as np
import warnings

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
warnings.filterwarnings('ignore')

# Download the 'punkt' package quietly
nltk.download('punkt', quiet=True)

#Download and parse the article
article = Article('https://www.geeksforgeeks.org/python-programming-language-tutorial/')
article.download()
article.parse()
article.nlp()
corpus = article.text

#Print the articles text
print(corpus)

#Tokenization
text = corpus
sentence_list = nltk.sent_tokenize(text) #A list of sentences

#Print the list of sentences
print(sentence_list)

# Define the greeting response function
def greeting_response(text):
    user_greetings = ['hello', 'hi', 'greetings', 'sup', 'what\'s up', 'hey']
    bot_greetings = ['Hello! Ready to learn Python?', 'Hi there! Excited to learn Python?', 'Hey! Let\'s learn Python together!']

    for word in text.lower().split():
        if word in user_greetings:
            return random.choice(bot_greetings)
    return None

# Response generation using cosine similarity
def response(user_input):
    user_input = user_input.lower()
    sentence_list.append(user_input)

    # Convert the text to a matrix of token counts
    bot_response = ''
    vectorizer = CountVectorizer().fit_transform(sentence_list)
    vectors = vectorizer.toarray()

    # Compute the cosine similarity between the user input and the corpus
    cosine_matrix = cosine_similarity(vectors[-1], vectors)
    similar_sentence_number = cosine_matrix.argsort()[0][-2]

    # Extract the highest cosine similarity score
    matched_vector = cosine_matrix.flatten()
    matched_vector.sort()
    highest_similarity_score = matched_vector[-2]

    # Check if the score is high enough
    if highest_similarity_score == 0:
        bot_response = "I apologize, I don't understand. Let's focus on learning Python!"
    else:
        bot_response = sentence_list[similar_sentence_number]

    sentence_list.remove(user_input)
    return bot_response

# Main chatbot loop
exit_list = ['exit', 'bye', 'see you later', 'quit']

print("Bot: Hello! I'm your 'Learn Python Programming' bot. Ask me anything about Python programming or type 'exit' to end the conversation.")

while True:
    user_input = input("You: ")
    if user_input.lower() in exit_list:
        print("Bot: Goodbye! Happy Python programming!")
        break
    else:
        if greeting_response(user_input) is not None:
            print("Bot: " + greeting_response(user_input))
        else:
            print("Bot: " + response(user_input))