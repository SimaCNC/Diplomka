/*
 * BH1750.h
 *
 *  Created on: Oct 4, 2025
 *      Author: simek
 */

#ifndef INC_BH1750_H_
#define INC_BH1750_H_

#include "main.h"

#define BH1750_I2C hi2c1
extern I2C_HandleTypeDef BH1750_I2C;
extern volatile uint8_t lux_data[2];
extern volatile uint8_t i2c_busy;


//adresa
#define BH1750_adress 0x23 << 1

//prikazy datasheet str 5/17
#define BH1750_power_down 0x00
#define BH1750_power_on 0x01
#define BH1750_reset 0x07


//mody mereni
//vicenasobne mereni
#define BH1750_cont_h_res 0x10
#define BH1750_cont_h_res2 0x11
#define BH1750_cont_l_res 0x13

//jedno mereni
#define BH1750_one_h_res 0x20
#define BH1750_one_h_res2 0x21
#define BH1750_one_l_res 0x23

//Struktura senzoru
typedef struct
{
	I2C_HandleTypeDef *hi2c;
	uint8_t adresa;
	uint8_t mod;
}BH1750_t;

uint8_t BH1750_Init(BH1750_t *dev, I2C_HandleTypeDef *hi2c, uint8_t adresa, uint8_t mod);
uint8_t BH1750_SetMode(BH1750_t *dev, uint8_t mod);
uint8_t BH1750_ReadLux(BH1750_t *dev, float *lux);
uint8_t BH1750_OneTimeRead(BH1750_t *dev, float *lux);

#endif /* INC_BH1750_H_ */
