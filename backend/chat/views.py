import sys

from django.db.models import Subquery, Q, OuterRef

from chat.models import ChatMessage, User, Profile
from chat.serializer import ChatMessageSerializer, ProfileSerializer

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from chat.utills import error_logger


class MyInbox(generics.ListAPIView):
    serializer_class = ChatMessageSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            a = 5 / 0
        except Exception as e:
            error_logger(e, sys.exc_info())
        user_id = self.kwargs['user_id']
        messages = ChatMessage.objects.filter(
            id__in=Subquery(
            User.objects.filter(
                Q(sender__receiver=user_id) | Q(receiver__sender=user_id)
            ).distinct().annotate(
                last_msg=Subquery(
                    ChatMessage.objects.filter(
                        Q(sender=OuterRef('id'), receiver=user_id)|
                        Q(receiver=OuterRef('id'), sender=user_id)
                    ).order_by('-id')[:1].values_list('id', flat=True)
                )
            ).values_list('last_msg', flat=True).order_by('id')
        )
    ).order_by('-id')
        return  messages

class GetMessages(generics.ListAPIView):
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        sender_id = self.kwargs['sender_id']
        receiver_id = self.kwargs['receiver_id']

        messages = ChatMessage.objects.filter(
            sender__in=[sender_id, receiver_id],
            receiver__in=[sender_id, receiver_id]
        )
        return messages

class SendMessage(generics.CreateAPIView):
    serializer_class = ChatMessageSerializer


class ProfileDetail(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]


class SearchUser(generics.ListAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        username = self.kwargs['username']
        logged_in_user = self.request.user
        users = Profile.objects.filter(
            Q(user__username__icontains=username) | Q(full_name__icontains=username) |
            Q(email__icontains=username) & ~Q(user=logged_in_user)
        )

        if not users.exists():
            return Response(
                {"detail": "No Users Found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)


