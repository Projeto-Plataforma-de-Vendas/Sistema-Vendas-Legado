from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name='Funcionario',
                    fields=[
                        ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('nome', models.CharField(max_length=100, verbose_name='Nome')),
                        ('rg', models.CharField(blank=True, max_length=30, verbose_name='RG')),
                        ('cpf', models.CharField(max_length=20, unique=True, verbose_name='CPF')),
                        ('email', models.EmailField(max_length=200, verbose_name='E-mail')),
                        ('cargo', models.CharField(max_length=100, verbose_name='Cargo')),
                        ('nivel_acesso', models.CharField(max_length=50, verbose_name='Nível de Acesso')),
                        ('telefone', models.CharField(max_length=30, verbose_name='Telefone')),
                        ('celular', models.CharField(max_length=30, verbose_name='Celular')),
                        ('cep', models.CharField(max_length=100, verbose_name='CEP')),
                        ('endereco', models.CharField(max_length=255, verbose_name='Endereço')),
                        ('numero', models.IntegerField(verbose_name='Número')),
                        ('complemento', models.CharField(blank=True, max_length=200, verbose_name='Complemento')),
                        ('bairro', models.CharField(max_length=100, verbose_name='Bairro')),
                        ('cidade', models.CharField(max_length=100, verbose_name='Cidade')),
                        ('estado', models.CharField(max_length=2, verbose_name='Estado')),
                    ],
                    options={
                        'db_table': 'tb_funcionarios',
                        'ordering': ['nome'],
                        'verbose_name': 'Funcionário',
                        'verbose_name_plural': 'Funcionários',
                    },
                ),
            ],
            database_operations=[],
        ),
    ]
