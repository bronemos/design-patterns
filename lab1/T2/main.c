#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef double (*PTRFUN)(double x);

// sturctures

typedef struct
{
    PTRFUN *vTable;
    int lower_bound;
    int upper_bound;
} Unary_Function;

typedef struct
{
    Unary_Function;
    double a;
    double b;
} Linear;

typedef struct
{
    Unary_Function;
} Square;

double value_at(Unary_Function *unaryFunction, double x)
{
    return unaryFunction->vTable[0](x);
}

double negative_value_at(Unary_Function *unaryFunction, double x)
{
    return -unaryFunction->vTable[0](x);
}

PTRFUN vTable[2];

void constructUnaryFunction(Unary_Function *unaryFunction, int lb, int ub)
{
    (*unaryFunction).lower_bound = lb;
    (*unaryFunction).upper_bound = ub;
    (*unaryFunction).vTable = vTable;
}

Unary_Function *createUnaryFunction(int lb, int ub)
{
    Unary_Function *unaryFunction = (Unary_Function *)malloc(sizeof(Unary_Function));
    constructUnaryFunction(unaryFunction, lb, ub);
    return unaryFunction;
}

double linear_value_at(Linear *linear, double x)
{
    return (*linear).a * x + (*linear).b;
}

PTRFUN vTableLinear[2] = {
    (PTRFUN)linear_value_at,
    (PTRFUN)negative_value_at};

void constructLinear(Linear *linear, int lb, int ub, double a_coef, double b_coef)
{
    (*linear).vTable = vTableLinear;
    (*linear).lower_bound = lb;
    (*linear).upper_bound = ub;
    (*linear).a = a_coef;
    (*linear).b = b_coef;
}

Unary_Function *createLinear(int lb, int ub, double a_coef, double b_coef)
{
    Unary_Function *linear = (Unary_Function *)malloc(sizeof(Linear));
    constructLinear((Linear *)linear, lb, ub, a_coef, b_coef);
    return linear;
}

double square_value_at(Square *square, double x)
{
    return x * x;
}

PTRFUN vTableSquare[2] = {
    (PTRFUN)square_value_at,
    (PTRFUN)negative_value_at};

void constructSquare(Square *square, int lb, int ub)
{
    (*square).vTable = vTableSquare;
    (*square).lower_bound = lb;
    (*square).upper_bound = ub;
}

Unary_Function *createSquare(int lb, int ub)
{
    Unary_Function *square = (Unary_Function *)malloc(sizeof(Square));
    constructSquare((Square *)square, lb, ub);
    return square;
}

static bool same_functions_for_ints(Unary_Function *f1, Unary_Function *f2, double tolerance)
{
    if (f1->lower_bound != f2->lower_bound)
        return false;
    if (f1->upper_bound != f2->upper_bound)
        return false;
    for (int x = f1->lower_bound; x <= f1->upper_bound; x++)
    {
        double delta = value_at(f1, x) - value_at(f2, x);
        if (delta < 0)
            delta = -delta;
        if (delta > tolerance)
            return false;
    }
    return true;
}

void tabulate(Unary_Function *unaryFunction)
{
    for (int x = (*unaryFunction).lower_bound; x <= (*unaryFunction).upper_bound; x++)
    {
        printf("f(%d)=%lf\n", x, value_at(unaryFunction, x));
    }
}

int main(void)
{
    Unary_Function *f1 = createSquare(-2, 2);
    tabulate(f1);

    Unary_Function *f2 = createLinear(-2, 2, 5, -2);
    tabulate(f2);

    free(f1);
    free(f2);
    return 0;
}