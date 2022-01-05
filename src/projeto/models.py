from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=4096)
    image = models.ImageField(upload_to='post_images', blank=True)
    is_login_required = models.IntegerField(default=0)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)