import json

import requests

from trans.models import Word


def query_from_iciba_and_save(word: str):
    key = '72BA1B55C1DD18AA0C64FD68C99434C1'
    url_prefix = 'http://dict-co.iciba.com/api/dictionary.php?type=json&key=' + key + '&w='
    response = requests.get(url_prefix + word).json()
    try:
        word = Word(
            word_name=response['word_name'],
            word_ph_en=response['symbols'][0]['ph_en'],
            word_ph_en_mp3=requests.get(response['symbols'][0]['ph_en_mp3']).content
            if len(response['symbols'][0]['ph_en_mp3']) > 0 else '',
            word_ph_am=response['symbols'][0]['ph_am'],
            word_ph_am_mp3=requests.get(response['symbols'][0]['ph_am_mp3']).content
            if len(response['symbols'][0]['ph_am_mp3']) > 0 else '',
        )
    except KeyError:
        raise Word.WordNotFound()
    word.save()
    for mean in response['symbols'][0]['parts']:
        mean_mean = mean['means'][0]
        for m in mean['means'][1:]:
            mean_mean += ', '
            mean_mean += m
        word.mean_set.create(
            mean_language=1,
            mean_part=mean['part'],
            mean_mean=mean_mean,
        )
    return word
