## 这是一个小型账户系统,包含密码找回

## 简单的使用方法


创建虚拟环境
使用pip安装第三方依赖
修改settings.example.py 文件为 settings.py
运行migrate命令，创建数据库和数据表
运行python manage.py runserver启动服务器

路由设置：


from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', include('login.urls')),
    path('captcha/',include('captcha.urls')),
    path('',include('login.urls')),
]