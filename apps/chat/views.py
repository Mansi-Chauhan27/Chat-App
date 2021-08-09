from django.shortcuts import render
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from .serializers import MessageSerializer

from .models import Message


def index(request):
    return render(request, 'index.html', {})


def room(request, room_name):
    return render(request, 'chatroom.html', {
        'room_name': room_name
    })


class NewMessageView(CreateAPIView):
    serializer_class = MessageSerializer

class GetMessageView(APIView):
    serializer_class = MessageSerializer
    def get(self,request,group_id):
            try:
                    print(group_id)
                    result = Message.objects.filter(to_group_id = group_id)
                    serializer = MessageSerializer(result, many = True)
                    print(serializer.data)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                    data = {"params":"please check the input parameters"}
                    return Response(data, status = status.HTTP_400_BAD_REQUEST)
    