
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class AbstractBaseModel(models.Model):
    # creator = models.IntegerField('creator', null=True)
    created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True)

    # modifier = models.IntegerField('modifier', null=True)
    modified_at = models.DateTimeField(verbose_name='Modified at', auto_now=True)

    class Meta:
        abstract = True
    

class User(AbstractUser, AbstractBaseModel):
    nickname = models.CharField('昵称', null=True, blank=True, max_length=20)
    
    class Meta(AbstractUser.Meta):
        db_table = 'annot_user'
        swappable = 'AUTH_USER_MODEL'


# 任务表（定义任务）
class Task(models.Model):
    name = models.CharField('任务名称', max_length=30)
    description = models.TextField('任务描述', max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name='Modified at', auto_now=True)

    class Meta:
        db_table = 'annot_task'


# 进程表（子任务）
class Process(models.Model):
    task = models.ForeignKey('Task', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    assign_num = models.IntegerField('分配数量', default=0)
    finished_num = models.IntegerField('完成数量', default=0)
    created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name='Modified at', auto_now=True)

    class Meta:
        db_table = 'annot_process'


# 进程分配
class ProcessAssignment(models.Model):
    process = models.ForeignKey('Process', on_delete=models.CASCADE)
    item_id = models.IntegerField(verbose_name='Item ID')   # 根据标注粒度，比如对话标注中第N个对话的id
    status = models.IntegerField('状态', default=0)   # 单个标注任务的状态，0: 初始化, 1: 已开始, 2: 已完成, 3: 已取消, 4: 保留
    created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name='Modified at', auto_now=True)

    class Meta:
        db_table = 'annot_process_assignment'