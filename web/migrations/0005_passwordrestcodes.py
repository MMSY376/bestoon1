# Generated by Django 3.1.2 on 2020-10-13 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='Passwordrestcodes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=32)),
                ('email', models.CharField(max_length=120)),
                ('time', models.DateTimeField()),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
    ]
