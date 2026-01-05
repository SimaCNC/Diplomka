/*
 * BME280.h
 *
 *  Created on: Sep 6, 2025
 *
 *      inspirovano z: BME280_STM32.h
 * 	  	  	  	  	   ControllersTech.com
 *	  	  	  	  	   Updated:    Dec 14, 2021
 */

#ifndef INC_BME280_H_
#define INC_BME280_H_

#include "main.h"

#define BME280_I2C hi2c1
extern I2C_HandleTypeDef BME280_I2C;
extern volatile uint8_t i2c_busy;

#define SUPPORT_64BIT 1

#define BME280_ADDRESS 0xEC // SDO je nejspise na GND, tak adresa 0xEC viz. datasheet

int BME280_Config (uint8_t osrs_t, uint8_t osrs_p, uint8_t osrs_h, uint8_t mode, uint8_t t_sb, uint8_t filter);

void BME280_WakeUP(void);

/* mereni teploty, tlaku a vlhkosti
 */
void BME280_Measure(float *temperature, float *pressure, float *humidity);

// Oversampling definitions
#define OSRS_OFF    	0x00
#define OSRS_1      	0x01
#define OSRS_2      	0x02
#define OSRS_4      	0x03
#define OSRS_8      	0x04
#define OSRS_16     	0x05


// MODE Definitions
#define MODE_SLEEP      0x00
#define MODE_FORCED     0x01
#define MODE_NORMAL     0x03


// Standby Time
#define T_SB_0p5    	0x00
#define T_SB_62p5   	0x01
#define T_SB_125    	0x02
#define T_SB_250    	0x03
#define T_SB_500    	0x04
#define T_SB_1000   	0x05
#define T_SB_10     	0x06
#define T_SB_20     	0x07


// IIR Filter Coefficients
#define IIR_OFF     	0x00
#define IIR_2       	0x01
#define IIR_4       	0x02
#define IIR_8       	0x03
#define IIR_16      	0x04


// REGISTERS DEFINITIONS
#define ID_REG      	0xD0
#define RESET_REG  		0xE0
#define CTRL_HUM_REG    0xF2
#define STATUS_REG      0xF3
#define CTRL_MEAS_REG   0xF4
#define CONFIG_REG      0xF5
#define PRESS_MSB_REG   0xF7
#endif /* INC_BME280_H_ */
