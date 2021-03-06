# Generated by Django 4.0.3 on 2022-06-28 05:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0002_remove_audited_total_filled_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='audited',
            name='audit_date_from',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='audited',
            name='audit_date_to',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='log_table',
            name='fuel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='fuel', to='offer.fuel'),
        ),
    ]
