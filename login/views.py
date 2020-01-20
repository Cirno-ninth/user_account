from django.shortcuts import render
from django.shortcuts import redirect
from . import forms
from . import models
import hashlib
import datetime
import random
from django.conf import settings

# Create your views here.
def index(request):
    if not request.session.get('is_login', None):
        return redirect('/login/login/')
    return render(request, 'login/index.html')

def login(request):
    if request.session.get('is_login', None): #不允许重复登录
        return redirect('/login/index/')

    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            try:
                user = models.User.objects.get(name = username)
            except:
                message = '用户不存在！'
                return render(request, 'login/login.html', locals())
            
            if not user.has_confirmed:
                message = '用户还未进行邮件确认，请前往邮箱查看邮件'
                return render(request, 'login/login.html', locals())
            if user.password == hashcode(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/login/index/')
            else:
                message = '密码错误!'
                return render(request, 'login/login.html', locals())
        else:
            return render(request, 'login/login.html', locals())
    login_form = forms.UserForm()
    return render(request, 'login/login.html', locals())

def email_login(request):
    if request.session.get('is_login', None):
        return redirect('/login/index/')
    if request.method == "POST":
        login_form = forms.EUserForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():
            email = login_form.cleaned_data.get('email')
            password = login_form.cleaned_data.get('password')

            try:
                user = models.User.objects.get(email = email)
            except:
                message = '用户不存在！'
                return render(request, 'login/email_login.html', locals())
            if user.password == hashcode(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/login/index/')
            else:
                message = '密码错误！'
                return render(request, 'login/email_login.html', locals())
        else:
            return render(request, 'login/email_login.html', locals())
    login_form = forms.EUserForm()
    return render(request, 'login/email_login.html', locals())

def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/login/login/')
    request.session.flush()
    return redirect('/login/login/')

def register(request):
    if request.session.get('is_login', None):
        return redirect('/login/index/')
    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = '请检查填写的内容！'
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            
            if password1 != password2:
                message = '两次输入的密码不一致！'
            else:
                same_name_user = models.User.objects.filter(name = username)
                if same_name_user:
                    message = '用户名已存在！'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email = email)
                if same_email_user:
                    message = '该邮箱已被注册！'
                    return render(request, 'login/register.html', locals())

                id = random.randint(100000,199999) + random.randint(0,9999)
                
                new_user = models.User()
                new_user.name = username
                new_user.password = hashcode(password1)
                new_user.email = email
                try:
                    new_user.uid = id
                    new_user.save()
                except:
                    new_user.uid = id + random.randint(id,id*2)
                    new_user.save()

                code = make_confirm_code(new_user)
                send_mail(email, code)

                message = '请前往邮箱进行确认！'
                return render(request, 'login/confirm.html', locals())
        else:
            return render(request, 'login/register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())

def hashcode(s, salt='cirnovip'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()

def make_confirm_code(user):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    code = hashcode(user.name, now)
    models.ConfirmString.objects.create(code=code,user=user)
    return code


def send_mail(email,code):
    from django.core.mail import EmailMultiAlternatives

    subject = '来自www.cirno.vip的注册确认邮件'
    text_content = '''感谢注册www.cirno.vip，如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系网站管理员'''
    html_content = '''
                      <p><a href="http://{}/login/confirm/?code={}" target=blank>感谢注册www.cirno.vip</a></p>
                      <p>请点击站点链接完成注册确认！</p>
                      <p>此链接有效期为{}天！</p>
                      '''.format('127.0.0.1:8080', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_email_for_password(email,code):
    #忘记密码确认邮件
    from django.core.mail import EmailMultiAlternatives

    subject = '来自www.cirno.vip的修改密码验证邮件'
    text_content = '''
                    <p>此邮件为忘记密码的修改确认邮件，若不是本人操作，可能你的密码已泄露，请尽快修改密码。</p>
                    <p>请复制以下链接进入修改密码页面</p>
                    <p>http://{}/login/forgot_password/?code={}</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8080', code, '1')
    html_content = '''
                      <p><a href="http://{}/login/forgot_password/?code={}" target=blank>请点击这里进入修改密码页面,此邮件为忘记密码的修改确认邮件，若不是本人操作，可能你的密码已泄露，请尽快修改密码。</a></p>
                      <p>请点击站点链接完成密码修改！</p>
                      <p>此链接有效期为{}天！</p>
                      '''.format('127.0.0.1:8080', code, '1')
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()



def user_confirm(request):
    code = request.GET.get('code', None)
    message = ' '
    try:
        confirm = models.ConfirmString.objects.get(code = code)
    except:
        message = '无效的确认请求!'
        return render(request, 'login/confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '注册码已过期！'
        return render(request, 'login/register.html' , locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录'
        return render(request, 'login/confirm.html', locals())

def forgot_password(request):
    #忘记密码处理页面
    if request.method == "POST":
        forgot_password_form = forms.ForgotPForm(request.POST)
        message = '请检查填写的内容！'
        if forgot_password_form.is_valid():
            email = forgot_password_form.cleaned_data.get('email')

            try:
                user = models.User.objects.get(email = email)
            except:
                message = '用户不存在！'
                return render(request, 'login/forgot_password.html', locals())

            try:
                code = make_confirm_code(user)
                send_email_for_password(email, code)
            except:
                message = '用户还未进行邮件确认！'
                return render(request, 'login/forgot_password.html', locals())

            message = '请前往邮箱进行确认！'
            return render(request, 'login/forgot_password.html', locals())
    code = request.GET.get('code', None)
    if code:
        message = ' '
        try:
            confirm = models.ConfirmString.objects.get(code = code)
            set_password_form = forms.SetPasswordForm()
        except:
            message = '无效的确认请求！'
            return render(request, 'login/forgot_password.html', locals())

        c_time = confirm.c_time
        now = datetime.datetime.now()
        if now > c_time + datetime.timedelta(1):
            confirm.delete()
            message = '验证信息已过期！'
            return render(request, 'login/forgot_password.html', locals())
        else:
            return render(request, 'login/set_password.html', locals())


    forgot_password_form = forms.ForgotPForm()
    return render(request, 'login/forgot_password.html', locals())

def set_password(request):
    #忘记密码设置密码页面
    if request.method == "POST":
        set_password_form = forms.SetPasswordForm(request.POST)
        message = '请检查填写的内容！'
        code = request.POST.get('code')
        if set_password_form.is_valid():
            password1 = set_password_form.cleaned_data.get('password1')
            password2 = set_password_form.cleaned_data.get('password2')

            if password1 != password2:
                message = '两次输入的密码不一致！'
                return render(request, 'login/set_password.html', locals())
            else:
                try:
                    confirm = models.ConfirmString.objects.get(code = code)
                except:
                    message = '验证信息失效！'
                    return render(request, 'login/set_password.html', locals())
                confirm.user.password = hashcode(password1)
                confirm.user.save()
                confirm.delete()
                request.session.flush()
                message = '修改成功，请使用新密码登录!'
                login_form = forms.UserForm()
                return render(request, 'login/login.html', locals())
        return render(request, 'login/set_password.html', locals())
    set_password_form = forms.SetPasswordForm()
    return render(request, 'login/set_password.html', locals())

                