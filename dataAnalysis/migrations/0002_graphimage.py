# Generated by Django 2.2.3 on 2019-09-23 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataAnalysis', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GraphImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imageURL', models.CharField(blank=True, default=None, max_length=1000, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=models.CharField(blank=True, default=None, max_length=1000, null=True))),
            ],
        ),
    ]
