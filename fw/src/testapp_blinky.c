
#include <stdint.h>
#include <string.h>

volatile uint32_t * const gpio_dir = (volatile uint32_t *)0x40010000;
volatile uint32_t * const gpio_pin = (volatile uint32_t *)0x40010004;
volatile uint32_t * const gpio_pout = (volatile uint32_t *)0x40010008;

void delay(void)
{
    // appx 50 milliseconds
    for (int i = 0; i < 125000; i++)
    {
        __asm volatile("nop");
    }
}

void main(void) 
{
    // Setup GPIO port w/ lowest 8 bits as output (LEDs).
    *gpio_dir = 0x000000FF;

    uint8_t a = 0;
    while(1)
    {
        // Running lights 2x
        for (int rpt = 0; rpt < 2; rpt++)
        {       
            for (a = 1; a != 0; a <<= 1) {
                *gpio_pout = a;
                delay();
            }
        }

        // On-off flash 4x
        for (int rpt = 0; rpt < 4; rpt++)
        {
            *gpio_pout = 0xFF;
            delay();

            *gpio_pout = 0x00;
            delay();
        }
    }
}
