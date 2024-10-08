# Generated by Django 4.1.7 on 2024-01-18 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_qualityitem_nodetype_alter_qualityitem_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='qualityitem',
            name='graphLeft',
            field=models.IntegerField(null=True, verbose_name='界面图表默认百分比左值区域'),
        ),
        migrations.AddField(
            model_name='qualityitem',
            name='graphRight',
            field=models.IntegerField(null=True, verbose_name='界面图表默认百分比右值区域'),
        ),
    ]
