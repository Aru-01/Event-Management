from django.urls import path
from user.views import sign_up, activate_user, sign_in

urlpatterns = [
    path("sign-up/", sign_up, name="sign-up"),
    path("activate/<int:user_id>/<str:token>/", activate_user),
    path("sign-in/", sign_in, name="sign-in"),
]
