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
    if (x == 0) std::cout << "\033[K" << '|';

    std::cout << (v ? "\u2588" : " ");

    if (x == (le.get_field_width() - 1))
    {
        std::cout << "|\033[K\n";
    }
}


void draw_frame_line(size_t size)
{
    std::cout << "\033[K" << '+';
    for (int i = 0; i < size; ++i) std::cout << '-';
    std::cout << "+\033[K\n";
}


int main(int argc, const char **argv)
{
    if (argc < 3 || argc > 4)
    {
        std::cerr << argv[0] << " <width> <height> [delay]" << std::endl;
        return EXIT_FAILURE;
    }

    long long delay = (argc == 4) ? atol(argv[3]) : 50000;

    std::srand(time(0));

    LifeEngine le(atoi(argv[1]), atoi(argv[2]), dist_func);
    std::cout << "\033[0;0H";

    while (true)
    {
        if (!le.step()) break;
        ::usleep(delay);

        // Save cursor position.
        draw_frame_line(le.get_field_width());
        le.visualize(visitor_func);
        draw_frame_line(le.get_field_width());
        std::cout << "\033[0;0H";
    }

    return EXIT_SUCCESS;
}
