from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
import uuid
import requests
from io import BytesIO
from celery import shared_task
import os

from .models import Document, DocumentChunk, IndexingTask
from .serializers import (
    DocumentListSerializer,
    DocumentDetailSerializer,
    DocumentCreateSerializer,
    DocumentUploadByUrlSerializer,
    DocumentChunkSerializer,
    IndexingTaskSerializer,
    IndexingResponseSerializer,
    DocumentUploadResponseSerializer,
)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Custom permission to allow document owners to edit their documents."""
    
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class DocumentViewSet(viewsets.ModelViewSet):
    
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['uploaded_at', 'title']
    ordering = ['-uploaded_at']
    
    def get_queryset(self):
        return Document.objects.filter(owner=self.request.user)
    
    def get_serializer_class(self):
    
        if self.action == 'create':
            return DocumentCreateSerializer
        elif self.action == 'retrieve':
            return DocumentDetailSerializer
        elif self.action == 'list':
            return DocumentListSerializer
        elif self.action == 'upload_by_url':
            return DocumentUploadByUrlSerializer
        return DocumentDetailSerializer
    
    # 1. List all documents
    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {'detail': f'Error retrieving documents: {str(e)}'}
                ,status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            
            output_serializer = DocumentUploadResponseSerializer(
                serializer.instance,
                context={'request': request}
            )
            return Response(
                output_serializer.data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'detail': f'Error uploading document: {str(e)}'}
                ,status=status.HTTP_400_BAD_REQUEST
            )
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {'detail': 'Document not found.'}
                ,status=status.HTTP_404_NOT_FOUND
            )
    

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(
                {'detail': 'Document not found.'}
                ,status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'], url_path='index')
    def index(self, request, pk=None):

        document = self.get_object()
        
        if document.status == 'processing':
            return Response(
                {'message': 'Document is already being indexed.'},
                status=status.HTTP_409_CONFLICT
            )
        
        try:
            task_id = str(uuid.uuid4())
            indexing_task = IndexingTask.objects.create(
                document=document,
                task_id=task_id,
                status='pending'
            )
            
            # Update document status
            document.status = 'processing'
            document.save(update_fields=['status'])
            
            # Trigger async indexing task (Celery would be used in production)
            # For now, we'll create a placeholder
            # In production: index_document_task.delay(document.id, task_id)
            
            serializer = IndexingResponseSerializer({
                'message': 'Indexing started.',
                'document_id': document.id,
                'task_id': task_id,
                'status': 'processing'
            })
            
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        
        except IndexingTask.DoesNotExist:
            return Response(
                {'message': 'Document is already being indexed.'},
                status=status.HTTP_409_CONFLICT
            )
        except Exception as e:
            document.status = 'failed'
            document.save(update_fields=['status'])
            return Response(
                {'detail': f'Error starting indexing: {str(e)}'}
                ,status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'], url_path='chunks')
    def chunks(self, request, pk=None):

        document = self.get_object()
        
        if document.status != 'indexed':
            return Response(
                {'detail': 'Document not found or not yet indexed.'}
                ,status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            chunks = document.chunks.all()
            page = self.paginate_queryset(chunks)
            
            if page is not None:
                serializer = DocumentChunkSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = DocumentChunkSerializer(chunks, many=True)
            return Response({
                'count': chunks.count(),
                'results': serializer.data
            })
        except Exception as e:
            return Response(
                {'detail': f'Error retrieving chunks: {str(e)}'}
                ,status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
