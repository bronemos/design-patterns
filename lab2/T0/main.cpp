#include <iostream>
#include <assert.h>
#include <stdlib.h>
#include <list>

struct Point
{
    int x;
    int y;
};

class Shape
{
private:
    Point center;

public:
    Shape(int x, int y)
    {
        center.x = x;
        center.y = y;
    }
    Shape()
    {
        center.x = 0;
        center.y = 0;
    }
    virtual void draw() = 0;
    virtual void move(int t_x, int t_y)
    {
        center.x += t_x;
        center.y += t_y;
    }
};
class Circle : public Shape
{
    virtual void draw()
    {
        std::cerr << "in drawCircle\n";
    }
};
class Square : public Shape
{
    virtual void draw()
    {
        std::cerr << "in drawSquare\n";
    }
};
class Rhomb : public Shape
{
    virtual void draw()
    {
        std::cerr << "in drawRhomb\n";
    }
};
void drawShapes(const std::list<Shape *> &fig)
{
    std::list<Shape *>::const_iterator it;
    for (it = fig.begin(); it != fig.end(); ++it)
    {
        (*it)->draw();
    }
}

void moveShapes(const std::list<Shape *> &fig, int t_x, int t_y)
{
    std::list<Shape *>::const_iterator it;
    for (it = fig.begin(); it != fig.end(); ++it)
    {
        (*it)->move(t_x, t_y);
    }
}

int main()
{
    std::list<Shape *> shapes;
    shapes.push_back((Shape *)new Circle);
    shapes.push_back((Shape *)new Square);
    shapes.push_back((Shape *)new Rhomb);
    shapes.push_back((Shape *)new Circle);

    drawShapes(shapes);
    moveShapes(shapes, 1, 2);
}