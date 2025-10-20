# 🛒 Sistema de Vendas - Legado

Sistema de vendas desktop desenvolvido em Java com interface gráfica Swing, integração com banco de dados MySQL e funcionalidades completas para gestão comercial.

## 📋 Sobre o Projeto

Este é um sistema legado de vendas que oferece uma solução completa para pequenos e médios negócios, permitindo o gerenciamento de clientes, fornecedores, produtos, funcionários, estoque e vendas através de uma interface desktop intuitiva.

## ✨ Funcionalidades

### 🔐 Sistema de Login
- Autenticação de funcionários
- Controle de níveis de acesso
- Segurança por credenciais

### 👥 Gestão de Clientes
- Cadastro completo de clientes
- Consulta de CEP automática via WebService
- Edição e exclusão de registros
- Busca e filtros avançados

### 📦 Gestão de Produtos
- Cadastro de produtos com preços
- Controle de estoque
- Vinculação com fornecedores
- Relatórios de estoque

### 🏢 Gestão de Fornecedores
- Cadastro completo de fornecedores
- Controle de dados comerciais
- Relacionamento com produtos

### 👨‍💼 Gestão de Funcionários
- Cadastro de funcionários
- Controle de cargos e níveis de acesso
- Gerenciamento de credenciais

### 💰 Sistema de Vendas
- Processamento de vendas
- Cálculo automático de totais
- Controle de itens vendidos
- Baixa automática no estoque

### 📊 Relatórios e Histórico
- Histórico completo de vendas
- Detalhamento de vendas por período
- Relatórios de estoque
- Consultas personalizadas

## 🛠️ Tecnologias Utilizadas

- **Java SE** - Linguagem de programação principal
- **Swing** - Interface gráfica desktop
- **MySQL** - Banco de dados relacional
- **JDBC** - Conectividade com banco de dados
- **NetBeans** - IDE de desenvolvimento
- **Apache Ant** - Automação de build

### 📚 Bibliotecas e Dependências

- `mysql-connector-java-8.0.27.jar` - Driver MySQL
- `dom4j-2.0.3.jar` - Parser XML para WebService CEP
- `javax.mail.jar` - Funcionalidades de email
- `activation.jar` - Suporte a MIME types

## 🗄️ Estrutura do Banco de Dados

O sistema utiliza as seguintes tabelas principais:

- **tb_clientes** - Dados dos clientes
- **tb_fornecedores** - Informações dos fornecedores
- **tb_funcionarios** - Cadastro de funcionários
- **tb_produtos** - Catálogo de produtos
- **tb_vendas** - Registro de vendas
- **tb_itensvendas** - Itens detalhados por venda

## 🚀 Como Executar

### Pré-requisitos

1. **Java Development Kit (JDK)** 8 ou superior
2. **MySQL Server** 5.7 ou superior
3. **NetBeans IDE** (recomendado) ou outra IDE Java

### Configuração do Banco de Dados

1. Execute o script SQL localizado em `Script BD Vendas/Script Banco BDVendas.sql`
2. Certifique-se de que o MySQL está rodando na porta 3306 (baixar em https://dev.mysql.com/downloads/mysql/)
3. Verifique as credenciais no arquivo `ConnectionFactory.java`:
   ```java
   private final String user = "usuario";
   private final String pass = "123";
   ```

### Executando a Aplicação

1. **Via NetBeans:**
   ```bash
   # Abra o projeto no NetBeans
   # Compile e execute através da IDE
   ```

2. **Via linha de comando:**
   ```bash
   # Compilar o projeto
   ant compile
   
   # Gerar o JAR
   ant jar
   
   # Executar a aplicação
   java -cp "dist/Sistema_Vendas_Resolvido.jar:lib/*" view.FrmLogin
   ```

3. **Executar diretamente:**
   ```bash
   # Navegar até o diretório do projeto
   cd "c:\Users\user\OneDrive\Documentos\Biopark\Sistema-Vendas-Legado"
   
   # Compilar via Ant
   ant clean build
   
   # Executar
   java -jar "dist/Sistema Vendas (Resolvido).jar"
   ```

## 📱 Interface do Sistema

O sistema possui as seguintes telas principais:

- **FrmLogin** - Tela de autenticação
- **FrmMenu** - Menu principal do sistema
- **FrmCliente** - Gestão de clientes
- **FrmFornecedor** - Gestão de fornecedores
- **FrmFuncionario** - Gestão de funcionários
- **FrmProduto** - Gestão de produtos
- **FrmVenda** - Processamento de vendas
- **FrmEstoque** - Controle de estoque
- **FrmHistorico** - Histórico de vendas
- **FrmPagamento** - Gestão de pagamentos

## 🔧 Configurações Importantes

### Conexão com Banco de Dados
O arquivo `ConnectionFactory.java` contém as configurações de conexão:

```java
private final String ip = "127.0.0.1";
private final String port = "3306";
private final String user = "usuario";
private final String pass = "123";
private final String bd = "BDVENDAS";
```

### WebService de CEP
O sistema integra com webservice de consulta de CEP para preenchimento automático de endereços.

## 🏗️ Arquitetura do Projeto

```
src/
├── dao/          # Data Access Objects - Acesso aos dados
├── jdbc/         # Configuração e teste de conexão
├── model/        # Classes de modelo/entidade
├── view/         # Interfaces gráficas (Swing)
└── imagens/      # Recursos visuais da aplicação
```

## 📄 Licença

Este projeto é um sistema legado educacional desenvolvido para fins de aprendizado e pode ser utilizado como base para outros projetos.

## 👨‍💻 Autor

**Tampelini** - Desenvolvimento inicial

## 🤝 Contribuições

Este é um projeto legado que serve como base para estudos e desenvolvimento de novos sistemas. Sinta-se à vontade para:

1. Fazer fork do projeto
2. Criar uma branch para sua feature
3. Implementar melhorias
4. Submeter um pull request

## 📞 Suporte

Para dúvidas sobre a implementação ou configuração do sistema, consulte:

1. A documentação do código fonte
2. Os comentários nas classes principais
3. O script de criação do banco de dados

## 🔄 Versão

**Versão Atual:** Sistema Vendas (Resolvido) - Versão Legado

---

*Este sistema foi desenvolvido como solução educacional e pode ser adaptado para necessidades específicas de negócio.*
