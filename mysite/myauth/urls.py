from django.urls import path
from django.contrib.auth.views import LoginView

from .views import (MyLogoutView,
                    set_cookie_view,
                    get_cookie_view,
                    set_session_view,
                    get_session_view,
                    AboutMeViews,
                    RegisterView,
                    ChangeAvatarUser,
                    UserListView,
                    UserDetailView,
                    UserUpdate,
                    )

app_name = 'myauth'

urlpatterns = [
    path(
        'login/',
        LoginView.as_view(
            template_name="myauth/login.html",
            redirect_authenticated_user=True,
        ),
        name='login'
    ),
    path("logout/", MyLogoutView.as_view(), name="logout"),
    path("cookie/get/", get_cookie_view, name="cookie-get"),
    path("cookie/set/", set_cookie_view, name="cookie-set"),
    path("session/get/", get_session_view, name="session-get"),
    path("session/set/", set_session_view, name="session-set"),
    path("about-me/", AboutMeViews.as_view(), name="about-me"),
    path("register/", RegisterView.as_view(), name="register"),
    path("users/", UserListView.as_view(), name="users-list"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="users-detail"),
    path("change_avatar/<int:pk>/", ChangeAvatarUser.as_view(), name="change-avatar"),

    path("users/update/<int:pk>/", UserUpdate.as_view(), name="users-update"),

]
