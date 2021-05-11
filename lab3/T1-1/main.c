#include "myfactory.h"

#include <stdio.h>
#include <stdlib.h>

typedef char const *(*PTRFUN)();

struct Animal
{
  PTRFUN *vtable;
  // vtable entries:
  // 0: char const* name(void* this);
  // 1: char const* greet();
  // 2: char const* menu();
};

// parrots and tigers defined in respective dynamic libraries

void animalPrintGreeting(struct Animal *p)
{
  printf("%s pozdravlja: %s\n", (p->vtable[0])(p), (p->vtable[1])(p));
}

void animalPrintMenu(struct Animal *p)
{
  printf("%s voli: %s\n", (p->vtable[0])(p), (p->vtable[2])(p));
}

int main(int argc, char *argv[])
{
  for (int i = 0; i < argc; ++i)
  {
    struct Animal *p = (struct Animal *)myfactory(argv[i], "Modrobradi");
    if (!p)
    {
      printf("Creation of plug-in object %s failed.\n", argv[i]);
      continue;
    }

    animalPrintGreeting(p);
    animalPrintMenu(p);
    free(p);
  }
}