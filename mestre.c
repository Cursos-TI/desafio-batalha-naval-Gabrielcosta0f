// mestre.c — Batalha Naval (Nível Mestre)
#include <stdio.h>
#include <string.h>

#define N 9   // use ímpar para centralizar padrões (ex.: 5, 7, 9)

void print_matriz(int M[N][N]) {
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) printf("%d ", M[i][j]);
        printf("\n");
    }
}

int main(void) {
    int M[N][N];
    int cx = N/2, cy = N/2; // centro

    // ====== CONE (vértice no topo, abrindo para baixo) ======
    memset(M, 0, sizeof(M));
    for (int i = 0; i <= cx; i++) {               // da linha 0 até o centro
        int largura = i;                          // cresce 1 a cada linha
        for (int j = cy - largura; j <= cy + largura; j++) {
            if (j >= 0 && j < N) M[i][j] = 1;
        }
    }
    printf("Habilidade CONE:\n");
    print_matriz(M);
    printf("\n");

    // ====== OCTAEDRO (losango) com raio R ======
    memset(M, 0, sizeof(M));
    int R = N/2; // raio máximo até as bordas
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            int dist = (i > cx ? i - cx : cx - i) + (j > cy ? j - cy : cy - j);
            if (dist <= R) M[i][j] = 1;
        }
    }
    printf("Habilidade OCTAEDRO:\n");
    print_matriz(M);
    printf("\n");

    // ====== CRUZ (linhas e colunas que passam pelo centro) ======
    memset(M, 0, sizeof(M));
    for (int j = 0; j < N; j++) M[cx][j] = 1; // linha central
    for (int i = 0; i < N; i++) M[i][cy] = 1; // coluna central
    printf("Habilidade CRUZ:\n");
    print_matriz(M);

    return 0;
}