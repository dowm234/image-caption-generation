from django.db import models

class Registration(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.name


class CaptionHistory(models.Model):
    user = models.ForeignKey(Registration, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='captions/')
    caption = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'caption_history'

    def __str__(self):
        return f"{self.user.name} - {self.caption[:30]}"
