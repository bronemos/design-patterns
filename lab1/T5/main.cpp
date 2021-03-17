#include <iostream>

class B
{
public:
    virtual int __cdecl prva() = 0;
    virtual int __cdecl druga(int) = 0;
};

class D : public B
{
public:
    virtual int __cdecl prva() { return 42; }
    virtual int __cdecl druga(int x) { return prva() + x; }
};

void printReturns(B *b)
{
    typedef int (*pfun)(B *);
    typedef int (*pfun2)(B *, int);

    unsigned int vtblAddress = *(unsigned int *)b;

    pfun prvaVirtual = (pfun)(*(unsigned int *)(vtblAddress));
    pfun2 drugaVirtual = (pfun2)(*(unsigned int *)(vtblAddress + 4));
    std::cout << prvaVirtual(b) << " " << drugaVirtual(b, 5) << std::endl;
}

int main()
{
    D b;
    printReturns(&b);
}