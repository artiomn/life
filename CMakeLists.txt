cmake_minimum_required(VERSION 2.8)

project(life)

file(GLOB headers engine/include/*.h interface/*.h)

file(GLOB src engine/src/*.cpp interface/*.cpp)

include_directories(AFTER SYSTEM engine/include)
add_executable(${PROJECT_NAME} ${headers} ${src})
