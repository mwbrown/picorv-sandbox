
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

function(add_sim_target NAME)
    _add_picosb_fw_tgt_internal(sim_${NAME})
endfunction()

function(add_testapp_target NAME)
    _add_picosb_fw_tgt_internal(testapp_${NAME})
endfunction()