/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file    usart.c
  * @brief   This file provides code for the configuration
  *          of the USART instances.
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
/* Includes ------------------------------------------------------------------*/
#include "usart.h"

/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

UART_HandleTypeDef huart3;

/* USART3 init function */

void MX_USART3_UART_Init(void)
{

  /* USER CODE BEGIN USART3_Init 0 */

  /* USER CODE END USART3_Init 0 */

  /* USER CODE BEGIN USART3_Init 1 */

  /* USER CODE END USART3_Init 1 */
  huart3.Instance = USART3;
  huart3.Init.BaudRate = 115200;
  huart3.Init.WordLength = UART_WORDLENGTH_8B;
  huart3.Init.StopBits = UART_STOPBITS_1;
  huart3.Init.Parity = UART_PARITY_NONE;
  huart3.Init.Mode = UART_MODE_TX_RX;
  huart3.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart3.Init.OverSampling = UART_OVERSAMPLING_16;
  if (HAL_UART_Init(&huart3) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN USART3_Init 2 */

  /* USER CODE END USART3_Init 2 */

}

void HAL_UART_MspInit(UART_HandleTypeDef* uartHandle)
{

  GPIO_InitTypeDef GPIO_InitStruct = {0};
  if(uartHandle->Instance==USART3)
  {
  /* USER CODE BEGIN USART3_MspInit 0 */

  /* USER CODE END USART3_MspInit 0 */
    /* USART3 clock enable */
    __HAL_RCC_USART3_CLK_ENABLE();

    __HAL_RCC_GPIOB_CLK_ENABLE();
    /**USART3 GPIO Configuration
    PB10     ------> USART3_TX
    PB11     ------> USART3_RX
    */
    GPIO_InitStruct.Pin = USART3_TX_Pin;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
    HAL_GPIO_Init(USART3_TX_GPIO_Port, &GPIO_InitStruct);

    GPIO_InitStruct.Pin = USART3_RX_Pin;
    GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
    GPIO_InitStruct.Pull = GPIO_PULLUP;
    HAL_GPIO_Init(USART3_RX_GPIO_Port, &GPIO_InitStruct);

    /* USART3 interrupt Init */
    HAL_NVIC_SetPriority(USART3_IRQn, 0, 0);
    HAL_NVIC_EnableIRQ(USART3_IRQn);
  /* USER CODE BEGIN USART3_MspInit 1 */

  /* USER CODE END USART3_MspInit 1 */
  }
}

void HAL_UART_MspDeInit(UART_HandleTypeDef* uartHandle)
{

  if(uartHandle->Instance==USART3)
  {
  /* USER CODE BEGIN USART3_MspDeInit 0 */

  /* USER CODE END USART3_MspDeInit 0 */
    /* Peripheral clock disable */
    __HAL_RCC_USART3_CLK_DISABLE();

    /**USART3 GPIO Configuration
    PB10     ------> USART3_TX
    PB11     ------> USART3_RX
    */
    HAL_GPIO_DeInit(GPIOB, USART3_TX_Pin|USART3_RX_Pin);

    /* USART3 interrupt Deinit */
    HAL_NVIC_DisableIRQ(USART3_IRQn);
  /* USER CODE BEGIN USART3_MspDeInit 1 */

  /* USER CODE END USART3_MspDeInit 1 */
  }
}

/* USER CODE BEGIN 1 */

int code_transform(uint8_t*code)
{
    int x=0,y=0,z=0,sum=0;
    switch(*code)
    {
    case '0':
        x=0;
        break;
    case '1':
        x=1;
        break;
    case '2':
        x=2;
        break;
    case '3':
        x=3;
        break;
    case '4':
        x=4;
        break;
    case '5':
        x=5;
        break;
    case '6':
        x=6;
        break;
    case '7':
        x=7;
        break;
    case '8':
        x=8;
        break;
    case '9':
        x=9;
        break;
    }
    switch(*(code+1))
    {
    case '0':
        y=0;
        break;
    case '1':
        y=1;
        break;
    case '2':
        y=2;
        break;
    case '3':
        y=3;
        break;
    case '4':
        y=4;
        break;
    case '5':
        y=5;
        break;
    case '6':
        y=6;
        break;
    case '7':
        y=7;
        break;
    case '8':
        y=8;
        break;
    case '9':
        y=9;
        break;
    }
    if((*(code+2))!='\0')
    {
     switch(*(code+2))
    {
    case '0':
        z=0;
        break;
    case '1':
        z=1;
        break;
    case '2':
        z=2;
        break;
    case '3':
        z=3;
        break;
    case '4':
        z=4;
        break;
    case '5':
        z=5;
        break;
    case '6':
        z=6;
        break;
    case '7':
        z=7;
        break;
    case '8':
        z=8;
        break;
    case '9':
        z=9;
        break;
    }
    sum=100*x+10*y+z;
    }
    else
        sum=10*x+y;
    return sum;
}

/* USER CODE END 1 */
