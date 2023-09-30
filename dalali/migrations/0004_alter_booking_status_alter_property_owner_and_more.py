# Generated by Django 4.1.10 on 2023-09-26 05:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dalali', '0003_alter_propertyphoto_property'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.IntegerField(blank=True, choices=[(1, 'Pending'), (2, 'Confirmed'), (3, 'Terminated')], default=1, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dalali.userprofile'),
        ),
        migrations.AlterField(
            model_name='propertyamenity',
            name='property',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='amenities', to='dalali.property'),
        ),
        migrations.AlterField(
            model_name='propertyphoto',
            name='url',
            field=models.FileField(blank=True, null=True, upload_to='images/%Y/%m/%d'),
        ),
    ]