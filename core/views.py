from rest_framework import generics, viewsets
from rest_framework.response import Response
from django.db.models.signals import post_save, pre_save
from rest_framework.decorators import action
from django.utils import timezone
from django.dispatch import receiver
from .models import *
from .serializers import *
from django.utils import timezone
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status

from .models import UserProcedure
from .serializers import UserProcedureSerializer


class RecommendationViewSet(viewsets.ModelViewSet):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer

class ProcedureViewSet(viewsets.ModelViewSet):
    queryset = Procedure.objects.all()
    serializer_class = ProcedureSerializer

class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

class UserProcedureViewSet(viewsets.ModelViewSet):
    serializer_class = UserProcedureSerializer
    queryset = UserProcedure.objects.all()

    @action(detail=False, methods=['get'])
    def upcoming_procedures(self, request):
        procedures = UserProcedure.objects.filter(date_limit__lte=timezone.now().date() + timezone.timedelta(days=3))
        message = ''
        for procedure in procedures:
            message += f'Olá {procedure.user.username}, seu procedimento {procedure.procedure.title} está próximo do prazo final ({procedure.date_limit}).\n'
            procedure.notified = True
            procedure.save()
        return Response({'message': message})

@receiver(post_save, sender=UserProcedure)
def atualizar_data(sender, instance, **kwargs):
    if instance.done:
        new_date = timezone.now()
        UserProcedure.objects.filter(pk=instance.pk).update(date_done=new_date)

@receiver(pre_save, sender=UserProcedure)
def reset_date_done(sender, instance, **kwargs):
    if not instance.done and instance.pk:
        original = UserProcedure.objects.get(pk=instance.pk)
        if original.done:
            instance.date_done = None

@receiver(post_save, sender=UserProcedure)
def notify_user(sender, instance, **kwargs):
    if instance.date_limit <= timezone.now().date() + timezone.timedelta(days=3):
        user = instance.user
        message = f'Olá {user.username}, seu procedimento {instance.procedure.title} está próximo do prazo final ({instance.date_limit}).'
        print(f'Notificação enviada para o usuário {user.username}: {message}')
        post_save.disconnect(notify_user, sender=UserProcedure)

        instance.notified = True
        instance.save()
        post_save.connect(notify_user, sender=UserProcedure)
        return Response({'message': message}, status=200)
