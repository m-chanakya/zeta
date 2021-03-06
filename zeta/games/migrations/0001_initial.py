# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-09 11:18
from __future__ import unicode_literals

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
            name='CardBet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_of_tickets', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='CardCell',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suit', models.CharField(choices=[('C', 'Clubs'), ('S', 'Spades'), ('D', 'Diamonds'), ('H', 'Hearts')], max_length=1)),
                ('value', models.CharField(choices=[('J', 'Jack'), ('Q', 'Queen'), ('K', 'King')], max_length=1)),
                ('group', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C')], max_length=1)),
                ('total_bets', models.PositiveIntegerField(default=0)),
                ('winner', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Cards',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_cost', models.PositiveIntegerField(default=10)),
                ('winner_prize', models.PositiveIntegerField(default=100)),
                ('is_result_generated', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TileBet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_of_tickets', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TileCell',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suit', models.CharField(choices=[('A', 'A'), ('B', 'B')], max_length=1)),
                ('value', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=1)),
                ('group', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C')], max_length=1)),
                ('total_bets', models.PositiveIntegerField(default=0)),
                ('winner', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Tiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_cost', models.PositiveIntegerField(default=10)),
                ('winner_prize', models.PositiveIntegerField(default=100)),
                ('is_result_generated', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='tilecell',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cells', to='games.Tiles'),
        ),
        migrations.AddField(
            model_name='tilebet',
            name='cell',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.TileCell'),
        ),
        migrations.AddField(
            model_name='tilebet',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cardcell',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cells', to='games.Cards'),
        ),
        migrations.AddField(
            model_name='cardbet',
            name='cell',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.CardCell'),
        ),
        migrations.AddField(
            model_name='cardbet',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='tilecell',
            unique_together=set([('game', 'suit', 'value', 'group')]),
        ),
        migrations.AlterUniqueTogether(
            name='cardcell',
            unique_together=set([('game', 'suit', 'value', 'group')]),
        ),
    ]
