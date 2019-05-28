import json

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from trans import wx
from trans.models import Word, User
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
        'result': result,
    }))


def mark(request, user_openid: str, word: str):
    users = User.objects.filter(user_openid__exact=user_openid)
    if users.count() == 0:
        return HttpResponse(json.dumps({
            'status_code': -1,
            'error_message': 'no such user',
        }))
    user = users.first()

    words = Word.objects.filter(word_name__exact=word)
    if words.count() == 0:
        return HttpResponse(json.dumps({
            'status_code': -1,
            'error_message': 'no such word in database, query first',
        }))
    word = words.first()

    user.user_marks.add(word)
    return HttpResponse(json.dumps({
        'status_code': 0,
        'error_message': 'success',
    }))


def login(request, app_id: str, app_secret: str, js_code: str):
    openid = wx.get_openid(app_id, app_secret, js_code)

    # check if this user has logged-in before
    users = User.objects.filter(user_openid__exact=openid)
    if users.count() == 0:
        new_user = User(user_openid=openid)
        new_user.save()

    return HttpResponse(json.dumps({
        'status_code': 0,
        'error_message': 'success',
        'openid': openid,
    }))
