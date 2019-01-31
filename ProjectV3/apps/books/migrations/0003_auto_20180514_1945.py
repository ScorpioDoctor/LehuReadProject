# Generated by Django 2.0.2 on 2018-05-14 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20180513_1814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='wordcount',
            field=models.IntegerField(default=0, null=True, verbose_name='文章字数'),
        ),
        migrations.AlterField(
            model_name='book',
            name='wordcount',
            field=models.IntegerField(default=0, null=True, verbose_name='总字数'),
        ),
        migrations.AlterField(
            model_name='chapter',
            name='wordcount',
            field=models.IntegerField(default=0, null=True, verbose_name='章节字数'),
        ),
    ]
