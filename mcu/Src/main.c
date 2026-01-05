/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2025 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "usb_device.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "usbd_cdc_if.h"
#include "kruhovyBuffer.h"
#include "string.h"
#include "stdio.h"
#include "msg_drive.h"
#include "LM35.h"
#include "BME280.h"
#include "zpracovani_periferie.h"
#include "BH1750.h"
#include "kruhovyBuffer.h"
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
#define BUFF 256
#define IDLE 0
#define DONE 1
#define FILTR 300

typedef enum {
	STAV_WAIT = 0,
	STAV_PRIJEM = 1,
	STAV_MERENI = 2,
	STAV_MERENI_PULZY = 3,
	STAV_MERENI_AD = 4,
	STAV_ODESLANI_KONEC = 5,
	STAV_CEKANI_STOP_PULZY = 6,
}Stav;

typedef enum {
	Vyber_X = 0,
	Vyber_D = 1,
	Vyber_SD = 2
}Vyber;
/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
ADC_HandleTypeDef hadc1;
DMA_HandleTypeDef hdma_adc1;

I2C_HandleTypeDef hi2c1;
DMA_HandleTypeDef hdma_i2c1_rx;
DMA_HandleTypeDef hdma_i2c1_tx;

TIM_HandleTypeDef htim2;
DMA_HandleTypeDef hdma_tim2_ch1;

/* USER CODE BEGIN PV */


/*GPIO PINY*/
#define CERVENA_LED GPIO_PIN_8 //GPIOB
#define ZELENA_LED GPIO_PIN_15 //GPIOA
/*GPIO PINY*/

#define UART_BUFF 64
volatile unsigned short uart_2_mgr[7] = {0, 0, 0, 1, '\n', 0, 0};
uint8_t UART_2_msg[UART_BUFF] = {0};
uint8_t siz = 0;
volatile uint8_t flag_odeslat = 0;
volatile uint8_t uart_tx_ready = 1; //flag pro TXuart - 1 volny, 0 odeslano

//***CASOVAC INPUT CAPTURE
volatile uint8_t gu8_State = IDLE;
volatile uint8_t gu8_MSG[BUFF] = {'\0'};
volatile uint32_t gu32_T1 = 0;
volatile uint32_t gu32_T2 = 0;
volatile uint32_t gu32_Ticks = 0;
volatile uint16_t gu16_TIM2_OVC = 0;
volatile uint32_t gu32_Freq = 0;
uint32_t merit_pulzy = 0;
volatile uint32_t zachycene_pulzy = 0;

//implementace DMA - pokus o nahradu na IT na input capture mod
#define DMA_BUFF_size 1024
uint32_t dma_buff[DMA_BUFF_size] = {'\0'};
volatile uint32_t dma_index = 0;

/*//datova struktura kruhovy buffer pro zapis do DMA bufferu
typedef struct {
	volatile uint16_t buffer[DMA_BUFF_size];
	volatile uint16_t head;
	volatile uint16_t tail;
}kruhovy_buffer_t;*/

#define TX_QUEUE_SIZE  16
#define TX_MSG_SIZE 32
char tx_queue[TX_QUEUE_SIZE][TX_MSG_SIZE];  // fronta na zpravy
volatile uint8_t tx_head = 0, tx_tail = 0;
volatile uint8_t uart_busy = 0;

volatile Stav stav = STAV_WAIT;
Vyber vyber = Vyber_X;
//***CASOVAC INPUT CAPTURE
volatile uint8_t domereno_IC = 0;

//I2C - BME280
volatile float Temperature, Pressure, Humidity;
volatile uint8_t i2c_busy = 0;
//I2C - BH1750
BH1750_t svetlo_snimac;
volatile float lux = 0;
volatile uint8_t lux_data[2];

//ADCko - cteni dat
volatile uint16_t AD_RES = 0;
volatile uint16_t zmerene_ad = 0;
volatile uint16_t merit_ad = 0;
volatile uint16_t res_ad = 0;
volatile uint8_t adc_ready = 0;
#define KONSTANTA_3V3_4095 0.0008058608059

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_DMA_Init(void);
static void MX_ADC1_Init(void);
static void MX_I2C1_Init(void);
static void MX_TIM2_Init(void);
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_DMA_Init();
  MX_ADC1_Init();
  MX_I2C1_Init();
  MX_TIM2_Init();
  MX_USB_DEVICE_Init();
  /* USER CODE BEGIN 2 */


  //LM35_Init(&hadc1);
  char pole_teplota[10];

  char pole_merit_pulzy[15];
  memset(pole_merit_pulzy, 0, sizeof(pole_merit_pulzy));

  //BH1750 konfigurace
    if (BH1750_Init(&svetlo_snimac, &hi2c1, BH1750_adress, BH1750_cont_h_res) == HAL_OK)
    {

  	  if (BH1750_ReadLux(&svetlo_snimac, &lux) == HAL_OK)
  	  {
  		  HAL_Delay(50);
  	  }
    }
    else
    {
  	  Error_Handler();
    }

  //BME280 konfigurace
  if (BME280_Config(OSRS_2, OSRS_16, OSRS_1, MODE_NORMAL, T_SB_0p5, IIR_16) != 0)
  {
	  Error_Handler();
  }
  BME280_Measure(&Temperature, &Pressure, &Humidity);

  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
	  USB_zpracovatQueue();

	  switch (stav)
	  	  		{

	  	  		case STAV_WAIT:

 	  	  			HAL_GPIO_WritePin(GPIOB, ZELENA_LED, GPIO_PIN_SET);
	  	  			HAL_GPIO_WritePin(GPIOA, CERVENA_LED, GPIO_PIN_RESET);

	  	  			if (uart_2_mgr[1])
	  	  			{
	  	  				uart_2_mgr[1] = 0;
	  	  				stav = STAV_PRIJEM;
	  	  			}break;

	  	  		case STAV_PRIJEM:

	  	  			HAL_GPIO_WritePin(GPIOB, ZELENA_LED, GPIO_PIN_RESET);
	  	  			HAL_GPIO_WritePin(GPIOA, CERVENA_LED, GPIO_PIN_SET);
	  	  			//mereni pulzu - prikaz D
	  	  			if (UART_2_msg[0] == '#' && UART_2_msg[1] == 'D')
	  	  			{
	  	  				BH1750_OneTimeRead(&svetlo_snimac, &lux); // musim pouzit DMA - delay ve funkci dela problemy s jinymi prerusenimi
	  	  				vyber = Vyber_D;
	  	  				merit_pulzy = dekodovat_D(UART_2_msg); //kolikrat se maji merit pulzy
	  	  				gu16_TIM2_OVC = 0;
	  	  				//HAL_TIM_Base_Start(&htim2); //zapnout preteceni?
	  	  				HAL_TIM_IC_Start_DMA(&htim2, TIM_CHANNEL_1, (uint32_t*)dma_buff, DMA_BUFF_size); //zapnout IT pro IC
	  	  				sprintf(pole_merit_pulzy, "%lu", merit_pulzy);
	  	  				memset(UART_2_msg, 0, sizeof(UART_2_msg));
	  	  				stav = STAV_MERENI_PULZY;
	  	  			}

	  	  			//STREAM mereni pulzu -prikaz SD .... (Stream Data)
	  	  			else if(UART_2_msg[0] == '#' && UART_2_msg[1] == 'S' && UART_2_msg[2] == 'D')
	  	  			{
	  	  				vyber = Vyber_SD;
	  	  				HAL_TIM_IC_Start_DMA(&htim2, TIM_CHANNEL_1, (uint32_t*)dma_buff, 6); //zapnout IT pro IC
	  	  				stav = STAV_CEKANI_STOP_PULZY;
	  	  			}

	  	  			//mereni teploty - prikaz T
	  	  			else if (UART_2_msg[0] == '#' && UART_2_msg[1] == 'T')
	  	  			{
	  	  //				float teplota = LM35_Read(&hadc1, &huart1);
	  	  //				uint8_t cast_teplota = (int)teplota;
	  	  //				uint8_t desetina_teplota = (int)(teplota*10) - cast_teplota* 10;
	  	  //				snprintf(pole_teplota, sizeof(pole_teplota), "%d.%d\n", cast_teplota, desetina_teplota);
	  	  //				HAL_UART_Transmit(&huart1, (uint8_t*)pole_teplota,strlen(pole_teplota), 100);
	  	  				BME280_Measure(&Temperature, &Pressure, &Humidity);
	  	  				uint8_t cast_teplota = (int) Temperature;
	  	  				uint8_t desetina_teplota = (int) (Temperature * 10)- cast_teplota * 10;
	  	  				snprintf(gu8_MSG, sizeof(gu8_MSG), "%d.%d\r\n", cast_teplota, desetina_teplota);
	  	  				USB_pridatMSG(gu8_MSG);
	  	  				//HAL_UART_Transmit(&huart1, (uint8_t*) gu8_MSG, strlen(gu8_MSG), 100);
	  	  				memset(gu8_MSG, 0, sizeof(gu8_MSG));
	  	  				memset(UART_2_msg, 0, sizeof(UART_2_msg));
	  	  				stav = STAV_WAIT;
	  	  			}

	  	  			//mereni pres BME280
	  	  			else if(UART_2_msg[0] == '#' && UART_2_msg[1] == 'B' && UART_2_msg[2] == 'M' && UART_2_msg[3] == 'E')
	  	  			{
	  	  				BME280_Measure(&Temperature, &Pressure, &Humidity);
	  	  				uint8_t cast_teplota = (int)Temperature;
	  	  				uint8_t desetina_teplota = (int)(Temperature*10) - cast_teplota * 10;

	  	  				uint32_t cast_pressure = (int)Pressure;
	  	  				uint8_t desetina_pressure = (int)(Pressure*10) - cast_pressure * 10;

	  	  				uint8_t cast_humidity = (int)Humidity;
	  	  				uint8_t desetina_humidity = (int)(Humidity*10) - cast_humidity * 10;

	  	  				snprintf(gu8_MSG, sizeof(gu8_MSG), "T=%d.%d P=%d.%d H=%d.%d\r\n",
	  	  						cast_teplota, desetina_teplota, cast_pressure, desetina_pressure, cast_humidity, desetina_humidity);
	  	  				USB_pridatMSG(gu8_MSG);
	  	  				//HAL_UART_Transmit(&huart1, (uint8_t*)gu8_MSG,strlen(gu8_MSG), 100);
	  	  				memset(gu8_MSG, 0, sizeof(gu8_MSG));
	  	  				stav = STAV_WAIT;
	  	  			}

	  	  			else if(UART_2_msg[0] == '#' && UART_2_msg[1] == 'A')
	  	  			{
	  	  				merit_ad = dekodovat_D(UART_2_msg); //pouziti funkce D - jedna se o totez jak u frekvence - parsovani dat
	  	  				HAL_ADC_Start_DMA(&hadc1, &AD_RES, 1);
	  	  				stav = STAV_MERENI_AD;

	  	  			}

	  	  			//funkce pro nalezeni I2C zarizeni dostupnych - vypis pres uart
	  	  			else if(UART_2_msg[0] == '#' && UART_2_msg[1] == 'S' && UART_2_msg[2] == 'C')
	  	  			{
	  	  				HAL_StatusTypeDef res;
	  	  				for (uint8_t i = 1; i < 128; i++)
	  	  				{
	  	  					res = HAL_I2C_IsDeviceReady(&hi2c1, i << 1, 1, 10);
	  	  					if (res == HAL_OK)
	  	  					{
	  	  						snprintf(gu8_MSG, sizeof(gu8_MSG), "Nalezeno zarizeni na adrese 0x%02X\r\n", i);
	  	  						USB_pridatMSG(gu8_MSG);
	  	  						memset(gu8_MSG, 0, sizeof(gu8_MSG));
	  	  					}
	  	  				}
	  	  				memset(UART_2_msg, 0, sizeof(UART_2_msg));
	  	  				stav = STAV_WAIT;
	  	  			}

	  	  			//funkce pro zjisteni lux
	  	  			else if(UART_2_msg[0] == '#' && UART_2_msg[1] == 'L' && UART_2_msg[2] == 'U' && UART_2_msg[3] == 'X')
	  	  			{
	  	  				BH1750_OneTimeRead(&svetlo_snimac, &lux);
	  	  				(int)lux;
	  	  				snprintf(gu8_MSG, sizeof(gu8_MSG), "lux: %d\r\n", (int)lux);
	  	  				USB_pridatMSG(gu8_MSG);
	  	  				memset(gu8_MSG, 0, sizeof(gu8_MSG));
	  	  				memset(UART_2_msg, 0, sizeof(UART_2_msg));
	  	  				stav = STAV_WAIT;
	  	  			}
	  	  			//SPATNA INSTRUKCE
	  	  			else
	  	  			{
	  	  				USB_pridatMSG("SPATNA INSTRUKCE\r\n");
	  	  				stav = STAV_WAIT;
	  	  			}



	  	  			memset(UART_2_msg, 0, sizeof(UART_2_msg));
	  	  			break;

	  	  		case STAV_MERENI_PULZY:

	  				if (domereno_IC == 0)
	  				{
	  					break;
	  				}

	  				domereno_IC = 0;

	  				uint8_t cast_teplota = (int) Temperature;
	  				uint8_t desetina_teplota = (int) (Temperature * 10) - cast_teplota * 10;

	  				uint32_t cast_pressure = (int) Pressure;
	  				uint8_t desetina_pressure = (int) (Pressure * 10) - cast_pressure * 10;

	  				uint8_t cast_humidity = (int) Humidity;
	  				uint8_t desetina_humidity = (int) (Humidity * 10) - cast_humidity * 10;

	  				for (int i = 0; i < (merit_pulzy); i++)
	  				{
	  					uint32_t delta = (dma_buff[i + FILTR] - dma_buff[i]);
	  					float freq = 0;
	  					freq = (96000000.0f * FILTR) / (float) delta; //nasobeni *2 FCLK = 144000000
	  					zachycene_pulzy++;
	  					snprintf(gu8_MSG, sizeof(gu8_MSG),
	  							"D=%d, F=%d, T=%d.%d, P=%d.%d, H=%d.%d, L=%d\r\n",
	  							delta, (uint32_t) freq, cast_teplota, desetina_teplota,
	  							cast_pressure, desetina_pressure, cast_humidity,
	  							desetina_humidity, (int) lux);
	  					USB_pridatMSG(gu8_MSG);
	  				}

	  				if (zachycene_pulzy >= merit_pulzy)
	  				{
	  					// stop DMA
	  					zachycene_pulzy = 0;
	  					HAL_TIM_IC_Stop_DMA(&htim2, TIM_CHANNEL_1);
	  					memset(dma_buff, 0, sizeof(dma_buff));
	  					stav = STAV_ODESLANI_KONEC;
	  					break;
	  				}

	  	  		case STAV_MERENI_AD:

	  	  			if (adc_ready)
	  	  			{
	  	  				//data z BME mereni
	  	  				uint8_t cast_teplota = (int) Temperature;
	  	  				uint8_t desetina_teplota = (int) (Temperature * 10) - cast_teplota * 10;
	  	  				uint32_t cast_pressure = (int) Pressure;
	  	  				uint8_t desetina_pressure = (int) (Pressure * 10) - cast_pressure * 10;
	  	  				uint8_t cast_humidity = (int) Humidity;
	  	  				uint8_t desetina_humidity = (int) (Humidity * 10) - cast_humidity * 10;

	  	  				//AD konverze
	  	  				adc_ready = 0;
	  	  				uint32_t napeti_mV = (AD_RES * 3300UL) / 4095;
	  	  				uint32_t volts = napeti_mV * 0.001;
	  	  				uint32_t mV = napeti_mV % 1000;
	  	  				snprintf(gu8_MSG, sizeof(gu8_MSG), "AD=%d, V=%lu.%03lu, T=%d.%d, P=%d.%d, H=%d.%d L=%d\r\n",AD_RES ,volts, mV, cast_teplota, desetina_teplota, cast_pressure, desetina_pressure, cast_humidity, desetina_humidity, (int) lux);
	  	  				USB_pridatMSG(gu8_MSG);
	  	  				memset(gu8_MSG, 0, sizeof(gu8_MSG));
	  	  				zmerene_ad++;


	  	  				if (zmerene_ad >= merit_ad)
	  	  				{
	  	  					BME280_Measure(&Temperature, &Pressure, &Humidity);
	  	  					BH1750_OneTimeRead(&svetlo_snimac, &lux);
	  	  					HAL_ADC_Stop_DMA(&hadc1);
	  	  					stav = STAV_ODESLANI_KONEC;
	  	  					//stav = STAV_WAIT;
	  	  					merit_ad = 0;
	  	  					zmerene_ad = 0;
	  	  				}
	  	  				else
	  	  				{

	  	  					HAL_ADC_Start_DMA(&hadc1, (uint32_t*) &AD_RES, 1);
	  	  				}
	  	  			}
	  	  			break;
	  	  			//break;

	  	  		case STAV_CEKANI_STOP_PULZY:
	  	  			if(UART_2_msg[0] == '#' && UART_2_msg[1] == 'X' && UART_2_msg[2] == 'S' && UART_2_msg[3] == 'D')
	  	  			{
	  	  				HAL_TIM_IC_Stop_DMA(&htim2, TIM_CHANNEL_1);
	  	  				stav = STAV_ODESLANI_KONEC;
	  	  				uart_2_mgr[1] = 0;
	  	  				break;
	  	  			}
	  	  			else
	  	  			{
	  	  				HAL_TIM_IC_Start_DMA(&htim2, TIM_CHANNEL_1, (uint32_t*)dma_buff, 10); //zapnout IT pro IC
	  	  			}
	  	  			proces_tx_frontu();
	  	  			break;

	  	  		case STAV_ODESLANI_KONEC:

	  	  			// Reset fronty a stavu UARTu


	  	  			memset(UART_2_msg, 0, sizeof(UART_2_msg));
	  	  			stav = STAV_WAIT;
	  	  			break;


	  	  		default: break;
	  	  		} /*switch (stav)*/
	    	}/*while (1)*/
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Configure the main internal regulator output voltage
  */
  __HAL_RCC_PWR_CLK_ENABLE();
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE;
  RCC_OscInitStruct.HSEState = RCC_HSE_ON;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
  RCC_OscInitStruct.PLL.PLLM = 25;
  RCC_OscInitStruct.PLL.PLLN = 192;
  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV2;
  RCC_OscInitStruct.PLL.PLLQ = 4;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV2;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_3) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
  * @brief ADC1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_ADC1_Init(void)
{

  /* USER CODE BEGIN ADC1_Init 0 */

  /* USER CODE END ADC1_Init 0 */

  ADC_ChannelConfTypeDef sConfig = {0};

  /* USER CODE BEGIN ADC1_Init 1 */

  /* USER CODE END ADC1_Init 1 */

  /** Configure the global features of the ADC (Clock, Resolution, Data Alignment and number of conversion)
  */
  hadc1.Instance = ADC1;
  hadc1.Init.ClockPrescaler = ADC_CLOCK_SYNC_PCLK_DIV4;
  hadc1.Init.Resolution = ADC_RESOLUTION_12B;
  hadc1.Init.ScanConvMode = DISABLE;
  hadc1.Init.ContinuousConvMode = DISABLE;
  hadc1.Init.DiscontinuousConvMode = DISABLE;
  hadc1.Init.ExternalTrigConvEdge = ADC_EXTERNALTRIGCONVEDGE_NONE;
  hadc1.Init.ExternalTrigConv = ADC_SOFTWARE_START;
  hadc1.Init.DataAlign = ADC_DATAALIGN_RIGHT;
  hadc1.Init.NbrOfConversion = 1;
  hadc1.Init.DMAContinuousRequests = DISABLE;
  hadc1.Init.EOCSelection = ADC_EOC_SINGLE_CONV;
  if (HAL_ADC_Init(&hadc1) != HAL_OK)
  {
    Error_Handler();
  }

  /** Configure for the selected ADC regular channel its corresponding rank in the sequencer and its sample time.
  */
  sConfig.Channel = ADC_CHANNEL_7;
  sConfig.Rank = 1;
  sConfig.SamplingTime = ADC_SAMPLETIME_3CYCLES;
  if (HAL_ADC_ConfigChannel(&hadc1, &sConfig) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN ADC1_Init 2 */

  /* USER CODE END ADC1_Init 2 */

}

/**
  * @brief I2C1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_I2C1_Init(void)
{

  /* USER CODE BEGIN I2C1_Init 0 */

  /* USER CODE END I2C1_Init 0 */

  /* USER CODE BEGIN I2C1_Init 1 */

  /* USER CODE END I2C1_Init 1 */
  hi2c1.Instance = I2C1;
  hi2c1.Init.ClockSpeed = 100000;
  hi2c1.Init.DutyCycle = I2C_DUTYCYCLE_2;
  hi2c1.Init.OwnAddress1 = 0;
  hi2c1.Init.AddressingMode = I2C_ADDRESSINGMODE_7BIT;
  hi2c1.Init.DualAddressMode = I2C_DUALADDRESS_DISABLE;
  hi2c1.Init.OwnAddress2 = 0;
  hi2c1.Init.GeneralCallMode = I2C_GENERALCALL_DISABLE;
  hi2c1.Init.NoStretchMode = I2C_NOSTRETCH_DISABLE;
  if (HAL_I2C_Init(&hi2c1) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN I2C1_Init 2 */

  /* USER CODE END I2C1_Init 2 */

}

/**
  * @brief TIM2 Initialization Function
  * @param None
  * @retval None
  */
static void MX_TIM2_Init(void)
{

  /* USER CODE BEGIN TIM2_Init 0 */

  /* USER CODE END TIM2_Init 0 */

  TIM_ClockConfigTypeDef sClockSourceConfig = {0};
  TIM_MasterConfigTypeDef sMasterConfig = {0};
  TIM_IC_InitTypeDef sConfigIC = {0};

  /* USER CODE BEGIN TIM2_Init 1 */

  /* USER CODE END TIM2_Init 1 */
  htim2.Instance = TIM2;
  htim2.Init.Prescaler = 0;
  htim2.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim2.Init.Period = 4294967295;
  htim2.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
  htim2.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;
  if (HAL_TIM_Base_Init(&htim2) != HAL_OK)
  {
    Error_Handler();
  }
  sClockSourceConfig.ClockSource = TIM_CLOCKSOURCE_INTERNAL;
  if (HAL_TIM_ConfigClockSource(&htim2, &sClockSourceConfig) != HAL_OK)
  {
    Error_Handler();
  }
  if (HAL_TIM_IC_Init(&htim2) != HAL_OK)
  {
    Error_Handler();
  }
  sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;
  sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;
  if (HAL_TIMEx_MasterConfigSynchronization(&htim2, &sMasterConfig) != HAL_OK)
  {
    Error_Handler();
  }
  sConfigIC.ICPolarity = TIM_INPUTCHANNELPOLARITY_RISING;
  sConfigIC.ICSelection = TIM_ICSELECTION_DIRECTTI;
  sConfigIC.ICPrescaler = TIM_ICPSC_DIV1;
  sConfigIC.ICFilter = 0;
  if (HAL_TIM_IC_ConfigChannel(&htim2, &sConfigIC, TIM_CHANNEL_1) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN TIM2_Init 2 */

  /* USER CODE END TIM2_Init 2 */

}

/**
  * Enable DMA controller clock
  */
static void MX_DMA_Init(void)
{

  /* DMA controller clock enable */
  __HAL_RCC_DMA2_CLK_ENABLE();
  __HAL_RCC_DMA1_CLK_ENABLE();

  /* DMA interrupt init */
  /* DMA1_Stream0_IRQn interrupt configuration */
  HAL_NVIC_SetPriority(DMA1_Stream0_IRQn, 0, 0);
  HAL_NVIC_EnableIRQ(DMA1_Stream0_IRQn);
  /* DMA1_Stream1_IRQn interrupt configuration */
  HAL_NVIC_SetPriority(DMA1_Stream1_IRQn, 0, 0);
  HAL_NVIC_EnableIRQ(DMA1_Stream1_IRQn);
  /* DMA1_Stream5_IRQn interrupt configuration */
  HAL_NVIC_SetPriority(DMA1_Stream5_IRQn, 0, 0);
  HAL_NVIC_EnableIRQ(DMA1_Stream5_IRQn);
  /* DMA2_Stream0_IRQn interrupt configuration */
  HAL_NVIC_SetPriority(DMA2_Stream0_IRQn, 0, 0);
  HAL_NVIC_EnableIRQ(DMA2_Stream0_IRQn);

}

/**
  * @brief GPIO Initialization Function
  * @param None
  * @retval None
  */
static void MX_GPIO_Init(void)
{
  GPIO_InitTypeDef GPIO_InitStruct = {0};
  /* USER CODE BEGIN MX_GPIO_Init_1 */

  /* USER CODE END MX_GPIO_Init_1 */

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOH_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOB, GPIO_PIN_15, GPIO_PIN_RESET);

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOA, GPIO_PIN_8, GPIO_PIN_RESET);

  /*Configure GPIO pin : PB15 */
  GPIO_InitStruct.Pin = GPIO_PIN_15;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

  /*Configure GPIO pin : PA8 */
  GPIO_InitStruct.Pin = GPIO_PIN_8;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

  /* USER CODE BEGIN MX_GPIO_Init_2 */

  /* USER CODE END MX_GPIO_Init_2 */
}

/* USER CODE BEGIN 4 */
void USB_CDC_RxHandler(uint8_t* Buf, uint32_t Len)
{
	memcpy(UART_2_msg, Buf, Len);
    //CDC_Transmit_FS(Buf, Len);
    UART_ISR_m(2, uart_2_mgr, UART_2_msg);
    uart_2_mgr[1] = 1;
}

void HAL_TIM_IC_CaptureCallback(TIM_HandleTypeDef *htim)
{
	/*AA*/
	if (htim->Instance == TIM2)
	{
		if (vyber == Vyber_D) {
			//stare mereni okolni pres LM35
			//float teplota = LM35_Read(&hadc1, &huart1);
			//uint8_t cast_teplota = (int)teplota;
			//uint8_t desetina_teplota = (int)(teplota*10) - cast_teplota* 10;

			if (i2c_busy == 0) {
				BME280_Measure(&Temperature, &Pressure, &Humidity);
			}

			domereno_IC = 1;
		}

	}

}

void zaradit_msg(const char *msg)
{
	uint8_t dalsi = (tx_head + 1) % TX_QUEUE_SIZE;
	if (dalsi != tx_tail)
	{
		strncpy(tx_queue[tx_head], msg, sizeof(tx_queue[0]));
		tx_head = dalsi;
	}
}

void proces_tx_frontu(void)
{
	  if (!uart_busy && tx_head != tx_tail)
	  {
		uart_busy = 1;
		CDC_Transmit_FS((uint8_t*) tx_queue[tx_tail],strlen(tx_queue[tx_tail]));
		//HAL_UART_Transmit_IT(&huart1, (uint8_t*) tx_queue[tx_tail], strlen(tx_queue[tx_tail]));
	   }
}

void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef* hadc)
{
	//AB
	AD_RES = (uint16_t)AD_RES;
	adc_ready = 1;
}


void HAL_I2C_MasterRxCpltCallback(I2C_HandleTypeDef *hi2c)
{
	if (hi2c->Instance == I2C1)
	{
	    uint16_t raw = (lux_data[0] << 8) | lux_data[1];
	    lux = raw / 1.2f;
	    i2c_busy = 0;
	}
}
/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
