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
from django.urls import include, re_path
from Feedbacks import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView,PasswordResetCompleteView

from django.contrib.auth import views as auth_views

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),

    re_path(r'^$', views.login, name='login'),
    re_path(r'^login/$', views.login, name='login'),
    re_path(r'^auth/$', views.auth_view),
    re_path(r'^logout/$', views.logout),
    re_path(r'^loggedin/$', views.loggedin),
    re_path(r'^invalid$', views.invalid_login),
    re_path(r'^Psicologo$', views.Psicologo_view),
    re_path(r'^Psicologo/novo_cliente/$', views.novo_cliente_view),
    re_path(r'^Psicologo/novo_usuario/$', views.novo_usuario_view),
    re_path(r'^Psicologo/editar_cliente/(?P<WebKey>[0-9a-z-]+)$', views.editar_cliente_view),
    re_path(r'^Psicologo/create/$', views.criar_novo_usuario_view),
    # re_path(r'^Cliente/(?P<WebKey>[0-9a-z-]+)$', views.cliente_view, name = 'cliente' ),
    re_path(r'^Cliente/sucesso/$', views.sucesso),
    re_path(r'^Cliente/sucesso_indicado/$', views.sucesso_indicado),
    re_path(r'^Indicado/(?P<WebKey>[0-9a-z-]+)$', views.indicado_view, name='indicado'),
    re_path(r'^pdf/(?P<WebKey>[0-9a-z-]+)$', views.create_report, name='create_report'),
    re_path(r'^pdf_completo/(?P<WebKey>[0-9a-z-]+)$', views.create_complete_report, name='create_compmidrlete_report'),
    re_path(r'^Psicologo/mudar_senha/$', views.mudar_senha_view),
    re_path(r'^Psicologo/perfil/$', views.perfil_view),
    re_path(r'^Psicologo/auth_mudar_senha/$', views.auth_mudar_senha_view),

    re_path(r'^password_reset/$', auth_views.PasswordResetView.as_view(), {'template_name': 'registration/password_reset_form.html'},
        name="password_reset"),
    re_path(r'^password/reset/done/$', auth_views.PasswordResetDoneView.as_view(), {'template_name': 'registration/password_reset_done.html'}, name='password_reset_done'),
    re_path(r'^password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.PasswordResetConfirmView.as_view(), {'post_reset_redirect': '/password/done/', 'template_name': 'registration/password_reset_confirm.html'}, name='password_reset_confirm'),
    re_path(r'^password/done/$', auth_views.PasswordResetCompleteView.as_view(), {'template_name': 'registration/password_reset_complete.html'}, name='password_reset_complete'),

    re_path(r'^Cliente/(?P<WebKey>[0-9a-z-]+)$', views.cadastro_indicados_view, name='cliente'),
    re_path(r'^DeletarCliente/(?P<WebKey>[0-9a-z-]+)$', views.delete_cliente ),
    re_path(r'^nova_categoria/(?P<WebKey>[0-9a-z-]+)$', views.nova_categoria_view),
    re_path(r'^EmailCliente/(?P<WebKey>[0-9a-z-]+)$', views.email_cliente),
    re_path(r'^EmailIndicado/(?P<WebKey>[0-9a-z-]+)$', views.email_indicados),
]