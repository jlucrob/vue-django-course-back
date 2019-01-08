# Generated by Django 2.1.5 on 2019-01-05 18:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Incident',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000)),
                ('start', models.DateTimeField(auto_now_add=True)),
                ('end', models.DateTimeField(blank=True, null=True)),
                ('solved', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('url', models.URLField()),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Update',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('identified', 'Identified'), ('investigating', 'Investigating'), ('monitoring', 'Monitoring'), ('resolved', 'Resolved')], max_length=20)),
                ('incident', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='incidents.Incident')),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Uptime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('response_time', models.IntegerField()),
                ('status', models.CharField(choices=[('up', 'All is good'), ('issue', 'We are having some issues'), ('down', 'Our website is down')], max_length=10)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='incidents.Site')),
            ],
        ),
        migrations.AddField(
            model_name='incident',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='incidents.Site'),
        ),
    ]