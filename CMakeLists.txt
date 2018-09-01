cmake_minimum_required(VERSION 3.1)

project(life)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

file(GLOB headers engine/include/*.h interface/*.h)

file(GLOB src engine/src/*.cpp interface/*.cpp)

include_directories(AFTER SYSTEM engine/include)
add_executable(${PROJECT_NAME} ${headers} ${src})
