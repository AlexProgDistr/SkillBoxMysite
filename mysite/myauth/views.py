from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View, TemplateView, CreateView, UpdateView, ListView, DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


from .models import Profile
from .forms import AvatarChange

class MyLogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('myauth:login')


class AboutMeViews(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Profile
    template_name = 'myauth/about-me.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def test_func(self):
        return self.request.user == self.get_object().user



class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "myauth/register.html"
    success_url = reverse_lazy("myauth:about-me")

    def form_valid(self, form):
        respose = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(request=self.request, username=username, password=password)
        login(self.request, user)
        return respose


def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie set")
    response.set_cookie("fizz", "buzz", max_age=3600)
    return response


def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("fizz", "default value")
    return HttpResponse(f"Cookie value {value!r}")

def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["foobar"] = "spameggs"
    return HttpResponse("Session Set")

def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("foobar", "default value")
    return HttpResponse(f"Session value {value!r}")

class ChangeAvatarUser(UpdateView):
    """Смена аватарки пользователем со страницы about-me"""
    model = Profile
    form_class = AvatarChange
    template_name = "myauth/profile_change_avatar.html"

    def get_success_url(self):
        return reverse("myauth:about-me")

class UserListView(ListView):
    """Класс отображение списка пользователей"""
    model = User
    template_name = 'myauth/users-list.html'
    context_object_name = 'users'


class UserDetailView(DetailView):
    """Класс просмотра пользователя"""
    template_name = 'myauth/user-detail.html'
    queryset = User.objects.select_related('profile')
    context_object_name = 'user'



class UserUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Класс изменения пользователя"""

    model = Profile
    form_class = AvatarChange
    template_name = "myauth/profile_change_avatar.html"

    def test_func(self):
        """редактирровать могут админы, суперпользователи и хозяин аккаунта"""
        return (self.request.user.is_superuser or
                self.request.user.is_staff or
                self.request.user == self.get_object().user)

    def get_success_url(self):
        return reverse('myauth:users-detail', kwargs={'pk': self.object.user.pk})

