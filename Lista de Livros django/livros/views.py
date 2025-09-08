import re
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from django.utils import timezone
from datetime import datetime

def book_list(request):
    sort = request.GET.get("sort", "date_read")
    direction = request.GET.get("direction", "asc")
    search = (request.GET.get("search") or "").strip()
    filter_read = request.GET.get("filter_read", "")
    
    allowed_sorts = {"title", "date_start", "date_reg", "date_read", "read"}
    if sort not in allowed_sorts:
        sort = "date_reg"
    
    order_by_field = sort if direction == "asc" else f"-{sort}"
    
    if request.method == "POST":
        title = request.POST.get("title")
        author = request.POST.get("author")
        date_start = request.POST.get("date_start") or None
        ano_publicacao = request.POST.get("ano_publicacao")
        paginas = request.POST.get("paginas")
        tema_principal = request.POST.get("tema_principal")
        preco = request.POST.get("preco") or None
        edicao = request.POST.get("edicao") or None
        avaliacao_pessoal = request.POST.get("avaliacao_pessoal") or None
        date_start = request.POST.get("date_start") or None
        
        if title and author and ano_publicacao and paginas and tema_principal:
            Book.objects.create(
            title=title,
            author=author,
            ano_publicacao=int(ano_publicacao),
            preco=preco,
            edicao=edicao,
            paginas=int(paginas),
            tema_principal=tema_principal,
            avaliacao_pessoal=avaliacao_pessoal,
            date_start=date_start
        )
        return redirect("book_list")
    
    books = Book.objects.all()
    
    if search:
        terms = re.split(r"\s+", search)
        q = Q()
        for t in terms:
            q &= (Q(title__icontains=t) | Q(author__icontains=t))
        books = books.filter(q)
        
    if filter_read == "read":
        books = books.filter(read=True)
    elif filter_read == "unread":
        books = books.filter(read=False)
    
    books = books.order_by(order_by_field, "read", "date_reg")       
    
    
    
    return render(request, "livros/books.html", {
        "books": books, 
        "current_sort": sort, 
        "current_direction": direction,
        "search": search,
        "filter_read": filter_read,
        })

def toggle_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        if book.read:
            book.read = False
            book.date_read = None
        else:
            book.read = True
            book.date_read = timezone.now().date()
        book.save()
    return redirect("book_list")

def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return redirect("book_list")

def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == "POST":
        book.title = request.POST.get("title")
        book.author = request.POST.get("author")
        date_start_str = request.POST.get("date_start")
        if date_start_str:
            book.date_start = datetime.strptime(date_start_str, "%Y-%m-%d").date()
        else:
            book.date_start = None
        book.ano_publicacao = int(request.POST.get("ano_publicacao")) if request.POST.get("ano_publicacao") else None
        book.paginas = int(request.POST.get("paginas")) if request.POST.get("paginas") else None
        book.tema_principal = request.POST.get("tema_principal")
        book.preco = float(request.POST.get("preco")) if request.POST.get("preco") else None
        book.edicao = request.POST.get("edicao")
        book.avaliacao_pessoal = int(request.POST.get("avaliacao_pessoal")) if request.POST.get("avaliacao_pessoal") else None
        book.save()
        return redirect("book_list")
    return render(request, "livros/edit_book.html", {"book": book})