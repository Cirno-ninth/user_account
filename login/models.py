from django.db import models
import uuid

# Create your models here.
class User(models.Model):
    objects = models.Manager()

    uid = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email    = models.EmailField(unique=True)
    c_time   = models.DateTimeField(auto_now=True)  #注册时间
    has_confirmed = models.BooleanField(default=False) #是否经过邮件确认

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'

class UserInfo(User):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    head_img = models.ImageField( '头像', upload_to='head_img') #头像
    article_num = models.PositiveIntegerField() #发帖数
    info     = models.CharField(max_length=128) #简介
    sex      = models.CharField(max_length=32, choices=gender, default="男")

    
class UserTags(models.Model):
    # 用户标签
    tag =  models.ManyToManyField(
        'User',
        related_name='UserTag',
        related_query_name= 'UserTag',
    )

class Fans(models.Model):
    #粉丝，关注
    fans = models.ManyToManyField(
        'User',
        related_name= 'fans',
        related_query_name= 'fans',
    )

class ConfirmString(models.Model):
    # 注册码
    code = models.CharField(max_length=256)
    user = models.OneToOneField('User', on_delete= models.CASCADE)
    c_time = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.user.name + ': ' +self.code

    class Meta:
        ordering = ['-c_time']
        verbose_name = '确认码'
        verbose_name_plural = '确认码'
    



