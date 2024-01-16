from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Blog(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(null=True)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    # add in thumbnail(small pic) later
    thumb = models.ImageField(default="default.png",blank=True)
    # add in author later
    author=models.ForeignKey(User,default=None,blank=True,null=True,on_delete=models.CASCADE)


    def __str__(self):
        return self.title
    
    # tüm blogların listelendiği sayfada blog bodysinde ilk 50 karakteri alıcak fakat detay sayfasında tüm blog açıklaması olucak
    def snippet(self):
        return self.body[:50] + "..."

class Comment(models.Model):
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.text[:50]}"