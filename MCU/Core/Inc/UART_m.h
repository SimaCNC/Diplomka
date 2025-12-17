/*
 * UART_m.h
 *
 *  Created on: May 7, 2025
 *      Author: simek
 */

#ifndef INC_UART_M_H_
#define INC_UART_M_H_

extern volatile uint8_t msg_lock;
//extern UART_HandleTypeDef huart1;


void UART_ISR_m(unsigned short uart,unsigned short uart_mgr[], char str[]);
void str_empty(char str[]);
uint8_t str_size(uint8_t str[]);



#endif /* INC_UART_M_H_ */
