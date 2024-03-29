# Generated by Django 4.0.3 on 2022-12-15 17:10

from django.conf import settings
import django.core.validators
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
            name='ShopSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reservation_function_using', models.BooleanField(default=True)),
                ('approval_system', models.BooleanField(default=True)),
                ('one_hour_max_reservation', models.IntegerField(default=2)),
                ('max_visits_count', models.IntegerField(default=10)),
                ('reservation_shortest_reception_hours', models.IntegerField(default=3, validators=[django.core.validators.MinValueValidator(1)])),
                ('reservation_longest_reception_hours', models.IntegerField(default=240, validators=[django.core.validators.MinValueValidator(48)])),
                ('first_reservation_releasing_time', models.IntegerField(default=9)),
                ('last_reservation_releasing_time', models.IntegerField(default=19)),
                ('shop', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Manage.shop')),
            ],
        ),
        migrations.CreateModel(
            name='Reserve',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('reservation_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('staff_publication', models.BooleanField(default=False)),
                ('reserve_num', models.IntegerField(default=1)),
                ('reserver_id', models.IntegerField(default=1)),
                ('reserver_account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('shop', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Manage.shop')),
            ],
        ),
        migrations.AddConstraint(
            model_name='shopsetting',
            constraint=models.UniqueConstraint(fields=('shop',), name='shop_setting_unique'),
        ),
    ]
