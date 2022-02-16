
function(_add_picosb_fw_tgt_internal FULLNAME)
    add_executable(${FULLNAME}.elf
        src/${FULLNAME}.c
    )

    target_link_libraries(${FULLNAME}.elf picosb_startup)

    # Create a .vh verilog-style dump of the target.
    add_custom_command(TARGET ${FULLNAME}.elf POST_BUILD
        COMMAND ${OBJCOPY} -O verilog --verilog-data-width=4 ${FULLNAME}.elf ${FULLNAME}.vh
        COMMENT "Converting ${FULLNAME}.vh"
    )

    # Create a .bin file of the target.
    add_custom_command(TARGET ${FULLNAME}.elf POST_BUILD
        COMMAND ${OBJCOPY} -O binary ${FULLNAME}.elf ${FULLNAME}.bin
        COMMENT "Converting ${FULLNAME}.bin"
    )

    # Create an assembly listing.
    add_custom_command(TARGET ${FULLNAME}.elf POST_BUILD
        COMMAND ${OBJDUMP} -d ${FULLNAME}.elf > ${FULLNAME}.lst
        COMMENT "Disassembling ${FULLNAME}"
    )
endfunction()

function(add_firmware_targets)
    file(GLOB TESTAPP_FILES ${PROJECT_SOURCE_DIR}/src/testapp_*.c)
    file(GLOB SIM_FILES     ${PROJECT_SOURCE_DIR}/src/sim_*.c)

    foreach(SRCFILE ${TESTAPP_FILES} ${SIM_FILES})
        get_filename_component(BASENAME ${SRCFILE} NAME_WLE)
        _add_picosb_fw_tgt_internal(${BASENAME})
    endforeach()
endfunction()
