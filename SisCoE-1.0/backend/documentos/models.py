# models.py
from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe

class Documento(models.Model):
    TIPO_CHOICES = (
        ('PDF', 'PDF'),
        ('VIDEO', 'Vídeo'),
        ('AUDIO', 'Áudio'),
        ('DOC', 'Documento'),
        ('SHEET', 'Planilha'),
        ('IMAGEM', 'Imagem'),
        ('TEXT', 'Texto'),
        ('OUTRO', 'Outro'),
    )

    id = models.AutoField(primary_key=True)
    data_publicacao = models.DateTimeField()
    data_documento = models.DateTimeField()
    numero_documento = models.CharField(max_length=100)
    assunto = models.CharField(max_length=200)
    descricao = models.TextField()
    assinada_por = models.CharField(max_length=100)
    data_criacao = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='OUTRO')

    def __str__(self):
        return self.assunto

    @property
    def tipo_badge(self):
        if self.tipo == 'PDF':
            return mark_safe('<span class="bg-red-500 text-white px-2 py-1 rounded">PDF</span>')
        elif self.tipo == 'VIDEO':
            return mark_safe('<span class="bg-blue-500 text-white px-2 py-1 rounded">Vídeo</span>')
        elif self.tipo == 'AUDIO':
            return mark_safe('<span class="bg-green-500 text-white px-2 py-1 rounded">Áudio</span>')
        elif self.tipo == 'DOC':
            return mark_safe('<span class="bg-yellow-500 text-gray-800 px-2 py-1 rounded">Documento</span>')
        elif self.tipo == 'SHEET':
            return mark_safe('<span class="bg-purple-500 text-white px-2 py-1 rounded">Planilha</span>')
        elif self.tipo == 'IMAGEM':
            return mark_safe('<span class="bg-pink-500 text-white px-2 py-1 rounded">Imagem</span>')
        elif self.tipo == 'TEXT':
            return mark_safe('<span class="bg-gray-500 text-white px-2 py-1 rounded">Texto</span>')
        elif self.tipo == 'OUTRO':
            return mark_safe('<span class="bg-indigo-500 text-white px-2 py-1 rounded">Outro</span>')
        else:
            return mark_safe('<span class="bg-gray-300 text-gray-700 px-2 py-1 rounded">Desconhecido</span>')

class Arquivo(models.Model):
    documento = models.ForeignKey(Documento, related_name='arquivos', on_delete=models.CASCADE)
    arquivo = models.FileField(upload_to='documentos/')
    tipo = models.CharField(max_length=10, choices=Documento.TIPO_CHOICES)

    @property
    def extension(self):
        return self.arquivo.name.split('.')[-1].lower() if self.arquivo else ''
      
    def mime_type(self):
        ext = self.extension
        return {
            'mp4': 'video/mp4',
            'webm': 'video/webm',
            'mp3': 'audio/mpeg',
            'wav': 'audio/wav',
        }.get(ext, f'{self.tipo}/{ext}')