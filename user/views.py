from django.shortcuts import render, redirect, HttpResponse
from user.forms import CustomRegisterForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator


# Create your views here.
def sign_up(request):
    if request.method == "GET":
        form = CustomRegisterForm()
    if request.method == "POST":
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            print("\n\n\n", form.cleaned_data)
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get("password1"))
            user.is_active = False
            user.save()
            messages.success(
                request, "A activation Mail Send your mail. Plase check..."
            )
            return redirect("sign-in")
    return render(request, "sign-up/sign_up.html", {"form": form})


def activate_user(reqest, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect("sign-in")
        else:
            return HttpResponse("Invalid id or token")
    except User.DoesNotExist:
        return HttpResponse("User Not Found.!")


def sign_in(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    return render(request, "sign-in/sign_in.html", {"form": form})
