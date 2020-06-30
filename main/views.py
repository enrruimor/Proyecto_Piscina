# encoding:utf-8
import shelve
from main.models import Libro,Puntuacion
from main.forms import UsuarioForm, LibroForm
from django.shortcuts import render, get_object_or_404
from main.recommendations import  transformPrefs, getRecommendations, topMatches
from main.populate import populateDB
from django.shortcuts import Http404


def loadDict():
    Prefs={}   # matriz de usuarios y puntuaciones a cada a items
    shelf = shelve.open("dataRS.dat")
    puntuaciones = Puntuacion.objects.all()
    for p in puntuaciones:
        usuario = int(p.usuario)
        ISBN_libro = int(p.ISBN)
        libro = Libro.objects.get(ISBN=ISBN_libro)
        ISBN = libro.ISBN
        punt = int(p.puntuacion)
        Prefs.setdefault(usuario, {})
        Prefs[usuario][ISBN] = punt
    shelf['Prefs']=Prefs
    shelf['ItemsPrefs']=transformPrefs(Prefs)
    shelf.close()

def index(request):
    return render(request,'index.html')

def populateDB1(request):
    populateDB()
    return render(request,'poblar.html')

def loadRS(request):
    loadDict()
    return render(request,'cargaRS.html')

def puntuacionesUsuario(request):
    if request.method=='GET':
        form = UsuarioForm(request.GET, request.FILES)
        if form.is_valid():
            user = form.cleaned_data['usuario']
            puntuaciones = Puntuacion.objects.filter(usuario=int(user))
            field_object = Puntuacion._meta.get_field("ISBN")
            libros = []
            if len(puntuaciones)==0:
                raise Http404('El usuario no existe o no ha puntuado ningún libro')
            for p in puntuaciones:
                valor = field_object.value_from_object(p)
                libros.append(Libro.objects.get(ISBN=int(valor)))
            datos = zip(puntuaciones, libros)
            return render(request, 'puntuacionesUsuario.html', {'id': user, 'datos': datos})
    form=UsuarioForm()
    return render(request, 'buscarUsuario.html', {'form': form})

def mejoresLibros(request):
    if request.method == 'GET':
        libros = Libro.objects.all()
        i = 0
        mej_libros = []
        field_object = Libro._meta.get_field("ISBN")
        field_objectp = Puntuacion._meta.get_field("puntuacion")
        for libro in libros:
            i += 1
            ISBN = field_object.value_from_object(libro)
            punt = Puntuacion.objects.filter(ISBN=ISBN)
            punts = [field_objectp.value_from_object(p) for p in punt]
            try:
                punt_avg = sum(punts) / len(punts)
            except:
                punt_avg = 0
            if len(mej_libros) == 0:
                mej_libros.append((libro, punt_avg))
                menor_punt = punt_avg
            elif len(mej_libros) < 3:
                if punt_avg > menor_punt:
                    a = [(libro, punt_avg)]
                    a.extend(mej_libros)
                    mej_libros = a
                else:
                    mej_libros.append((libro, punt_avg))
                    menor_punt = punt_avg
            else:
                if punt_avg > menor_punt:
                    if punt_avg > mej_libros[0][1]:
                        a = [(libro, punt_avg)]
                        a.extend(mej_libros[:-1])
                        mej_libros = a
                        menor_punt = mej_libros[2][1]

                    elif punt_avg > mej_libros[1][1]:
                        mej_libros = [mej_libros[0], (libro, punt_avg), mej_libros[1]]
                        menor_punt = mej_libros[2][1]
                    else:
                        mej_libros = mej_libros[:-1]
                        mej_libros.append((libro, punt_avg))
                        menor_punt = punt_avg

    return render(request, 'mejoresLibros.html', {'data': mej_libros})


def librosParecidos(request):
    if request.method=='GET':
        form = LibroForm(request.GET, request.FILES)
        if form.is_valid():
            ISBN_libro = form.cleaned_data['ISBN']
            libro = get_object_or_404(Libro, pk=ISBN_libro)
            shelf = shelve.open("dataRS.dat")
            ItemPrefs = shelf['ItemsPrefs']
            shelf.close()
            recommended = topMatches(ItemPrefs, int(ISBN_libro), n=5)
            libros = []
            similar = []
            for re in recommended:
                libros.append(Libro.objects.get(ISBN=re[1]))
                similar.append(re[0])
            datos = zip(libros, similar)
            return render(request, 'librosParecidos.html', {'ISBN': ISBN_libro, 'datos': datos})
    form = LibroForm()
    return render(request, 'buscarLibro.html', {'form':form})

def recomendarLibros(request):
    if request.method=='GET':
        form = UsuarioForm(request.GET, request.FILES)
        if form.is_valid():
            user = form.cleaned_data['usuario']
            shelf = shelve.open("dataRS.dat")
            Prefs = shelf['Prefs']

            punt= Puntuacion.objects.filter(usuario=int(user))

            if len(punt)==0:
                raise Http404('El usuario no existe o no ha puntuado nigún libro')

            shelf.close()
            rankings = getRecommendations(Prefs, int(user))
            recommended = rankings[:10]
            libros = []
            scores = []

            for r in recommended:
                libros.append(Libro.objects.get(ISBN=r[1]))
                scores.append(r[0])
            datos = zip(libros,scores)
            return render(request, 'recomendarLibros.html', {'user':user, 'datos': datos})
    form = UsuarioForm()
    return render(request, 'buscarUsuario.html', {'form': form})