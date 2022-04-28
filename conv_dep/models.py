from django.db import models


# 对话表
class Conv(models.Model):
    convId = models.BigIntegerField(primary_key=True)


# 句子表
class Utterance(models.Model):
    conv = models.ForeignKey('Conv', on_delete=models.CASCADE)


# 将词汇和句子关联
class Utr_Word(models.Model):
    utr = models.ForeignKey('Utterance', on_delete=models.CASCADE)
    word = models.ForeignKey('Word', on_delete=models.CASCADE)

    def __str__(self):
        return f"第{self.utr.conv.convId}个对话，第{self.utr.id}句话：{self.word.word} "


# 词表
class Word(models.Model):
    word = models.CharField(max_length=64)

    def __str__(self):
        return self.word


# 关系表
class Relation(models.Model):
    name = models.CharField(max_length=10)
    color = models.CharField(max_length=8)

    def __str__(self):
        return self.name


# 关系三元组表
class Relationship(models.Model):
    relation = models.ForeignKey('Relation', on_delete=models.CASCADE)
    head = models.ForeignKey('Word', on_delete=models.CASCADE, related_name='head_rel')
    tail = models.ForeignKey('Word', on_delete=models.CASCADE, related_name='tail_rel')

    def __str__(self):
        return f"{self.head.word}---{self.relation.name}-->{self.tail.word}"
