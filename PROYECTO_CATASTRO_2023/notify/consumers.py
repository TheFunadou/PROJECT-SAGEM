import json
from channels.generic.websocket import AsyncWebsocketConsumer
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PROYECTO_CATASTRO_2023.settings')  # Reemplaza 'tu_proyecto.settings' con el nombre de tu módulo de configuración de Django
django.setup()

# Channels, converitr la base de datos de sincrona a asincrona
from notify import models as m_n
from django.contrib.auth.models import User
from channels.db import database_sync_to_async

#PRUEBA DE SOCKET  
class TestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        # Responder al mensaje recibido
        response = f"Recibido: {message}"
        await self.send(text_data=json.dumps({'response': response}))