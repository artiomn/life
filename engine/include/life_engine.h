//
// Life Engine Main Class.
//

#include <functional>
#include <vector>


template<typename ElementType>
class LifeEngine
{
public:
    typedef ElementType e_type;
    typedef std::function<e_type(size_t, size_t, const e_type&)> dist_funct;

public:
    LifeEngine(std::size_t field_width, std::size_t field_height, dist_funct f);
    void step(long step_size = 1);
    const e_type& get_cell(size_t x, size_t y) const;

protected:
    void make_one_step(bool forward);

private:
    const size_t width;
    const size_t height;
    std::vector<bool> field_;
};
