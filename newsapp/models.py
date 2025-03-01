from django.db import models

class Source(models.Model):

    source_id=models.CharField(max_length=255,blank=True,null=True)
    name=models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Article(models.Model):

    source = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles')
    author=models.CharField(max_length=255,blank=True,null=True)
    title=models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    url = models.URLField(unique=True)
    url_to_image = models.URLField(blank=True, null=True)
    published_at = models.DateTimeField()
    content = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=255,blank=True,null=True)

    def __str__(self):
        return self.title