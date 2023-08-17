"""
ASGI config for PROYECTO_CATASTRO_2023 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

#Websockets
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# Importar urls de los consumers
import notify.routing
import catastro.routing
import finanzas.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PROYECTO_CATASTRO_2023.settings')

# INTEGRAR LA LIBRERIA DJANGO CHANNELS AL PROYECTO

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    
    'websocket':AuthMiddlewareStack(
        URLRouter(
            #notify.routing.websocket_urlpatterns +
            catastro.routing.websocket_urlpatterns +
            finanzas.routing.websocket_urlpatterns
        )
    )  
})

