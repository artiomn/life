#include <life_engine.h>


template<typename ElementType>
LifeEngineBase<ElementType>::LifeEngineBase(std::size_t field_width, std::size_t field_height, dist_funct f) :
    width_(field_width), height_(field_height)
{
    field_.reserve(field_height * field_width);

    for (size_t i = 0; i < field_width * field_height; ++i)
    {
        size_t x = i / field_width;
        size_t y = i - x * field_width;
        field_.push_back(f(x, y, *this));
    }
}


template<typename ElementType>
void LifeEngineBase<ElementType>::step(long step_size)
{
    const bool forward = step_size >= 0;

    for (long i = 0; i < abs(step_size); ++i) make_one_step(forward);
}


template<typename ElementType>
void LifeEngineBase<ElementType>::make_one_step(bool forward)
{

}
