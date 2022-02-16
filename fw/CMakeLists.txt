
cmake_minimum_required(VERSION 3.0.0 FATAL_ERROR)

include(cmake/toolchain.cmake)
include(cmake/utils.cmake)

enable_language(C ASM)

project(picosb_fw)

add_library(picosb_startup src/crt0.s)

# Automatically detect targets with sim_ or testapp_ prefixes.
add_firmware_targets()
