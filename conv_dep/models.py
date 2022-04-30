from django.db import models


# 对话表
class Conv(models.Model):
    conv_id = models.BigIntegerField(primary_key=True)


# 句子表，将词语信息也加入其中，减少外键依赖，通过程序进行约束
class Utterance(models.Model):
    conv = models.ForeignKey('Conv', on_delete=models.CASCADE)
    utr_id = models.IntegerField()  # 相对于对话的句子编号
    word_id = models.IntegerField() # 相对于句子的单词编号
    word = models.CharField(max_length=64)

    class Meta:
        ordering = ['utr_id', 'word_id']
        unique_together = [['conv', 'utr_id', 'word_id']]

    def __str__(self):
        return f"对话ID: {self.conv.conv_id}; 话语ID: {self.utr_id}; 词: {self.word} "


# 将词汇和句子关联
# class Utr_Word(models.Model):
#     utr = models.ForeignKey('Utterance', on_delete=models.CASCADE)
#     word = models.ForeignKey('Word', on_delete=models.CASCADE)

#     def __str__(self):
#         return f"对话ID: {self.utr.conv.convId}; 话语ID: {self.utr.id}; 词: {self.word.word} "


# 词表
class Word(models.Model):
    word = models.CharField(max_length=64, unique=True)  # 词表中没有重复，减少容量

    def __str__(self):
        return f"ID: {self.id}; 词: {self.word}"


# 关系表
class Relation(models.Model):
    name = models.CharField(max_length=10)
    color = models.CharField(max_length=8)

    def __str__(self):
        return self.name


# 关系三元组表
class Relationship(models.Model):
    conv = models.ForeignKey('Conv', on_delete=models.CASCADE)
    relation = models.ForeignKey('Relation', on_delete=models.CASCADE)
    head = models.ForeignKey('Word', on_delete=models.CASCADE, related_name='head_rel')
    tail = models.ForeignKey('Word', on_delete=models.CASCADE, related_name='tail_rel')

    def __str__(self):
        return f"对话: {self.conv.conv_id}; 关系: {self.head.word}---{self.relation.name}-->{self.tail.word}"
