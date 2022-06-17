# Generated by Django 3.1.14 on 2022-06-17 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_auto_20220617_1708'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='process',
            name='item_id',
        ),
        migrations.RemoveField(
            model_name='process',
            name='status',
        ),
        migrations.AddField(
            model_name='process',
            name='assign_num',
            field=models.IntegerField(default=0, verbose_name='分配数量'),
        ),
        migrations.AddField(
            model_name='process',
            name='finished_num',
            field=models.IntegerField(default=0, verbose_name='完成数量'),
        ),
        migrations.CreateModel(
            name='ProcessAssignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.IntegerField(verbose_name='Item ID')),
                ('status', models.IntegerField(default=0, verbose_name='状态')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified at')),
                ('process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.process')),
            ],
            options={
                'db_table': 'annot_process_assignment',
            },
        ),
    ]