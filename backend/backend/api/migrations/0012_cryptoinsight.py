# Generated by Django 5.1.7 on 2025-06-30 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_alter_cryptonews_summary'),
    ]

    operations = [
        migrations.CreateModel(
            name='CryptoInsight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('link', models.URLField(max_length=512)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('source', models.CharField(max_length=255)),
                ('image', models.URLField(blank=True, null=True)),
                ('category', models.CharField(max_length=20)),
            ],
        ),
    ]
