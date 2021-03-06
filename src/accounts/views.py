from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    DetailView, CreateView, TemplateView, ListView)
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import FormView
from .forms import UserForm, UserDetailsForm, ProfileForm
from django.urls import reverse_lazy, reverse
from .models import Profile, UserLog
from django.contrib.auth.decorators import login_required

# Create your views here.
User = get_user_model()


class UserRegisterView(FormView):
    form_class = UserForm
    template_name = 'accounts/registration.html'
    success_url = '/accounts/login'

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        new_user = User.objects.create(username=username, email=email)
        new_user.set_password(password)
        new_user.save()
        return super(UserRegisterView, self).form_valid(form)


@login_required
def UserDetailsEditView(request):
    user = get_object_or_404(Profile, user=request.user)
    profile_form = ProfileForm(request.POST or None, instance=user)
    user_form = UserDetailsForm(request.POST or None, instance=request.user)

    if request.method == 'POST':

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            image = request.FILES.get('image')
            bio = request.POST.get('bio')
            social = request.POST.get('social')
            user_profile = Profile.objects.get(user=request.user)
            user_profile.bio = bio
            user_profile.social = social
            user_profile.image = image
            user_profile.save()
            return HttpResponseRedirect(reverse('accounts:profile'))

    return render(request, 'dashboard/user.html', {
        'head': 'User Profile',
        'contact_form': user_form,
        'profile_form': profile_form,
    })


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/user.html'

    def get_queryset(self):
        queryset = User.objects.get(username=self.request.user.username)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['head'] = 'User Profile'
        return context


class UserLogListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = UserLog

    def get_context_data(self, **kwargs):
        context = super(UserLogListView, self).get_context_data(**kwargs)
        context['head'] = 'User Activity'
        context['sub_head'] = 'List'
        return context

    def test_func(self):
        return self.request.user.is_superuser


class UserLogDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = UserLog

    def get_context_data(self, **kwargs):
        context = super(UserLogDetailView, self).get_context_data(**kwargs)
        context['head'] = 'User Activity'
        context['sub_head'] = 'Details'
        return context

    def test_func(self):
        return self.request.user.is_superuser
