# Generated by Django 4.0.5 on 2022-07-28 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('overflow', '0004_alter_answer_date_alter_commentsa_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='ans_verified',
            field=models.BooleanField(default=False),
        ),
    ]