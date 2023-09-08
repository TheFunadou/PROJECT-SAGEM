from django.db import models
from django.contrib.auth.models import User

# Signals
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# Create your models here.
class notify(models.Model):
    remitente = models.CharField(max_length=30)
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=60)
    cuerpo = models.CharField(max_length=200)
    fecha_hora= models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.titulo
    
    def complete_notification(self):
        return f"De: {self.remitente}\n{self.titulo}\n{self.cuerpo}\n{self.fecha}     {self.hora}"
    
