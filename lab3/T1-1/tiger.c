#include <stdlib.h>

typedef char const *(*PTRFUN)();

struct Tiger
{
    PTRFUN *vtable;
    char const *name;
};

char const *name(void *this)
{
    return ((struct Tiger *)this)->name;
}

char const *greet()
{
    return "Hi I'm a tiger!";
}

char const *menu()
{
    return "meso";
}

PTRFUN tigerVTable[3] = {
    (PTRFUN)name,
    (PTRFUN)greet,
    (PTRFUN)menu,
};

void *create(char const *name)
{
    struct Tiger *tiger = malloc(sizeof(struct Tiger));
    tiger->vtable = tigerVTable;
    tiger->name = name;
    return tiger;
}