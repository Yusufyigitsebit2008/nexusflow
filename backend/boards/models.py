import uuid
import os
from django.db import models
from django.conf import settings 
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class TimeStampedModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Workspace(TimeStampedModel):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='owned_workspaces'
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='workspaces',
        blank=True
    )

    def __str__(self):
        return self.name

class Board(TimeStampedModel):
    workspace = models.ForeignKey(
        Workspace, 
        on_delete=models.CASCADE, 
        related_name='boards'
    )
    name = models.CharField(max_length=100)
    background_image = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class List(TimeStampedModel):
    board = models.ForeignKey(
        Board, 
        on_delete=models.CASCADE, 
        related_name='lists'
    )
    title = models.CharField(max_length=100)
    position = models.FloatField(default=65535)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.title
    
    # Sinyaller için gerekli yardımcı metod
    def get_content_type_obj(self):
        return ContentType.objects.get_for_model(self)

class Card(TimeStampedModel):
    PRIORITY_CHOICES = [
        ('low', 'Düşük'),
        ('medium', 'Orta'),
        ('high', 'Yüksek'),
        ('urgent', 'Acil'),
    ]
    labels = models.JSONField(default=list, blank=True)
    list = models.ForeignKey(
        List, 
        on_delete=models.CASCADE, 
        related_name='cards'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    position = models.FloatField(default=65535) 
    assignees = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='assigned_cards',
        blank=True
    )
    
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    due_date = models.DateTimeField(null=True, blank=True)
    is_ai_generated = models.BooleanField(default=False)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.title

    # Sinyaller için gerekli yardımcı metod
    def get_content_type_obj(self):
        return ContentType.objects.get_for_model(self)

class Comment(TimeStampedModel):
    card = models.ForeignKey(
        Card, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    text = models.TextField()

    class Meta:
        ordering = ['created_at'] 

    def __str__(self):
        return f"{self.author.username}: {self.text[:20]}"
    
    # Sinyaller için gerekli yardımcı metod
    def get_content_type_obj(self):
        return ContentType.objects.get_for_model(self)

class Attachment(models.Model):
    card = models.ForeignKey(Card, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to='attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"File for {self.card.title}"
    
    @property
    def filename(self):
        return os.path.basename(self.file.name)

    # Sinyaller için gerekli yardımcı metod
    def get_content_type_obj(self):
        return ContentType.objects.get_for_model(self)

class ChecklistItem(models.Model):
    card = models.ForeignKey(Card, related_name='checklist_items', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} ({'Done' if self.is_done else 'Todo'})"

class Activity(models.Model):
    # DÜZELTME: User yerine settings.AUTH_USER_MODEL kullandık
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    action_type = models.CharField(max_length=50) 
    
    # Hangi nesne üzerinde? (Burada büyü yapıyoruz: GenericForeignKey)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    target = GenericForeignKey('content_type', 'object_id')
    
    # Hangi panoda oldu?
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='activities')
    
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at'] 

    def __str__(self):
        return f"{self.actor.username} {self.action_type}"