# -*- coding: UTF-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.template import Context

from django.template.loader import render_to_string, get_template

from django.contrib import auth
from django.template import loader
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from .models import *
from .form import *
from django.core.mail import EmailMessage
from django.conf import settings
from django.forms import inlineformset_factory
from django.forms import formset_factory
from django.views.generic.edit import UpdateView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from datetime import date

import reportlab
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch, cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen.canvas import Canvas
from io import BytesIO

from django.templatetags.static import static



# Create your views here.
pagina = 'http://feedback360pro.web1f17.kinghost.net/'
email_dominio = ' @braincon.com.br'

def login(request):
    if request.user.is_authenticated:
        update_StatusDeadline(request.user) #TODO mudar depois !!! usar cron
        return HttpResponseRedirect('/Psicologo')
    c = {'invalid': False}
    c.update(csrf(request))
    return render(None, 'login.html', c)


def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/Psicologo')

    else:
        c = {'invalid': True}
        c.update(csrf(request))
        return render(None, "login.html", c)  # our template can detect this variable
        #return HttpResponseRedirect('/invalid')

def novo_usuario_view(request):
    c = {}
    c.update(csrf(request))
    return render(None, 'new_user.html', c)

def criar_novo_usuario_view(request):

    username = request.POST.get('username', '')
    nome = request.POST.get('nome', '')
    usuario = User.objects.filter(username = username)


    if not usuario.exists() :
        mail = username + email_dominio
        password = User.objects.make_random_password(length=5, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
        usuario = User.objects.create_user(username, mail, password)

        responsavel  = Responsavel.objects.create(DjangoUser=usuario, Nome=nome)

        subject = 'Registro em WMP'

        mensagem = u"Caro %s, \n \n Você cadastrou com sucesso seu usuário no sistema FEED! \n \n Nome de usuário:  %s\n Senha: %s \n \n Por favor acesse:  %slogin/ \n" % (responsavel.Nome, usuario.username, password, pagina)

        email = EmailMessage(subject, mensagem, settings.EMAIL_HOST_USER, [usuario.email])
        email.send()

        return render(None, 'loading_page.html') #TODO pagina de sucesso no registro

    else:
        return HttpResponseRedirect('/invalid') #TODO pagina de registro invalido

@login_required
def mudar_senha_view(request):
    template = loader.get_template('MudarSenha.html')
    context = {
        'user': request.user
    }
    return render(request, 'MudarSenha.html', context)


@login_required
def auth_mudar_senha_view(request):
    password = request.POST.get('password', '')
    NewPassword = request.POST.get('NewPassword', '')
    NewPassword2 = request.POST.get('NewPassword2', '')
    # user = auth.authenticate(username=username, password=password)

    CheckUser = auth.authenticate(username=request.user.username, password=password)
    if CheckUser is not None:
        if (NewPassword == NewPassword2):
            request.user.set_password(NewPassword)
            request.user.save()
            return HttpResponseRedirect('/Psicologo')

    messages = "Senha invalida, tente novamente"
    context = {
        'message': messages
    }
    return render(request, 'MudarSenha.html', context)


def loggedin(request):
    return render(None, 'loggedin.html',
                              {'full_name': request.user.username})


def invalid_login(request):
    return render(None, 'invalid_login.html')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


@login_required
def Psicologo_view(request):
    template = loader.get_template('Psicologo.html')

    perfil, created = Responsavel.objects.get_or_create(DjangoUser=request.user)

    clientes = Cliente.objects.filter(Orientador=request.user)

    for client in clientes:
        indicados  = Indicado.objects.filter(cliente=client)
        allCount = 0.0
        doneCount = 0.0
        for indic in indicados:
            if (indic.Status):
                doneCount = doneCount+1

            allCount = allCount+1
        if allCount == 0:
            client.ProgressBar = 0
        else:
            client.ProgressBar = (doneCount/allCount) * 100

        client.save()

    context = {
        'perfil': perfil,
        'user': request.user,
        'clientes': Cliente.objects.filter(Orientador=request.user)
    }

    return HttpResponse(template.render(context, request))


@login_required
def novo_cliente_view(request):

    form = ClienteForm(request.user, request.POST or None)

    if request.method == 'POST':

        if form.is_valid():
            cliente = form.save()

            ct1 = Categoria(cat="Amigos", cliente=cliente)
            ct1.save()
            ct2 = Categoria(cat="Família", cliente=cliente)
            ct2.save()
            ct3 = Categoria(cat="Universidade", cliente=cliente)
            ct3.save()
            ct4 = Categoria(cat="Trabalho", cliente=cliente)
            ct4.save()

            email_cliente(request, cliente.WebKey)

            return HttpResponseRedirect('/Psicologo')

    args = {}
    args.update(csrf(request))
    args['form'] = form
    return render(None, 'novo_cliente.html', args)

@login_required
def editar_cliente_view(request, WebKey):

    cliente = get_object_or_404(Cliente, WebKey=WebKey)
    form = EditClienteForm(request.POST or None, instance=cliente)


    if request.method == 'POST':

        if form.is_valid():
            cliente = form.save()

            email_cliente(request, cliente.WebKey)

            return HttpResponseRedirect('/Psicologo')

    args = {}
    args.update(csrf(request))
    args['form'] = form
    args['cliente'] = cliente
    return render(None, 'edit_cliente.html', args)

@login_required
def perfil_view(request):

    djangoU = request.user

    responsavel, created = Responsavel.objects.get_or_create(DjangoUser=djangoU)


    form = ResponsavelForm(request.POST or None, instance=responsavel)

    if request.method == 'POST':

        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/Psicologo')

    args = {}
    args.update(csrf(request))
    args['form'] = form
    args['user'] = djangoU

    return render(None, 'profile.html', args)

def sucesso(request):

    return render(None, 'sucesso.html')

def sucesso_indicado(request):
    return render(None,'sucesso_indicado.html')

def indicado_view(request, WebKey):

    indicado = get_object_or_404(Indicado, WebKey=WebKey)
    cliente = indicado.cliente

    if cliente.Deadline < date.today():
        return render(None, 'DeadlineAtingido.html')

    psicologo = cliente.Orientador
    perfil, created = Responsavel.objects.get_or_create(DjangoUser=psicologo)

    if request.method == 'POST':
        form = IndicadoPageForm(request.POST, instance=indicado)

        if form.is_valid():
            indicado = form.save()
            indicado.Status = True
            indicado.save()
            return render(None, 'sucesso_indicado.html')

    else:
        args = {}
        args.update(csrf(request))
        args['form'] = IndicadoPageForm(instance=indicado)
        args['indicado'] = indicado
        args['cliente'] = cliente
        args['perfil'] = perfil
        args['psicologo'] = psicologo
        return render(None, 'indicado.html', args)


def cadastro_indicados_view(request, WebKey):

    cliente = get_object_or_404(Cliente, WebKey=WebKey)
    psicologo = cliente.Orientador
    perfil, created = Responsavel.objects.get_or_create(DjangoUser=psicologo)

    path = '/Cliente/%s' % WebKey

    if cliente.Deadline < date.today():
        return render(None, 'DeadlineAtingido.html')

    if cliente.Status:
        return render(None, 'sucesso.html')


    cliente_formsetFactory = inlineformset_factory(Cliente, Indicado, form=IndicadoForm, extra=0, min_num=3, validate_min=True,)
    formset = cliente_formsetFactory(request.POST or None, instance=cliente, form_kwargs={'cliente': cliente})
    categoria = CategoriaInputForm( request.POST or None)
    DoNotCheck = False

    if request.method == 'POST':

        if 'Categoria' in request.POST:
            if categoria.is_valid():
                cat = categoria.save(commit=False)
                cat.cliente = cliente
                cat.save()
                categoria = CategoriaInputForm()
                DoNotCheck = True

        else:
            if formset.is_valid():
                indicados = formset.save()
                # path = '/Cliente/%s' % WebKey
                cliente.Status = formset.is_valid()
                cliente.save()
                email_indicados(request, cliente.WebKey)
                return render(None, 'sucesso.html')
                DoNotCheck = False


    args = {}
    args.update(csrf(request))
    args['formset'] = formset
    args['categoria'] = categoria
    args['cliente'] = cliente
    args['responsavel'] = psicologo
    args['perfil'] = perfil
    args['DoNotCheck'] =  DoNotCheck

    return render(None, 'cadastro_indicados.html', args)

@login_required
def delete_cliente (request, WebKey):

    cliente = get_object_or_404(Cliente, WebKey=WebKey)
    cliente.delete()

    return HttpResponseRedirect('/Psicologo')


@login_required
def lembrete_cliente (request, WebKey):

    cliente = get_object_or_404(Cliente, WebKey=WebKey)
    email_cliente(cliente)

    return HttpResponseRedirect('/Psicologo')




## envia email de confirmacao para orientador
# def email_conf_orientador(cliente)

## envia email de confirmação para cliente
# def email_conf_cliente(cliente)

## envia email com a página para cliente
def email_cliente(request, WebKey):


    cliente = get_object_or_404(Cliente, WebKey=WebKey)
    psicologo, created = Responsavel.objects.get_or_create(DjangoUser=cliente.Orientador)

    ctx ={
        'cliente': cliente.Nome,
        'responsavel': psicologo.Nome,
        'link': pagina + 'Cliente/' + str(cliente.WebKey),
        'coaching': cliente.FeedbackNome,
        'data': cliente.Deadline,
    }

    subject = 'WMFB - Processo de Feedback'
    template = get_template('email_cliente.html')
    message = template.render(ctx)

    email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [cliente.Email])
    email.content_subtype = 'html'
    email.send()

    return HttpResponseRedirect('/Psicologo')


## envia email com a página para os indicados
def email_indicados(request, WebKey):

    cliente = get_object_or_404(Cliente, WebKey=WebKey)
    psicologo, created = Responsavel.objects.get_or_create(DjangoUser=cliente.Orientador)

    indicados = Indicado.objects.filter(cliente=cliente)
    subject = 'WMFB - Processo de Feedback'
    template = get_template('email_indicado.html')

    for indicado in indicados:

        ctx = {
            'indicado': indicado.Nome,
            'cliente': cliente.Nome,
            'responsavel': psicologo.Nome,
            'coaching': cliente.FeedbackNome,
            'link': pagina + 'Indicado/' + str(indicado.WebKey),
            'data': cliente.Deadline,
        }

        message = template.render(ctx)

        email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [indicado.Email])
        email.content_subtype = 'html'
        email.send()

    return render(None, 'sucesso.html')


def nova_categoria_view(request, WebKey):

    path = '/Cliente/%s' % WebKey
    cl = get_object_or_404(Cliente, WebKey=WebKey)

    if request.method == 'POST':
        categoria = CategoriaInputForm(request.POST)

        if categoria.is_valid():
            cat = categoria.save(commit=False)
            cat.cliente = cl
            cat.save()
            return HttpResponseRedirect(path)

    return HttpResponseRedirect(path)

def update_StatusDeadline(user):

    clientes = Cliente.objects.filter(Orientador=user).filter(StatusDeadline=False)

    for cliente in clientes:
        if cliente.Deadline < date.today():
            cliente.StatusDeadline=True
            cliente.save()

def create_report(request, WebKey):

    cliente = get_object_or_404(Cliente, WebKey=WebKey)
    pdfName = "relatorio_anonimo_cliente_%s.pdf" % cliente.Nome

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=%s' % pdfName

    buff = BytesIO()
    # Create the PDF object, using the response object as its "file."

    menu_pdf = SimpleDocTemplate(buff, pagesize=letter, rightMargin=72,
                                 leftMargin=72, topMargin=40, bottomMargin=18)


    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='justify', alignment=TA_JUSTIFY))


    responsavel = Responsavel.objects.get(DjangoUser=cliente.Orientador)


    # container for pdf elements
    elements = []

    # logo = settings.STATIC_ROOT + 'images/wmfb.png'
    # im = Image(logo, 2 * cm, 2 * cm, hAlign='LEFT')
    # elements.append(im)

    elements.append(Spacer(1, 10))
    elements.append(Paragraph("Relatório da Atividade Feedback", styles["Title"]))
    elements.append(Spacer(1, 25))
    elements.append(Paragraph("<b> Orientador: </b>%s" % responsavel.Nome, styles["Normal"]))
    elements.append(Paragraph("<b>Cliente: </b>%s" % cliente.Nome, styles["Normal"]))
    elements.append(Paragraph("<b>Tipo de Feedback: </b>%s" % cliente.TipoDeFeedback, styles["Normal"]))
    elements.append(Paragraph("<b>Nome da Atividade de Feedback: </b>%s" % cliente.FeedbackNome, styles["Normal"]))
    elements.append(Paragraph("<b>Data: </b>%s" % cliente.Deadline.strftime('%d/%m/%y'), styles["Normal"]))
    elements.append(Spacer(1, 25))
    elements.append(Paragraph("01. %s" % cliente.Pergunta1, styles["Heading5"]))

    categs = Categoria.objects.filter(cliente = cliente)

    for categ in categs:
        ind_categoria = Indicado.objects.filter(Categ=categ)
        if ind_categoria.exists():
            total = ind_categoria.filter(Status=True).count()
            elements.append(Spacer(1, 8))
            elements.append(Paragraph("%s (%s respostas)" % (categ.cat, total),
                                      styles["Normal"]))

            for ind in ind_categoria:
                elements.append(Paragraph("%s" %ind.Resposta1,
                styles["Code"]))


    elements.append(Spacer(1, 12))
    elements.append(Paragraph("02. %s" %cliente.Pergunta2, styles["Heading5"]))


    for categ in categs:
        ind_categoria = Indicado.objects.filter(Categ=categ)
        if ind_categoria.exists():
            total = ind_categoria.filter(Status=True).count()
            elements.append(Spacer(1, 8))
            elements.append(Paragraph("%s (%s respostas)" % (categ.cat, total),
                                      styles["Normal"]))
            for ind in ind_categoria:
                elements.append(Paragraph("%s" % ind.Resposta2,
                                          styles["Code"]))

    elements.append(Spacer(1, 18))
    total = Indicado.objects.filter(Status=True, cliente=cliente).count()
    elements.append(Paragraph("<b>Total de Partipantes: </b>%s" % total, styles["Normal"]))
    menu_pdf.build(elements)
    response.write(buff.getvalue())
    buff.close()
    return response

def create_complete_report(request, WebKey):

    cliente = get_object_or_404(Cliente, WebKey=WebKey)
    pdfName = "relatorio_completo_cliente_%s.pdf" % cliente.Nome

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=%s' % pdfName

    buff = BytesIO()
    # Create the PDF object, using the response object as its "file."

    menu_pdf = SimpleDocTemplate(buff, pagesize=letter, rightMargin=72,
                                 leftMargin=72, topMargin=40, bottomMargin=18)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='justify', alignment=TA_JUSTIFY))

    responsavel = Responsavel.objects.get(DjangoUser=cliente.Orientador)
    total = 0
    # container for pdf elements
    elements = []

    # logo = settings.STATIC_ROOT + 'images/wmfb.png'
    # im = Image(logo, 2 * cm, 2 * cm, hAlign='LEFT')
    # elements.append(im)

    elements.append(Spacer(1, 10))
    elements.append(Paragraph("Relatório da Atividade Feedback", styles["Title"]))
    elements.append(Spacer(1, 25))
    elements.append(Paragraph("<b> Orientador: </b>%s" % responsavel.Nome, styles["Normal"]))
    elements.append(Paragraph("<b>Cliente: </b>%s" % cliente.Nome, styles["Normal"]))
    elements.append(Paragraph("<b>Tipo de Feedback: </b>%s" % cliente.TipoDeFeedback, styles["Normal"]))
    elements.append(Paragraph("<b>Nome da Atividade de Feedback: </b>%s" % cliente.FeedbackNome, styles["Normal"]))
    elements.append(Paragraph("<b>Data: </b>%s" % cliente.Deadline.strftime('%d/%m/%y'), styles["Normal"]))
    elements.append(Spacer(1, 25))
    elements.append(Paragraph("01. %s" % cliente.Pergunta1, styles["Heading5"]))

    categs = Categoria.objects.filter(cliente = cliente)

    for categ in categs:
        ind_categoria = Indicado.objects.filter(Categ=categ)
        if ind_categoria.exists():

            total = ind_categoria.filter(Status=True).count()
            elements.append(Spacer(1, 8))
            elements.append(Paragraph("%s (%s respostas)" % (categ.cat, total),
                                      styles["Normal"]))

            for ind in ind_categoria:
                if ind.Status:
                    elements.append(Paragraph("<b>%s (%s):</b> %s" % (ind.Nome, ind.Email, ind.Resposta1), styles["Code"]))
                    total = total +1


    elements.append(Spacer(1, 12))
    elements.append(Paragraph("02. %s" %cliente.Pergunta2, styles["Heading5"]))


    for categ in categs:
        ind_categoria = Indicado.objects.filter(Categ=categ)
        if ind_categoria.exists():
            total = ind_categoria.filter(Status=True).count()
            elements.append(Spacer(1, 8))
            elements.append(Paragraph("%s (%s respostas)" % (categ.cat, total),
                                      styles["Normal"]))
            for ind in ind_categoria:
                if ind.Status:
                    elements.append(Paragraph("<b>%s (%s):</b> %s" % (ind.Nome, ind.Email, ind.Resposta2), styles["Code"]))
                    total = total + 1

    elements.append(Spacer(1, 18))
    total = Indicado.objects.filter(Status=True, cliente=cliente).count()
    elements.append(Paragraph("<b>Total de Partipantes: </b>%s" % total, styles["Normal"]))
    menu_pdf.build(elements)
    response.write(buff.getvalue())
    buff.close()
    return response
