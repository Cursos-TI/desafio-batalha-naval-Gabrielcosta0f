// aventureiro.c — Batalha Naval (Nível Aventureiro)
#include <stdio.h>
#include <string.h>

#define N 10

int main(void) {
    int m[N][N];
    memset(m, 0, sizeof(m));

    // ======= ENTRADAS (por variáveis) =======
    // 1) Navio horizontal (tamanho 4) iniciando em (2,1)
    int h_l = 2, h_c = 1, h_t = 4;
    // 2) Navio vertical (tamanho 5) iniciando em (0,8)
    int v_l = 0, v_c = 8, v_t = 5;
    // 3) Navio diagonal ↘ (tamanho 3) iniciando em (5,2)
    int d1_l = 5, d1_c = 2, d1_t = 3;
    // 4) Navio diagonal ↗ (tamanho 3) iniciando em (7,1)
    int d2_l = 7, d2_c = 1, d2_t = 3;

    // ======= POSICIONAMENTO =======
    for (int i = 0; i < h_t; i++) m[h_l][h_c + i] = 3;          // horizontal
    for (int i = 0; i < v_t; i++) m[v_l + i][v_c] = 3;          // vertical
    for (int i = 0; i < d1_t; i++) m[d1_l + i][d1_c + i] = 3;   // diagonal ↘
    for (int i = 0; i < d2_t; i++) m[d2_l - i][d2_c + i] = 3;   // diagonal ↗

    // ======= SAÍDA =======
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            printf("%d ", m[i][j]);
        }
        printf("\n");
    }
    return 0;
}