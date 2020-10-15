# -*- coding: utf-8 -*-

import requests
import random
import string
import time

from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
#from utils.json import JSONEncoder
from json import JSONEncoder
from django.views.decorators.csrf import csrf_exempt
from web.models import User,Token,Expense,Income,Passwordresetcodes
from datetime import datetime
from django.contrib.auth.hashers import make_password
from postmark import PMMail
#def Expense(request):
#    return render(request)
# Create your views here

random_str=lambda N:''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits))

def get_client_ip(request):
    x_forwarded_for=request.META.get('HOOP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip=x_forwarded_for.split(',')[0]
    else:
        ip=request.META.get('REMOTE_ADDR')
    return ip

def grecaptcha_verify(request):
    data=request.POST
    captcha_rs=data.get('g-recaptcha-response')
    url="https://www.google.com/recaptcha/api/siteverify"
    params={
          'secret':settings.RRECPTCHA_SECRET_KEY,
          'response':captcha_rs,
          'remoteip':get_client_ip(request)
    }
    verify_rs = requests.get(url,params=params,verify=True)
    verify_rs = verify_rs.json()
    return verify_rs.get("success",False)




def register(request):
    if 'requestcode' in request.POST:
       #is this spam?
          if not grecaptcha_verify(request):
              context={'message':'  کد یا کلیک یا تشخیص عکس زیر فرم را درست بر کنید.ببخشید که فرم به شکل اولیه بر نگشته'}
              return render(request,'register.html',context)


          if User.objects.filter(email=request.POST['email']).exists():
              context={'message':'از صفحه ورود گزینه فراموش رمز رو انتخاب کنید.ببخشید که فرم ذخیره نشده.درست میشه'}
              #TODO:
              return render(request,'register.html',context)

          if not User.objects.filter(username=request.POST['username']).exists():
              code=random_str(28)
              now=datetime.now()
              email=request.POST['email']
              password=make_password(request.POST['password'])
              username=request.POST['username']
              temporarycode=Passwordresetcodes(email=email,time=now,code=code,username=username,password=password)
              temporarycode.save()
              message=PMMail(api_key=settings.POSTMARK_API_TOKEN,
                             subject="فعال سازی اکانت بستون۱",
                             sender="melikamosayebi1376@gmail.com",
                             to=email,
                             text_body="برای فعال سازی اکانت بستون۱ خود روی لینک رو به رو کلیک کنید:http://localhost:8009/accounts/register/?email={}&code={}".format(email,code),
                             tag="account request")
              message.send()
              context={'message':' .ایمیل شما ساخته شد.لطفا بس از چک کردن ایمیل روی لینک کلیک کنید'}
              return render(request,'login.html',context)
          else: 
              context={'message':'.متاسفانه این نام کاربری قبلا استفاده شده.ببخشید که فرم ذخیره نشده.درست میشه'}
              #TODO:keep the form data
              return render(request,'register.html',context)
    elif  'code' in request.GET:#user clicked on code
          email=request.GET['email']
          code=request.GET['code']
          if Passwordresetcodes.objects.filter(code=code).exists():#if code is in temperory
              new_temp_user=Passwordresetcodes.objects.get(code=code)
              newuser=User.objects.create(username=new_temp_user.username,password=new_temp_user.password,email=email)
              this_token=random_str(48)
              token = Token.objects.create(user=newuser,token=this_token)
              Passwordresetcodes.objects.filter(code=code).delete()
              context={'message':'.اکانت شما ساخته شد.توکن شما{}است.آن را ذخیره کنید چون دیگر نمایش داده نخواهد شد'.format(this_token)}
              return render(request,'login.html',context)
          else:
              context={'message':'این کد فعال سازی معتبر نیست در صورت نیاز دوباره تلاش کنید'}
              return render(request,'login.html',context)
    else:
      context={'message':'کد فعال سازی معتبر نیست در صورت نیاز دوباره تلاش کنید'}
      return render(request,'register.html',context)


@csrf_exempt

def submit_income(request):
    """submits an income"""

    #TODO: validate data.user might be fake.token might be fake.amount might be
    this_token=request.POST['token']
    this_user=User.objects.filter(token__token=this_token).get()
    if 'date' not in request.POST:
        date=datetime.now()
    Income.objects.create(user=this_user,amount=request.POST['amount'],
            text=request.POST['text'],date=date)


    return JsonResponse({
    'status':'ok',
    },encoder=JSONEncoder)

@csrf_exempt

def submit_expense(request):
    """submits an expense"""

    #TODO: validate data.user might be fake.token might be fake.amount might be
    this_token=request.POST['token']
    this_user=User.objects.filter(token__token=this_token).get()
    if 'date' not in request.POST:
        date=datetime.now()


    Expense.objects.create(user=this_user,amount=request.POST['amount'],
            text=request.POST['text'],date=now)


    return JsonResponse({
    'status':'ok',
    },encoder=JSONEncoder)
