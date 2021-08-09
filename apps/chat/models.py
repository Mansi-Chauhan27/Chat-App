from django.db import models
from django.contrib.auth.models import User


class Group(models.Model):
    name = models.CharField(max_length=128)
    user = models.ManyToManyField(User, related_name='group_detail',)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(null=True,blank=True)
   

    class Meta:
        db_table = "groups"
        verbose_name = "Group"
        managed  = True

    def get_group_by_userid(userid):
        return Group.objects.filter(user=userid)


class Message(models.Model):
    to_group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    from_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    s3_url_link = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
   

    class Meta:
        db_table = "messages"
        verbose_name = "Message"
        managed  = True


class UrlToken(models.Model):
    token = models.CharField(max_length=500)
    message_id = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
   

    class Meta:
        db_table = "urltokens"
        verbose_name = "Url Token"
        managed  = True



