# Generated by Django 4.0.3 on 2022-12-15 17:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Manage', '0003_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(default='お客', max_length=20)),
                ('status', models.BooleanField(default=True)),
                ('total_fee', models.FloatField(default=0)),
                ('account_coordination', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('room', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Manage.room')),
                ('shop', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Manage.shop')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(blank=True, default=False)),
                ('cook_status', models.BooleanField(blank=True, default=False)),
                ('count', models.IntegerField(default=1)),
                ('amount', models.FloatField(default=100)),
                ('order_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('option', models.JSONField(blank=True, null=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Customer.customer')),
                ('menu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Manage.menu')),
            ],
        ),
        migrations.CreateModel(
            name='OrderConclusion',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('orders', models.ManyToManyField(blank=True, to='Customer.order')),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=1)),
                ('amount', models.FloatField(blank=True)),
                ('option', models.JSONField(blank=True, null=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Customer.customer')),
                ('menu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Manage.menu')),
            ],
        ),
    ]
