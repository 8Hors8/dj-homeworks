from django.shortcuts import render

from .models import Book


def books_view(request):
    template = 'books/books_list.html'
    books = Book.objects.all().order_by('pub_date')
    context = {
        'books': books
    }
    return render(request, template, context)


def books_by_date(request, pub_date):
    template = 'books/books_list.html'

    try:
        books = Book.objects.filter(pub_date=pub_date).order_by('pub_date')
        prev_date = Book.objects.filter(pub_date__lt=pub_date).order_by('-pub_date').first()
        next_date = Book.objects.filter(pub_date__gt=pub_date).order_by('pub_date').first()
    except Book.DoesNotExist:
        raise Http404("Книги за эту дату не найдены.")

    context = {
        'books': books,
        'prev_date': prev_date.pub_date if prev_date else None,
        'next_date': next_date.pub_date if next_date else None
    }
    return render(request, template, context)
