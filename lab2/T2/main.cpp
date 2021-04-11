#include <iostream>

template <typename Iterator, typename Predicate>
Iterator mymax(
    Iterator first, Iterator last, Predicate pred)
{
    // ...
}

int arr_int[] = {1, 3, 5, 7, 4, 6, 9, 2, 0};
int main()
{
    const int *maxint = mymax(&arr_int[0],
                              &arr_int[sizeof(arr_int) / sizeof(*arr_int)], gt_int);
    std::cout << *maxint << "\n";
}