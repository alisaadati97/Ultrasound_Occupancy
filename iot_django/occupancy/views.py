from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import *
import numpy as np

def Kmean(centeroids , Motions_score ):
    points = []
    for i in Motions_score:
        d0 = i - centeroids[0]
        d1 = i - centeroids[1]
        if abs(d0) > abs(d1):
            points.append([i,1])
        elif abs(d0) < abs(d1):
            points.append([i,0])
    return np.array(points)

def Centers(points):
    label0 = points[points[:,1] == 0]
    label1 = points[points[:,1] == 1]
    mean0 = np.mean(label0[:,0])
    mean1 = np.mean(label1[:,0])
    labels = points[:,1]
    centeroids = [mean0 , mean1 ]
    return centeroids , labels


def traindata():
    motion_objs = MotionScore.objects.all()[:100]
    motion_scores = [motion_objs.value for obj in motion_objs]
    centeroids = np.random.uniform(min(motion_scores), high=max(motion_scores), size=(2,))
    centeroids.sort()
    
    epsilon = 0.01
    last_centeroids = centeroids.copy()
    
    while True:
        points = Kmean(centeroids , motion_scores )
        centeroids , labels = Centers(points)
        diff = np.subtract(centeroids,last_centeroids)
        if diff[0] < epsilon and diff[1] < epsilon:
            break
        last_centeroids = centeroids.copy()    
    
    Boundry.objects.create(value = sum(centeroids)/len(centeroids))


def index(request):
    return render(request , 'occupancy/index.html')

@csrf_exempt
def getdata(request):
    value = int(request.POST["MotionScoreValue"])
    MotionScore.objects.create(value=value)
    if len(MotionScore.objects.all()) == 100 :
        traindata()
    
    return HttpResponse('ok')

@csrf_exempt
def senddata(request):
    last_motion_score = MotionScore.objects.all().order_by('-created')[0]
    last_motion_score = last_motion_score.value
    boundry = Boundry.objects.all()[0].value
    if last_motion_score > boundry :
        label = 1
    else:
        label = 0
    print(label)
    return HttpResponse(label)
