import json
from channels.generic.websocket import AsyncWebsocketConsumer
import os
import django

# Channels, converitr la base de datos de sincrona a asincrona
from notify import models as m_n
from django.contrib.auth.models import User
from channels.db import database_sync_to_async


class NotifyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.username = self.scope['url_route']['kwargs']['username']
        username= self.username
        self.group_name=f'consumer_notifications_{username}'
        
        # Suscribir a usuario al grupo
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        
    
    async def disconnect(self,close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
           
    async def receive(self, text_data):
        data = json.loads(text_data)
        event = data.get('event')
        
        username= self.username
       
        if (event == 'conexion'):
           # Obtener resultados de la consulta
            get_notify= await self.get_notify_db(username)
        
            # recorrer y mandar los resultados en un json
            notifications = await self.serialize_notifications(get_notify)
        
            return await self.send(text_data=notifications)
        
    async def update_not(self,event):
        
        # Obtener username del destinatario
        destinatario = event['destinatario']
        
        # Obtener resultados de la consulta
        get_notify = await self.get_notify_db(destinatario)

        # recorrer y mandar los resultados en un json
        notifications = await self.serialize_notifications(get_notify)

        # Enviar el mensaje JSON al cliente WebSocket
        await self.send(text_data=notifications)
       
    @database_sync_to_async
    def get_notify_db(self,username):
        id_dest = User.objects.get(username=username)
        return m_n.notify.objects.all().filter(destinatario=id_dest)
    
    @database_sync_to_async
    def serialize_notifications(self, notifications):
        return json.dumps([{'titulo': notify.titulo, 'remitente': notify.remitente} for notify in notifications])
        

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
        
        
# class index_contribuyentes(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
    
#     async def disconnect(self, code):
#         return await super().disconnect(code)
    
#     async def receive(self, text_data):
#         data = json.load(text_data)
        
        