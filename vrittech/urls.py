"""
URL configuration for vrittech project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
router = DefaultRouter()

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Vrit Technologies",
      default_version='v1',
      description="Vrit Tech",
      terms_of_service="https://vrittechnologies.com/",
      contact=openapi.Contact(email="info@vrittechnologies.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

from accounts.routers.routers import router as accounts_router
from blog.routers.routers import router as blog_router
from career.routers.routers import router as career_router
from casestudy.routers.routers import router as casestudy_router
from clients.routers.routers import router as clients_router
from department.routers.routers import router as department_router
from emailmanagement.routers.routers import router as emailmanagement_router
from faqs.routers.routers import router as faqs_router
from gallery.routers.routers import router as gallery_router
from globalpresence.routers.routers import router as globalpresence_router
from inquires.routers.routers import router as inquires_router
from newslettersubscription.routers.routers import router as newslettersubscription_router
from plan.routers.routers import router as plan_router
from projects.routers.routers import router as projects_router
from socialmedia.routers.routers import router as socialmedia_router
from testimonial.routers.routers import router as testimonial_router
from sitesetting.routers.routers import router as sitesetting_router

router.registry.extend(accounts_router.registry)
router.registry.extend(blog_router.registry)
router.registry.extend(career_router.registry)
router.registry.extend(casestudy_router.registry)
router.registry.extend(clients_router.registry)
router.registry.extend(department_router.registry)
router.registry.extend(emailmanagement_router.registry)
router.registry.extend(faqs_router.registry)
router.registry.extend(gallery_router.registry)
router.registry.extend(globalpresence_router.registry)
router.registry.extend(inquires_router.registry)
router.registry.extend(newslettersubscription_router.registry)
router.registry.extend(plan_router.registry)
router.registry.extend(projects_router.registry)
router.registry.extend(socialmedia_router.registry)
router.registry.extend(testimonial_router.registry)
router.registry.extend(sitesetting_router.registry)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/', include('accounts.urls')),

    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

