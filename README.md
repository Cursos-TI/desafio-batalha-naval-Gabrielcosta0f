# Desafio Batalha Naval — Estácio (duas entregas)

Este pacote traz **duas soluções** do desafio:
1. **python/** — jogo jogável em Python (CLI) com salvar/carregar e modo 2 jogadores (local).
2. **c/** — três arquivos em C (Novato, Aventureiro, Mestre) usando `printf` e matrizes conforme o enunciado MateCheck.

## Como usar este pacote com seu repositório do GitHub
### Método fácil pelo site (sem instalar nada)
1. Baixe este ZIP e **extraia** no seu computador.
2. Acesse seu repositório em: `https://github.com/Cursos-TI/desafio-batalha-naval-Gabrielcosta0f`
3. Clique em **Add file → Upload files**.
4. **Arraste as pastas** `python`, `c` e a pasta `.github` (e o `README.md`) para a área de upload.
5. Desça a página e clique em **Commit changes**.
6. Abra a aba **Actions** e aguarde o fluxo **tests** ficar **verde** (os testes do Python passaram!).

### Método Git (para quem usa terminal)
```bash
git clone https://github.com/Cursos-TI/desafio-batalha-naval-Gabrielcosta0f.git
cd desafio-batalha-naval-Gabrielcosta0f
# copie todo o conteúdo deste pacote para dentro desta pasta
git add .
git commit -m "Entrega: Python + C (Novato/Aventureiro/Mestre) + CI"
git push origin main
```

## Como rodar localmente (Python)
```bash
cd python
pip install -r requirements.txt
python src/batalha_naval.py
```
Testes:
```bash
pytest -q
```

## Como compilar (C)
```bash
cd c
gcc novato.c -o novato && ./novato
gcc aventureiro.c -o aventureiro && ./aventureiro
gcc mestre.c -o mestre && ./mestre
```