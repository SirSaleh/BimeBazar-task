# Generated by Django 4.2.1 on 2024-08-02 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='bookreview',
            constraint=models.CheckConstraint(check=models.Q(('rating__gte', 1), ('rating__lte', 5)), name='rating_range'),
        ),
    ]
