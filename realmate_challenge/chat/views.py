from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Conversation, Message
from .serializers import ConversationSerializer, ConversationListSerializer
from django.db import IntegrityError # Importar IntegrityError

class WebhookView(APIView):
    def post(self, request):
        evt = request.data
        etype = evt.get('type')
        data = evt.get('data', {})
        try:
            if etype == 'NEW_CONVERSATION':
                # Adicionar verificação de timestamp se necessário para o modelo Conversation
                Conversation.objects.create(id=data['id'])
            elif etype == 'NEW_MESSAGE':
                conv = get_object_or_404(Conversation, id=data['conversation_id'])
                if conv.state != Conversation.OPEN:
                    return Response({'error': 'Conversation closed'}, status=status.HTTP_400_BAD_REQUEST)
                
                # Garantir que o timestamp está presente no payload do evento NEW_MESSAGE
                timestamp = evt.get('timestamp')
                if not timestamp:
                    return Response({'error': 'Timestamp missing for new message'}, status=status.HTTP_400_BAD_REQUEST)

                Message.objects.create(
                    id=data['id'],
                    conversation=conv,
                    direction=data['direction'],
                    content=data['content'],
                    timestamp=timestamp # Usar o timestamp validado
                )
            elif etype == 'CLOSE_CONVERSATION':
                conv = get_object_or_404(Conversation, id=data['id'])
                conv.state = Conversation.CLOSED
                conv.save()
            else:
                return Response({'error': 'Unknown event type'}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({'message': f'Event {etype} processed successfully'}, status=status.HTTP_200_OK)

        except KeyError as e:
            return Response({'error': f'Invalid payload: missing key {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            # Ex: ID duplicado para Conversation ou Message
            return Response({'error': f'Database integrity error: {str(e)}'}, status=status.HTTP_409_CONFLICT) # 409 Conflict é mais apropriado
        except Conversation.DoesNotExist: # Especificamente para get_object_or_404 em Conversation
            return Response({'error': 'Conversation not found for new message'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Logar a exceção e retornar um erro genérico para o cliente
            # import logging
            # logging.error(f"Unexpected error in WebhookView: {str(e)}")
            return Response({'error': 'An unexpected error occurred on the server.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ConversationListView(APIView):
    def get(self, request):
        qs = Conversation.objects.all().order_by('id')
        ser = ConversationListSerializer(qs, many=True)
        return Response(ser.data)

class ConversationDetail(APIView):
    def get(self, request, id):
        conv = get_object_or_404(Conversation, id=id)
        ser = ConversationSerializer(conv)
        return Response(ser.data)
