# Generated by Django 3.1.14 on 2022-06-22 11:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Conv',
            fields=[
                ('conv_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('status', models.IntegerField(default=0)),
                ('set', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='Relation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('color', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=64, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Relationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('head', models.CharField(max_length=8)),
                ('tail', models.CharField(max_length=8)),
                ('conv', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conv_dep.conv')),
                ('relation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conv_dep.relation')),
            ],
        ),
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
