# Generated by Django 2.2.7 on 2020-04-20 14:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0003_delete_reply'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='parent_id',
        ),
        migrations.AddField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='comment.Comment'),
        ),
    ]