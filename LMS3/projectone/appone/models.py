from django.db import models
from django.contrib.auth.models import User

class Module(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title
    
    class Meta:
        permissions = [
            ('can_view_module', 'Can view module')  # Custom permission name
        ]

class SubModule(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    main_module = models.ForeignKey(Module, related_name='submodules', on_delete=models.CASCADE)
    topic = models.TextField()
    video_link = models.URLField()

    def __str__(self):
        return f"{self.title} (Part of {self.main_module.title})"

class UserAssignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'module')  # Prevent duplicate assignments

    def __str__(self):
        return f"{self.user.username} - {self.module.title}"