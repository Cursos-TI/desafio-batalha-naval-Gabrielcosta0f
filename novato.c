// novato.c — Batalha Naval (Nível Novato)
#include <stdio.h>

int main(void) {
    // Tamanho do tabuleiro (referência)
    const int LINHAS = 5, COLUNAS = 5;

    // ======= ENTRADAS (definidas por variáveis) =======
    // Navio horizontal com tamanho 3, começando em (linha=1, col=0)
    int h_linha = 1, h_col = 0, h_tam = 3;

    // Navio vertical com tamanho 4, começando em (linha=0, col=3)
    int v_linha = 0, v_col = 3, v_tam = 4;

    // ======= SAÍDA =======
    printf("Coordenadas do navio HORIZONTAL (tamanho %d):\n", h_tam);
    for (int c = 0; c < h_tam; c++) {
        printf("(%d,%d)\n", h_linha, h_col + c);
    }

    printf("\nCoordenadas do navio VERTICAL (tamanho %d):\n", v_tam);
    for (int l = 0; l < v_tam; l++) {
        printf("(%d,%d)\n", v_linha + l, v_col);
    }

    return 0;
}