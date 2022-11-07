from django.shortcuts import render
from django.utils import timezone
from .models import Post
import requests
import json
from django.conf import settings
from django.http import HttpResponse

SECRET_SUBWAY_KEY = getattr(settings, 'SECRET_SUBWAY_KEY', None)

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'subwayapp/post_list.html', {'posts': posts})

def matching(request):
    infoInput = request.POST['infoInput']

    if infoInput == "0":
        subwayLineNumber = request.POST['subwayLineNumber']
        trainNumber = request.POST['trainNumber']
        getOffStationName = request.POST['getOffStationName']
        userNickname = request.POST['userNickname']

        fileType = "json"

        idx_start = "0"
        idx_last = "20"

        requestUrl = "http://swopenAPI.seoul.go.kr/api/subway/" + \
                      SECRET_SUBWAY_KEY + "/" + fileType + "/realtimePosition/" + \
                      "/" + idx_start + "/" + idx_last + "/" + subwayLineNumber

        requestData = requests.get(requestUrl)
        jsonData = requestData.json()

        jsonDataList = jsonData["realtimePositionList"]

        stationName = ""

        for data in jsonDataList:
            if trainNumber == data["trainNo"]:
                stationName = data["statnNm"]

        if(stationName == ""):
            return render(request, 'subwayapp/post_list.html', {'arriveTimeSec': "결과가 없습니다"})

        requestUrl = "http://swopenAPI.seoul.go.kr/api/subway/" + \
                      SECRET_SUBWAY_KEY + "/" + fileType + "/realtimeStationArrival/" + \
                      "/" + idx_start + "/" + idx_last + "/" + stationName

        requestData = requests.get(requestUrl)
        jsonData = requestData.json()

        jsonDataList = jsonData["realtimeArrivalList"]

        arriveTimeSec = ""

        for data in jsonDataList:
            if data["btrainNo"] == trainNumber:
                arriveTimeSec = data["barvlDt"]

        if(arriveTimeSec == ""):
            return render(request, 'subwayapp/post_list.html', {'arriveTimeSec': "결과가 없습니다2"})

        return render(request, 'subwayapp/post_list.html', {'arriveTimeSec': arriveTimeSec})

    else:
        return HttpResponse(json.dumps({'arriveTimeSec': arriveTimeSec}, ensure_ascii=False), content_type=u"application/json; charset=utf-8")


