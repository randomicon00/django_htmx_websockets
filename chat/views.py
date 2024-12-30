from django.shortcuts import render
from .models import Message


def index(request):
    messages = Message.objects.all().order_by("timestamp")
    return render(request, "chat/index.html", {"messages": messages})
