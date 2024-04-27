#include "beep.h"
#include "main.h"
	   
//到时候根据需要再调整

/**************************************************************************
函数功能：蜂鸣器接口初始化
入口参数：无 
返回  值：无
**************************************************************************/	    
//蜂鸣器初始化

void BEEP_light(void)
{
   
   HAL_GPIO_WritePin(BEEP_GPIO_Port,BEEP_Pin,GPIO_PIN_RESET);
  int i=0;
    for (i=0;i<500000;i++);
   HAL_GPIO_WritePin(BEEP_GPIO_Port,BEEP_Pin,GPIO_PIN_SET);
}

void LED_light(void)
{
   
   HAL_GPIO_WritePin(LED1_GPIO_Port,LED1_Pin,GPIO_PIN_RESET);
 int i=0;
    for (i=0;i<500000;i++);
   HAL_GPIO_WritePin(LED1_GPIO_Port,LED1_Pin,GPIO_PIN_SET);
}
