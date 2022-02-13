
function(add_sim_target NAME)
    add_executable(sim_${NAME}.elf
        #src/crt0.s
        src/sim_${NAME}.c
    )

    target_link_libraries(sim_${NAME}.elf picosb_startup)
endfunction()

function(add_testapp_target NAME)
    add_executable(testapp_${NAME}.elf
        #src/crt0.s
        src/testapp_${NAME}.c
    )

    target_link_libraries(testapp_${NAME}.elf picosb_startup)
endfunction()
