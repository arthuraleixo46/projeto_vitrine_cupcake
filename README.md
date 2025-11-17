
# Cupcake Store — Vitrine (Flask + MongoDB)

## Descrição
Projeto para vitrine virtual de cupcakes com área pública e painel administrativo.
Backend: Flask (Python). Database: MongoDB. Frontend: HTML + Bootstrap.
## Requisitos
- Python 3.10+
- MongoDB local ou Atlas

## Instalação rápida
1. Crie e ative um venv

```bash
python -m venv venv
source venv/bin/activate  # linux/mac
venv\\Scripts\\activate   # windows
```

2. Instale dependências
```bash
pip install -r requirements.txt
```

3. Configure variável de ambiente (opcional)
```bash
export MONGO_URI="sua_mongo_uri"
export FLASK_SECRET="uma_chave_secreta"
```

4. Criar um usuário admin (script Python)
```python
from werkzeug.security import generate_password_hash
from mongo_manager import MongoManager
md = MongoManager(uri='sua_mongo_uri')
md.create_user('admin@example.com', generate_password_hash('sua_senha'))
```

5. Rodar a aplicação
```bash
python app.py
```

6. Abra: http://127.0.0.1:5000

## Observações
- Imagens enviadas pelo admin são salvas em `static/uploads`.
- Para produção, configure um caminho de upload seguro e ajuste permissões.
