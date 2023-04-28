from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import *

router = SimpleRouter()
router.register('reco', RecommendationViewSet)
router.register('proc', ProcedureViewSet)
router.register('user', UsersViewSet)
router.register('userprocedure', UserProcedureViewSet)
# router.register('avaliacoes', AvaliacaoViewSet)


urlpatterns = [
    # path('reco/', RecommendationViewSet.as_view(), name='reco'),

]