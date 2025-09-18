from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('books/<int:book_id>/toggle/', views.toggle_book, name='toggle_book'),
    path('books/<int:book_id>/delete/', views.delete_book, name='delete_book'),
    path('books/<int:book_id>/edit/', views.edit_book, name='edit_book'),
    path("stats/", views.stats_view, name="stats"),
]