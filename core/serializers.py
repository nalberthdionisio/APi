from rest_framework import serializers
from django.utils import timezone
from .models import *


class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = '__all__'

class ProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedure
        fields = '__all__'

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

class UserProcedureSerializer(serializers.ModelSerializer):
    message = serializers.CharField(read_only=True)

    class Meta:
        model = UserProcedure
        fields = ['id', 'done', 'date_limit', 'date_done', 'notified', 'user', 'procedure', 'message']

    def to_representation(self, instance):
        if instance.date_limit <= timezone.now().date() + timezone.timedelta(days=3):
            representation = super().to_representation(instance)
            representation['message'] = f'Olá {instance.user.username}, seu procedimento {instance.procedure.title} está próximo do prazo final ({instance.date_limit}).'
            return representation
        else:
            representation = super().to_representation(instance)
            return representation
