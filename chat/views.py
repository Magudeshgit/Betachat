from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .models import ChatBase
import random

# Create your views here.

@login_required(login_url='Home/')
def Home(request):
    try: 
        data=ChatBase.objects.filter(Users=request.user.id)
    except ObjectDoesNotExist:
        data=None

    print(data)
    return render(request, 'pages/main.html',{'data': data})

@login_required(login_url='Home/')
def Searchops(request):
    if request.method == 'POST':
        searchquery = request.POST.get('searchquery').strip()
        searchitems = ChatBase.objects.filter(unique_id=searchquery)
        print(searchquery, searchitems)
        if not searchitems:
            return render(request, 'pages/search.html', {'Data': "NRF"})
        else:
            return render(request, 'pages/search.html', {'Data': searchitems})
    return render(request, 'pages/search.html' )

def JoinRoom(request, roomid):
    room = ChatBase.objects.get(id=roomid)
    if request.method ==  'POST':
        roomname = request.POST.get('roomname')
        roompin = request.POST.get('roompin')
        if room.group_name == roomname and room.group_PIN == roompin:
            room.Users.add(request.user)
            return redirect('/')
        else:
            return redirect(f'/join/{roomid}')
    else:
        roomusers = room.Users.all()
        USERPRESENT = False
        for rms in roomusers:
            if request.user == rms.username:
                USERPRESENT = True
        if USERPRESENT:
            print('already autheticated')
            return redirect('/')
        else:
            print('auth')
            return render(request, 'pages/roomauth.html', {'roomname': room.group_name, 'room_desc': room.group_description})
        
def CreateRoom(request):
    if request.method == 'POST':
        roomname=request.POST.get('roomname').strip()
        roomdesc=request.POST.get('description').strip()
        pin1, pin2 = request.POST.get('pin1').strip(), request.POST.get('pin2').strip()
        if pin1 != pin2:
            return render(request, 'pages/createroom.html', {'error': 'Both the passwords should be same'})
        else:
            uid = str(random.randint(111111111,999999999))
            unique_id=uid[:3]+'-'+uid[3:6]+'-'+uid[6:9]
            room = ChatBase.objects.create(
                unique_id=unique_id,
                group_name=roomname,
                group_admin=request.user,
                group_description=roomdesc,
                group_PIN=pin2
            )
            room.Users.set([request.user.id])
            print('room in db created')
            return redirect('/')
    return render(request, 'pages/createroom.html')

def RemoveRoom(request, roomid):
    item = ChatBase.objects.get(id=roomid)
    item.Users.remove(request.user)
    return redirect('/')
    
def DeleteRoom(request, roomid):
    item = ChatBase.objects.get(id=roomid).delete()
    return redirect('/')