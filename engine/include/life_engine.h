//
// Life Engine Main Class.
//

#include <functional>
#include <utility>
#include <vector>


template<typename ElementType>
class LifeEngineBase
{
public:
    typedef ElementType e_type;
    typedef std::function<e_type(size_t, size_t, const LifeEngineBase&)> dist_funct;
    typedef std::function<void(size_t, size_t, const e_type&, const LifeEngineBase&)> vis_funct;

    // Minimum field size. Hard limit.
    const size_t min_size = 3;

    // The number of neighbors is necessary to make changes.
    const size_t neighbors_limit = 3;

public:
    LifeEngineBase(std::size_t field_width, std::size_t field_height, dist_funct df);

    bool step(long step_size = 1);

    void visualize(vis_funct vf);
    const e_type& get_cell(size_t x, size_t y) const { return field_[(y % height_) * width_ + (x % width_)]; }

    const size_t get_field_width() const { return width_; }
    const size_t get_field_height() const { return height_; }

protected:
    bool make_one_step(bool forward);

private:
    std::pair<size_t, size_t> &&get_xy_from_counter(size_t cell_index) const;
    size_t cell_active_neighbors_count(size_t cell_index) const;

private:
    // Columns number.
    const size_t width_;
    // Rows number.
    const size_t height_;

    const size_t change_list_capacity_;

    std::vector<e_type> field_;
    std::vector<size_t> change_list_;
};


typedef LifeEngineBase<bool> LifeEngine;
