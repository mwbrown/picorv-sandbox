
# TODO: support for other systems or allowing to specify path to compiler
# Currently only supports riscv64-unknown-elf-gcc on Ubuntu 21.10

# Flags for the ISA and ABI
set(SPECS_FLAGS "-specs=picolibc.specs")
set(RV32_CPU_FLAGS "-march=rv32ic -mabi=ilp32")
set(SECT_FLAGS "-ffunction-sections -fdata-sections")

set(CMAKE_SYSTEM_NAME Generic)
set(CMAKE_SYSTEM_PROCESSOR RV32)

set(CMAKE_C_COMPILER   "riscv64-unknown-elf-gcc" CACHE PATH "" FORCE)
set(CMAKE_CXX_COMPILER "riscv64-unknown-elf-g++" CACHE PATH "" FORCE)
set(CMAKE_ASM_COMPILER "riscv64-unknown-elf-gcc" CACHE PATH "" FORCE)
set(CMAKE_LINKER       "riscv64-unknown-elf-gcc" CACHE PATH "" FORCE)

# Set flags common to both C/C++
set(C_CXX_FLAGS "${SPECS_FLAGS} ${RV32_CPU_FLAGS} ${SECT_FLAGS}")

# Set up all the compiler flags for various languages based on the above.
set(CMAKE_C_FLAGS   "${C_CXX_FLAGS}" CACHE INTERNAL "" FORCE)
set(CMAKE_CXX_FLAGS "${C_CXX_FLAGS}" CACHE INTERNAL "" FORCE)
set(CMAKE_ASM_FLAGS "${RV32_CPU_FLAGS}" CACHE INTERNAL "" FORCE)

# Set linker flags.
set(CMAKE_EXE_LINKER_FLAGS "${SPECS_FLAGS} ${RV32_CPU_FLAGS} -nostartfiles -T${CMAKE_SOURCE_DIR}/rv32-fpga.ld -Wl,-gc-sections" CACHE INTERNAL "" FORCE)

# Redefine the CMAKE_C_LINK_EXECUTABLE rule because the default
# configuration also seems to include CMAKE_C_FLAGS, which is not
# desired in this case as we want low-level control of which flags
# are passed to the linker, and which to the compiler.
set(CMAKE_C_LINK_EXECUTABLE
    "<CMAKE_C_COMPILER> <CMAKE_C_LINK_FLAGS> <LINK_FLAGS> <OBJECTS> -o <TARGET> <LINK_LIBRARIES>")

set(CMAKE_C_FLAGS_DEBUG "-Og -g" CACHE INTERNAL "")
set(CMAKE_CXX_FLAGS_DEBUG "-Og -g" CACHE INTERNAL "")
set(CMAKE_ASM_FLAGS_DEBUG "-g" CACHE INTERNAL "")
set(CMAKE_EXE_LINKER_FLAGS_DEBUG "" CACHE INTERNAL "")

set(CMAKE_C_FLAGS_RELEASE "-Os -flto" CACHE INTERNAL "")
set(CMAKE_CXX_FLAGS_RELEASE "-Os -flto" CACHE INTERNAL "")
set(CMAKE_ASM_FLAGS_RELEASE "" CACHE INTERNAL "")
set(CMAKE_EXE_LINKER_FLAGS_RELEASE "-flto" CACHE INTERNAL "")

# Avoid the -rdynamic flag bug
set(CMAKE_SHARED_LIBRARY_LINK_C_FLAGS "")
set(CMAKE_SHARED_LIBRARY_LINK_CXX_FLAGS "")

# Don't bother doing a full executable sanity check.
set(CMAKE_TRY_COMPILE_TARGET_TYPE STATIC_LIBRARY)
