from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.views import View
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from .forms import SignUpForm
from django.core.mail import EmailMessage, send_mail


class SignUpWithVerification(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('home')

    def send_verification_email(self, user):
        token = default_token_generator.make_token(user)
        verify_url = self.request.build_absolute_uri(f'/verify/{user.pk}/{token}/')
        subject = 'Verify your email'
        message = f'Hello {user.username}, please click the link below to verify your email:\n\n{verify_url}'
        send_mail(subject, message, 'sender@example.com', [user.email])

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object  
        user.is_active = False
        user.save()
        self.send_verification_email(self.object)
        return response


class VerificationSuccessView(TemplateView):
    template_name = 'verification_success.html'


class VerificationErrorView(TemplateView):
    template_name = 'verification_error.html'


class VerifyEmailView(View):
    def get(self, request, user_pk, token):
        user = get_user_model().objects.get(pk=user_pk)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('verification_success')
        else:
            return redirect('verification_error')
