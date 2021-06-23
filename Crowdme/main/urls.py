from django.urls import path

from django.conf.urls.static import static
from django.conf import settings

from .views import MainPage
from .views import Authorization
from .views import Registration
from .views import ClientsSettingsPage
from .views import ProjectPage
from .views import PageTest


main_page = MainPage()
authorization_page = Authorization()
registration_page = Registration()
clients_settings = ClientsSettingsPage()
projects_page = ProjectPage()
test_page = PageTest()


urlpatterns = [
    path('', main_page.handle, name='main'),
    path('login/', authorization_page.handle, name='login'),
    path('signup/', registration_page.handle, name='register'),
    path('settings/<slug:user_name>', clients_settings.handle, name='user_settings'),
    path('projects/<int:project_id>', projects_page.handle, name='project'),
    path('request', test_page.handle, name='test')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
