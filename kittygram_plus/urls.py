from django.urls import include, path

# from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

# Зарегистрируем этот LightCatViewSet вьюсет в роутере:
# это мы добавили вьюсет и мексин во вьюху
from cats.views import CatViewSet, LightCatViewSet, OwnerViewSet


router = DefaultRouter()
router.register('cats', CatViewSet)
router.register('owners', OwnerViewSet)
#  что это за r - регулярное выражение.!!!
router.register(r'mycats', LightCatViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # добавили маршрут для получения токена
    # это дизейблим, надо было для Автотокена, теперь будем делать все на JWT
    # path('api-token-auth/', views.obtain_auth_token),
    # А теперь на JWT
    # Djoser создаст набор необходимых эндпоинтов.
    # базовые, для управления пользователями в Django:
    path('auth/', include('djoser.urls')),
    # JWT-эндпоинты, для управления JWT-токенами:
    path('auth/', include('djoser.urls.jwt')),
]
