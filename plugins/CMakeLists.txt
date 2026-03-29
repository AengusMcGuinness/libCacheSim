cmake_minimum_required(VERSION 3.12)
project(cs2640_plugins CXX C)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

find_package(PkgConfig REQUIRED)
pkg_check_modules(GLIB REQUIRED glib-2.0)

find_library(LIBCACHESIM_LIBRARY
    NAMES CacheSim libCacheSim
    PATHS /usr/local/lib /usr/lib
    DOC "libCacheSim unified library"
)

find_path(LIBCACHESIM_INCLUDE_DIR
    NAMES libCacheSim.h
    PATHS /usr/local/include /usr/include
    DOC "libCacheSim include directory"
)

if(NOT LIBCACHESIM_LIBRARY OR NOT LIBCACHESIM_INCLUDE_DIR)
    message(FATAL_ERROR "libCacheSim not found. Install it before building plugins.")
endif()

set(PLUGINS fifo)

foreach(plugin IN LISTS PLUGINS)
    add_library(plugin_${plugin}_hooks SHARED plugin_${plugin}.cpp)
    target_compile_options(plugin_${plugin}_hooks PRIVATE
        -Wall -Wextra
        -Wno-unused-parameter
    )
    target_include_directories(plugin_${plugin}_hooks PRIVATE
        ${GLIB_INCLUDE_DIRS}
        ${LIBCACHESIM_INCLUDE_DIR}
    )
    target_link_libraries(plugin_${plugin}_hooks
        ${GLIB_LIBRARIES}
        ${LIBCACHESIM_LIBRARY}
    )
endforeach()
