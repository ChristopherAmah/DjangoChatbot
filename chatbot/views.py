from django.shortcuts import render, redirect
from django.http import JsonResponse
# import openai
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat
from django.utils import timezone
import json
import random



# openai_api_key = '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'
# openai.api_key = openai_api_key

# def ask_openai(message):
#     response = openai.Completion.create(
#         model = "davinci-002",
#         prompt = message,
#         max_tokens=150,
#         n=1,
#         stop=None,
#         temperature=0.7,
#     )
#     answer = response.choices[0].text.strip()
#     return answer

# Load responses from JSON file
with open('responses.json') as file:
    responses = json.load(file)

# Function to generate a response based on user input
def generate_response(user_input):
    if 'hello' in user_input.lower() or 'hi' in user_input.lower():
        return random.choice(responses['greetings'])
    elif 'bye' in user_input.lower() or 'goodbye' in user_input.lower():
        return random.choice(responses['farewell'])
    elif '?' in user_input:
        return random.choice(responses['questions'])
    elif 'yes' in user_input.lower() or 'sure' in user_input.lower() or 'yeah' in user_input.lower():
        return random.choice(responses['affirmative'])
    elif 'no' in user_input.lower() or 'nah' in user_input.lower():
        return random.choice(responses['negative'])
    else:
        return random.choice(responses['generic'])



# Create your views here.
def chatbot(request):
    chats = Chat.objects.filter(user=request.user)

    if request.method == 'POST':
        message = request.POST.get('message')
        response = generate_response(message)

        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html', {'chats': chats})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('chatbot')
        else:
            error_message = "Invalid username or password"
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect('chatbot')
            except:
                error_message = 'Error creating account'
                return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = 'Password do not match'
            return render(request, 'register.html', {'error_message': error_message})
    return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('login')