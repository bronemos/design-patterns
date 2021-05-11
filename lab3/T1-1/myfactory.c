#include "myfactory.h"
#include <windows.h>

typedef struct Animal *(*FUNPTR_AC)(char const *);

void *myfactory(char const *libname, char const *ctorarg)
{
    HMODULE hModule = LoadLibrary(libname);

    FUNPTR_AC create = (FUNPTR_AC)GetProcAddress(hModule, "create");
    return create(ctorarg);
}