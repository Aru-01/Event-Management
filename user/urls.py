from django.urls import path
from user.views import (
    sign_up,
    activate_user,
    sign_in,
    sign_out,
    admin_dashboard,
    group_list,
    event_dashboard,
    create_group,
    change_role,
    delete_user,
)

urlpatterns = [
    # authentication related
    path("users/sign-up/", sign_up, name="sign-up"),
    path("users/activate/<int:user_id>/<str:token>/", activate_user),
    path("users/sign-in/", sign_in, name="sign-in"),
    path("users/sign-out/", sign_out, name="sign-out"),
    # admin related
    path("admin/dashboard/", admin_dashboard, name="admin-dashboard"),
    path("admin/dashboard/group-list", group_list, name="group-list"),
    path("admin/event-dashboard/", event_dashboard, name="event-dashboard"),
    path("admin/dashboard/create-group/", create_group, name="create-group"),
    path("admin/dashboard/change-role/<int:user_id>", change_role, name="change-role"),
    path("admin/dashboard/delete-user/<int:user_id>", delete_user, name="delete-user"),
]
