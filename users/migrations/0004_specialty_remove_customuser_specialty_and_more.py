# Generated by Django 5.1.6 on 2025-03-04 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_customuser_specialty'),
    ]

    operations = [
        migrations.CreateModel(
            name='Specialty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='specialty',
        ),
        migrations.AddField(
            model_name='customuser',
            name='specialties',
            field=models.ManyToManyField(blank=True, to='users.specialty'),
        ),
    ]
