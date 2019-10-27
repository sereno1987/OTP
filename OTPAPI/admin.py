from django.contrib import admin
from .models import User,PhoneOTP
# Register your models here.
admin.site.register(PhoneOTP)
admin.site.register(User)

