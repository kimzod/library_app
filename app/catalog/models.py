import uuid
from django.db import models
from django.urls import reverse


class Genre(models.Model):
    name = models.CharField(max_length=200, help_text="책의 장르를 입력하세요 (e.g. Science Fiction)")

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=200, help_text='책의 언어를 입력하세요(e.g English, French, Korean etc.)')

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['first_name', 'last_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text='책에 대한 간략한 설명을 입력하세요')
    isbn = models.CharField('ISBN', max_length=13, help_text='13자리 숫자 <a href="https://www.isbn-international.org'
                                                             '/content/what-isbn">ISBN 번호</a>')
    genre = models.ManyToManyField('Genre', help_text='이 책의 장르를 선택하세요')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'

    # def get_absolute_url(self):
    #     return reverse('book-detail', args=[str(self.id), ])


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='책의 고유 ID')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', '점검'),
        ('o', '대출'),
        ('a', '대출가능'),
        ('r', '예약됨'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='도서 대출여부')

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f'{self.id} ({self.book.title})'
