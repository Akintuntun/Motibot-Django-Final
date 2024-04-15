from django.shortcuts import render, HttpResponse
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from django.http import JsonResponse
import json
import pickle
import numpy as np
from django.conf import settings
import os



model_path = os.path.join(settings.BASE_DIR, 'myapp', 'ml', 'bilstm_chatbot_model.h5')
tokenizer_encoder_path = os.path.join(settings.BASE_DIR, 'myapp', 'ml', 'tokenizer_and_encoder.pkl')
intents_path = os.path.join(settings.BASE_DIR, 'myapp', 'ml', 'intentsE.json')

model = load_model(model_path)

    # Load the Tokenizer and Label Encoder used during training
with open(tokenizer_encoder_path, 'rb') as file:
    data = pickle.load(file)
    tokenizer = data['tokenizer']
    label_encoder = data['encoder']

    # Load intents data from intents.json
with open(intents_path, 'r', encoding='utf-8') as intents_file:
    intents_data = json.load(intents_file)


# Function to get model prediction
def predict_intent(text):
    input_sequence = tokenizer.texts_to_sequences([text])
    padded_input_sequence = pad_sequences(input_sequence, maxlen=model.input_shape[1])
    predictions = model.predict(padded_input_sequence)
    predicted_intent = label_encoder.inverse_transform([np.argmax(predictions)])
    confidence_score = np.max(predictions)
    return predicted_intent[0], confidence_score


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
    if confidence_score > .98 :
        response = get_response(predicted_intent)
        return HttpResponse(response)
    else:
        # Return a placeholder response or indicate low confidence
        return HttpResponse('Im not sure how to respond to that.')
