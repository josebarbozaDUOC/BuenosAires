# Generated by Django 4.2.1 on 2023-07-07 01:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_factura_idprod'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='descfac',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
