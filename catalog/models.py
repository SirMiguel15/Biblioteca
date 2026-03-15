from django.db import models

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author,on_delete=models.PROTECT)
    isbn = models.CharField(unique=True, max_length=13)
    is_available = models.BooleanField(default=True)
    
    class Meta:
        ordering = ["title"]
    
    def __str__(self):
        return self.title