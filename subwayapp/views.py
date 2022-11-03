from django.shortcuts import render

def post_list(request):
    return render(request, 'subwayapp/post_list.html', {})