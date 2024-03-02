from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.conf.global_settings import LANGUAGES
from django.db.models import Count
from django.http import JsonResponse, HttpResponse
from authentication.models import BetaUser
from .models import ChatBase, ChatMessages, MGCloudIndex
import random
import json
import requests as r

jsonDecode=json.decoder.JSONDecoder()

#23
#MGCloud Integrations
MGCFILES = 'http://mgcloudapi.pythonanywhere.com/cloud/'


#Source Code
@login_required(login_url='Home/')
def Home(request):
    try: 
        data=ChatBase.objects.filter(Users=request.user.id)
    except ObjectDoesNotExist:
        data=None

    #print(data)
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
        #roomname = request.POST.get('roomname')
        roomname=room.group_name
        roompin = request.POST.get('roompin')
        if room.group_PIN == roompin:
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
    ChatBase.objects.get(id=roomid).delete()
    return redirect('/')
def Profile(request):
    userData=[]
    userData.append(request.user.email)
    userData.append(request.user.Note)
    if request.method=='POST':
        language=request.POST.get('language')
        userObject = BetaUser.objects.filter(username=request.user)
        userObject.update(language_preference=language)
        return render(request,'pages/profile.html', {'languages': LANGUAGES})
    else:
        return render(request,'pages/profile.html', {'languages': LANGUAGES})
def Group_config(request,roomid):
    keywords = ChatBase.objects.get(id=roomid)
    lop = keywords.keyword
    if lop!='':
        keywordList=jsonDecode.decode(lop)
    else:
        keywordList=[]

    try: 
        data=ChatBase.objects.get(id=roomid)
        print(data)
        count = ChatBase.objects.annotate(Count('Users'))
        count = count[0].Users__count
    except ObjectDoesNotExist:
        data=None
    if request.method=='POST':
        keyword = request.POST.get('keyword')
        if keyword=="":
            pass
        else:       
            keywordList.append(keyword)
            data.keyword = json.dumps(keywordList)
            data.save()
            return render(request,'pages/configure.html', {'data':data, 'count':count,'rmusr':data.Users.all(),'keywords': keywordList, 'key1': json.dumps(keywordList)})
    else:
        return render(request,'pages/configure.html', {'data':data, 'count':count,'rmusr':data.Users.all(),'keywords': keywordList, 'key1': json.dumps(keywordList)})
def Remove_User(request,roomid):
    chat = ChatBase.objects.get(id=roomid)
    chat.Users.remove(request.user.id)
    return render(request,'pages/configure.html')
def Remove_Keyword(request,rm_keyword,roomid):
    count = ChatBase.objects.annotate(Count('Users'))
    count = count[0].Users__count
    data = ChatBase.objects.get(id=roomid)
    keywordList = jsonDecode.decode(data.keyword)
    keywordList.remove(rm_keyword)
    data.keyword = json.dumps(keywordList)
    data.save()
    return render(request,'pages/configure.html', {'data':data, 'count':count,'rmusr':data.Users.all(), 'keywords':keywordList})

def Message_Data(request, roomid):
    chat = ChatBase.objects.get(unique_id=roomid)
    chatBlob = []
    messages = ChatMessages.objects.filter(chat_group=chat.id)
    for message in messages:
        chatBlob.append({
            'user': message.user.get_queryset()[0].username, 
            'content': message.content,
            'timestamp': str(message.timestamp)
            })

    #msg_json = serializers.serialize('json', chatBlob)
    return HttpResponse(json.dumps(chatBlob), content_type='application/json') 

@login_required(login_url='/Home')
def joinChatLink(request, roomid):
    try:
        chatobj = ChatBase.objects.get(unique_id=roomid)
        roomid = chatobj.id
    except ObjectDoesNotExist:
        return render(request, 'pages/notfound.html')
    return redirect('/join/'+str(roomid))

def shareFiles(request, roomid):
    try: 
        data=MGCloudIndex.objects.filter(chat_room=roomid)
    except ObjectDoesNotExist:
        data=None
    if request.method == 'POST':
        file = request.FILES.get('file')
        send = r.post(MGCFILES,data={'foreign_key': 23},files={'file':file})
        response = json.loads(send.text)
    
        Store_File = MGCloudIndex.objects.create(
            chat_room = ChatBase.objects.get(id=roomid),
            file_name = str(file),
            MGCID = response.get('id')
        )

        Store_File.user_sent.set([request.user.id])
        Store_File.save()

        return render(request, 'pages/sharefile.html', {'data': data})
            #    if send.status_code==200:

            #         print("File Uploaded Succesfully ", send.text)
            #         self.LB.insert(1,filename)
            #         self.__Files()
    return render(request, 'pages/sharefile.html', {'data': data})





# send = requests.post(up_api,data={'foreign_key':self.ForeignKey},files={'file':file})
#                if send.status_code==200:
#                     messagebox.showinfo('Upload Success!!','File Uploaded to MGCloud')
#                     print("File Uploaded Succesfully ", send.text)
#                     self.LB.insert(1,filename)
#                     self.__Files()