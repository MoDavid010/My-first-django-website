from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, UpdateView

from .forms import UpdateProfileForm, SignupForm
from .models import CustomUser


class SignupView(View):
    template_name = 'core/signup.html'
    form = SignupForm

    def get(self, request, *args, **kwargs):
        context = {
            'form': self.form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('core:profile', kwargs={'user_id': user.id}))
        else:
            return render(request, self.template_name, {
                'form': form,
            })


@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse("posts:index"))


class ProfileView(DetailView):
    model = CustomUser
    template_name = 'core/profile.html'
    pk_url_kwarg = 'user_id'
    context_object_name = 'profile'


class ProfileEditView(UpdateView):
    model = CustomUser
    template_name = 'core/edit_profile.html'
    pk_url_kwarg = 'user_id'
    context_object_name = 'profile'
    form_class = UpdateProfileForm

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj != request.user:
            raise Http404('Вам сюда нельзя! это не ваш профиль! Уходите! >:С')
        return super().dispatch(request, *args, **kwargs)


class AddRemoveFriend(View):
    def post(self, request, user_id, *args, **kwargs):
        profile = get_object_or_404(CustomUser, id=user_id)
        if profile.friends.filter(id=request.user.id).exists():
            friend = profile.friends.get(id=request.user.id)
            profile.friends.remove(friend)
            request.user.friends.remove(profile)
        else:
            profile.friends.add(request.user)
            request.user.friends.add(profile)
        return redirect(request.META.get('HTTP_REFERER'), request)

