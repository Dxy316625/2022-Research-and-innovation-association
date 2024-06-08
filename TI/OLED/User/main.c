#include "include.h"
#include "uart.h"
#include "uartstdio.h"
#include "LED.h"
 
 #ifdef DEBUG
void
__error__(char *pcFilename, uint32_t ui32Line)
{
}
#endif


int main(void)
{     

	//初始化函数
   LED_GPIO_Config();
 
	
	/*OLED初始化*/
	OLED_Init();

	/*在(0, 0)位置显示字符'A'，字体大小为8*16点阵*/
	OLED_ShowChar(0, 0, 'A', OLED_8X16);
	
	/*调用OLED_Update函数，将OLED显存数组的内容更新到OLED硬件进行显示*/
	OLED_Update();
	

  while(1)
  {


			
   }
}


