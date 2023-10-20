from django.contrib import admin
from django.urls import path, include
from app.views import SignUpWithVerification, VerifyEmailView, VerificationSuccessView, VerificationErrorView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', SignUpWithVerification.as_view(), name='home'),
    path('verify/<int:user_pk>/<str:token>/', VerifyEmailView.as_view(), name='verify_email'),
    path('verification_success/', VerificationSuccessView.as_view(), name='verification_success'),
    path('verification_error/', VerificationErrorView.as_view(), name='verification_error'),
]