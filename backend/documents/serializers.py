from rest_framework import serializers
from django.core.files.storage import default_storage
from .models import Document, DocumentChunk, IndexingTask
import os


class DocumentChunkSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentChunk
        fields = ['chunk_id', 'content_preview', 'embedding_length']
        read_only_fields = ['chunk_id', 'content_preview', 'embedding_length']


class DocumentListSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = ['id', 'title', 'file_url', 'status', 'uploaded_at', 'owner', 'chunk_count']
        read_only_fields = ['id', 'uploaded_at', 'owner', 'chunk_count']
    
    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file:
            file_url = obj.file.url
            if request:
                return request.build_absolute_uri(file_url)
            return file_url
        return None


class DocumentDetailSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = [
            'id', 'title', 'file_url', 'description', 'status', 'uploaded_at',
            'last_indexed_at', 'chunk_count', 'file_size', 'mime_type'
        ]
        read_only_fields = [
            'id', 'uploaded_at', 'last_indexed_at', 'chunk_count', 'file_size', 'mime_type'
        ]
    



class DocumentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['title', 'file', 'description']
    
    def validate_file(self, value):
        """Validate file type and size"""
        # Check file extension
        allowed_extensions = ['pdf', 'docx', 'txt']
        ext = os.path.splitext(value.name)[1][1:].lower()
        
        if ext not in allowed_extensions:
            raise serializers.ValidationError(
                f"Unsupported file type. Only {', '.join(allowed_extensions).upper()} allowed."
            )
        

        if value.size > 50 * 1024 * 1024:
            raise serializers.ValidationError("File size must not exceed 50MB.")
        
        return value
    
    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        
        file_obj = validated_data['file']
        ext = os.path.splitext(file_obj.name)[1][1:].lower()
        mime_types = {
            'pdf': 'application/pdf',
            'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'txt': 'text/plain'
        }
        validated_data['mime_type'] = mime_types.get(ext, 'application/octet-stream')
        

        validated_data['file_size'] = self._format_file_size(file_obj.size)
        
        return super().create(validated_data)
    
    @staticmethod
    def _format_file_size(size_bytes):
        """Convert bytes to human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"


class DocumentUploadByUrlSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    url = serializers.URLField()
    description = serializers.CharField(required=False, allow_blank=True)
    
    def validate_url(self, value):
        """Validate that the URL points to a valid document"""
        # Check if URL ends with allowed extensions
        allowed_extensions = ['pdf', 'docx', 'txt']
        url_lower = value.lower()
        
        if not any(url_lower.endswith(ext) for ext in allowed_extensions):
            raise serializers.ValidationError(
                f"URL must point to a {', '.join(allowed_extensions).upper()} file."
            )
        
        return value


class IndexingTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndexingTask
        fields = ['task_id', 'status', 'error_message']
        read_only_fields = ['task_id', 'status', 'error_message']


class DocumentUploadResponseSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = ['id', 'title', 'file_url', 'status', 'uploaded_at', 'owner']
        read_only_fields = ['id', 'uploaded_at', 'owner']
    
    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file:
            file_url = obj.file.url
            if request:
                return request.build_absolute_uri(file_url)
            return file_url
        return None


class IndexingResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    document_id = serializers.IntegerField()
    task_id = serializers.CharField()
    status = serializers.CharField()