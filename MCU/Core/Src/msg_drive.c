/*
 * msg_drive.c
 *
 *  Created on: May 8, 2025
 *      Author: simek
 */

#include "main.h"
#include "msg_drive.h"
#include "string.h"
#include "stdio.h"

void make_msg_check(char uart, char channels, uint32_t data[])
{
	char i = 0;
	char wip[32] = {0};
	char myMsg[100] = "#D";
	int msg_len = 0;

	for(i = 0; i < channels; i++)
	{
		msg_len += VlozitData(data[i], wip);
		//strcat(myMsg, wip);
		strncat(myMsg, wip, sizeof(myMsg) - strlen(myMsg) - 1);
	}

	VlozitData(msg_len, wip);
	//strcat(myMsg, wip);
	strncat(myMsg, wip, sizeof(myMsg) - strlen(myMsg) - 1);


	//strcat(myMsg, "#\n");
	strncat(myMsg, "#\n", sizeof(myMsg) - strlen(myMsg) - 1);
	//HAL_UART_Transmit(&huart1, (uint8_t*)myMsg, strlen(myMsg), 100);

	memset(wip, 0, 32);
	memset(myMsg, 0, 100);
}

int VlozitData(uint32_t num, char wip[])
{
	int cnt = 0;
	char numWip[32] = {0};

	cnt = sprintf(numWip, "#%d", num)-1;
	memset(wip, 0, 32);
	strcat(wip, numWip);

	return cnt;
}



//vraci hodnotu kolikrat se ma provest mereni pulzu (dekodovat_D)
//str prichazi ve formatu #Xxxx#\n\0 ... ale je nutne mit format  #X .. proste hastag a pak jeden znak .. napr #D nebo #A
uint32_t dekodovat_D(uint8_t str[])
{
	uint32_t mereni = 0;
	uint8_t pole[15];
	memset(pole, '\0', 15);

	for(uint8_t i = 2; str[i] != '#' && i < 15; i++)
	{
		pole[i-2] = str[i];
	}

	mereni = (uint32_t)atoi((char*)pole);

	return mereni;
} /* dekodovat_D() */



