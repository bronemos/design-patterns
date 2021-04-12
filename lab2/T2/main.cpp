#include <iostream>
#include <cstring>

template <typename Iterator, typename Predicate>
Iterator mymax(
    Iterator curr, Iterator last, Predicate pred)
{
    Iterator max;

    for (max = curr; curr != last; ++curr)
        if (pred(curr, max))
            max = curr;

    return max;
}

int compar_gt_int(const void *a, const void *b) { return *((int *)a) > *((int *)b); }
int compar_gt_char(const void *a, const void *b) { return *((char *)a) > *((char *)b); }
int compar_gt_str(const void *a, const void *b) { return strcmp(*((char **)a), *((char **)b)) > 0; }

int main()
{
    int arr_int[] = {1, 3, 5, 7, 4, 6, 9, 2, 0};
    char arr_char[] = "Suncana strana ulice";
    const char *arr_str[] = {
        "Gle", "malu", "vocku", "poslije", "kise",
        "Puna", "je", "kapi", "pa", "ih", "njise"};
    std::cout << *mymax(arr_int, arr_int + sizeof(arr_int) / sizeof(*arr_int), compar_gt_int) << std::endl;
    std::cout << *mymax(arr_char, arr_char + sizeof(arr_char) / sizeof(*arr_char), compar_gt_char) << std::endl;
    std::cout << *mymax(arr_str, arr_str + sizeof(arr_str) / sizeof(*arr_str), compar_gt_str) << std::endl;
}