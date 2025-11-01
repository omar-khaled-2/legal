from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class Document(models.Model):
    STATUS_CHOICES = [
        ('uploaded', 'Uploaded'),
        ('processing', 'Processing'),
        ('indexed', 'Indexed'),
        ('failed', 'Failed'),
    ]
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(
        upload_to='documents/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx', 'txt'])]
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='uploaded'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    last_indexed_at = models.DateTimeField(null=True, blank=True)
    chunk_count = models.IntegerField(default=0)
    file_size = models.CharField(max_length=50, blank=True, null=True)
    mime_type = models.CharField(max_length=50, blank=True, null=True)
    source_url = models.URLField(blank=True, null=True)
    
    class Meta:
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['owner', '-uploaded_at']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return self.title
    
    @property
    def file_url(self):
        if self.file:
            return self.file.url
        return None


class DocumentChunk(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='chunks')
    content = models.TextField()
    content_preview = models.TextField(max_length=500)
    embedding = models.BinaryField(null=True, blank=True)
    embedding_length = models.IntegerField(default=0)
    chunk_index = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['chunk_index']
        indexes = [
            models.Index(fields=['document', 'chunk_index']),
        ]
    
    def __str__(self):
        return f"{self.document.title} - {self.pk}"


class IndexingTask(models.Model):
    TASK_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    document = models.OneToOneField(Document, on_delete=models.CASCADE, related_name='indexing_task')
    status = models.CharField(max_length=20, choices=TASK_STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Task {self.pk} - {self.document.title}"
