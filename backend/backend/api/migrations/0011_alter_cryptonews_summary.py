# Generated by Django 5.1.7 on 2025-06-28 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_cryptonews_summary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cryptonews',
            name='summary',
            field=models.TextField(blank=True, null=True),
        ),
    ]
