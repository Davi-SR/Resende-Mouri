# Gestão de Documentos - Desafio Técnico Estágio Full Stack

Aplicação web para gestão de documentos com upload de arquivos (PDF/JPG/PNG) e sistema de comentários.

## 📋 Descrição

Sistema desenvolvido como parte do processo seletivo para Estagiário Desenvolvedor Full Stack. A aplicação permite:

- Upload de documentos (PDF, JPG, PNG)
- Cadastro de título e descrição para cada documento
- Listagem de todos os documentos enviados
- Visualização e download de documentos
- Sistema de comentários por documento com data/hora

## 🚀 Tecnologias Utilizadas

### Backend
- **Python 3.8+**
- **Flask** - Framework web
- **SQLite** - Banco de dados relacional
- **Werkzeug** - Utilitários para upload seguro

### Frontend
- **HTML5** - Estrutura
- **CSS3** - Estilização (design moderno e responsivo)
- **JavaScript** - Validações e interatividade

## 📁 Estrutura do Projeto

```
document_manager/
├── app.py                 # Backend Flask (rotas e lógica)
├── requirements.txt       # Dependências Python
├── README.md             # Documentação
├── .gitignore            # Arquivos ignorados pelo Git
├── templates/            # Templates HTML
│   ├── index.html        # Página principal
│   └── document.html     # Página de detalhes do documento
├── static/               # Arquivos estáticos
│   ├── styles.css        # Estilos CSS
│   └── app.js            # JavaScript
└── uploads/              # Pasta para arquivos enviados
    └── .gitkeep          # Mantém pasta no Git
```

## 🔧 Como Executar Localmente

### Pré-requisitos
- Python 3.8 ou superior instalado
- pip (gerenciador de pacotes Python)

### Passo a passo

1. **Clone ou baixe o projeto**
```bash
cd document_manager
```

2. **Crie um ambiente virtual (recomendado)**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Execute a aplicação**
```bash
python app.py
```

5. **Acesse no navegador**
```
http://127.0.0.1:5000
```

## 💡 Funcionalidades Implementadas

### ✅ Requisitos Funcionais
- [x] Upload de documentos (PDF, JPG, PNG)
- [x] Cadastro de título (obrigatório)
- [x] Cadastro de descrição (opcional)
- [x] Armazenamento local dos arquivos
- [x] Persistência em banco de dados SQLite
- [x] Listagem de documentos com data de upload
- [x] Visualização de detalhes do documento
- [x] Download de arquivos
- [x] Sistema de comentários por documento
- [x] Data e hora em cada comentário

### ✅ Requisitos Técnicos
- [x] Frontend: HTML, CSS, JavaScript
- [x] Backend: Python com Flask
- [x] Banco de dados: SQLite com relacionamento entre tabelas
- [x] Versionamento: Git
- [x] Documentação: README completo

## 🗄️ Estrutura do Banco de Dados

### Tabela: documents
- `id` - INTEGER PRIMARY KEY
- `title` - TEXT NOT NULL
- `description` - TEXT
- `original_filename` - TEXT NOT NULL
- `stored_filename` - TEXT NOT NULL
- `uploaded_at` - TEXT NOT NULL (ISO 8601)

### Tabela: comments
- `id` - INTEGER PRIMARY KEY
- `document_id` - INTEGER (FK para documents)
- `content` - TEXT NOT NULL
- `created_at` - TEXT NOT NULL (ISO 8601)

## 🎨 Interface

- Design moderno com tema escuro
- Interface responsiva (funciona em mobile)
- Validações no frontend e backend
- Feedback visual para ações do usuário
- Navegação intuitiva

## ⚠️ Observações e Limitações

- Não há sistema de autenticação (conforme especificado no desafio)
- Limite de upload: 20MB por arquivo
- Banco de dados local (SQLite) - arquivo `app.db` criado automaticamente
- Arquivos são armazenados na pasta `uploads/`
- Timestamps em UTC (ISO 8601)

## 🔒 Segurança

- Validação de extensões de arquivo
- Sanitização de nomes de arquivo (secure_filename)
- Limite de tamanho de upload
- Proteção contra SQL injection (uso de prepared statements)
- Validação de dados no frontend e backend

## 📝 API Endpoints

### Páginas
- `GET /` - Página principal (listagem)
- `GET /documents/<id>` - Detalhes do documento

### Ações
- `POST /upload` - Upload de novo documento
- `POST /documents/<id>/comments` - Adicionar comentário
- `GET /files/<filename>` - Download de arquivo

### API JSON (opcional)
- `GET /api/documents` - Lista documentos (JSON)
- `GET /api/documents/<id>/comments` - Lista comentários (JSON)

## 👨‍💻 Desenvolvimento

Projeto desenvolvido seguindo boas práticas:
- Código organizado e comentado
- Separação de responsabilidades (MVC)
- Validações em múltiplas camadas
- Tratamento de erros
- Commits organizados no Git

## 📧 Contato

Desenvolvido como parte do processo seletivo para Resende Mori Hutchison Advocacia.

---

**Prazo de entrega:** 13/12 às 12h  
**Nível:** Estágio Desenvolvedor Full Stack
