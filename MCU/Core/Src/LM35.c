/*
 * LM35.c
 *
 *  Created on: Jul 26, 2025
 *      Author: simek
 */

#include "LM35.h"
#include "main.h"

static uint8_t calibrated = 0;

void LM35_Init(ADC_HandleTypeDef *hadc)
{
	if (calibrated == 0)
	{
		HAL_ADCEx_Calibration_Start(hadc);
		calibrated = 1;
	}
}

float LM35_Read(ADC_HandleTypeDef *hadc)
{
	uint32_t AD_vysledek = 0;
	float temp = 0;

	float filtrace = 0;
	for(uint8_t i = 0; i <20; i++)
	{
		HAL_ADC_Start(hadc);
		HAL_ADC_PollForConversion(hadc, 10);
		AD_vysledek = HAL_ADC_GetValue(hadc);
		filtrace  += AD_vysledek;
	}

	temp = (filtrace/20.0f) * 0.0805664f; //temp = (ADC_value * Vref)


	return temp;
}
