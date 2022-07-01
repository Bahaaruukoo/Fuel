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
from django.urls import re_path as url
from offer.views import readme, confirmation, echo, updateView, searchView, addPromotion, getOverdraw_asManager, approveAudit, getOverdraw_asAuditor, dailyBalanceWork, approve, unaudited, paymentRequests, paymentDetail
from django.contrib.auth.views import LoginView, LogoutView
from accounts import views as accounts_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [ 
    path('admin/', admin.site.urls),
    path('', searchView, name='search'),
    path('<int:pk>/<int:fuel_typ>/', updateView, name='update'),
    path('success/', echo, name='echo'),
    path('promotion/', addPromotion, name='promotion'),
    path('overdraw/', getOverdraw_asAuditor, name='overdraw'),
    #path('overfilled/', getOverdraw_asManager, name='overFilled'),
    path('overfilled/<int:id>/', getOverdraw_asManager, name='overfilledAgent'),
    path('balance/<int:id>/', dailyBalanceWork, name='balance'),
    path('approve/<int:id>/', approve, name='approve'),
    path('audit/', unaudited, name='audit'),
    url('^audit/(?P<pk>[0-9]+)/(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})$', approveAudit, name = 'approveAudit'),
    path('payments/', paymentRequests, name='payments'),
    path('payments/<int:id>', paymentDetail, name='paymentDetail'),
    path('confirmation', confirmation, name='confirmation'),
    path('addmanager/', accounts_view.addManager, name='addManager'),
    path('addstaff/<str:act>/', accounts_view.addAuditorFinance, name='addAuditorFinance'),
    path('profile/', accounts_view.profile, name='profile'),
    path('profile/<int:id>/', accounts_view.profileEditor, name='profileEditor'),
    path('register/', accounts_view.register, name='register'),
    path('agents/', accounts_view.agentList, name='agents'),
    path('addagents/', accounts_view.addAgent, name='addagents'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('readme/', readme, name='readme')
]

if settings.DEBUG:
    urlpatterns  +=  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)