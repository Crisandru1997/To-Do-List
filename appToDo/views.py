import datetime
from tkinter.tix import Tree
from django.shortcuts import redirect, render
from pytz import timezone
from appToDo.forms import proyectoForm
from .models import Proyecto, Tarea
from .forms import proyectoForm, tareaFormGeneral, tareaFormProyecto
from django.shortcuts import get_object_or_404

# Create your views here.
def index(request):
    todos_los_proyectos = Proyecto.objects.filter(propietario=request.user)
    todas_las_tareas_hoy = Tarea.objects.filter(completado=False, propietario=request.user).order_by('id')
    tareas_completadas = Tarea.objects.filter(completado=True, propietario=request.user)
    form_nueva_tarea = nueva_tarea_general(request)
    form_nuevo_proyecto = nuevoProyecto(request)
    return render(request, 'appToDo/listado_tareas.html', {'proyectos':todos_los_proyectos, 'tareas_hoy':todas_las_tareas_hoy, 'tareas_completadas':tareas_completadas, 'form_tarea':form_nueva_tarea, 'form_proyecto':form_nuevo_proyecto})

def nuevoProyecto(request):
    if request.method == 'POST':
        form = proyectoForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.propietario = request.user
            post.save()
            form = proyectoForm()
    else:
        form = proyectoForm()
    return form

def verificar(request, proyecto):
    esta = get_object_or_404(Proyecto, propietario=request.user, titulo_proyecto=proyecto)
    if esta:
        return True
    else:
        return False

def proyecto_seleccionado(request, proyecto):
    esta = verificar(request, proyecto)
    if esta:
        # Seleccionamos el proyecto seleccionado.
        proyectos = Proyecto.objects.filter(propietario=request.user)
        proyecto = get_object_or_404(Proyecto, titulo_proyecto=proyecto)
        # Generamos el formulario para ese proyecto en especifico.
        form = nueva_tarea_proyecto(request, proyecto)
        form_nuevo_proyecto = nuevoProyecto(request)
        listado_tareas = Tarea.objects.filter(completado=False, titulo_proyecto=proyecto, propietario=request.user).order_by('id')
        tareas_completadas = Tarea.objects.filter(completado=True, titulo_proyecto=proyecto, propietario=request.user)
        return render(request, 'appToDo/proyecto_individual.html', {'proyecto':proyecto, 'form':form, 'tareas':listado_tareas, 'tareas_completadas':tareas_completadas, 'proyectos':proyectos, 'form_proyecto':form_nuevo_proyecto})
    else:
        return render(request, 'appToDo/error.html', {})

# Se creara una nueva tarea segun el proyecto seleccionado.
def nueva_tarea_proyecto(request, proyecto):
    if request.method == 'POST':
        form = tareaFormProyecto(request.user ,request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.titulo_proyecto = proyecto
            tarea.propietario = request.user
            tarea.save()
            form = tareaFormGeneral()
    else:
        form = tareaFormProyecto()
    return form

# Se creara una tarea general, sin un proyecto especificado.
def nueva_tarea_general(request):
    if request.method == 'POST':
        form = tareaFormGeneral(request.user , request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.propietario = request.user
            tarea.save()
            form = tareaFormGeneral(request.user)
    else:
        form = tareaFormGeneral(request.user)
    return form

def completar_tarea(request, pk):
    tarea = get_object_or_404(Tarea, pk=pk)
    tarea.completar()
    return redirect(request.META['HTTP_REFERER'])

def descompletar_tarea(request, pk):
    tarea = get_object_or_404(Tarea, pk=pk)
    tarea.descompletar()
    return redirect(request.META['HTTP_REFERER'])
