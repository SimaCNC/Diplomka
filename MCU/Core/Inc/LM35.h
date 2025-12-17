/*
 * LM35.h
 *
 *  Created on: Jul 26, 2025
 *      Author: simek
 */

#ifndef INC_LM35_H_
#define INC_LM35_H_
#include "main.h"

void LM35_Init(ADC_HandleTypeDef *hadc);
float LM35_Read(ADC_HandleTypeDef *hadc);

#endif
