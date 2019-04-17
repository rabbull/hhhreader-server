import base64
import datetime
import json

from django.db import models


# Create your models here.
from django.utils import timezone


class Word(models.Model):
    class WordNotFound(BaseException):
        pass

    word_name = models.CharField(max_length=64, unique=True, null=False)
    word_update_time = models.DateTimeField(default=timezone.now)
    word_ph_en = models.CharField(max_length=64, null=True)
    word_ph_am = models.CharField(max_length=64, null=True)
    word_ph_en_mp3 = models.BinaryField()
    word_ph_am_mp3 = models.BinaryField()

    def __str__(self):
        return self.word_name

    def updated_recently(self):
        return self.word_update_time >= timezone.now() - datetime.timedelta(days=32)

    def as_dict(self):
        means = []
        for mean in self.mean_set.all():
            means.append(mean.as_dict())
        ret = {
            'id': self.id,
            'name': self.word_name,
            'ph_en': self.word_ph_en,
            'ph_en_mp3': str(self.word_ph_en_mp3),
            'ph_us': self.word_ph_am,
            'ph_us_mp3': str(self.word_ph_am_mp3),
            'fresh': self.updated_recently(),
            'means': means,
        }
        return ret

    def as_json(self):
        return json.dumps(self.as_dict())


class Mean(models.Model):
    mean_word = models.ForeignKey(Word, on_delete=models.CASCADE)
    # 0 for EN;
    # 1 for CN;
    mean_language = models.IntegerField(default=1)
    mean_part = models.CharField(max_length=64, null=False)
    mean_mean = models.CharField(max_length=1024, null=False)

    def __str__(self):
        return self.mean_mean

    def as_dict(self):
        return {
            'id': self.id,
            'lang': self.mean_language,
            'part': self.mean_part,
            'mean': self.mean_mean,
        }

    def as_json(self):
        return json.dumps(self.as_dict())
