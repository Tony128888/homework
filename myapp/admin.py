### 3. Django管理面板配置 (admin.py)
```python
from django.contrib import admin
from .models import Author, Book, Publisher

class BookInline(admin.TabularInline):
    model = Book
    extra = 0
    fields = ['title', 'publication_date', 'genre', 'price']
    readonly_fields = ['publication_date']

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'birth_date']
    search_fields = ['name', 'country']
    list_filter = ['country']
    inlines = [BookInline]

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'genre', 'publication_date', 'price']
    list_filter = ['genre', 'publication_date']
    search_fields = ['title', 'isbn']
    autocomplete_fields = ['author']
    date_hierarchy = 'publication_date'

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_email', 'website']
    filter_horizontal = ['books']
    search_fields = ['name', 'contact_email']
```
