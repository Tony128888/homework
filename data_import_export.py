### 2. 独立数据处理脚本 (data_import_export.py)
#```python
import os
import sys
import django
import json
import random
from datetime import datetime, timedelta
from faker import Faker

# 设置Django环境
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

from your_app.models import Author, Book, Publisher

fake = Faker('zh_CN')

def clean_raw_data(raw_data):
    """清理原始数据"""
    cleaned = []
    for item in raw_data:
        # 清理ISBN：移除非数字字符
        if 'isbn' in item:
            item['isbn'] = ''.join(filter(str.isdigit, item['isbn']))
        
        # 确保价格是数值类型
        if 'price' in item:
            try:
                item['price'] = float(item['price'])
            except (TypeError, ValueError):
                item['price'] = 0.0
        
        # 确保页数是整数
        if 'pages' in item:
            try:
                item['pages'] = int(item['pages'])
            except (TypeError, ValueError):
                item['pages'] = 0
        
        cleaned.append(item)
    return cleaned

def generate_sample_data(num_records=20):
    """生成样本数据"""
    authors = []
    books = []
    publishers = []
    
    # 创建作者
    for _ in range(num_records):
        author = {
            'name': fake.name(),
            'birth_date': fake.date_of_birth(minimum_age=25, maximum_age=85),
            'country': fake.country(),
            'biography': fake.text(max_nb_chars=500)
        }
        authors.append(author)
    
    # 创建书籍
    genres = ['FIC', 'SCI', 'HIS', 'BIO', 'EDU']
    for i in range(num_records):
        book = {
            'title': fake.catch_phrase(),
            'publication_date': fake.date_between(start_date='-30y', end_date='today'),
            'genre': random.choice(genres),
            'isbn': fake.isbn13(),
            'pages': random.randint(100, 800),
            'price': round(random.uniform(5.99, 99.99), 2)
        }
        books.append(book)
    
    # 创建出版社
    for _ in range(min(5, num_records)):  # 创建5家出版社
        publisher = {
            'name': fake.company(),
            'address': fake.address(),
            'website': fake.url(),
            'contact_email': fake.company_email()
        }
        publishers.append(publisher)
    
    return {
        'authors': authors,
        'books': books,
        'publishers': publishers
    }

def import_to_database(data):
    """将数据导入数据库"""
    # 导入作者
    author_objs = []
    for author_data in data['authors']:
        author = Author(**author_data)
        author_objs.append(author)
    Author.objects.bulk_create(author_objs)
    
    # 导入书籍
    all_authors = list(Author.objects.all())
    book_objs = []
    for book_data in data['books']:
        book_data['author'] = random.choice(all_authors)
        book = Book(**book_data)
        book_objs.append(book)
    Book.objects.bulk_create(book_objs)
    
    # 导入出版社并关联书籍
    all_books = list(Book.objects.all())
    publisher_objs = []
    for publisher_data in data['publishers']:
        publisher = Publisher.objects.create(**publisher_data)
        # 每个出版社随机关联5-10本书
        books_to_assign = random.sample(all_books, min(10, len(all_books)))
        publisher.books.set(books_to_assign)
        publisher_objs.append(publisher)
    
    return {
        'authors': len(author_objs),
        'books': len(book_objs),
        'publishers': len(publisher_objs)
    }

def export_from_database(filename='library_export.json'):
    """从数据库导出数据到JSON文件"""
    data = {
        'authors': [],
        'books': [],
        'publishers': []
    }
    
    # 导出作者
    for author in Author.objects.all():
        data['authors'].append({
            'name': author.name,
            'birth_date': author.birth_date.isoformat(),
            'country': author.country,
            'biography': author.biography
        })
    
    # 导出书籍
    for book in Book.objects.all():
        data['books'].append({
            'title': book.title,
            'author': book.author.name,
            'publication_date': book.publication_date.isoformat(),
            'genre': book.genre,
            'isbn': book.isbn,
            'pages': book.pages,
            'price': float(book.price)
        })
    
    # 导出出版社
    for publisher in Publisher.objects.all():
        publisher_data = {
            'name': publisher.name,
            'address': publisher.address,
            'website': publisher.website,
            'contact_email': publisher.contact_email,
            'books': [book.title for book in publisher.books.all()]
        }
        data['publishers'].append(publisher_data)
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return len(data['authors']), len(data['books']), len(data['publishers'])

def main():
    # 步骤1: 生成原始数据
    print("生成样本数据...")
    raw_data = generate_sample_data(25)  # 生成25条记录
    
    # 步骤2: 清理数据
    print("清理数据...")
    cleaned_data = clean_raw_data(raw_data)
    
    # 步骤3: 导入数据库
    print("导入数据库...")
    import_results = import_to_database(cleaned_data)
    print(f"导入完成: {import_results['authors']} 作者, {import_results['books']} 书籍, {import_results['publishers']} 出版社")
    
    # 步骤4: 导出数据
    print("导出数据到文件...")
    export_results = export_from_database()
    print(f"导出完成: {export_results[0]} 作者, {export_results[1]} 书籍, {export_results[2]} 出版社")
    
    print("操作完成！请在Django管理面板中检查数据")

if __name__ == '__main__':
    main()
#```
