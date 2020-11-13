from __future__ import unicode_literals

from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse

from utils.decorators import LoginRequiredMixin,  StaffRequiredMixin, EnfermeiroRequiredMixin

from .models import Triagem


class TriagemListView(LoginRequiredMixin, ListView):
    model = Triagem
    
    
class TriagemCreateView(LoginRequiredMixin,  EnfermeiroRequiredMixin, CreateView):
    model = Triagem
    fields = ['codigo', 'data', 'hora', 'nomePaciente', 'idade', 'altura', 'IMC', 'febre', 'dorCabeca', 'secrecaoEspirro', 'dorGarganta'
    , 'tosseSeca', 'dificuldadeRespiratoria', 'doresCorpo', 'diarreia', 'viagem', 'contato' ,'ResultadoTriagem']
    success_url = 'triagem_list'
    
    def form_valid(self, form):
        limite_mb = 100 * 1024 * 1024
        triagem = form.instance
        
        if (not triagem.arquivo_anexo1 or (triagem.arquivo_anexo1 and triagem.arquivo_anexo1.file.size <= limite_mb)):
            form.save()
            return super(TriagemCreateView, self).form_valid(form)
        else:
            messages.warning(self.request, 'Sistema somente suporta 100 Mb no anexo!')
            return super(TriagemCreateView, self).form_invalid(form)
    
    def get_success_url(self):
        messages.success(self.request, 'Triagem cadastrada com sucesso na plataforma!')
        return reverse(self.success_url)
        

class TriagemUpdateView(LoginRequiredMixin,  EnfermeiroRequiredMixin, UpdateView):
    model = Triagem
    fields = ['codigo', 'data', 'hora', 'nomePaciente', 'idade', 'altura', 'IMC', 'febre', 'dorCabeca', 'secrecaoEspirro', 'dorGarganta'
    , 'tosseSeca', 'dificuldadeRespiratoria', 'doresCorpo', 'diarreia', 'viagem', 'contato' ,'ResultadoTriagem']
    success_url = 'triagem_list'
    
    def form_valid(self, form):
        limite_mb = 100 * 1024 * 1024
        triagem = form.instance
        
        if (not triagem.arquivo_anexo1 or (triagem.arquivo_anexo1 and triagem.arquivo_anexo1.file.size <= limite_mb)):
            form.save()
            return super(TriagemUpdateView, self).form_valid(form)
        else:
            messages.warning(self.request, 'Sistema somente suporta 100 Mb no anexo!')
            return super(TriagemUpdateView, self).form_invalid(form)
    
    def get_success_url(self):
        messages.success(self.request, 'Dados da triagem atualizados com sucesso na plataforma!')
        return reverse(self.success_url)


class TriagemDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Triagem
    success_url = 'triagem_list'

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL. If the object is protected, send an error message.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            self.object.delete()
        except Exception as e:
            messages.error(request, 'Há dependências ligadas à essa triagem, permissão negada!')
        return redirect(self.success_url)
    
    
class TriagemDetailView(LoginRequiredMixin, DetailView):
    model = Triagem
    template_name = 'triagens/triagem_detail.html'