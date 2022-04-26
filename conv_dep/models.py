from django.db import models

# Create your models here.
class Utterances(models.Model):
    items = models.TextField(max_length=2048) # json


class UtrsIds(models.Model):
    utrsId = models.ForeignKey('Utterances', on_delete=models.CASCADE)


'''
class Convs(models.Model):
    utrId = models.ForeignKey('Utterance', on_delete=models.CASCADE)

class ConvIds(models.Model):
    convId = models.ForeignKey('Conv', on_delete=models.CASCADE)

class Utterances(model.Model):
    wordId = models.

class Words(model.Model):
    word = models.CharField(max_length=128)
    utrId = models.ForeignKey('Utterances', on_delete=models.CASCADE)

class Relations(models.Model):
    convId = models.ForeignKey('Conv', on_delete=models.CASCADE)
    headWordId = model.CharField(max_length=10)
    tailWordId = model.CharField(max_length=10)
    rel = model.CharField(max_length=10)
'''