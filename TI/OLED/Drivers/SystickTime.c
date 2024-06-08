#include <stdint.h>
#include <stdbool.h>

#include "Time.h"
#include "SystickTime.h"
#include "sysctl.h"
#include "systick.h"

static volatile uint32_t counter;

static void SycTickHandler(void) {
  counter++;
}

void initTime(void) {
  SysTickPeriodSet(SysCtlClockGet() / 1000000UL); // 1000 for milliseconds & 1000000 for microseconds
  SysTickIntRegister(SycTickHandler);
  SysTickIntEnable();
  SysTickEnable();
}

void delay(uint32_t ms) {
  delayMicroseconds(ms * 1000UL);
}

void delayMicroseconds(uint32_t us) {
  uint32_t start = micros();
  while ((int32_t)(micros() - start) < us) {
    // Do nothing
  };
}

uint32_t millis(void) {
  return counter / 1000UL;
}

uint32_t micros(void) {
  return counter;
}

void Delay_Ms(uint32_t x)
{
  delay(x);
}

void delay_ms(uint32_t x)
{
  Delay_Ms(x);
}


void delay_us(uint32_t x)
{
  delayMicroseconds(x);
}


void Delay_Us(uint32_t x) 
{
  delayMicroseconds(x);
}



void Test_Period(Testime *Time_Lab)
{
  Time_Lab->Last_Time=Time_Lab->Now_Time;
  Time_Lab->Now_Time=micros()/1000.0f;//(10000*TIME_ISR_CNT+TimerValueGet(TIMER1_BASE,TIMER_A)/80.0f)/1000.0f;//µ¥Î»ms
  Time_Lab->Time_Delta=(Time_Lab->Now_Time-Time_Lab->Last_Time);
  Time_Lab->Time_Delta_INT=(uint16_t)(Time_Lab->Time_Delta);
}

