from django.shortcuts import redirect, render
from pytz import timezone

from appToDo.forms import proyectoForm
from .models import Proyecto, Tarea
from .forms import proyectoForm, tareaFormGeneral, tareaFormProyecto
from django.shortcuts import get_object_or_404

# Create your views here.
def listado_tareas(request):
    proyectos = Proyecto.objects.all().order_by('id')
    form_proyectos = nuevoProyecto(request)
    form_tareas = nueva_tarea_general(request)
    return render(request, 'appToDo/todas_las_tareas.html', {'proyectos':proyectos, 'form_proyectos':form_proyectos, 'form_tareas':form_tareas})

def nuevoProyecto(request):
    if request.method == 'POST':
        form = proyectoForm(request.POST)
        if form.is_valid():
            post = form.save()
            post.save()
    else:
        form = proyectoForm()
    return form

def proyecto_seleccionado(request, proyecto):
    # Seleccionamos el proyecto seleccionado.
    proyecto = get_object_or_404(Proyecto, titulo_proyecto=proyecto)
    # Generamos el formulario para ese proyecto en especifico.
    form = nueva_tarea_proyecto(request, proyecto)
    listado_tareas = Tarea.objects.filter(titulo_proyecto=proyecto)
    return render(request, 'appToDo/proyecto.html', {'proyecto':proyecto, 'form':form, 'tareas':listado_tareas})

# Se creara una nueva tarea segun el proyecto seleccionado.
def nueva_tarea_proyecto(request, proyecto):
    if request.method == 'POST':
        form = tareaFormProyecto(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.titulo_proyecto = proyecto
            tarea.save()
    else:
        form = tareaFormProyecto()
    return form

# Se creara una tarea general, sin un proyecto especificado.
def nueva_tarea_general(request):
    if request.method == 'POST':
        form = tareaFormGeneral(request.POST)
        if form.is_valid():
            tarea = form.save()
            tarea.save()
    else:
        form = tareaFormGeneral()
    return form

def completar_tarea(request, pk):
    tarea = get_object_or_404(Tarea, pk=pk)
    tarea.completar()
    return redirect(request.META['HTTP_REFERER'])

def descompletar_tarea(request, pk):
    tarea = get_object_or_404(Tarea, pk=pk)
    tarea.descompletar()
    return redirect(request.META['HTTP_REFERER'])
