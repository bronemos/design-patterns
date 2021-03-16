#include <iostream>

class CoolClass
{
public:
    virtual void set(int x) { x_ = x; };
    virtual int get() { return x_; };

private:
    int x_;
};

class PlainOldClass
{
public:
    void set(int x) { x_ = x; };
    int get() { return x_; };

private:
    int x_;
};

int main()
{
    std::cout << "Size of CoolClass: " << sizeof(CoolClass) << std::endl;
    std::cout << "Size of PlainOldClass: " << sizeof(PlainOldClass) << std::endl;
}

/*
Strukture podataka imaju različite zahtjeve za poravnanje, sukladno tome compiler dodaje neimenovane podatke kako bi svi podaci bili poravnati na odgovarajući način.
CoolClass sadrži virtualnu tablicu koja je veličine 4B.
*/