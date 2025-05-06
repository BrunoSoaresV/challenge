import uuid
from django.db import models

class Conversation(models.Model):
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'
    STATE_CHOICES = [(OPEN, OPEN), (CLOSED, CLOSED)]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    state = models.CharField(max_length=6, choices=STATE_CHOICES, default=OPEN)

class Message(models.Model):
    SENT = 'SENT'
    RECEIVED = 'RECEIVED'
    DIR_CHOICES = [(SENT, SENT), (RECEIVED, RECEIVED)]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    direction = models.CharField(max_length=8, choices=DIR_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField()
