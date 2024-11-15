from django.db import models

# http://127.0.0.1:8000/appone/
# Main Modules
# Title, Description, Actions
class MainModule(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title

# http://127.0.0.1:8000/appone/1/submodules/
# SubModules
# Title, Topic, VideoLink, Actions
class SubModule(models.Model):
    main_module = models.ForeignKey(MainModule, related_name='submodules', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    topic = models.TextField()
    video_link = models.URLField()

    def __str__(self):
        return self.title
