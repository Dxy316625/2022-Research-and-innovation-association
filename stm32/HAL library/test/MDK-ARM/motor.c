#include "motor.h"
#include "tim.h"
#include "main.h"




//void run(int* A,int* B)
//{
//    HAL_GPIO_WritePin(LF_1_GPIO_Port,LF_1_Pin,GPIO_PIN_SET); HAL_GPIO_WritePin(LF_2_GPIO_Port,LF_2_Pin,GPIO_PIN_RESET);//左前
//    HAL_GPIO_WritePin(RF_1_GPIO_Port,RF_1_Pin,GPIO_PIN_RESET); HAL_GPIO_WritePin(RF_2_GPIO_Port,RF_2_Pin,GPIO_PIN_SET);//右前
////    HAL_GPIO_WritePin(LB_1_GPIO_Port,LB_1_Pin,GPIO_PIN_SET); HAL_GPIO_WritePin(LB_2_GPIO_Port,LB_2_Pin,GPIO_PIN_RESET);//左后
////    HAL_GPIO_WritePin(RB_1_GPIO_Port,RB_1_Pin,GPIO_PIN_RESET); HAL_GPIO_WritePin(RB_2_GPIO_Port,RB_2_Pin,GPIO_PIN_SET);//右后
//    *A=40;*B=40;

//}
//void left(int* A,int* B)
//{
//    HAL_GPIO_WritePin(LF_1_GPIO_Port,LF_1_Pin,GPIO_PIN_SET); HAL_GPIO_WritePin(LF_2_GPIO_Port,LF_2_Pin,GPIO_PIN_RESET);//左前
//    HAL_GPIO_WritePin(RF_1_GPIO_Port,RF_1_Pin,GPIO_PIN_RESET); HAL_GPIO_WritePin(RF_2_GPIO_Port,RF_2_Pin,GPIO_PIN_SET);//右前
//    *A=50-*A;
////    HAL_GPIO_WritePin(LB_1_GPIO_Port,LB_1_Pin,GPIO_PIN_RESET); HAL_GPIO_WritePin(LB_2_GPIO_Port,LB_2_Pin,GPIO_PIN_SET);//左后
////    HAL_GPIO_WritePin(RB_1_GPIO_Port,RB_1_Pin,GPIO_PIN_RESET); HAL_GPIO_WritePin(RB_2_GPIO_Port,RB_2_Pin,GPIO_PIN_SET);//右后
//    
//    
//}
//void right(int* A,int* B)
//{
//    
//    HAL_GPIO_WritePin(LF_1_GPIO_Port,LF_1_Pin,GPIO_PIN_SET); HAL_GPIO_WritePin(LF_2_GPIO_Port,LF_2_Pin,GPIO_PIN_RESET);//左前
//    HAL_GPIO_WritePin(RF_1_GPIO_Port,RF_1_Pin,GPIO_PIN_RESET); HAL_GPIO_WritePin(RF_2_GPIO_Port,RF_2_Pin,GPIO_PIN_SET);//右前
//    *B=(*B/2);
////    HAL_GPIO_WritePin(LB_1_GPIO_Port,LB_1_Pin,GPIO_PIN_SET); HAL_GPIO_WritePin(LB_2_GPIO_Port,LB_2_Pin,GPIO_PIN_RESET);//左后
////    HAL_GPIO_WritePin(RB_1_GPIO_Port,RB_1_Pin,GPIO_PIN_SET); HAL_GPIO_WritePin(RB_2_GPIO_Port,RB_2_Pin,GPIO_PIN_RESET);//右后
//   
//    
//}

void stop(void)
{
    HAL_GPIO_WritePin(LF_1_GPIO_Port,LF_1_Pin,GPIO_PIN_RESET); HAL_GPIO_WritePin(LF_2_GPIO_Port,LF_2_Pin,GPIO_PIN_RESET);//左前
    HAL_GPIO_WritePin(RF_1_GPIO_Port,RF_1_Pin,GPIO_PIN_RESET); HAL_GPIO_WritePin(RF_2_GPIO_Port,RF_2_Pin,GPIO_PIN_RESET);//右前
//    HAL_GPIO_WritePin(LB_1_GPIO_Port,LB_1_Pin,GPIO_PIN_RESET); HAL_GPIO_WritePin(LB_2_GPIO_Port,LB_2_Pin,GPIO_PIN_RESET);//左后
//    HAL_GPIO_WritePin(RB_1_GPIO_Port,RB_1_Pin,GPIO_PIN_RESET); HAL_GPIO_WritePin(RB_2_GPIO_Port,RB_2_Pin,GPIO_PIN_RESET);//右后

    
}

//RB_1_Pin GPIO_PIN_12
//  RB_1_GPIO_Port GPIOB
//  RB_2_Pin GPIO_PIN_13
//  RB_2_GPIO_Port GPIOB
//  LB_1_Pin GPIO_PIN_14
//  LB_1_GPIO_Port GPIOB
//  LB_2_Pin GPIO_PIN_15
//  LB_2_GPIO_Port GPIOB
//  RF_1_Pin GPIO_PIN_6
//  RF_1_GPIO_Port GPIOC
//  RF_2_Pin GPIO_PIN_7
//  RF_2_GPIO_Port GPIOC
//  LF_1_Pin GPIO_PIN_8
//  LF_1_GPIO_Port GPIOC
//  LF_2_Pin GPIO_PIN_9
//  LF_2_GPIO_Port GPIOC


