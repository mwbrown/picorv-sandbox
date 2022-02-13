
cmake_minimum_required(VERSION 3.0.0 FATAL_ERROR)

include(cmake/toolchain.cmake)
include(cmake/utils.cmake)

enable_language(C ASM)

project(picosb_fw)

add_library(picosb_startup src/crt0.s)

# Create firmware builds for each simulation file.
add_sim_target(main)

# Create firmware builds for each test app.
add_testapp_target(blinky)
