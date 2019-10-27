from rest_framework import serializers
from .models import User,PhoneOTP

class ValidatePhoneSendOTPSerializer(serializers.ModelSerializer):
    print("serializer")
    class Meta:
        model =PhoneOTP
        fields = ('phone','otp')


    def create(self,validated_data):
        phone_otp=PhoneOTP.objects.create(**validated_data)
        return phone_otp






class UserSerializerOTP(serializers.ModelSerializer):
    class Meta:
        model =User
        fields = ('phone', 'password')
        # extra_kwargs= {'password':{'write_only':True},}

    def create(self,validated_data):
        user=User.objects.create(**validated_data)
        return user
