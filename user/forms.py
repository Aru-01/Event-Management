from django import forms
from django.contrib.auth.models import User
import re


class CustomRegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(), label="Password")
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(), label="Confirm Password"
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "confirm_password",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        css_class = "w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition ml-1"
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = css_class
            if not field.widget.attrs.get("placeholder"):
                field.widget.attrs["placeholder"] = f"Enter {field.label.lower()}"

    def clean_email(self):
        email = self.cleaned_data.get("email")
        email_exists = User.objects.filter(email=email).exists()
        if email_exists:
            raise forms.ValidationError("Email already exists")
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        errors = []
        if len(password1) < 8:
            errors.append("Password must be at least 8 character long")

        if not re.search(r"[A-Z]", password1):
            errors.append("Password must include at least one uppercase letter")

        if not re.search(r"[a-z]", password1):
            errors.append("Password must include at least one lowercase letter")

        if not re.search(r"[0-9]", password1):
            errors.append("Password must include at least one number")

        if not re.search(r"[@#$%^&+=]", password1):
            errors.append("Password must include at least one special character")

        if errors:
            raise forms.ValidationError(errors)

        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("confirm_password")

        if password1 != confirm_password:
            raise forms.ValidationError("Password don't match")

        return cleaned_data
