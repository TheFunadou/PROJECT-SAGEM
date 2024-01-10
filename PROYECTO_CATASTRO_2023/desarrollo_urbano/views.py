from django.shortcuts import render, redirect

# PROFILE VIEWS
# LOGOUUT
def logout(request):
    return redirect('logout')

def view_desarrollo_urbano_profile(request):
    return render(request,'desarrollo_urbano/inicio_desarrollo_u.html',{'nom_pag': 'Catastro', 'titulo_pag': 'CATASTRO: CAMPO','username':request.user.username})

