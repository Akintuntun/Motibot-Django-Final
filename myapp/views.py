from django.shortcuts import render, HttpResponse

def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

def team_members(request):
    return render(request, "teammembers.html")

def chat(request):
    return render(request, "chat.html")