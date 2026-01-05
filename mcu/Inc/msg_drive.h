/*
 * msg_drive.h
 *
 *  Created on: May 8, 2025
 *      Author: simek
 */

#ifndef INC_MSG_DRIVE_H_
#define INC_MSG_DRIVE_H_

//extern UART_HandleTypeDef huart1;

void make_msg_check(char uart, char channels, uint32_t data[]);

int VlozitData(uint32_t num, char* wip);


//funkce pro dekodovani prikazu D
uint32_t dekodovat_D(uint8_t str[]);

#endif /* INC_MSG_DRIVE_H_ */
