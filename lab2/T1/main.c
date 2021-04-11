#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const void *mymax(
    const void *base, size_t nmemb, size_t size,
    int (*compar)(const void *, const void *))
{
    unsigned char *curr_element = (unsigned char *)base;
    unsigned char *max_element = curr_element;

    for (int i = 0; i < nmemb; ++i, curr_element += size)
        if (compar((const void *)curr_element, (const void *)max_element))
            max_element = curr_element;
    return (void *)max_element;
}

int compar_gt_int(const void *a, const void *b) { return *((int *)a) > *((int *)b); }
int compar_gt_char(const void *a, const void *b) { return *((char *)a) > *((char *)b); }
int compar_gt_str(const void *a, const void *b) { return strcmp(*((char **)a), *((char **)b)) > 0; }

int main(void)
{
    int arr_int[] = {1, 3, 5, 7, 4, 6, 9, 2, 0};
    char arr_char[] = "Suncana strana ulice";
    const char *arr_str[] = {
        "Gle", "malu", "vocku", "poslije", "kise",
        "Puna", "je", "kapi", "pa", "ih", "njise"};
    printf("%d\n", *((int *)mymax(arr_int, sizeof(arr_int) / sizeof(*arr_int), sizeof(*arr_int), &compar_gt_int)));
    printf("%c\n", *((char *)mymax(arr_char, sizeof(arr_char) / sizeof(*arr_char), sizeof(*arr_char), &compar_gt_char)));
    printf("%s", *((char **)mymax(arr_str, sizeof(arr_str) / sizeof(*arr_str), sizeof(*arr_str), &compar_gt_str)));
    return 0;
}