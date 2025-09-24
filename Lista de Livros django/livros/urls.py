from django.urls import path
from . import views
from .views import CustomLoginView, LogoutView, RegisterView


urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('books/<int:book_id>/toggle/', views.toggle_book, name='toggle_book'),
    path('books/<int:book_id>/delete/', views.delete_book, name='delete_book'),
    path('books/<int:book_id>/edit/', views.edit_book, name='edit_book'),
    path("stats/", views.stats_view, name="stats"),
    path('export-excel/', views.export_books_excel, name='export_books_excel'),
    path("login/", CustomLoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
]