# Versão Python (CLI)

Como rodar:
```bash
cd python
pip install -r requirements.txt
python src/batalha_naval.py
```

Opções ao iniciar:
- `1` → Jogador x CPU
- `2` → 2 Jogadores (local)
- `C` → Carregar partida salva (`.json`)

Comandos durante o jogo:
- `salvar` ou `salvar nome.json` → salva o jogo
- `sair` → encerra

Testes:
```bash
pytest -q
```