from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
    path('api/newmessage/', views.NewMessageView.as_view(), name = 'newmessage'),
    path('api/messages/<int:group_id>', views.GetMessageView.as_view(), name = 'messages'),
]