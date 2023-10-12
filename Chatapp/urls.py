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
    path('profile/', chat.Profile, name='profile'),
    path('configure/<int:roomid>', chat.Group_config, name='configure'),
    path('remove_user/<int:roomid>', chat.Remove_User, name='remove_user'),
    path('remove_keyword/<str:rm_keyword>/<int:roomid>', chat.Remove_Keyword, name='remove_keyword'),

]
