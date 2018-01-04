from django.conf.urls import url, include
from django.contrib import admin

from polls.api import router
from polls.views import HandleMessageView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^bot/MTFjZmM5NjJjYzIyYTBlMTIzZjY4Zjk2/', HandleMessageView.as_view())
]
