# Generated by Django 5.2.1 on 2025-05-18 11:46

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='payment',
            name='currency',
            field=models.CharField(default='PLN', max_length=10),
        ),
        migrations.AlterField(
            model_name='payment',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('paid', 'Paid'), ('unpaid', 'Unpaid')], default='unpaid', max_length=20),
        ),
        migrations.AlterField(
            model_name='payment',
            name='visit_id',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
