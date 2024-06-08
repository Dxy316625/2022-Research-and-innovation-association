#include "include.h"
#include "LED.h"
 
void LED_GPIO_Config(void)
{
 
    //LED
    //使能GPIOF时钟
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);
		while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOF))
    {
    }
    //配置RGB灯的三个引脚为输出模式
    GPIOPinTypeGPIOOutput(GPIO_PORTF_BASE, GPIO_PIN_1);
    GPIOPinTypeGPIOOutput(GPIO_PORTF_BASE, GPIO_PIN_2);
    GPIOPinTypeGPIOOutput(GPIO_PORTF_BASE, GPIO_PIN_3);
}
