#include <life_engine.h>

#include <algorithm>
#include <iostream>
#include <stdexcept>


template<typename ElementType>
LifeEngineBase<ElementType>::LifeEngineBase(std::size_t field_width, std::size_t field_height, dist_funct df) :
    width_(field_width), height_(field_height), change_list_capacity_(std::max(field_width, field_height))
{
    if (field_width < min_size || field_height < min_size)
    {
        throw std::invalid_argument("A very small field");
    }

    field_.reserve(field_height * field_width);
    change_list_.reserve(field_width);

    for (size_t i = 0; i < field_width * field_height; ++i)
    {
        auto coords = std::move(get_xy_from_counter(i));

        field_.push_back(df(coords.first, coords.second, *this));
    }
}


template<typename ElementType>
std::pair<size_t, size_t> &&LifeEngineBase<ElementType>::get_xy_from_counter(size_t cell_index) const
{
    std::pair<size_t, size_t> result;

    result.second = cell_index / width_;
    result.first = cell_index % width_;

    return std::move(result);
}


template<typename ElementType>
void LifeEngineBase<ElementType>::visualize(vis_funct vf)
{
    for (size_t i = 0; i < field_.size(); ++i)
    {
        auto coords = get_xy_from_counter(i);
        vf(coords.first, coords.second, field_[i], *this);
    }
}


template<typename ElementType>
bool LifeEngineBase<ElementType>::step(long step_size)
{
    if (step_size < 0)
    {
        throw std::invalid_argument("Negative step_size is not supported");
    }

    bool result = false;
    const bool forward = step_size >= 0;

    for (long i = 0; i < abs(step_size); ++i) result |= make_one_step(forward);

    return result;
}


template<typename ElementType>
size_t LifeEngineBase<ElementType>::cell_active_neighbors_count(size_t cell_index) const
{
    // 1-order Moore neighborhood test (https://ru.wikipedia.org/wiki/Окрестность_Мура).
    size_t live_cells = 0;
    auto ci_coords = get_xy_from_counter(cell_index);

    for (int i = -1; i < 2; ++i)
    {
        for (int j = -1; j < 2; ++j)
        {
            if (i == 0 && j == 0) continue;

            long x = ci_coords.first + i;
            long y = ci_coords.second + j;

            if (x < 0) x = width_ - 1;
            else if (x == width_) x = 0;

            if (y < 0) y = height_ - 1;
            else if (y == height_) y = 0;

            /*std::cout << "X = " << x << ", Y = " << y
                      << ", P = " <<  ci_coords.first << ", " << ci_coords.second
                      << ", N = " << (y % height_) * width_ + (x % width_)
                      << ", size = " << field_.size()
                      << std::endl;
            */
            live_cells += static_cast<int>(field_[(y % height_) * width_ + (x % width_)]);
        }
    }

    return live_cells;
}


template<typename ElementType>
bool LifeEngineBase<ElementType>::make_one_step(bool /*forward*/)
{
    size_t live_cells_count = 0;

    for (size_t i = 0; i < field_.size(); ++i)
    {
        const auto cell_value = field_[i];
        const auto neighbors_count = cell_active_neighbors_count(i);

        live_cells_count += static_cast<size_t>(cell_value);

        // Game ruleset.
        if (cell_value)
        {
            // Live cell.
            const auto live_condition = static_cast<int>(neighbors_limit) - neighbors_count;
            if (live_condition != 0 && live_condition != 1)
            {
                // Kill it with fire!
                change_list_.push_back(i);
            }
        }
        else
        {
            // Dead cell.
            if (neighbors_count == neighbors_limit)
            {
                // She's alive, alive!
                change_list_.push_back(i);
            }
        }
    }

    if (change_list_.empty()) live_cells_count = 0;

    for (auto i : change_list_)
    {
        // Change field values.
        field_[i] = !field_[i];
    }

    change_list_.clear();

    if (change_list_.capacity() > change_list_capacity_) change_list_.reserve(change_list_capacity_);

    return live_cells_count != 0;
}


template class LifeEngineBase<bool>;
