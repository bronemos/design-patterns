#include <stdio.h>
#include <stdlib.h>

typedef char const *(*PTRFUN)();
PTRFUN catFunctions[2];
PTRFUN dogFunctions[2];

typedef struct
{
    char const *name;
    PTRFUN *functions;
} Animal;

void constructDog(Animal *animal, char const *name)
{
    (*animal).name = name;
    (*animal).functions = dogFunctions;
}

void constructCat(Animal *animal, char const *name)
{
    (*animal).name = name;
    (*animal).functions = catFunctions;
}

Animal *createDog(char const *name)
{
    Animal *dog = malloc(sizeof(Animal));
    constructDog(dog, name);
    return dog;
}

Animal *createNDogs(int n)
{
    Animal *dogs = (Animal *)malloc(sizeof(Animal) * n);
    Animal *p = NULL;

    for (p = dogs; p < dogs + n; p++)
    {
        constructDog(p, "Dog");
    }

    return dogs;
}

Animal createDogStack(char const *name)
{
    Animal dog;

    dog.name = name;
    dog.functions = dogFunctions;

    return dog;
}

Animal *createCat(char const *name)
{
    Animal *cat = malloc(sizeof(Animal));
    constructCat(cat, name);
    return cat;
}

Animal createCatStack(char const *name)
{
    Animal cat;

    cat.name = name;
    cat.functions = catFunctions;

    return cat;
}

void animalPrintGreeting(Animal *animal)
{
    printf("%s pozdravlja: %s\n", (*animal).name, animal->functions[0]());
}

void animalPrintMenu(Animal *animal)
{
    printf("%s voli: %s\n", (*animal).name, animal->functions[1]());
}

char const *dogGreet(void)
{
    return "vau!";
}
char const *dogMenu(void)
{
    return "kuhanu govedinu";
}
char const *catGreet(void)
{
    return "mijau!";
}
char const *catMenu(void)
{
    return "konzerviranu tunjevinu";
}

void testAnimalsHeap(void)
{
    Animal *p1 = createDog("Hamlet");
    Animal *p2 = createCat("Ofelija");
    Animal *p3 = createDog("Polonije");

    animalPrintGreeting(p1);
    animalPrintGreeting(p2);
    animalPrintGreeting(p3);

    animalPrintMenu(p1);
    animalPrintMenu(p2);
    animalPrintMenu(p3);

    free(p1);
    free(p2);
    free(p3);
}

void testAnimalsStack(void)
{
    Animal p1 = createDogStack("Hamlet");
    Animal p2 = createCatStack("Ofelija");
    Animal p3 = createDogStack("Polonije");

    animalPrintGreeting(&p1);
    animalPrintGreeting(&p2);
    animalPrintGreeting(&p3);

    animalPrintMenu(&p1);
    animalPrintMenu(&p2);
    animalPrintMenu(&p3);
}

int main(void)
{
    catFunctions[0] = &catGreet;
    catFunctions[1] = &catMenu;
    dogFunctions[0] = &dogGreet;
    dogFunctions[1] = &dogMenu;
    testAnimalsHeap();
    testAnimalsStack();

    int n = 2;

    Animal *dogs = createNDogs(n);

    for (Animal *p = dogs; p; p++)
    {
        printf("%s\n", (*p).name);
    }

    return 0;
}