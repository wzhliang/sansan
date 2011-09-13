#include <stdio.h>
#define BLACK 1
#define WHITE 2
#define WALL 0
#define EMPTY 3

typedef struct cluster_tag
{
    int n;
    int c[400];
} cluster_t;

cluster_t cluster;

int board[21][21];

void init_board(void)
{
    int i, j;

    for ( i = 1; i < 20; i ++ )
    {
        for ( j = 1; j < 20; j++ )
        {
            board[i][j] = EMPTY;
        }
    }

    for ( i = 0; i < 21 ; i ++ )
    {
        board[0][i] = WALL;
    }

    for ( i = 0; i < 21 ; i ++ )
    {
        board[20][i] = WALL;
    }

    for ( i = 0; i < 21 ; i ++ )
    {
        board[i][0] = WALL;
    }

    for ( i = 0; i < 21 ; i ++ )
    {
        board[20][0] = WALL;
    }
}

void test_1(int *x, int *y, int *color)
{
    printf("========== 1 ========= \n");
    /* Should be dead */
    board[0][2] = WHITE;
    board[1][2] = WHITE;

    board[0][1] = BLACK;
    board[1][1] = BLACK;
    board[2][2] = BLACK;
    board[0][3] = BLACK;
    board[1][3] = BLACK;

    *x = 1;
    *y = 2;
    *color = WHITE;
}

void test_2(int *x, int *y, int *color)
{
    printf("========== 2 ========= \n");
    board[0][0] = BLACK;
    board[0][1] = WHITE;
    board[1][0] = WHITE;

    *x = 0;
    *y = 0;
    *color = BLACK;
}

void test_3(int *x, int *y, int *color)
{
    printf("========== 3 ========= \n");
    /* dead ones */
    board[2][2] = WHITE;
    board[3][2] = WHITE;
    board[4][2] = WHITE;
    board[4][3] = WHITE;

    /* killer */
    board[2][1] = BLACK;
    board[3][1] = BLACK;
    board[4][1] = BLACK;
    board[1][2] = BLACK;
    board[5][2] = BLACK;
    board[2][3] = BLACK;
    board[3][3] = BLACK;
    board[5][3] = BLACK;
    board[4][4] = BLACK;

    *x = 2;
    *y = 2;
    *color = WHITE;
}

void test_4(int *x, int *y, int *color)
{
    printf("========== 4 ========= \n");

    /* dead ones */
    board[0][1] = WHITE;
    board[0][2] = WHITE;
    board[0][3] = WHITE;
    board[1][2] = WHITE;
    board[1][3] = WHITE;

    /* killer */
    board[0][0] = BLACK;
    board[0][4] = BLACK;
    board[1][1] = BLACK;
    board[1][4] = BLACK;
    board[2][2] = BLACK;
    board[2][3] = BLACK;

    *x = 0;
    *y = 1;
    *color = WHITE;
}

void reset_cluster(cluster_t *c)
{
    c->n = 0;
}

void append(cluster_t *c, int id)
{
    /*printf("appending %d\n", id);*/
    c->c[c->n] = id;
    c->n ++;
}

int in_cluster(int id, cluster_t *c)
{
    int i;
    for ( i = 0; i < c->n; i ++ )
    {
        if ( c->c[i] == id )
        {
            return 1;
        }
    }

    return 0;
}

int has_liberty(int x, int y)
{
    if ( 
            board[x-1][y] == EMPTY ||
            board[x+1][y] == EMPTY ||
            board[x][y-1] == EMPTY ||
            board[x][y+1] == EMPTY )
    {
        return 1;
    }
    else
    {
        return 0;
    }
}

int xy2id(int x, int y)
{
    return x*19+y;
}

void id2xy(int id, int *x, int *y)
{
    *x = id / 19;
    *y = id % 19;
}

int is_alive(int x, int y, int color)
{
    int id;

    /*printf("is_alive(%d,%d,%d)\n", x, y, color);*/

    if ( board[x][y] != color )
    {
        return 0;
    }

    if ( has_liberty(x, y) )
    {
        return 1;
    }

    id = xy2id(x, y);
    if ( in_cluster(id, &cluster) )
    {
        return 0;
    }

    append( &cluster, id );

    if ( is_alive(x-1, y, color) )
    {
        return 1;
    }

    if ( is_alive(x+1, y, color ) )
    {
        return 1;
    }

    if ( is_alive(x, y-1, color) )
    {
        return 1;
    }

    if ( is_alive(x, y+1, color) )
    {
        return 1;
    }

    return 0;
}

typedef void (*test_func_t)(int *, int *, int *);

void run_test( test_func_t t )
{
    int x, y, color;
    int alive;
    int i;

    init_board();
    reset_cluster(&cluster);
    t( &x, &y, &color);

    alive = is_alive(x, y, color);
    printf("Group:\n");
    for ( i = 0 ; i < cluster.n; i++ )
    {
        id2xy( cluster.c[i], &x, &y );
        printf("   %d, %d\n", x, y );
    }

    if ( alive )
    {
        printf("is alive!\n");
    }
    else
    {
        printf("is dead!\n");
    }
}

int main(void)
{
    int i;

    test_func_t tests[] = 
    {
        test_1, 
        test_2,
        test_3,
        test_4
    };

    for ( i = 0; i < 4; i ++ )
    {
        run_test( tests[i] );
    }
}
