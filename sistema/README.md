# InovaTech Supply

Sistema interno de **gestão de estoque e pedidos**, com API REST em Flask, banco de dados configurável (MySQL ou SQLite) e catálogo web dinâmico com visual HUD/gamer.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-API%20REST-000000?logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1?logo=mysql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-orange)

<!-- Adicione um print da tela principal em docs/screenshot.png e descomente a linha abaixo. -->
<!-- ![Tela principal](docs/screenshot.png) -->

---

## Sobre o projeto

O **InovaTech Supply** centraliza o controle de produtos, clientes, fornecedores, pedidos e pagamentos de uma loja de tecnologia. O back-end expõe uma API REST organizada em Blueprints, enquanto o front-end consome essa API para exibir um catálogo de produtos com detalhes, carrinho e finalização de pedido.

O projeto foi desenvolvido com foco em back-end, modelagem de banco de dados e lógica de programação, seguindo uma arquitetura em camadas com models, rotas, templates e arquivos estáticos.

## Funcionalidades

- CRUD para produtos, clientes, fornecedores, pedidos, itens de pedido e pagamentos
- Catálogo dinâmico com skeleton loaders durante o carregamento
- Página de detalhes do produto
- Carrinho de compras salvo no navegador com `localStorage`
- Notificações visuais (toasts) para feedback ao usuário
- Cadastro de clientes e finalização de pedido
- Imagens de produtos servidas pela aplicação
- Cadastro automático das tabelas na inicialização
- Popularização inicial de produtos a partir das imagens locais do catálogo
- Configuração do banco por variáveis de ambiente
- Fallback automático para SQLite quando as variáveis do MySQL não estão definidas
- Testes automatizados básicos da aplicação

## Tecnologias

| Camada | Tecnologias |
| --- | --- |
| Back-end | Python, Flask, Flask-SQLAlchemy, Flask-CORS |
| Banco de dados | MySQL com PyMySQL ou SQLite local |
| Front-end | HTML5, CSS3 e JavaScript vanilla |
| Testes | `unittest` e compatibilidade com Pytest |
| Design | Tema escuro com tipografia Orbitron e Rajdhani |

## Estrutura do projeto

```text
.
├── README.md
├── .gitignore
├── .env                         # configurações locais, não versionado
├── run.py                       # ponto de entrada da aplicação
├── config.py                    # configuração do banco e ambiente
├── requirements.txt             # dependências Python
├── app/
│   ├── __init__.py              # application factory e inicialização
│   ├── extensions.py            # extensões, como SQLAlchemy
│   ├── models/                  # modelos de cliente, produto, pedido...
│   ├── routes/                  # Blueprints da API
│   ├── templates/               # páginas HTML
│   └── static/                  # CSS, JavaScript e imagens
├── tests/                       # testes automatizados
└── *.py                         # scripts utilitários de imagens e produtos
```

## Como executar

### Pré-requisitos

- [Python 3.10+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)
- MySQL 8+ em execução, caso opte pelo banco MySQL

### 1. Clone o repositório

```bash
git clone https://github.com/SEU-USUARIO/NOME-DO-REPO.git
cd NOME-DO-REPO/sistema
```

### 2. Crie e ative o ambiente virtual

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados

A aplicação funciona sem configuração adicional usando SQLite. Para usar MySQL, crie um arquivo `.env` na pasta `sistema/` com as variáveis abaixo:

```env
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=3306
DB_NAME=gestao
```

O arquivo `.env` já está no `.gitignore` e não deve ser enviado ao repositório.

Para criar o banco no MySQL:

```sql
CREATE DATABASE gestao
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

As tabelas são criadas automaticamente quando a aplicação é iniciada.

### 5. Inicie a aplicação

```bash
python run.py
```

Acesse [http://localhost:5000](http://localhost:5000) no navegador.

## Rotas da aplicação

### Páginas web

| Rota | Descrição |
| --- | --- |
| `/` | Catálogo principal |
| `/produto/<id>` | Detalhes de um produto |
| `/clientes/cadastrar` | Cadastro de clientes |
| `/Finalizar%20Pedido` | Finalização do pedido |

### API REST

Todas as entidades possuem operações de consulta, criação, atualização e remoção, conforme a rota:

| Recurso | Endpoint |
| --- | --- |
| Produtos | `/produtos/` |
| Clientes | `/clientes/` |
| Fornecedores | `/fornecedores/` |
| Pedidos | `/pedidos/` |
| Itens de pedido | `/itens_pedido/` |
| Pagamentos | `/pagamentos/` |

Para buscar um registro específico, acrescente o identificador ao endpoint, por exemplo: `/produtos/1`.

Exemplo de requisição:

```bash
curl http://localhost:5000/produtos/
```

Exemplo de criação de produto:

```bash
curl -X POST http://localhost:5000/produtos/ \
  -H "Content-Type: application/json" \
  -d '{"nome":"Teclado gamer","descricao":"Teclado mecânico","preco":299.90,"estoque":10,"categoria":"Periféricos"}'
```

## Testes

Os testes podem ser executados com a biblioteca padrão do Python:

```bash
python -m unittest discover -s tests
```

Também é possível usar Pytest, caso esteja instalado no ambiente:

```bash
pip install pytest
pytest
```

## Roadmap

- [ ] Autenticação e controle de acesso por perfil
- [ ] Painel administrativo com indicadores de estoque e vendas
- [ ] Filtros e busca avançada no catálogo
- [ ] Migrações de banco com Flask-Migrate
- [ ] Deploy em ambiente de produção

## Autor

**Davi Lima Ramos de Oliveira**  
Estudante de Desenvolvimento Full Stack na Universidade Cruzeiro do Sul

[![GitHub](https://img.shields.io/badge/GitHub-SEU--USUARIO-181717?logo=github)](https://github.com/SEU-USUARIO)

## Licença

Este projeto está em desenvolvimento. Caso a licença MIT seja adotada, adicione um arquivo `LICENSE` com o texto oficial da licença ao repositório.
