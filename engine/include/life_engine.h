//
// Life Engine Main Class.
//

#include <functional>
#include <vector>


template<typename ElementType>
class LifeEngineBase
{
public:
    typedef ElementType e_type;
    typedef std::function<e_type(size_t, size_t, const LifeEngineBase&)> dist_funct;

public:
    LifeEngineBase(std::size_t field_width, std::size_t field_height, dist_funct f);
    void step(long step_size = 1);

    const e_type& get_cell(size_t x, size_t y) const { return field_[x * width_ + y]; }
    const size_t get_field_width() const { return width_; }
    const size_t get_field_height() const { return height_; }

protected:
    void make_one_step(bool forward);

private:
    const size_t width_;
    const size_t height_;
    std::vector<e_type> field_;
};


typedef LifeEngineBase<bool> LifeEngine;
