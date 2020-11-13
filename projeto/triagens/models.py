from __future__ import unicode_literals

import os

from django.conf import settings
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from utils.gerador_hash import gerar_hash
    
class Triagem(models.Model):
    codigo = models.CharField(_('Código da traigem *'), unique=True, max_length=20, help_text='* Campos obrigatórios')
    data = models.DateField(_('Data da reunião *'), max_length=11, help_text='dd/mm/aaaa')
    hora = models.CharField(_('Hora da reunião *'), max_length=5, help_text='hh:mm')
    nomePaciente = models.CharField(_('Nome Completo do Paciente *'), max_length=50)
    idade = models.IntegerField(_('Idade'))
    altura = models.FloatField(_('Altura'))
    peso = models.FloatField(_('Peso'))    
    IMC = models.FloatField(_('IMC'))
    #Sintomas
    febre = models.BooleanField(_('Tem Febre?'))
    dorCabeca = models.BooleanField(_('Tem Dor de Cabeça?'))
    secrecaoEspirro = models.BooleanField(_('Tem Secreção nasal ou espirro?'))
    dorGarganta = models.BooleanField(_('Tem Dor/Irritação na garganta?'))
    tosseSeca = models.BooleanField(_('Tem Tosse Seca?'))
    dificuldadeRespiratoria = models.BooleanField(_('Tem Dificuldade Respiratória?'))
    doresCorpo = models.BooleanField(_('Tem Dores no Corpo?'))
    diarreia = models.BooleanField(_('Tem Diarreia?'))
    viagem = models.BooleanField(_('Viajou, nos últimos 14 dias, para um local com casos confirmados de COVID-19?'))
    contato = models.BooleanField(_('Esteve em contato, nos últimos 14 dias, com um caso diagnosticados com COVID-19?'))
    ResultadoTriagem = models.CharField(_('Resultado'), max_length=50)

    
    slug = models.SlugField('Hash',max_length= 200, null=True, blank=True)
    
    objects = models.Manager()
    
    class Meta:
        ordering            =   ['codigo','-data','-hora']
        verbose_name        =   ('triagem')
        verbose_name_plural =   ('triagens')
        unique_together     =   ['codigo', 'data', 'hora'] #criando chave primária composta no BD

    def __str__(self):
        return "Triagem: %s. Data: %s." % (self.codigo, self.data)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gerar_hash()
        self.codigo = self.codigo.upper()
        super(Triagem, self).save(*args, **kwargs)

    @property
    def get_absolute_url(self):
        return reverse('triagem_update', args=[str(self.id)])

    @property
    def get_delete_url(self):
        return reverse('triagem_delete', args=[str(self.id)])
    
    @property
    def get_visualiza_url(self):
        return reverse('triagem_detail', args=[str(self.id)])
    



