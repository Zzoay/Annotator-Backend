# Generated by Django 3.1.14 on 2022-04-29 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conv_dep', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='utterance',
            name='word_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='utterance',
            unique_together={('utr_id', 'word_id'), ('conv', 'utr_id')},
        ),
    ]