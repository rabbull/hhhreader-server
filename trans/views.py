import json

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from trans.models import Word
from trans.online_dicts import query_from_iciba_and_save
from trans.online_translate_apis import baidu_fanyi_api


def query_word(request, word):
    word = word.lower()
    word_list = Word.objects.filter(word_name__exact=word)
    if word_list.count() == 0:
        try:
            word = query_from_iciba_and_save(word)
        except Word.WordNotFound:
            return HttpResponse(json.dumps({
                'id': -1,
            }))
    else:
        word = word_list.first()
    return HttpResponse(word.as_json())


def connection_test(request):
    return HttpResponse("success")

def query_paragraph(request):
    try:
        paragraph = request.POST['paragraph']
    except KeyError:
        return HttpResponse(json.dumps({
            'status_code': -1,
            'error_message': 'paragraph is empty',
        }))
    try:
        result = baidu_fanyi_api(paragraph)
    except:
        return HttpResponse(json.dumps({
            'status_code': -1,
            'error_message': 'failed to fetch from baidu',
        }))
    return HttpResponse(json.dumps({
        'status_code': 0,
        'apt_result': result,
    }))