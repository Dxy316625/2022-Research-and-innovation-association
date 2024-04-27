/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2023 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
#include "main.h"
#include "tim.h"
#include "usart.h"
#include "gpio.h"
#include "motor.h"
#include <math.h>
#include <stdlib.h>
#include "beep.h"
#include "OLED.h"

void AutoReloadCallback(void);
void Give_Motor_PWM(int F_MotorL_PWM,int F_MotorR_PWM);
void track_control(void);
int Position_PID(float error1);


uint8_t Serial_RxPacket[10];
uint8_t Serial_RxFlag;
int target_speed=0;//目标速度
int cnt2=0;
int start=0;
int motor_flag;
int error_position=0;
int total_distance;
int delay_time=0;
int goal_piece;
int time_cnt;
int flag=0;
int js_cnt=0;
int encoder_count; // 编码器检测到的脉冲数
int encoderNum[4] = {0};//编码数
int initial_speed=500;
int end_flag=0;
int jtag_flag=0;
int jtag_piece=0;
int piece1=0; int piece2=0; int piece3=0; int piece4=0;

/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/


/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/

/* USER CODE BEGIN PV */

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  
  /* USER CODE BEGIN 2 */
    MX_GPIO_Init();
    MX_USART3_UART_Init();
    HAL_UART_Receive_IT(&huart3, (uint8_t *)&Serial_RxPacket[0], 3);
    OLED_Init();
    OLED_ColorTurn(0);
    OLED_DisplayTurn(0);
    OLED_ShowString(0,32,&Serial_RxPacket[0],16,0);
    OLED_Refresh();

// char c;
// c='c';
//    BEEP_light();
    MX_TIM1_Init();
    MX_TIM2_Init();
    MX_TIM3_Init();
//  MX_TIM4_Init();
//  MX_TIM5_Init();
    MX_TIM6_Init();

    HAL_TIM_Base_Start_IT(&htim6);
    HAL_TIM_PWM_Start(&htim1,TIM_CHANNEL_1);
    HAL_TIM_PWM_Start(&htim1,TIM_CHANNEL_2);


//  __HAL_TIM_SetCompare(&htim1, TIM_CHANNEL_1, 50);
//  run();
    HAL_TIM_Encoder_Start(&htim2, TIM_CHANNEL_ALL);
    HAL_TIM_Encoder_Start(&htim3, TIM_CHANNEL_ALL);
//  HAL_TIM_Encoder_Start(&htim4, TIM_CHANNEL_ALL);
//  HAL_TIM_Encoder_Start(&htim5, TIM_CHANNEL_ALL);

  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
    while (1)
    {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
//        OLED_Clear();
        OLED_ShowString(0,0,"time:",16,1);
        OLED_ShowNum(40,0,time_cnt,3,16,1);
//        OLED_Refresh();
        OLED_ShowString(0,16,"distance:",16,1);
        OLED_ShowNum(72,16,total_distance,6,16,1);
//        OLED_Refresh();
        OLED_ShowString(0,32,"1:",16,1);OLED_ShowNum(16,32,piece1,4,16,1);
        OLED_ShowString(56,32,"2:",16,1);OLED_ShowNum(72,32,piece2,4,16,1);
        OLED_ShowString(0,48,"3:",16,1);OLED_ShowNum(16,48,piece3,4,16,1);
        OLED_ShowString(56,48,"4:",16,1);OLED_ShowNum(72,48,piece4,4,16,1);
//        OLED_Refresh();
//        OLED_ShowNum(0,48,__HAL_TIM_GET_COMPARE(&htim1,TIM_CHANNEL_1),4,16,0);
//        OLED_ShowNum(32,48,__HAL_TIM_GET_COMPARE(&htim1,TIM_CHANNEL_2),4,16,0);
//        OLED_ShowNum(0,48,jtag_piece,4,16,0);
        OLED_Refresh();
//        Give_Motor_PWM(-200,600);
        
        
        if(start==0)
        {
            stop();
        }
        else if (delay_time!=0)
        {
            stop();
            BEEP_light();
            LED_light();
            int i=0;
            for (i=0;i<500000;i++);
        }
        else if (end_flag==1)
        {
            HAL_TIM_Base_Stop(&htim6);
            __HAL_TIM_SET_COMPARE(&htim1,TIM_CHANNEL_1, 500);
            __HAL_TIM_SET_COMPARE(&htim1,TIM_CHANNEL_2, 500);
            int i=0;
            for(i=0;i<5000000;i++);
            HAL_TIM_Base_Stop(&htim1);
            HAL_NVIC_DisableIRQ(USART3_IRQn);
            stop();
            
        }
        else
        track_control();

        
//        if(jtag_flag==1)
//        {
//          HAL_Delay(100);
//         js_cnt++;
//           jtag_flag=0; 
//           if((js_cnt-1)%2==1)
//           {
//               jtag_piece=js_cnt/2;
//           }
//           else
//           {
//               jtag_piece=(js_cnt-1)/2;
//               switch(jtag_piece)
//           {
//                   case 1:
//                       piece1=total_distance;break;
//                   case 2:
//                       piece2=total_distance;break;
//                   case 3:
//                       piece3=total_distance;break;
//                   case 4:
//                       piece4=total_distance;break;
//                   default: break;
//           }
//                BEEP_light();
//                LED_light();
//           }
           
//        }
        
           if(jtag_flag==1)
        {
          HAL_Delay(50);
          js_cnt++;
           jtag_flag=0; 
           if((js_cnt)%2==1)
           {
               jtag_piece=(js_cnt+1)/2;
                switch(jtag_piece)
           {
                   case 1:
                       piece1=total_distance;break;
                   case 2:
                       piece2=total_distance;break;
                   case 3:
                       piece3=total_distance;break;
                   case 4:
                       piece4=total_distance;break;
                   default: break;
           }
                BEEP_light();
                LED_light();
           }
           
           
           else
           {
               jtag_piece=(js_cnt)/2;
           }
           

        }
        
        
//        if(start==0)
//        {
//            stop();
//        }
//        else if (delay_time!=0)
//        {
//            stop();
//            BEEP_light();
//            LED_light();
//            int i=0;
//            for (i=0;i<500000;i++);
//        }
//        else if (end_flag==1)
//        {
//            HAL_TIM_Base_Stop(&htim6);
//            __HAL_TIM_SET_COMPARE(&htim1,TIM_CHANNEL_1, 500);
//            __HAL_TIM_SET_COMPARE(&htim1,TIM_CHANNEL_2, 500);
//            int i=0;
//            for(i=0;i<5000000;i++);
//            HAL_TIM_Base_Stop(&htim1);
//            HAL_NVIC_DisableIRQ(USART3_IRQn);
//            stop();
//            
//        }
//        else
//        track_control();
    }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE;
  RCC_OscInitStruct.HSEState = RCC_HSE_ON;
  RCC_OscInitStruct.HSEPredivValue = RCC_HSE_PREDIV_DIV1;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
  RCC_OscInitStruct.PLL.PLLMUL = RCC_PLL_MUL9;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV2;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_2) != HAL_OK)
  {
    Error_Handler();
  }
}

/* USER CODE BEGIN 4 */

void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim)
{


    if(htim->Instance==htim6.Instance)
    {
        static int cnt=0;
        Serial_RxFlag=0;
        cnt++;
        cnt2++;
        if(cnt2>9)
        {
            AutoReloadCallback(); // 定时调用
            cnt2=0;
        }
        if(cnt>99)
        {
            time_cnt++;
            cnt=0;
            if(delay_time>0)
                delay_time--;
            else
                flag=0;
        }
        __HAL_TIM_CLEAR_FLAG(&htim6,TIM_FLAG_UPDATE);
    }

}

void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin)
{
    if(GPIO_Pin==JTAG_Pin)
    {
       
        jtag_flag=1;
        flag=1;
        if(start==0)
        {
             jtag_flag=0;
            flag=0;
        }
        if((jtag_piece==goal_piece-1)&&(js_cnt%2==0))
        {
        delay_time=2;
//            stop();
        }
        else if((jtag_piece==4-1)&&(js_cnt%2==0))
        {
            delay_time=5;
//            stop();
        }
        else
            delay_time=0;
       
    }
}



void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{


    if(start==0)
    {
        switch(Serial_RxPacket[1])
        {
        case'A':
            goal_piece=1;
            break;
        case'B':
            goal_piece=2;
            break;
        case'C':
            goal_piece=3;
            break;
        case'D':
            goal_piece=4;
            break;

        }
        start=1;
    }
    else
    {
        uint8_t *p;
        static int RxState=0;
        static uint8_t pRxPacket = 1;
        if (RxState == 0)
        {
            if (Serial_RxPacket[0] == '[' )
            {
                RxState = 1;
                pRxPacket = 1;
                int i ;
                for(i=1; Serial_RxPacket[i]!='\0'; i++)
                {
                    Serial_RxPacket[i]=0;
                }
            }
        }
        else if (RxState == 1)
        {
            if (Serial_RxPacket[0] == ']')
            {
                RxState = 0;
                Serial_RxPacket[pRxPacket] = '\0';
            }
            else
            {
                Serial_RxPacket[pRxPacket] = Serial_RxPacket[0];
                if(Serial_RxPacket[pRxPacket]=='e')
                end_flag=1;
                pRxPacket ++;
            }
        }
        
        p=&Serial_RxPacket[1];
        error_position=code_transform(p)-80;
    }
    HAL_UART_Receive_IT(&huart3, (uint8_t *)&Serial_RxPacket[0], 1);



}

void AutoReloadCallback(void)
{
//    int A1,B1;
//    float rotateSpeed[4] = {0};
    static int distance[4]= {0};//距离


    //距离=圈数*轮子周长  单位：cm   acos(-1.0)是π,轮子直径为4.8cm
    distance[0] = (float)(__HAL_TIM_GET_COUNTER(&htim2))/(4 * 13 * 20)*acos(-1.0)*4.8;
    distance[1] = (float)(__HAL_TIM_GET_COUNTER(&htim3))/(4 * 13 * 20)*acos(-1.0)*4.8;
    __HAL_TIM_SET_COUNTER(&htim2,0);
    __HAL_TIM_SET_COUNTER(&htim3,0);
//    switch(motor_flag)
//    {
//    case 0:
//        break;
//    case 1:
    if(distance[0]<100&&distance[1]<100)
        total_distance +=(distance[0]+distance[1])/2;
    else if(distance[0]<100&&distance[1]>100)
        total_distance +=distance[0];
    else if(distance[0]>100&&distance[1]<100)
        total_distance +=distance[1];
//        break;
//    case 2:
//        total_distance+=distance[0];
//        break;
//    case 3:
//        total_distance+=distance[1];
//        break;
//    default:
//        break;
//    }
    //距离累加并求平均值


    //转速(1秒钟转多少圈)=单位时间内的计数值/(总分辨率*时间系数) 单位：rad/s

}

int Position_PID(float error1)
{
    float Position_KP = 10.3, Position_KI = 0.06, Position_KD = 4.8;                                       // pid
    static float error, out, Integral_error, error_last;
    int new_out;
    // 误差 输出 积分 上一次误差
    error =  error1;                                                                      // 求出速度偏差，由测量值减去目标值。
    Integral_error += error;
//if(Integral_error>80)
//    Integral_error=80;
//if(Integral_error<-80)
//     Integral_error=-80;
    // 求出偏差的积分
    out = Position_KP * error + Position_KI * Integral_error + Position_KD * (error - error_last); // 位置式PID控制器
    if(out>400)
        out=400;
    if(out<-400)
        out=-400;
    new_out=(int)out;
    error_last = error;                                                                            // 保存上一次偏差
    return new_out;                                                                                    // 增量输出
}


void Give_Motor_PWM(int F_MotorL_PWM,int F_MotorR_PWM)
{
//    F_MotorL_PWM=limit_speed(F_MotorL_PWM);
//    F_MotorR_PWM=limit_speed(F_MotorR_PWM);
    if (F_MotorL_PWM>0) //左前电机正转
    {
       HAL_GPIO_WritePin(LF_1_GPIO_Port,LF_1_Pin,GPIO_PIN_SET); 
       HAL_GPIO_WritePin(LF_2_GPIO_Port,LF_2_Pin,GPIO_PIN_RESET);
        
    }
    else              //左前电机反转
    {
       HAL_GPIO_WritePin(LF_1_GPIO_Port,LF_1_Pin,GPIO_PIN_RESET); 
       HAL_GPIO_WritePin(LF_2_GPIO_Port,LF_2_Pin,GPIO_PIN_SET);
    }

    if (F_MotorR_PWM>0) //右前电机正转
    {
        HAL_GPIO_WritePin(RF_1_GPIO_Port,RF_1_Pin,GPIO_PIN_SET);
        HAL_GPIO_WritePin(RF_2_GPIO_Port,RF_2_Pin,GPIO_PIN_RESET);//右前
    }
    else              //右前电机反转
    {
        HAL_GPIO_WritePin(RF_1_GPIO_Port,RF_1_Pin,GPIO_PIN_RESET);
        HAL_GPIO_WritePin(RF_2_GPIO_Port,RF_2_Pin,GPIO_PIN_SET);//右前
    }
   
    __HAL_TIM_SET_COMPARE(&htim1,TIM_CHANNEL_1, abs(F_MotorL_PWM));
    __HAL_TIM_SET_COMPARE(&htim1,TIM_CHANNEL_2, abs(F_MotorR_PWM));
   

}

void track_control(void)
{
    int L_speed ;
    int R_speed ;
    L_speed = initial_speed + Position_PID(error_position)+50;
    R_speed = initial_speed - Position_PID(error_position);

    Give_Motor_PWM(L_speed,R_speed);
}

void delay(void)
{
    int i=0;
    for(i=0;i<5;i++)
    {
        BEEP_light(); 
        
    }
}
    
/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
    /* User can add his own implementation to report the HAL error return state */
    __disable_irq();
    while (1)
    {
    }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
    /* User can add his own implementation to report the file name and line number,
       ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
