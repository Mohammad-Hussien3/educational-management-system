# Generated by Django 5.0 on 2024-08-28 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctorId', models.IntegerField()),
                ('questions', models.JSONField(default=list)),
                ('degrees', models.JSONField(default=list)),
                ('answers', models.JSONField(default=list)),
            ],
        ),
    ]
