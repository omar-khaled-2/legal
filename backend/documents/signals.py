from django.db import models
from models import Document,IndexingTask
from django.db.models.signals import post_save
from django.dispatch import receiver
import boto3


sqs = boto3.resource('sqs')

@receiver(post_save, sender=Document)
def create_document(sender, instance, created, **kwargs):
    if created:
        IndexingTask.objects.create(
            document=instance
        )



@receiver(post_save, sender=IndexingTask)
def create_task(sender, instance, created, **kwargs):
    if created:
        queue = sqs.get_queue_by_name(QueueName='test')
        queue.send_message(MessageBody=instance.pk)
