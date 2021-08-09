from rest_framework import serializers

# from django.contrib.auth.models import Token
from .models import Group, Message, UrlToken
from django.contrib.auth.models import User



class GroupSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Group
        # fields = '__all__'
        fields = ('name','user','id','created_at','active','updated_at')



class MessageSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Message
        # fields = '__all__'
        fields = ('to_group_id','from_user_id','id','s3_url_link','created_at')



class UrlTokenSerialzer(serializers.ModelSerializer):
    class Meta:
        model = UrlToken
        # fields = '__all__'
        fields = ('token','message_id','id','is_active','created_at')



class UserSerialzer(serializers.ModelSerializer):
    group_detail = GroupSerialzer(many=True)
    class Meta:
        model = User
        fields = ['id','first_name','last_name','email','is_active','group_detail']
