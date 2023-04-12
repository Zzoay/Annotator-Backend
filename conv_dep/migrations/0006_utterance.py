# Generated by Django 3.1.14 on 2022-08-01 06:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('conv_dep', '0005_delete_utterance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Utterance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('utr_id', models.IntegerField()),
                ('word_id', models.IntegerField()),
                ('word', models.CharField(max_length=64)),
                ('conv', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conv_dep.conv')),
            ],
            options={
                'ordering': ['conv', 'utr_id', 'word_id'],
                'unique_together': {('conv', 'utr_id', 'word_id')},
            },
        ),
    ]
