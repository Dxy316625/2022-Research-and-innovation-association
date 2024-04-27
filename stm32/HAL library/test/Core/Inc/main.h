/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.h
  * @brief          : Header for main.c file.
  *                   This file contains the common defines of the application.
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
/* USER CODE END Header */

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __MAIN_H
#define __MAIN_H

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "stm32f1xx_hal.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Exported types ------------------------------------------------------------*/
/* USER CODE BEGIN ET */

/* USER CODE END ET */

/* Exported constants --------------------------------------------------------*/
/* USER CODE BEGIN EC */

/* USER CODE END EC */

/* Exported macro ------------------------------------------------------------*/
/* USER CODE BEGIN EM */

/* USER CODE END EM */

/* Exported functions prototypes ---------------------------------------------*/
void Error_Handler(void);

/* USER CODE BEGIN EFP */

/* USER CODE END EFP */

/* Private defines -----------------------------------------------------------*/
#define RF_1_Pin GPIO_PIN_0
#define RF_1_GPIO_Port GPIOC
#define RF_2_Pin GPIO_PIN_1
#define RF_2_GPIO_Port GPIOC
#define LF_1_Pin GPIO_PIN_1
#define LF_1_GPIO_Port GPIOA
#define LF_2_Pin GPIO_PIN_2
#define LF_2_GPIO_Port GPIOA
#define JTAG_Pin GPIO_PIN_0
#define JTAG_GPIO_Port GPIOB
#define JTAG_EXTI_IRQn EXTI0_IRQn
#define BEEP_Pin GPIO_PIN_2
#define BEEP_GPIO_Port GPIOB
#define USART3_TX_Pin GPIO_PIN_10
#define USART3_TX_GPIO_Port GPIOB
#define USART3_RX_Pin GPIO_PIN_11
#define USART3_RX_GPIO_Port GPIOB
#define PWM1_Pin GPIO_PIN_8
#define PWM1_GPIO_Port GPIOA
#define PWM2_Pin GPIO_PIN_9
#define PWM2_GPIO_Port GPIOA
#define ENCODER1_1_Pin GPIO_PIN_15
#define ENCODER1_1_GPIO_Port GPIOA
#define LED1_Pin GPIO_PIN_2
#define LED1_GPIO_Port GPIOD
#define ENCODER1_2_Pin GPIO_PIN_3
#define ENCODER1_2_GPIO_Port GPIOB
#define ENCODER2_1_Pin GPIO_PIN_4
#define ENCODER2_1_GPIO_Port GPIOB
#define ENCODER2_2_Pin GPIO_PIN_5
#define ENCODER2_2_GPIO_Port GPIOB
#define SCL_Pin GPIO_PIN_8
#define SCL_GPIO_Port GPIOB
#define SDA_Pin GPIO_PIN_9
#define SDA_GPIO_Port GPIOB

/* USER CODE BEGIN Private defines */

/* USER CODE END Private defines */

#ifdef __cplusplus
}
#endif

#endif /* __MAIN_H */
