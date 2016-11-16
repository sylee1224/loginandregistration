from django.shortcuts import render, redirect

# Create your views here.
from django.contrib import messages
from .models import Registration
import bcrypt

def index(request):
    context = {
        "users": Registration.objects.all()
    }
    print context
    return render(request, 'login/index.html', context)

def register(request):
    res = Registration.objects.add_user(request.POST)
    print request.POST

    if res['added']:
        messages.success(request, "Success! Welcome {}".format(res['new_user'].first_name))
        return render(request, 'login/success.html')
    else:
        for error in res['errors']:
            messages.error(request,error)
            return redirect('/')

def login(request):
    log = Registration.objects.validate(request.POST)
    print request.POST

    if log:
        messages.success(request, "Success! Welcome {}".format(log[1].first_name))
        return render(request, 'login/success.html')
    else:
        messages.success(request, "Password does not match")
        return redirect('/')
