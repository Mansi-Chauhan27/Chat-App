from django.shortcuts import render
from rest_framework import response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics
from apps.chat.models import Group, Message
from apps.chat.Serializers import GroupSerialzer, UserSerialzer, MessageSerialzer
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_405_METHOD_NOT_ALLOWED)

# from apps.common.utils4 import create_presigned_post


def index(request):
    return render(request, 'index.html', {})


def room(request, room_name):
    return render(request, 'chatroom.html', {
        'room_name': room_name
    })

# To get all the groups of a user and user info
class UserGroupList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerialzer

    def list(self, request, user_id):
        queryset = User.objects.filter(id=user_id)
        serializer = UserSerialzer(queryset, many=True)
        return Response(serializer.data)


# To Create Group
class GroupViewSet(generics.CreateAPIView):
    serializer_class = GroupSerialzer
    queryset = Group.objects.all()


# To Add User to group/ inactivate Group
class GroupActions(APIView):
   
    # Add Users to Group
    def put(self, request, group_id, format=None):
        result={}
        print(request.data)
        user_list_to_be_added=request.data
        user_list_to_be_added=[3]
        # TODO
        group_data = Group.objects.get(id=1)

        if group_id:
            if user_list_to_be_added:
                for item in user_list_to_be_added:
                    user = User.objects.get(id=item)
                    if user:
                        group_data.user.add(user)
                        return Response(status=HTTP_201_CREATED)
                    else :
                        return Response({'msg':'User Not Found'},status=HTTP_404_NOT_FOUND)
            else:
                return Response({'msg':'User Cannot Be Empty'}, status=HTTP_400_BAD_REQUEST)
        else:
            return Response({'msg':'Group Not Found'},status=HTTP_400_BAD_REQUEST)

    # Make group inactive
    def delete(self, request, group_id):
        group_data = Group.objects.get(id=group_id)
        serializer = GroupSerialzer(group_data, data={'active': False}, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(status = HTTP_200_OK) 
        else:
            return Response(status = HTTP_400_BAD_REQUEST) 



class GeneratePresignedUrl(APIView):

    def post(self, request):
        print(request.data)
        # response = create_presigned_post('mybucket-chatapp', request.data['fileName'])
        response = "Uncomment utils4.py file"
        print(response)
        return Response({'data':response}, status=HTTP_200_OK)

class AddMessage(CreateAPIView):
     serializer_class = MessageSerialzer

class ListMessages(APIView):
    def get(self, request, group_id):
        if group_id:
            queryset = Message.objects.filter(to_group_id = group_id)
            if queryset:
                serializer = MessageSerialzer(queryset, many=True)
                return Response(serializer.data)
            else:
                return Response({'msg':'Messages Not Found'},status=HTTP_404_NOT_FOUND)
        else:
                data = {"params":"Group Not Found"}
                return Response(data, status = HTTP_400_BAD_REQUEST)
