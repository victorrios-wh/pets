from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import MascotaForm
from .models import Mascota
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.core.urlresolvers import reverse_lazy
from refugio.forms import DivErrorList

# Create your views here.
def mascota_view(request):

    if request.method == 'POST':
        form = MascotaForm(request.POST, request.FILES, error_class=DivErrorList)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mascota registrada exitosamente')
            return redirect('mascota:mascota_listar_func')
    else:
        form = MascotaForm()
    
    contexto = {
        'title': 'Registrar mascota',
        'form': form
    }
    return render(request, 'mascota/mascota_form.html', contexto)

def mascota_list(request):
    mascotas = Mascota.objects.all().order_by('id')
    
    contexto = {
        'title': 'Lista de mascotas',
        'origin': 'func',
        'object_list': mascotas
    }
    return render(request, 'mascota/mascota_list.html', contexto)

def mascota_edit(request, id_mascota):
    mascota = Mascota.objects.filter(id=id_mascota).first()

    if mascota:
        if request.method == 'GET':
            form = MascotaForm(instance=mascota)
        else:
            form = MascotaForm(request.POST, request.FILES, instance=mascota, error_class=DivErrorList)
            if form.is_valid():
                form.save()
                messages.success(request, 'Mascota editada exitosamente')
                return redirect('mascota:mascota_listar_func')
    else:
        return redirect('home')
    
    contexto = {
        'title': 'Editar mascota',
        'form': form
    }
    return render(request, 'mascota/mascota_form.html', contexto)

def mascota_delete(request, id_mascota):
    mascota = Mascota.objects.filter(id=id_mascota).first()

    if mascota:
        if request.method == 'POST':
            mascota.delete()
            messages.error(request, 'Mascota eliminada exitosamente')
            return redirect('mascota:mascota_listar_func')
    else:
        return redirect('home')
    
    contexto = {
        'title': 'Eliminar mascota',
        'origin': 'func',
        'object': mascota
    }
    return render(request, 'mascota/mascota_delete.html', contexto)

class MascotaList(ListView):
    model = Mascota
    template_name = 'mascota/mascota_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de mascotas'
        return context

class MascotaCreate(CreateView):
    model = Mascota
    form_class = MascotaForm
    template_name = 'mascota/mascota_form.html'
    success_url = reverse_lazy('mascota:mascota_listar')

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, 'Mascota registrada exitosamente')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registrar mascota'
        return context
    
    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = {
            "initial": self.get_initial(),
            "prefix": self.get_prefix(),
        }
        if self.request.method in ("POST", "PUT"):
            kwargs.update(
                {
                    "data": self.request.POST,
                    "files": self.request.FILES,
                    "error_class": DivErrorList
                }
            )
        return kwargs
    
class MascotaUpdate(UpdateView):
    model = Mascota
    form_class = MascotaForm
    template_name = 'mascota/mascota_form.html'
    success_url = reverse_lazy('mascota:mascota_listar')

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, 'Mascota editada exitosamente')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar mascota'
        return context
    
    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        if hasattr(self, "object"):
            kwargs.update({"instance": self.object})
        if self.request.method in ("POST", "PUT"):
            kwargs.update(
                {
                    "error_class": DivErrorList
                }
            )
        return kwargs
    
class MascotaDelete(DeleteView):
    model = Mascota
    template_name = 'mascota/mascota_delete.html'
    success_url = reverse_lazy('mascota:mascota_listar')

    def delete(self, request, *args, **kwargs):
        messages.error(self.request, 'Mascota eliminada exitosamente')
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar mascota'
        return context
