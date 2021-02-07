# Generated by Django 3.1.5 on 2021-02-07 01:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uapapp_ms', '0006_auto_20210202_0653'),
    ]

    operations = [
        migrations.CreateModel(
            name='Period',
            fields=[
                ('code', models.IntegerField(primary_key=True, serialize=False, verbose_name='Codigo')),
                ('text', models.CharField(max_length=10, verbose_name='Texto')),
            ],
        ),
        migrations.AddField(
            model_name='report',
            name='periods',
            field=models.ManyToManyField(to='uapapp_ms.Period'),
        ),
    ]
