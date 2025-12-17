/*
 * BH1750.c
 *
 *  Created on: Oct 5, 2025
 *      Author: simek
 */

#include "BH1750.h"

#define BH1750_korekce 1.2f // datasheet pro konverzi vzdy 1,2


uint8_t BH1750_Init(BH1750_t *dev, I2C_HandleTypeDef *hi2c, uint8_t adresa, uint8_t mod)
{
	dev->hi2c = hi2c;
	dev->adresa = adresa;
	dev->mod = mod;

	//zapnuti senzoru
	uint8_t prikaz = BH1750_power_on;
	if (HAL_I2C_Master_Transmit(dev->hi2c, dev->adresa, &prikaz, 1, HAL_MAX_DELAY) != HAL_OK)	//HAL_ok = 0
		return 1;

	HAL_Delay(1);

	// Reset
	prikaz = BH1750_reset;
	if (HAL_I2C_Master_Transmit(dev->hi2c, dev->adresa, &prikaz, 1, HAL_MAX_DELAY) != HAL_OK)
		return 1;

	HAL_Delay(1);

	//rezim mereni
	return BH1750_SetMode(dev, mod);
}/*BH1750_Init*/

uint8_t BH1750_SetMode(BH1750_t *dev, uint8_t mod)
{
	dev->mod = mod;
	if (HAL_I2C_Master_Transmit(dev->hi2c, dev->adresa, &mod, 1, HAL_MAX_DELAY) != HAL_OK)
		return HAL_ERROR;
	HAL_Delay(200); //pockat na prvni konverzi
	return HAL_OK;
}/* BH1750_SetMode */


uint8_t BH1750_ReadLux(BH1750_t *dev, float *lux)
{
	uint8_t data[2];
	if (HAL_I2C_Master_Receive(dev->hi2c, dev->adresa, data, 2, HAL_MAX_DELAY) != HAL_OK)
		return HAL_ERROR;
	uint16_t raw = (data[0] << 8) | data[1];
	*lux = (float) raw / 1.2f;  // vypocet dle datasheetu
	return HAL_OK;
}/* BH1750_ReadLux */


uint8_t BH1750_OneTimeRead(BH1750_t *dev, float *lux)
{
    //uint8_t prikaz = BH1750_one_h_res;  // nebo BH1750_ONE_LOW_RES
    //HAL_I2C_Master_Transmit(dev->hi2c, dev->adresa, &prikaz, 1, HAL_MAX_DELAY);

	if (i2c_busy == 0)
	{
		HAL_I2C_Master_Receive_DMA(dev->hi2c, dev->adresa, lux_data, 2);
		i2c_busy = 1;
    }

    return HAL_OK;
}/* BH1750_OneTimeRead */



