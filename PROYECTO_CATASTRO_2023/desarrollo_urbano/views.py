from django.shortcuts import render


# Create your views here.
def perfil_desarrollo_urb(request):
    ctx={
        'url_pag': 'x',
        'nom_pag': 'Catastro',
        'titulo_pag': 'INICIO DESARROLLO URBANO'
    }
    
    return render(request,'sup_user/inicio_sup_user.html',ctx)

