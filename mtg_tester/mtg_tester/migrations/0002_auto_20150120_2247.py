# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def add_blank_card(apps, schema_editor):
    Card = apps.get_model("mtg_tester", "Card")
    Card.objects.create(card_name='back_of_card', image='images/back_of_card.jpg')


class Migration(migrations.Migration):

    dependencies = [
        ('mtg_tester', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deck',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DeckCard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.IntegerField()),
                ('card', models.ForeignKey(to='mtg_tester.Card')),
                ('deck', models.ForeignKey(to='mtg_tester.Deck')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='deck',
            name='cards',
            field=models.ManyToManyField(to='mtg_tester.Card', null=True, through='mtg_tester.DeckCard'),
            preserve_default=True,
        ),
        migrations.RunPython(add_blank_card),
    ]
