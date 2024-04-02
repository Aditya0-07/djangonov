# Generated by Django 5.0.3 on 2024-03-20 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('desc', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='categories')),
            ],
        ),
        migrations.DeleteModel(
            name='Items',
        ),
    ]
