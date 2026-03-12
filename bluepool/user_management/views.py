from django.shortcuts import render
from .models import Profile
from django.views.generic.edit import UpdateView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile
from .forms import ProfileForm, UserCreateForm


class ProfileCreateView(FormView):
    model = Profile
    template_name = 'profile-add.html'
    form_class = UserCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserCreateForm()
        return context

    def form_valid(self, form):
        form.save()
        new_profile = Profile(
            user=User.objects.get(username=form.cleaned_data['username']),
            name=form.cleaned_data['display_name'],
            email_address=form.cleaned_data['email']
        )
        # print('burger')
        new_profile.save()

        return super(ProfileCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('homepage', kwargs={})


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'profile.html'
    form_class = ProfileForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserCreateForm()
        return context
    
    def form_valid(self, form):
        #if self.request.user in Profile.objects.all():
        #    form.instance.user = self.request.user
        #   form.instance.email_address.widget.attrs['readonly'] = True
        return super(ProfileUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('profile:profile', args=[self.get_object().pk])
        #return super(ProfileUpdateView, self).form_valid(form)