
from django.urls import re_path,path
from catastro import consumers as consumers_catastro


"""
    r'^ws/play/(?P<room_code>\w+)/$':
    Esta es la ruta de URL que se está configurando para manejar WebSockets. Veamos cada parte de esta expresión:

    ^: Es un símbolo especial que indica que la ruta debe coincidir desde el inicio de la URL.
    ws/: Es simplemente un prefijo para indicar que esta ruta manejará conexiones WebSocket.
    play/: Es una parte de la URL específica para esta aplicación, lo que significa que esta ruta manejará conexiones WebSocket para el juego.
    (?P<room_code>\w+): Esta es una parte dinámica de la URL que captura un valor variable y lo asigna a una variable llamada "room_code". La expresión (?P<room_code> ... ) indica que estamos capturando un grupo de caracteres y asignándolo a la variable "room_code". \w+ es una expresión regular que coincide con uno o más caracteres alfanuméricos (letras y números) y guiones bajos (_). En otras palabras, captura cualquier cadena de caracteres alfanuméricos como "room_code".
"""

websocket_urlpatterns = [
    path('ws/load_notify/<str:username>/', consumers_catastro.NotifyConsumer.as_asgi()),
    path('prueba/',consumers_catastro.TestConsumer.as_asgi())
]

