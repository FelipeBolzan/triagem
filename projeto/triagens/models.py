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
    codigo = models.CharField(_('Código da traigem *'), unique=True, max_length=20, help_text=' Campos obrigatórios')
    data = models.DateField(_('Data da reunião *'), max_length=11, help_text='dd/mm/aaaa')
    hora = models.CharField(('Hora da reunião *'), max_length=5, help_text='hh:mm')
    nomePaciente = models.CharField(('Nome Completo do Paciente *'), max_length=50)
    idade = models.IntegerField(('Idade'))
    altura = models.FloatField(('Altura'))
    peso = models.FloatField(('Peso'))
    IMC = models.FloatField(('IMC'))
    #Sintomas
    febre = models.BooleanField(('Tem Febre?'))
    dorCabeca = models.BooleanField(('Tem Dor de Cabeça?'))
    secrecaoEspirro = models.BooleanField(('Tem Secreção nasal ou espirro?'))
    dorGarganta = models.BooleanField(('Tem Dor/Irritação na garganta?'))
    tosseSeca = models.BooleanField(('Tem Tosse Seca?'))
    dificuldadeRespiratoria = models.BooleanField(('Tem Dificuldade Respiratória?'))
    doresCorpo = models.BooleanField(('Tem Dores no Corpo?'))
    diarreia = models.BooleanField(('Tem Diarreia?'))
    viagem = models.BooleanField(('Viajou, nos últimos 14 dias, para um local com casos confirmados de COVID-19?'))
    contato = models.BooleanField(('Esteve em contato, nos últimos 14 dias, com um caso diagnosticados com COVID-19?'))
    ResultadoTriagem = models.CharField(('Resultado'), max_length=50)
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
 