from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:user_id>/group/', views.UserGroupList.as_view(), name='group'),
    path('creategroup/', views.GroupViewSet.as_view(), name='create-group'),
    path('sign_s3/', views.GeneratePresignedUrl.as_view(), name='presigned-url'),

    # path('<pk>/updategroup/', views.GroupUpdateView.as_view(), name='update-group'),
    path('group/<str:group_id>/action/', views.GroupActions.as_view(), name='actions-group'),
    path('<str:room_name>/', views.room, name='room'),
    path('api/addmessage/', views.AddMessage.as_view(), name = "addmessage"),
    path('api/messages/<int:group_id>', views.ListMessages.as_view(), name = "messages"),
    
]