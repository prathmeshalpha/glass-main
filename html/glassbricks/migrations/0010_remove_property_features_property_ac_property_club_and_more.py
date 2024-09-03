# Generated by Django 4.2.10 on 2024-09-03 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glassbricks', '0009_remove_propertyvideo_property_remove_property_video_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='features',
        ),
        migrations.AddField(
            model_name='property',
            name='ac',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='property',
            name='club',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='property',
            name='elevator',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='property',
            name='gym',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='property',
            name='parking',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='property',
            name='pool',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='property',
            name='powerbackup',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='property',
            name='security',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='property',
            name='wifi',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='property',
            name='specific_type1',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='specific_type2',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
