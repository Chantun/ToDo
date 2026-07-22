cmake_minimum_required(VERSION 3.16)
project(ToDo LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include(FetchContent)

FetchContent_Declare(
    dotenv-cpp
    GIT_REPOSITORY https://github.com/laserpants/dotenv-cpp.git
    GIT_TAG master
)
FetchContent_Declare(
    SQLiteCpp
    GIT_REPOSITORY https://github.com/SRombauts/SQLiteCpp
    GIT_TAG master
)

FetchContent_MakeAvailable(dotenv-cpp)
FetchContent_MakeAvailable(SQLiteCpp)

add_executable(migration src/migrations.cpp)

target_link_libraries(migration PRIVATE SQLiteCpp)
target_link_libraries(migration PRIVATE dotenv)
