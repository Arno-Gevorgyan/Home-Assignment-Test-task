# Generated by Django 4.2.7 on 2023-11-12 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExpressionHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expression', models.TextField()),
                ('result', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('SUCCESS', 'Success'), ('FAILED', 'Failed')], default='PENDING', max_length=7)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('evaluated_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]