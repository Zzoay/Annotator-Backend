
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
    nickname = models.CharField('昵称', null=True, blank=True, max_length=200)
    
    class Meta(AbstractUser.Meta):
        db_table = 'annot_user'
        swappable = 'AUTH_USER_MODEL'