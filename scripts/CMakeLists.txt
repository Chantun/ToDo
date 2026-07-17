cmake_minimum_required(VERSION 3.16)
project(ToDo LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_path(SQLITECPP_INCLUDE_DIR SQLiteCpp/SQLiteCpp.h)
find_library(SQLITECPP_LIBRARY SQLiteCpp)

include(FetchContent)

FetchContent_Declare(
    dotenv-cpp
    GIT_REPOSITORY https://github.com/laserpants/dotenv-cpp.git
    GIT_TAG master
)

FetchContent_MakeAvailable(dotenv-cpp)

add_executable(migration src/migrations.cpp)

target_include_directories(migration PRIVATE ${SQLITECPP_INCLUDE_DIR})
target_link_libraries(migration PRIVATE ${SQLITECPP_LIBRARY})
target_link_libraries(migration PRIVATE dotenv)
