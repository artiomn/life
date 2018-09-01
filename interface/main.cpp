#include <cstdlib>
#include <ctime>
#include <iostream>
#include <unistd.h>

#include <life_engine.h>


LifeEngine::e_type dist_func(size_t x, size_t y, const LifeEngine&)
{
    return rand() <= RAND_MAX / 2;
}


void visitor_func(size_t x, size_t y, const LifeEngine::e_type& v, const LifeEngine& le)
{
    std::cout << (v ? '*' : '#');

    if (x == (le.get_field_width() - 1))
    {
        std::cout << "\n";
    }
}


int main()
{
    std::srand(time(0));
    LifeEngine le(20, 10, dist_func);

    // Save cursor position.
    std::cout << "\033[s";

    while (true)
    {
        if (!le.step()) break;
        ::usleep(1000);

        std::cout << "\033[u";
        le.visualize(visitor_func);
    }
}
