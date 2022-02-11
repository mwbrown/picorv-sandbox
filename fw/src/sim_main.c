
#include <stdint.h>
#include <string.h>

volatile uint8_t * const dp8 = (volatile uint8_t *)0x20000000;
volatile uint16_t * const dp16 = (volatile uint16_t *)0x20000000;
volatile uint32_t * const dp32 = (volatile uint32_t *)0x20000000;

volatile uint32_t * const gpio_dir = (volatile uint32_t *)0x40010000;
volatile uint32_t * const gpio_pin = (volatile uint32_t *)0x40010004;
volatile uint32_t * const gpio_pout = (volatile uint32_t *)0x40010008;

uint32_t init_me = 0xABCDF00F;

// The simulator is listening for this memory access to signal
// the end of the test case.
void test_case_finish()
{
    volatile uint32_t * const finish = (volatile uint32_t *)0xF00F0000;
    *finish = 0xDEADDEAD;
    init_me++;
}

void writeData()
{
    // Write some test patterns to the RAM to inspect later.

    dp32[0] = 0xAAAABBBB;
    dp32[1] = 0xCCCCDDDD;
    dp32[2] = 0x0000FFFF;
    dp32[3] = 0xFFFF0000;

    dp32[4] = 0;
    dp32[5] = 0;
    dp32[6] = 0;
    dp32[7] = 0;

    dp8[16 + 0] = 0xFF;
    dp8[20 + 1] = 0xFF;
    dp8[24 + 2] = 0xFF;
    dp8[28 + 3] = 0xFF;

    memcpy((void *)&dp8[32], "hellowor", 8);
}

void main(void) 
{
    *gpio_dir = 0x11110000;
    *gpio_pout = ~(*gpio_pin);

    __asm volatile("nop");
    __asm volatile("nop");

    writeData();

    __asm volatile("nop");
    __asm volatile("nop");
    
    test_case_finish();
}
