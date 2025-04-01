from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from .models import Persona, Solicitud
from .forms import PersonaForm, SolicitudForm
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages

# Create your views here.
class SolicitudList(ListView):
    model = Solicitud
    template_name = 'adopcion/solicitudes_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de solicitudes'
        return context

class SolicitudCreate(CreateView):
    model = Solicitud
    template_name = 'adopcion/solicitud_form.html'
    form_class = SolicitudForm
    second_form_class = PersonaForm
    success_url = reverse_lazy('adopcion:solicitud_listar')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registrar solicitud'

        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.second_form_class()
        
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        if form.is_valid() and form2.is_valid():
            solicitud = form.save(commit=False)
            solicitud.persona = form2.save()
            solicitud.save()
            messages.success(self.request, 'Solicitud de adopcion creada exitosamente')
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2))
        
class SolicitudUpdate(UpdateView):
    model = Solicitud
    second_model = Persona
    template_name = 'adopcion/solicitud_form.html'
    form_class = SolicitudForm
    second_form_class = PersonaForm
    success_url = reverse_lazy('adopcion:solicitud_listar')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar solicitud'

        pk = self.kwargs.get('pk', 0)
        solicitud = self.model.objects.filter(id=pk).first()
        persona = self.second_model.objects.filter(id=solicitud.persona_id).first()
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.second_form_class(instance=persona)
        context['id'] = pk
        
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_solicitud = kwargs['pk']
        solicitud = self.model.objects.filter(id=id_solicitud).first()
        persona = self.second_model.objects.filter(id=solicitud.persona_id).first()
        form = self.form_class(request.POST, instance=solicitud)
        form2 = self.second_form_class(request.POST, instance=persona)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            messages.success(self.request, 'Solicitud de adopcion editada exitosamente')
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2))
        
class SolicitudDelete(DeleteView):
    model = Solicitud
    template_name = 'adopcion/solicitud_delete.html'
    success_url = reverse_lazy('adopcion:solicitud_listar')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Solicitud de adopcion eliminada exitosamente')
        return super().delete(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar solicitud'
        return context
    
def listar_solicitudes(request):
    solicitudes = Solicitud.objects.all().order_by('id')

    return render(request, 'adopcion/solicitud_list.html', {
        'origin': 'func',
        'title': 'Lista de solicitudes',
        'object_list': solicitudes
    })

def crear_solicitud(request):
    if request.method == 'POST':
        form = SolicitudForm(request.POST)
        form2 = PersonaForm(request.POST)
        if form.is_valid() and form2.is_valid():
            solicitud = form.save(commit=False)
            solicitud.persona = form2.save()
            solicitud.save()
            messages.success(request, 'Solicitud de adopcion creada exitosamente')
            return redirect('adopcion:solicitud_listar_func')
    else:
        form = SolicitudForm()
        form2 = PersonaForm()

    return render(request, 'adopcion/solicitud_form.html', {
        'title': 'Registrar solicitud',
        'form': form,
        'form2': form2
    })

def editar_solicitud(request, id_solicitud):
    solicitud = Solicitud.objects.filter(id=id_solicitud).first()
    persona = Persona.objects.filter(id=solicitud.persona.id).first()

    if solicitud:
        if request.method == 'GET':
            form = SolicitudForm(instance=solicitud)
            form2 = PersonaForm(instance=persona)
        else:
            form = SolicitudForm(request.POST, instance=solicitud)
            form2 = PersonaForm(request.POST, instance=persona)
            if form.is_valid() and form2.is_valid():
                solicitud = form.save(commit=False)
                solicitud.persona = form2.save()
                solicitud.save()
                messages.success(request, 'Solicitud editada exitosamente')
                return redirect('adopcion:solicitud_listar_func')
    else:
        return redirect('home')
    
    return render(request, 'adopcion/solicitud_form.html', {
        'title': 'Editar solicitud',
        'form': form,
        'form2': form2
    })

def eliminar_solicitud(request, id_solicitud):
    solicitud = Solicitud.objects.filter(id=id_solicitud).first()

    if solicitud:
        if request.method == 'POST':
            solicitud.delete()
            messages.success(request, 'Solicitud eliminada exitosamente')
            return redirect('adopcion:solicitud_listar_func')
    else:
        return redirect('home')
    
    contexto = {
        'title': 'Eliminar solicitud',
        'origin': 'func',
        'object': solicitud
    }
    return render(request, 'adopcion/solicitud_delete.html', contexto)