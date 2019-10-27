import json
import random
from urllib import request
import requests
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from .models import User, PhoneOTP
from .serializer import UserSerializerOTP,ValidatePhoneSendOTPSerializer
from django.shortcuts import get_object_or_404

import requests
# enter your information instead of yours

def get_token():
    url = "http://RestfulSms.com/api/Token"
    payload = {"UserApiKey": "yours..", "SecretKey": "yours"}
    headers = {
        'Content-Type': "application/json",
         }
    response = requests.request("POST", url, json=payload, headers=headers)
    response=response.json()
    return (response["TokenKey"])


def send_message(phone, code):
    token=str(get_token())
    v_code = str(code)
    url = "http://RestfulSms.com/api/MessageSend"
    payload = {"Messages": [v_code], "MobileNumbers": ["yours"], "LineNumber": "yours"}
    headers = {
        'Content-Type': "application/json",
        'x-sms-ir-secure-token':token,
        }

    response = requests.request("POST", url, json=payload, headers=headers)



def generate_otp(phone):
    if phone:
        code = random.randint(999, 9999)
        return code
    else:
        return False


class ValidatePhoneSendOTP(APIView):

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone')
        if phone_number:
            phone = str(phone_number)
            user = User.objects.filter(phone__iexact=phone)
            if user.exists():
                return Response({
                    'status': False,
                    'detail': ' phone already exist in db'
                })
            else:
                key = generate_otp(phone)
                if key:
                    old_otp = PhoneOTP.objects.filter(phone__iexact=phone)

                    if old_otp.exists():

                        old_otp = old_otp.first()
                        count = old_otp.count
                        if count > 20:
                            return Response({
                                'status': False,
                                'detail': ' some problem with key. limit exceeded'
                            })
                        old_otp.count = count + 1
                        old_otp.save()

                        return Response({
                            'status': True,
                            'detail': ' otp sent successfully'
                        })
                    else:
                        tem_data={
                            "phone":phone,
                            "otp":key
                        }
                        serializer = ValidatePhoneSendOTPSerializer(data=tem_data)
                        serializer.is_valid(raise_exception=True)
                        phone_otp = serializer.save()

                        send_message(phone, key)
                        return Response({
                            'status': True,
                            'detail': ' otp sent successfully'
                        })

                else:
                    return Response({
                        'status': False,
                        'detail': ' some problem with key'
                    })


        else:
            return Response({
                'status': False,
                'detail': 'No phone number'
            })


class ValidateOTP(APIView):

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone')
        sent_otp = request.data.get('otp')
        if phone and sent_otp:
            old = PhoneOTP.objects.filter(phone__iexact=phone)
            if old.exists:
                old = old.first()
                otp = old.otp
                if str(otp) == str(sent_otp):
                    old.validated = True
                    old.save()
                    return Response({
                        'status': True,
                        'detail': 'The Code matched'
                    })
                else:
                    return Response({
                        'status': False,
                        'detail': 'The Code doesnt match'
                    })

            else:
                return Response({
                    'status': False,
                    'detail': 'please send the OTP request first'
                })

        else:
            return Response({
                'status': False,
                'detail': 'Please provide the OTP and Phone number'
            })


class RegisterAfterOTPVerification(APIView):

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        password = request.data.get('password', False)
        if phone and password:
            old = PhoneOTP.objects.filter(phone__iexact=phone)
            if old.exists:
                old = old.first()
                valideted_phone = old.validated
                if valideted_phone == True:
                    temp_data = {
                        'phone': phone,
                        'password': password,
                    }
                    serializer = UserSerializerOTP(data=temp_data)
                    serializer.is_valid(raise_exception=True)
                    user = serializer.save()
                    old.delete()
                    return Response({
                        'status': True,
                        'detail': 'your password in registered'
                    })




                else:
                    return Response({
                        'status': False,
                        'detail': 'please verify your phone first'
                    })


            else:
                return Response({
                    'status': False,
                    'detail': 'please verify your phone first'
                })

        else:
            return Response({
                'status': False,
                'detail': 'Please provide the number and Phone password'
            })
