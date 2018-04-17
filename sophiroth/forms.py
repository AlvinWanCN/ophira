#coding:utf-8

from django import forms

class Register(forms.Form):
    username = forms.CharField(max_length=32,label='Username:',required=True)
    nickname = forms.CharField(max_length=32,label='Nickname:',required=True)
    email = forms.EmailField(max_length=40,label='Email:',required=False)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput,label='Password:',required=True)
    birthday = forms.DateField(widget=forms.DateInput,label='Birthday:',required=False)

    def clean_password(self): #命名必须是clean_字段名称
        password = self.cleaned_data['password']
        if password[0].isdigit(): #判断首字是否是数字
            raise forms.ValidationError("First can't be number")
        return password

class loginForm(forms.Form):
    username = forms.CharField(max_length=32,label='Username:',required=True)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput,label='Password:',required=True)
