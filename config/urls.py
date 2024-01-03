
from django.contrib import admin
from django.contrib.auth.views import LoginView

from django.urls import path,include
from home.views import home,GroupMonthArchiveView, StudentViewSet, my_login, my_logout, workers_profile
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')

urlpatterns = [ 
    path("__debug__/", include("debug_toolbar.urls")),

    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('profile/', workers_profile, name='workers_profile'),
    
    path('', my_login, name='login'),
    path('my_logout/', my_logout, name='my_logout'),
    path('home',home,name='homePage'),
    path('admins/',include('admins.urls')),
    path('income/',include('income.urls')),
    path('attendance/',include('attendance.urls')),
    path('boshliq/',include('boshliq.urls')),
    path('teacher/',include('teacher.urls')),
    path('groups/<int:year>/<int:month>/', GroupMonthArchiveView.as_view(), name='group_month_archive'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
