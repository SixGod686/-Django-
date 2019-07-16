# Create your models here.
from django.db import models




# 用户个人信息表
class User(models.Model):
    icon = models.ImageField(upload_to='headimages',null=True,blank=True)
    username = models.CharField(verbose_name='用户名', max_length=32)
    nickname = models.CharField(verbose_name='昵称', max_length=32)
    sex = models.BooleanField(verbose_name='性别', default=True)
    password = models.CharField(verbose_name='密码', max_length=32)
    phone = models.CharField(verbose_name='手机号', max_length=32)
    birthday = models.DateField(verbose_name='生日')
    token = models.CharField(max_length=256)

    class Meta:
        verbose_name_plural = '用户'
        # 重命名表格名字
        db_table = 'user'

    # 默认返回用户名和昵称，减少数据库压力
    def __str__(self):
        return self.username, self.nickname


# 收藏地点
class Site(models.Model):
    site = models.CharField(verbose_name='收藏地点', max_length=256,default=None)
    s_user = models.ForeignKey(User,verbose_name='用户')

    class Meta:
        verbose_name_plural = '收藏地点'
        # 重命名表格名字
        db_table = 'site'


# 收藏路线
class Collect(models.Model):
    line_origin = models.CharField(verbose_name='收藏路线起点',max_length=256,default=None)
    line_destination = models.CharField(verbose_name='收藏路线终点',max_length=256,default=None)
    c_user = models.ForeignKey(User,verbose_name='用户')

    class Meta:
        verbose_name_plural = '收藏路线'
        # 重命名表格名字
        db_table = 'collect'
