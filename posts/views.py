from django.shortcuts import render
from django.http import HttpResponse
from posts.models import News
import requests
from bs4 import BeautifulSoup
import datetime
import json

# Create your views here.
def index(request):
    counts =  News.objects.all()
    news = News.objects.all()[:30]
    titles = tuple(x.title for x in news)
    request_hackernews(news, titles)
    params = ['offset', 'limit', 'order', 'title', 'url', 'created']
    min_limits = 30
    offset = 0
    for k, v in request.GET.items():
        if k in params:
            if k == params[0]:
                if v.isdigit() == True:
                    if int(v) < min_limits:
                        offset = int(v)
                    else:
                        offset = 0
                else:
                    offset = 0
            elif k == params[1]:
                if v.isdigit() == True:
                    if int(v) < min_limits:
                        limits = int(v)
                    else:
                        limits = min_limits
                else:
                    limits = min_limits
            elif k == params[2]:
                if v in params:
                    order = v
    if 'order' not in locals():
        news = News.objects.all()[offset:limits]
    else:
        news = News.objects.order_by(order)[offset:limits]
    json_news = []
    for index, x in enumerate(news):
        elem = x.__dict__
        del elem['_state']
        json_news.append(elem)
    return HttpResponse(json.dumps(json_news))


def request_hackernews(news, titles):
    response = requests.get('https://news.ycombinator.com/newest', headers={'Connection': 'close'})
    soup = BeautifulSoup(response.text, "html.parser")
    data = soup.find_all('tr', class_='athing')
    for index, el in enumerate(data):
        soup_content = el.find('a', class_='storylink')
        if soup_content.text not in titles:
            try:
                news[index].title = soup_content.text
                news[index].url = soup_content.get('href')
                news[index].created = datetime.datetime.now().isoformat()
                news[index].save()
            except IndexError:
                b = News(title = soup_content.text, url = soup_content.get('href'), created = datetime.datetime.now().isoformat())
                b.save()

