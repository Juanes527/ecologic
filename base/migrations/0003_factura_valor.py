# Generated by Django 5.1.6 on 2025-03-02 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_remove_guionhistorial_guion_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='factura',
            name='valor',
            field=models.FloatField(default=0.0),
        ),
    ]
