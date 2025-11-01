from django.contrib import admin
from .models import Document, DocumentChunk, IndexingTask


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'status', 'uploaded_at', 'chunk_count']
    list_filter = ['status', 'uploaded_at', 'owner']
    search_fields = ['title', 'description', 'owner__email']
    readonly_fields = ['uploaded_at','status', 'last_indexed_at', 'chunk_count', 'file_size', 'mime_type']
    fields = [
        'owner',
        'title',
        'description',
        'file',
        'status',
        'uploaded_at',
        'last_indexed_at',
        'chunk_count',
        'file_size',
        'mime_type',
        'source_url',
    ]
    ordering = ['-uploaded_at']


@admin.register(DocumentChunk)
class DocumentChunkAdmin(admin.ModelAdmin):
    list_display = ['chunk_id', 'document', 'chunk_index', 'embedding_length']
    list_filter = ['document', 'created_at']
    search_fields = ['chunk_id', 'content', 'document__title']
    readonly_fields = ['chunk_id', 'created_at', 'embedding_length']
    fields = [
        'document',
        'chunk_id',
        'chunk_index',
        'content_preview',
        'embedding_length',
        'created_at',
    ]
    ordering = ['document', 'chunk_index']


@admin.register(IndexingTask)
class IndexingTaskAdmin(admin.ModelAdmin):
    list_display = ['task_id', 'document', 'status', 'created_at', 'completed_at']
    list_filter = ['status', 'created_at']
    search_fields = ['task_id', 'document__title']
    readonly_fields = ['task_id', 'created_at', 'completed_at']
    fields = [
        'task_id',
        'document',
        'status',
        'error_message',
        'created_at',
        'completed_at',
    ]
    ordering = ['-created_at']
