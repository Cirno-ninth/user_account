from django import forms
from captcha.fields import CaptchaField

class UserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=128, widget=forms.TextInput(attrs={'class':'form-control', 'autofocus':' '}))
    password = forms.CharField(label='密码', max_length=256, widget=forms.PasswordInput(attrs={'class':'form-control'}))
    captcha  = CaptchaField(label='验证码')

class EUserForm(forms.Form):
    email = forms.CharField(label="邮箱", widget=forms.EmailInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='密码', max_length=256, widget=forms.PasswordInput(attrs={'class':'form-control'}))
    captcha  = CaptchaField(label='验证码')

class ForgotPForm(forms.Form):
    #忘记密码处理表单
    email = forms.CharField(label='邮箱', widget=forms.EmailInput(attrs={'class':'form-control'}))
    captcha = CaptchaField(label='验证码')

class SetPasswordForm(forms.Form):
    #忘记密码修改密码表单
    password1 = forms.CharField(label='密码', max_length=256, widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='确认密码', max_length=256, widget=forms.PasswordInput(attrs={'class':'form-control'}))
    captcha = CaptchaField(label='验证码')

class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=128, widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='密码', max_length=256, widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='确认密码', max_length=256, widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label='邮箱', widget=forms.EmailInput(attrs={'class':'form-control'}))
    captcha = CaptchaField(label='验证码')
    