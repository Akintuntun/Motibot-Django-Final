from django.shortcuts import render, HttpResponse
from .models import Directory
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from django.http import JsonResponse
import json
import pickle
import numpy as np
from django.conf import settings
import os




model_path = os.path.join(settings.BASE_DIR, 'myapp', 'ml', 'svm_model.pkl')
tokenizer_encoder_path = os.path.join(settings.BASE_DIR, 'myapp', 'ml', 'tfidf_vectorizer.pkl')
intents_path = os.path.join(settings.BASE_DIR, 'myapp', 'ml', 'intentsEx.json')

with open(model_path, 'rb') as f:
    loaded_model = pickle.load(f)

    # Load the Tokenizer and Label Encoder used during training
with open(tokenizer_encoder_path, 'rb') as file:
    data = pickle.load(file)

    # Load intents data from intents.json
with open(intents_path, 'r', encoding='utf-8') as intents_file:
    intents_data = json.load(intents_file)



# Function to predict intents based on user input
def predict_intent(text):
    # Vectorize the user input using the loaded TF-IDF vectorizer
    user_input_vec = data.transform([text])

    # Predict the intent using the loaded SVM model
    intent = loaded_model.predict(user_input_vec)[0]
    confidence_score = loaded_model.decision_function(user_input_vec).max()
    return intent, confidence_score

# Function to get response based on intent
def get_response(intent):
    for intent_data in intents_data['intents']:
        if intent_data['tag'] == intent:
            responses = intent_data['responses']
            return np.random.choice(responses)
    return "I'm not sure how to respond to that."


def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

def team_members(request):
    return render(request, "teammembers.html")

def chat(request):
    welcome_message = "Welcome to the chat! How can I assist you today?"
    return render(request, "chat.html", {'welcome_message': welcome_message})


def getResponse(request):
    user_message = request.GET.get('userMessage')
    predicted_intent, confidence_score = predict_intent(user_message)
    response = get_response(predicted_intent)

    if predicted_intent == "fact-12":
        directories = Directory.objects.all()
        if directories.exists():
            directory_info = "<h2 class='botText'>For San Pablo City, here is the available list.</h2>"
            directory_info += "<ul class='botText style='list-style-type: none;'>"
            for directory in directories:
                directory_info += f"<strong>Directory Information</strong> <br><br>"
                directory_info += f"<strong>Address:</strong> {directory.address}<br>"
                directory_info += f"<strong>Name:</strong> {directory.name}<br>"
                directory_info += f"<strong>Contact Info:</strong> {directory.contact_info}<br>"
                directory_info += f"<strong>Services Offered:</strong> {directory.services}<br><br>"
            directory_info += "</ul>"
            response += "<br>" + directory_info
        else:
            response = "Sorry, there are currently no directory available."
        return HttpResponse(response)
    
    elif confidence_score > .5 :
        response = get_response(predicted_intent)
        return HttpResponse(response)
    
    else:
        # Return a placeholder response or indicate low confidence
        return HttpResponse('Im not sure how to respond to that.')
