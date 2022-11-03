from django.shortcuts import render
from django.utils import timezone
from .models import Post
import requests
import json

#secret_key = "5a6e7753626361763837624c6f7856"
secret_key = "sample"

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'subwayapp/post_list.html', {'posts': posts})

def matching(request):
    subwayLineNumber = request.POST['subwayLineNumber']
    trainNumber = request.POST['trainNumber']
    getOffStationName = request.POST['getOffStationName']
    userNickname = request.POST['userNickname']

    fileType = "json"

    idx_start = "0"
    idx_last = "5"

    requestUrl = "http://swopenAPI.seoul.go.kr/api/subway/" + \
                  secret_key + "/" + fileType + "/realtimePosition/" + \
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
                  secret_key + "/" + fileType + "/realtimeStationArrival/" + \
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


