from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

import chat.views as chat
import authentication.views as auth

urlpatterns = [
    path('admin/', admin.site.urls),

    path('Home/', auth.Home),
    path('Signin/', auth.Signin),
    path('Signup/', auth.Signup),
    path('logout/', auth.Logout),
    
    path('', chat.Home),
    path('search/', chat.Searchops),
    path('createroom/', chat.CreateRoom),
    path('join/<int:roomid>', chat.JoinRoom, name='join'),
    path('remove/<int:roomid>', chat.RemoveRoom, name='Remove'),
    path('delete/<int:roomid>', chat.DeleteRoom, name='Delete'),

]
