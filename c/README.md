# Batalha Naval — Níveis em C

- `novato.c`: 2 navios (1 horizontal, 1 vertical). **Saída:** coordenadas com `printf`.
- `aventureiro.c`: matriz 10x10, 4 navios (2 diagonais). **Saída:** matriz completa com `0` e `3`.
- `mestre.c`: padrões de habilidade **cone**, **octaedro (losango)** e **cruz**. **Saída:** 0/1.

> Entradas 100% via variáveis no código (sem `scanf`), conforme enunciado.

Como compilar e rodar (no terminal):
```bash
gcc novato.c -o novato && ./novato
gcc aventureiro.c -o aventureiro && ./aventureiro
gcc mestre.c -o mestre && ./mestre
```