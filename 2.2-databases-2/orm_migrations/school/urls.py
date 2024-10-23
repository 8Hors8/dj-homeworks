from django.urls import path, include
from django.conf import settings

from school.views import students_list

urlpatterns = [
    path('', students_list, name='students'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
