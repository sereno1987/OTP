from django.urls import path
from .views import ValidatePhoneSendOTP, ValidateOTP, RegisterAfterOTPVerification  

urlpatterns = [
    path('validate_phone/', ValidatePhoneSendOTP.as_view()),
    path('validate_otp/', ValidateOTP.as_view()),
    path('register_pass_otp/', RegisterAfterOTPVerification.as_view()),
]
