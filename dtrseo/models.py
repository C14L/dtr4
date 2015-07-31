# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models

IMPORT_BOARDS_NEWBS = (
        ('l', 'El Ligue'),
        ('k', 'Internet'),
        ('o', 'Videojuegos'),
        ('p', 'Gente del Ligue'),
        ('q', 'Fakes'),
        ('r', 'Chistoso'),
        ('a', 'Universidades'),
        ('d', 'deReventon'),
        ('e', 'Platicar'),
        ('b', 'Mujeres y Hombres'),
        ('c', 'Amistad'),
        ('f', 'Deportes'),
        ('g', 'Literatura'),
        ('h', 'Politica y Religion'),
        ('i', 'Peliculas'),
        ('j', 'Musica'),
        ('s', 'Interesante'),
        ('t', 'Erotico'),
        ('u', 'dEbRaYeS lOcOs'),
        ('z', 'Moderadores'), )

class OldThread(models.Model):
    # ID is the same as the pk in "dtrforum.models.Post".
    old_threadid = models.PositiveIntegerField()
    old_topicid = models.CharField(max_length=1)
