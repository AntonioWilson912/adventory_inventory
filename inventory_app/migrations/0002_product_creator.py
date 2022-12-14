# Generated by Django 2.2.4 on 2022-11-03 20:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
        ('inventory_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='creator',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='product_creators', to='user_app.User'),
            preserve_default=False,
        ),
    ]
