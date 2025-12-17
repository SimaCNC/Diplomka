/*
 * kruhovyBuffer.c
 *
 *  Created on: Oct 19, 2025
 *      Author: simek
 */

#include "kruhovyBuffer.h"
#include <string.h>
#include <stdio.h>
#include "usbd_cdc_if.h"


#define USB_QUEUE_VELIKOST 200
#define USB_MSG_VELIKOST 128

typedef struct
{
	char msg[USB_QUEUE_VELIKOST][USB_MSG_VELIKOST];
	volatile uint8_t head; //head pridava msg
	volatile uint8_t tail; //tail odebira msg
	volatile uint8_t count;
} USB_Queue_t;

static USB_Queue_t usb_queue = {0};
volatile uint8_t usb_busy = 0; // 1 znamena ze probiha prenos

//funkce pro pridani zpravy do fronty

void USB_pridatMSG(const char *msg)
{
	//overeni jestli je mista ve fronte a doplneni
	if (usb_queue.count < USB_QUEUE_VELIKOST)
	{
		strncpy(usb_queue.msg[usb_queue.head], msg, USB_MSG_VELIKOST-1);
		usb_queue.msg[usb_queue.head][USB_MSG_VELIKOST-1] = '\0'; //konec retezce
		usb_queue.head = (usb_queue.head + 1) % USB_QUEUE_VELIKOST;
		usb_queue.count++; //inkrementace count protoze se zvysuje pocet msg
	}
}

void USB_zpracovatQueue(void)
{
	if (!usb_busy && usb_queue.count > 0)
	{
		usb_busy = 1;

		uint8_t tail = usb_queue.tail;
		uint8_t len = strlen(usb_queue.msg[tail]);

		if (CDC_Transmit_FS((uint8_t*) usb_queue.msg[tail], len) == USBD_OK)
		{
			usb_queue.tail = (usb_queue.tail + 1) % USB_QUEUE_VELIKOST;
			usb_queue.count--; //dekrementace count prtoze se snizuje pocet msg
		}

		else
		{
			usb_busy = 0; //nepovedlo se odeslat zpravu
		}
	}
}

