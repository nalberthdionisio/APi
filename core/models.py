from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.contrib.auth.hashers import make_password

class Recommendation(models.Model):
    name = models.CharField(max_length=255, null=False)
    phone = models.CharField(max_length=20, null=False)
    email = models.CharField(max_length=100, null=False)
    street = models.CharField(max_length=100)
    number = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


def upload_image(instance, filename):
    return f'{instance.pk}-{filename}'
class Users(AbstractUser):
    UF= (
    ('CE','Ceará'),
    ('PB','Paraiba'),
)
    email = models.EmailField(unique=True)
    cpf = models.CharField('CPF', max_length=50, null=True)
    # avatar = models.ImageField(
    #     upload_to='medical/avatars/%Y/%m/%d/')
    birth_date = models.DateField('Data de Nascimento',null=True)
    street = models.CharField('Rua',max_length=100, null=True)
    number = models.CharField('Numero',max_length=50, null=True)
    district = models.CharField('Bairro',max_length=100, null=True)
    uf = models.CharField('UF', choices=UF ,max_length=2, null=True)
    phone = models.CharField('Celular',max_length=20, null=True)
    procedure = models.ManyToManyField('Procedure', through='UserProcedure', related_name='users', blank=True)
    created_at = models.DateField(auto_now_add=True, null=True)
    
   
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        if not self.pk and not self.password:
            self.password = make_password('opera')
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.username)

class Procedure(models.Model):
    title = models.CharField(max_length=255, null=False)
    description = models.TextField(null=False)
    days_limit = models.IntegerField(null=False)
    recommendation = models.ManyToManyField(Recommendation, blank=True)
    created_at = models.DateField(auto_now_add=True, null=True)

    
    # user = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return str(self.title)
    
class UserProcedure(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE)
    done = models.BooleanField('Feito', default=False)
    date_limit = models.DateField(null=True, blank=True)
    date_done = models.DateField(null=True, blank=True)
    notified = models.BooleanField('Notificado', default=False)

    def __str__(self):
        return f'{self.user.username} - {self.procedure.title}'