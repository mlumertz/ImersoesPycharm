"""Imersoes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from Feedbacks import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete

from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', views.login, name='login'),
    url(r'^login/$', views.login, name='login'),
    url(r'^auth/$', views.auth_view),
    url(r'^logout/$', views.logout),
    url(r'^loggedin/$', views.loggedin),
    url(r'^invalid$', views.invalid_login),
    url(r'^Psicologo$', views.Psicologo_view),
    url(r'^Psicologo/novo_cliente/$', views.novo_cliente_view),
    url(r'^Psicologo/novo_usuario/$', views.novo_usuario_view),
    url(r'^Psicologo/editar_cliente/(?P<WebKey>[0-9a-z-]+)$', views.editar_cliente_view),
    url(r'^Psicologo/create/$', views.criar_novo_usuario_view),
    # url(r'^Cliente/(?P<WebKey>[0-9a-z-]+)$', views.cliente_view, name = 'cliente' ),
    url(r'^Cliente/sucesso/$', views.sucesso),
    url(r'^Indicado/(?P<WebKey>[0-9a-z-]+)$', views.indicado_view, name='indicado'),
    url(r'^pdf/(?P<WebKey>[0-9a-z-]+)$', views.create_report, name='create_report'),
    url(r'^pdf_completo/(?P<WebKey>[0-9a-z-]+)$', views.create_complete_report, name='create_complete_report'),
    url(r'^Psicologo/mudar_senha/$', views.mudar_senha_view),
    url(r'^Psicologo/perfil/$', views.perfil_view),
    url(r'^Psicologo/auth_mudar_senha/$', views.auth_mudar_senha_view),
    url(r'^password_reset/$', auth_views.password_reset, {'post_reset_redirect': '/password/reset/done/'},
        name="password_reset"),
    url(r'^password/reset/done/$', password_reset_done),
    url(r'^password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        password_reset_confirm, {'post_reset_redirect': '/password/done/'}, name='password_reset_confirm'),
    url(r'^password/done/$', password_reset_complete),
    url(r'^Cliente/(?P<WebKey>[0-9a-z-]+)$', views.cadastro_indicados_view, name='cliente'),
    url(r'^DeletarCliente/(?P<WebKey>[0-9a-z-]+)$', views.delete_cliente ),
    url(r'^nova_categoria/(?P<WebKey>[0-9a-z-]+)$', views.nova_categoria_view),
    url(r'^EmailCliente/(?P<WebKey>[0-9a-z-]+)$', views.email_cliente),
    url(r'^EmailIndicado/(?P<WebKey>[0-9a-z-]+)$', views.email_indicados),
]