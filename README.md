# Gerenciador Python Web

Versao web do gerenciador de tarefas em Python. O app usa Flask e mantem as tarefas em memoria enquanto o servidor esta ligado

## Funcionalidades

- Criar tarefas com titulo e responsavel.
- Listar tarefas por status.
- Alterar status de uma tarefa.
- Criar novos status.
- Remover tarefas.
- Limpar todas as tarefas.

## Como executar

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Depois acesse:

```text
http://127.0.0.1:5000
```
