from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.views import View
from django.contrib import messages

from accounts.forms import (StudentCreationForm, 
                            InvigilatorCreationForm, 
                            UserUpdateForm, ProfileUpdateForm)
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Student, Invigilator, Profile
from django.contrib.auth import logout



def logout_view(request):
    logout(request)
    return redirect('index')


class ChooseSignUpView(TemplateView):
    template_name = 'registration/signup.html'


class StudentSignUpView(CreateView):
    form_class = StudentCreationForm
    template_name = 'accounts/student_signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        slug = self.object.slug
        self.success_url = reverse_lazy('accounts:student_profile', kwargs={'slug': slug})
        return response
    
    
class InvigilatorSignUpView(CreateView):
    form_class = InvigilatorCreationForm
    template_name = 'accounts/invigilator_signup.html'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        slug = self.object.slug
        self.success_url = reverse_lazy('accounts:invigilator_profile', kwargs={'slug': slug})
        return response


class CustomLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    success_url = reverse_lazy('accounts:profile') 
    
    
class StudentProfileView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = 'accounts/student_profile.html'
    context_object_name = 'student'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class InvigilatorProfileView(LoginRequiredMixin, DetailView):
    model = Invigilator
    template_name = 'accounts/invigilator_profile.html'
    context_object_name = 'invigilator'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    
class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user_form = UserUpdateForm(instance=request.user)
        
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            # If the profile does not exist, create one
            profile = Profile(user=request.user)
            profile.save()

        profile_form = ProfileUpdateForm(instance=profile)

        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        
        return render(request, 'accounts/profile.html', context)
    
    def post(self, request):
        user_form = UserUpdateForm(
            request.POST, 
            instance=request.user
        )
        
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            # If the profile does not exist, create one
            profile = Profile(user=request.user)
            profile.save()

        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,  # Ensure you include request.FILES here
            instance=profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            
            messages.success(request, 'Your profile has been updated successfully')
            
            return redirect('accounts:profile')
        else:
            context = {
                'user_form': user_form,
                'profile_form': profile_form
            }
            messages.error(request, 'Error updating your profile')
            
            return render(request, 'accounts/profile.html', context)
        
        