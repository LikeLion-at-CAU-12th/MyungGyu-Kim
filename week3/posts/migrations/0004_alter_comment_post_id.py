# Generated by Django 5.0.3 on 2024-04-01 12:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0003_alter_comment_writer_alter_post_writer"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="post_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="posts.post",
                verbose_name="포스트ID",
            ),
        ),
    ]