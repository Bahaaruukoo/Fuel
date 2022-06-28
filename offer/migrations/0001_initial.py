# Generated by Django 4.0.3 on 2022-06-26 11:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Audited',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('total_filled', models.IntegerField()),
                ('total_money', models.DecimalField(decimal_places=2, max_digits=12)),
            ],
        ),
        migrations.CreateModel(
            name='Compensation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_compensated', models.IntegerField()),
                ('total_money', models.DecimalField(decimal_places=2, max_digits=12)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('money_reciever', models.TextField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Gas_offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_number', models.CharField(blank=True, max_length=20)),
                ('plate_number', models.CharField(blank=True, max_length=10)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('permited_amount', models.IntegerField()),
                ('qr_code', models.CharField(blank=True, max_length=20)),
                ('status', models.BooleanField(default=True)),
                ('added_by', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Gasstation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('location', models.CharField(max_length=120)),
                ('identifier', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='log_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('filled_amount', models.IntegerField()),
                ('over_draw', models.IntegerField(default=0, null=True)),
                ('dailyBalanceDone', models.BooleanField(default=False, null=True)),
                ('audited', models.ForeignKey(default=0, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='offer.audited')),
                ('compensated', models.ForeignKey(default=0, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='offer.compensation')),
                ('gasstation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='offer.gasstation')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='offer.gas_offer')),
            ],
        ),
        migrations.CreateModel(
            name='DailyUsage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('used_amount', models.IntegerField()),
                ('left_amount', models.IntegerField()),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='offer.gas_offer')),
            ],
        ),
        migrations.AddField(
            model_name='compensation',
            name='gasstation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='offer.gasstation'),
        ),
        migrations.AddField(
            model_name='compensation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='audited',
            name='gasstation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='gasstation', to='offer.gasstation'),
        ),
        migrations.AddField(
            model_name='audited',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='auditor', to=settings.AUTH_USER_MODEL),
        ),
    ]
