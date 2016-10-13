from django.conf.urls import url, include


urlpatterns = [
    url(r'^podcast/', include('podcast.urls', namespace='podcast')),
]
