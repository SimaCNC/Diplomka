/*
 * UART_m.c
 *
 *  Created on: May 7, 2025
 *      Author: simek
 */
#include "main.h"
#include "UART_m.h"



UART_ISR_m(unsigned short uart, unsigned short uart_mgr[], char str[])
{
	//msg_lock = 1;
	if (uart_mgr[2] == 0)
	{
		if (uart_mgr[3])
		{
			uart_mgr[0] = 0;
			uart_mgr[1] = 1;
		}
/*		else
		{
			uart_mgr[0]++;
		}*/
	}
}

void str_empty(char str[])
{
	for(uint8_t i = 0; str[i] != '\0'; i++)
	{
		str[i] = '\0';
	}
}

uint8_t str_size(uint8_t str[])
{
	uint8_t size = 1;
	for(uint8_t i = 0; str[i] != '\n'; i++)
	{
		size++;
	}
	return size;
}






