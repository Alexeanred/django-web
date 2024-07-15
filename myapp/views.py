from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import google.generativeai as genai
import json
from django.shortcuts import redirect, render, get_object_or_404
from myapp.models import ChatMessage, Chat
from django.urls import reverse
import markdown
from django.utils.safestring import mark_safe

# Configure API key
genai.configure(api_key="AIzaSyDHphbtime4GeMrjmoH7qPhUDlmhbXX2I8")

# Create your views here.
def home(request):
    return render(request, 'homepage.html')

def about(request):
    return render(request, 'about.html')

def features(request):
    return render(request, 'features.html')

def contact(request):
    return render(request, 'contact.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('monthlysub')  # Redirect to homepage after login
        else:
            messages.error(request, 'Invalid login details.')
            return render(request, 'login.html')
    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST['firstName']
        last_name = request.POST['lastName']
        email = request.POST['email']
        password = request.POST['password']
        if not User.objects.filter(username=email).exists():
            user = User.objects.create_user(username=email, password=password, first_name=first_name, last_name=last_name)
            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('login')  # Redirect to login page after sign up
        else:
            messages.error(request, 'Email already in use.')
            return render(request, 'signup.html')
    return render(request, 'signup.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def monthlysub(request):
    return render(request, 'monthlysub.html')

def checkout(request):
    return render(request, 'checkout.html')

def chat(request):
    return render(request, 'chat.html')


def send_message(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

    if request.method == 'POST':
        genai.configure(api_key="AIzaSyDHphbtime4GeMrjmoH7qPhUDlmhbXX2I8")
        model = genai.GenerativeModel("gemini-1.5-flash")

        user_message = request.POST.get('user_message')

        # Lấy lịch sử hội thoại của chat hiện tại
        history = chat.messages.all().order_by('timestamp')

        # Tạo prompt dựa trên lịch sử hội thoại
        history_text = "\n".join([f"User: {msg.user_message}\nBot: {msg.bot_response}" for msg in history])
        prompt = f"{history_text}\nUser: {user_message}\nBot:"
        if not history.exists():
            instruction = (
                "Your name are CVGPT. In this chat, you will helping people write a CV. You have to ask the user to provide information needed for their CV. "
                "First, personal information (name and working position is strictly required). Then, ask for their CV headline/objective/summary (you can write it for them it they ask for). "
                "Next, ask them for work experiences. The work experience should include Job Title, Company Name, Dates Employed and Achievements and responsibilities; remember to list these for them and remind them if the information they provided lack any of these. "
                "Next, ask for their education history. Finally, ask for their skills. Continiously remind them for the remaining kind of informations they haven't provided during the chat. "
                "When gathered all of the information, print the whole CV for them to check. From now on, whenever they ask to fix any part of the CV, print out the whole updated CV again."
            )
            prompt = instruction + "\n" + prompt
        # Generate bot response
        bot_response = model.generate_content(prompt)

        if bot_response.text:
            # Convert markdown to HTML
            bot_response_html = markdown.markdown(bot_response.text)
            bot_response_html = mark_safe(bot_response_html)
            ChatMessage.objects.create(chat=chat, user_message=user_message, bot_response=bot_response_html)
        else:
            pass

    return redirect(reverse('list_messages_with_id', kwargs={'chat_id': chat_id}))


def list_messages(request, chat_id=None):
    chats = Chat.objects.all()
    if chat_id:
        chat = get_object_or_404(Chat, id=chat_id)
    else:
        chat = chats.first() or Chat.objects.create()

    messages = chat.messages.all().order_by('-id')[:4][::-1]
    return render(request, 'chat.html', {'messages': messages, 'chat_id': chat.id, 'chats': chats})

def new_chat(request):
    chat = Chat.objects.create()
    return redirect(reverse('list_messages_with_id', kwargs={'chat_id': chat.id}))

def delete_chat(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    chat.delete()
    return redirect('list_messages')

def about(request):
    return render(request, 'about.html')

def features(request):
    return render(request, 'features.html')

def contact(request):
    return render(request, 'contact.html')

def contact_submit(request):
    # Handle form submission logic
    return render(request, 'contact.html', {'message': 'Thank you for contacting us! We will get back to you soon.'})