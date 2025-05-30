# Generated by Django 4.2.20 on 2025-03-30 11:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Categorias',
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nome', models.CharField(max_length=100)),
                ('Email', models.EmailField(max_length=254)),
                ('Observacoes', models.TextField()),
                ('WebKey', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('Status', models.BooleanField(default=False)),
                ('FeedbackNome', models.CharField(choices=[('Aconselhamento de Carreira', 'Aconselhamento de Carreira'), ('Planejamento de Carreira', 'Planejamento de Carreira'), ('Coaching de Carreira', 'Coaching de Carreira')], default='Feedback I', max_length=50)),
                ('TipoDeFeedback', models.CharField(choices=[('Feedback I', 'Feedback I'), ('Feedback II', 'Feedback II'), ('Customizado', 'Customizado')], default='Aconselhamento de Carreira', max_length=50)),
                ('Deadline', models.DateField(blank=True, null=True)),
                ('StatusDeadline', models.BooleanField(default=False)),
                ('Arquivo', models.FileField(upload_to='')),
                ('ProgressBar', models.DecimalField(decimal_places=0, default=0, max_digits=3)),
                ('Pergunta1', models.TextField()),
                ('Pergunta2', models.TextField()),
                ('Orientador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Clientes',
            },
        ),
        migrations.CreateModel(
            name='Responsavel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nome', models.CharField(max_length=100)),
                ('Id_number', models.CharField(max_length=10)),
                ('Tipo_id', models.CharField(choices=[('', ''), ('CRP', 'CRP'), ('CRM', 'CRM')], max_length=10)),
                ('DjangoUser', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Indicado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nome', models.CharField(max_length=100)),
                ('Email', models.EmailField(max_length=100)),
                ('WebKey', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('Status', models.BooleanField(default=False)),
                ('Resposta1', models.TextField()),
                ('Resposta2', models.TextField()),
                ('Categ', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feedback360pro.categoria')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feedback360pro.cliente')),
            ],
            options={
                'verbose_name_plural': 'Indicados',
            },
        ),
        migrations.AddField(
            model_name='categoria',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feedback360pro.cliente'),
        ),
    ]
