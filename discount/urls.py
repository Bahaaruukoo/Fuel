"""discount URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from offer.views import updateView, searchView, addPromotion, getOverdraw_asStaff, getOverdraw_asManager
from django.contrib.auth.views import LoginView, LogoutView
from accounts import views as accounts_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [ 
    path('admin/', admin.site.urls),
    path('', searchView, name='search'),
    path('<int:pk>/', updateView, name='update'),
    path('promotion/', addPromotion, name='promotion'),
    path('overdraw/', getOverdraw_asStaff, name='overdraw'),
    path('overfilled/', getOverdraw_asManager, name='overFilled'),
    path('addmanager/', accounts_view.addManager, name='addManager'),
    path('profile/', accounts_view.profile, name='profile'),
    path('profile/<int:id>/', accounts_view.profileEditor, name='profileEditor'),
    path('register/', accounts_view.register, name='register'),
    path('agents/', accounts_view.agentList, name='agents'),
    path('addagents/', accounts_view.addAgent, name='addagents'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    
]

if settings.DEBUG:
    urlpatterns  +=  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)