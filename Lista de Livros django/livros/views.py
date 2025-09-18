import re
from django.db.models import Q
from django.db.models import Count
from django.db.models.functions import ExtractYear
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Avg, Sum, F
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
        date_read_str = request.POST.get("date_read")
        if date_read_str:
            book.date_read = datetime.strptime(date_read_str, "%Y-%m-%d").date()
            book.read = True  # marca como lido se tiver data
        else:
            book.date_read = None
            book.read = False
        book.ano_publicacao = int(request.POST.get("ano_publicacao")) if request.POST.get("ano_publicacao") else None
        book.paginas = int(request.POST.get("paginas")) if request.POST.get("paginas") else None
        book.tema_principal = request.POST.get("tema_principal")
        book.preco = float(request.POST.get("preco")) if request.POST.get("preco") else None
        book.edicao = request.POST.get("edicao")
        book.avaliacao_pessoal = int(request.POST.get("avaliacao_pessoal")) if request.POST.get("avaliacao_pessoal") else None
        book.save()
        return redirect("book_list")
    return render(request, "livros/edit_book.html", {"book": book})

def stats_view(request):
    total_livros = Book.objects.count()
    livros_lidos = Book.objects.filter(read=True, paginas__isnull=False)
    lidos = Book.objects.filter(read=True).count()
    nao_lidos = Book.objects.filter(read=False).count()
    media_paginas = Book.objects.aggregate(Avg("paginas"))["paginas__avg"] or 0
    media_avaliacao = Book.objects.aggregate(Avg("avaliacao_pessoal"))["avaliacao_pessoal__avg"] or 0
    preco_total = Book.objects.aggregate(Sum("preco"))["preco__sum"] or 0
    preco_total = round(preco_total, 2)

    paginas_por_ano = {}
    for livro in livros_lidos:
        if livro.date_read:
            ano = livro.date_read.year
            paginas_por_ano.setdefault(ano, []).append(livro.paginas)
            
    media_total_por_ano = {}
    total_paginas = 0

    for ano, paginas in paginas_por_ano.items():
        media_total_por_ano[ano] = {
        "media": sum(paginas) / len(paginas),
        "total": sum(paginas)
        }
        total_paginas += sum(paginas)
    
    paginas_por_ano_ordenado = dict(sorted(media_total_por_ano.items()))
    
    avaliacoes = (
        Book.objects
        .values("avaliacao_pessoal")
        .annotate(total=Count("id"))
        .order_by("avaliacao_pessoal")
    )
    
    books_by_year = (
        Book.objects.filter(read=True)
        .annotate(year=ExtractYear("date_read"))
        .values("year")
        .annotate(total=Count("id"))
        .order_by("year")
    )

    years = [b["year"] for b in books_by_year]
    totals = [b["total"] for b in books_by_year]

    
    
    labels = [a["avaliacao_pessoal"] for a in avaliacoes if a["avaliacao_pessoal"]]
    valores = [a["total"] for a in avaliacoes if a["avaliacao_pessoal"]]
    
    return render(request, "livros/stats.html", {
        "total_livros": total_livros,
        "lidos": lidos,
        "nao_lidos": nao_lidos,
        "media_paginas": round(media_paginas, 1),
        "media_avaliacao": round(media_avaliacao, 1),
        "preco_total": preco_total,
        "labels": labels,
        "valores": valores,
        "years": years,
        "totals": totals,
        "paginas_por_ano": paginas_por_ano_ordenado,
        "total_paginas": total_paginas,
    })