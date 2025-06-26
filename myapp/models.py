### 1. Django模型定义 (models.py)
#```python
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField()
    country = models.CharField(max_length=50)
    biography = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    class Book(models.Model):
     GENRE_CHOICES = [
        ('FIC', '小说'),
        ('SCI', '科幻'),
        ('HIS', '历史'),
        ('BIO', '传记'),
        ('EDU', '教育'),
    ]
    
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publication_date = models.DateField()
    genre = models.CharField(max_length=3, choices=GENRE_CHOICES)
    isbn = models.CharField(max_length=13, unique=True)
    pages = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.title

class Publisher(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    website = models.URLField()
    contact_email = models.EmailField()
    books = models.ManyToManyField(Book, related_name='publishers')

    def __str__(self):
        return self.name
#```
