from typing import Any, Mapping, Optional, Type, Union
from django.forms.utils import ErrorList
from django.shortcuts import render, HttpResponse
from django import forms
from .checkCode import generate_captcha_image,FFT
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from scipy import signal

import matplotlib.pyplot as plt


class loginForm(forms.Form):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {
                "class": "form-control",
                "placeholder": field.label
            }


def login(req):
    if req.method == "GET":
        form = loginForm()
        req.session['img_code'] = generate_captcha_image(
            100, 50, 4, 'arial.ttf', 'myapp\static\img\code.png')
        print(req.session.get('img_code'))
        return render(req, 'login.html', {'form': form})
    else:
        form = loginForm(data=req.POST)
        if form.is_valid() and form.cleaned_data['username'] == 'cgc' and form.cleaned_data['password'] == '123' and req.session.get('img_code').lower() == req.POST.get('code').lower():
            return render(req, 'chart.html')
        else:
            print(form.is_valid())
            print(form.cleaned_data['username'])
            print(form.cleaned_data['password'])
            print(req.session.get('img_code').lower())
            print(req.POST.get('code').lower())
            return render(req, 'login.html', {'form': form})

@csrf_exempt
def img(req):
    req.session['img_code'] = generate_captcha_image(
            100, 50, 4, 'arial.ttf', 'myapp\static\img\code.png')
    form = loginForm()
    return render(req, 'login.html', {'form': form})

def chart(req):
    
    return render(req, 'chart.html')


def chartdata(req):

    file_object = req.FILES.get("txt_file")
    f = open(file_object.name, mode='wb')
    for chunk in file_object.chunks():
        f.write(chunk)
    f.close()
    req.session['data'] = file_object.name

    return render(req, 'chart.html')


def chartdraw(req):
    data_list = []
    i = 1
    with open(f'{req.session.get("data")}', 'r') as file:
        for line in file:
            data_list.append([i, int(line)])
            i += 1

    data = [
        {
            "data": [],
            "type": 'line'
        }
    ]
    data[0]["data"] = data_list

    return JsonResponse({"data": data})


@csrf_exempt
def chartfilter(req):
    maxf = req.GET.get('maxf')
    minf = req.GET.get('minf')
    sample_rate = 100
    data = [
        {
            "data": [],
            "type": 'line',
            "symbol": 'none' 
        }
    ]
    data_list = []
    filter_list =[]
    i=1
    with open(f'{req.session.get("data")}', 'r') as file:
        for line in file:
            data_list.append(int(line))
    b, a = signal.butter(4, [(2*float(minf) )/sample_rate,(2*float(maxf))/sample_rate], 'bandpass')   #最大只能设置为4阶，scipy函数限制
    filt_data = signal.filtfilt(b, a, data_list)#为要过滤的信号
    for field in filt_data:
        filter_list.append([i, int(field)])
        i+=1
    
    data[0]["data"] = filter_list
    return JsonResponse({"data": data})

    # return HttpResponse('231')
def chartfft(req):
    data_list = []
    fft_list =[] 
    with open(f'{req.session.get("data")}', 'r') as file:
        for line in file:
            data_list.append(int(line))

    sample_rate = 100
    x, result = FFT(sample_rate, data_list)
    
    # for fre, amp in x, result:
    #     fft_list.append([fre,amp])
    fft_list = [[x, y] for x, y in zip(x, result)]
    print(fft_list)


    data = [
        {
            "data": [],
            "type": 'line',
            "symbol": 'none' 
        }
    ]
    data[0]["data"] = fft_list
    return JsonResponse({"data": data})
