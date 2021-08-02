from django.urls import path

from django.conf.urls.static import static
from django.conf import settings

from .views import MainPage
from .views import Authorization
from .views import Registration
from .views import ProjectPage


main_page = MainPage()
authorization_page = Authorization()
registration_page = Registration()
projects_page = ProjectPage()


urlpatterns = [
    path('', main_page.handle, name='main'),
    path('login/', authorization_page.handle, name='login'),
    path('signup/', registration_page.handle, name='register'),
    path('projects/<int:project_id>', projects_page.handle, name='project'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
