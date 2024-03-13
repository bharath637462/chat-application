from rest_framework import serializers

from chat.models import Profile, ChatMessage


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'full_name', 'image']


class ChatMessageSerializer(serializers.ModelSerializer):
    receiver_profile = ProfileSerializer(read_only=True)
    sender_profile = ProfileSerializer(read_only=True)
    sender_first_name = serializers.SerializerMethodField()
    receiver_first_name = serializers.SerializerMethodField()

    class Meta:
        model = ChatMessage
        fields = ['id', 'user', 'sender', 'sender_profile', 'receiver', 'receiver_profile', 'message', 'is_read',
                  'created_at', 'sender_first_name', 'receiver_first_name']

    def get_sender_first_name(self, obj):
        return obj.sender.first_name if obj.sender else None

    def get_receiver_first_name(self, obj):
        return obj.receiver.first_name if obj.receiver else None
