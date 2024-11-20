from django.db import models
from django.contrib.auth.models import User

class Module(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)  # Automatically sets the current date when a module is created
    image = models.ImageField(upload_to='module_images/', null=True, blank=True)  # For uploading images

    def __str__(self):
        return self.title

class SubModule(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    main_module = models.ForeignKey(Module, related_name='submodules', on_delete=models.CASCADE)
    topic = models.TextField()
    video_link = models.URLField()
    session = models.CharField(max_length=100, default='', null=True)  
    date_created = models.DateTimeField(auto_now_add=True)  # Automatically sets the current date when a module is created

    def __str__(self):
        return f"{self.title} (Part of {self.main_module.title})"
    
class UserAssignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'module')  # Prevent duplicate assignments

    def __str__(self):
        return f"{self.user.username} - {self.module.title}"