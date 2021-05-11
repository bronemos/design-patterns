#include <stdlib.h>

typedef char const *(*PTRFUN)();

struct Parrot
{
    PTRFUN *vtable;
    char const *name;
};

char const *name(void *this)
{
    return ((struct Parrot *)this)->name;
}

char const *greet()
{
    return "Hi I'm a parrot!";
}

char const *menu()
{
    return "sjemenke";
}

PTRFUN parrotVTable[3] = {
    (PTRFUN)name,
    (PTRFUN)greet,
    (PTRFUN)menu,
};

void *create(char const *name)
{
    struct Parrot *parrot = malloc(sizeof(struct Parrot));
    parrot->vtable = parrotVTable;
    parrot->name = name;
    return parrot;
}