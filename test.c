#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main()
{
    float teplota = 25.2;
    int cast = (int)teplota;

    int zbytek = (int)(teplota*10) - cast*10;

    printf("%d", zbytek);
}