from catastro import models as models_catastro

class Contribuyente:

    def __init__(self,rfc):
        self.rfc = rfc
    
    @property
    def informacion_gral(self):
        try:
            data = models_catastro.Datos_Contribuyentes.objects.get(rfc= self.rfc)
            return data
        except:
            return None
    
    
    
        