from django.core.validators import FileExtensionValidator
from django.db import models
from core.models import CustomUser
from django.urls import reverse


def post_image_path(instance, filename):
    user_id = instance.id
    return "posts/user-{}/{}".format(user_id, filename)


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    description = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='posts', blank=True, validators=[FileExtensionValidator(['jpeg', 'jpg', 'png'])])
    date_pub = models.DateTimeField(auto_now_add=True)
    date_edit = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(CustomUser, related_name='users_like_it', blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def get_absolute_url(self):
        return reverse('posts:post_detail', kwargs={'post_id': self.pk})

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    @property
    def like_count(self):
        return self.likes.count()

    def __str__(self):
        return "Post from {} with #{}".format(self.author, self.id)


class Comment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    likes = models.ManyToManyField(CustomUser, related_name='like_comments', blank=True)
    text = models.TextField(max_length=500)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    date_pub = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Comment from {} to post #{}".format(self.author, self.post.id)