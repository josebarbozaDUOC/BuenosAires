# Generated by Django 4.2.1 on 2023-07-02 20:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_perfilusuario_tipousu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='idprod',
            field=models.ForeignKey(db_column='idprod', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.producto'),
        ),
    ]
