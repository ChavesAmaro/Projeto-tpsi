from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    read = models.BooleanField(default=False)
    date_reg = models.DateField(auto_now_add=True)
    date_read = models.DateField(null=True, blank=True)
    date_start = models.DateField(null=True, blank=True)
    ano_publicacao = models.IntegerField(verbose_name="Ano de Publicação")
    preco = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)  
    edicao = models.CharField(max_length=100, null=True, blank=True)
    paginas = models.PositiveIntegerField(verbose_name="Número de Páginas")
    tema_principal = models.CharField(max_length=200, verbose_name="Tema Principal")

    AVALIACAO_CHOICES = [(i, str(i)) for i in range(1, 6)]
    avaliacao_pessoal = models.IntegerField(
        choices=AVALIACAO_CHOICES, null=True, blank=True, verbose_name="Avaliação Pessoal"
    )
    
    def __str__(self):
        return self.title

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "book_list"
LOGOUT_REDIRECT_URL = "login"