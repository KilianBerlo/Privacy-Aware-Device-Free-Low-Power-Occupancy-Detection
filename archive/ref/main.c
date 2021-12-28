#include <atmel_start.h>
#include "main.h"
#include "string.h"
#include "stdio.h"
#include "MLX90640_API.h"
#include "float.h"
#include "stdlib.h"

enum STAGE
{
	FIRST,
	SECOND
};

#define TA_SHIFT 8 

uint8_t setFeedbackResistor(enum STAGE stage, uint8_t value);
uint16_t setR1(enum STAGE stage, uint16_t value);


float mlx90640To[768];
paramsMLX90640 mlx90640;

//write data to uart
void uart_write(uint8_t *buffer, uint16_t length)
{
	 io_write(uart, buffer, length);
}

//value = 1 to 256
//255 = 1M
uint8_t setFeedbackResistor(enum STAGE stage, uint8_t value)
{
	
	uint8_t writeBuf[2];
	uint8_t readBuf[1];

	writeBuf[0] = 0x00;
	writeBuf[1] = 256 - value;

	if(stage == FIRST)
	{
		i2c_m_sync_get_io_descriptor(&I2C_1, &I2C_1_io);
		i2c_m_sync_enable(&I2C_1);
		i2c_m_sync_set_slaveaddr(&I2C_1, 0x2C, I2C_M_SEVEN);
		io_write(I2C_1_io,writeBuf, 2);
		io_read(I2C_1_io, readBuf, 1);
	}
	else
	{
		i2c_m_sync_get_io_descriptor(&I2C_2, &I2C_2_io);
		i2c_m_sync_enable(&I2C_2);
		i2c_m_sync_set_slaveaddr(&I2C_2, 0x2C, I2C_M_SEVEN);
		io_write(I2C_2_io,writeBuf, 2);
		io_read(I2C_2_io, readBuf, 1);
	}
	return 256-readBuf[0];
}

//value = 1 to 1024
//1024 = 100k
uint16_t setR1(enum STAGE stage, uint16_t value)
{

	uint8_t writeBuf[2];
	uint8_t readBuf[2];

	writeBuf[0] = 0x1C;
	writeBuf[1] = 0x03;

	if(stage == FIRST)
	{
		i2c_m_sync_get_io_descriptor(&I2C_1, &I2C_1_io);
		i2c_m_sync_enable(&I2C_1);
		i2c_m_sync_set_slaveaddr(&I2C_1, 0x2E, I2C_M_SEVEN);
		io_write(I2C_1_io,writeBuf, 2);
		//	 io_read(I2C_0_io, readBuf, 2);

		writeBuf[0] = 0x03 & (value>>8);
		writeBuf[0] = writeBuf[0] | 0x04;
		writeBuf[1] = value & 0xFF;

		io_write(I2C_1_io,writeBuf, 2);
		//	 io_read(I2C_1_io, readBuf, 2);

		writeBuf[0] = 0x08;
		writeBuf[1] = 0x00;

		io_write(I2C_1_io,writeBuf, 2);
		io_read(I2C_1_io, readBuf, 2);
	}
	else
	{
		i2c_m_sync_get_io_descriptor(&I2C_2, &I2C_2_io);
		i2c_m_sync_enable(&I2C_2);
		i2c_m_sync_set_slaveaddr(&I2C_2, 0x2E, I2C_M_SEVEN);
		io_write(I2C_2_io,writeBuf, 2);
		//	 io_read(I2C_2_io, readBuf, 2);
		
		writeBuf[0] = 0x03 & (value>>8);
		writeBuf[0] = writeBuf[0] | 0x04;
		writeBuf[1] = value & 0xFF;

		io_write(I2C_2_io,writeBuf, 2);
		//	 io_read(I2C_2_io, readBuf, 2);

		writeBuf[0] = 0x08;
		writeBuf[1] = 0x00;

		io_write(I2C_2_io,writeBuf, 2);
		io_read(I2C_2_io, readBuf, 2);
	}
	
	return (readBuf[0]<<8) + readBuf[1];
}

uint16_t readADC()
{
	uint8_t buffer[2];
	uint16_t adcData[1];
	
	adc_sync_read_channel(&ADC_0, 0, buffer, 2);
	adcData[0] = ((uint16_t)buffer[1]) << 8;
	adcData[0] = adcData[0] | buffer[0];
	return adcData[0];
	};

int main(void)
{
	atmel_start_init();
	
	usart_sync_get_io_descriptor(&USART_0, &uart);
	usart_sync_enable(&USART_0);
	
	i2c_m_sync_get_io_descriptor(&I2C_0, &mlx);
	i2c_m_sync_enable(&I2C_0);
	i2c_m_sync_set_slaveaddr(&I2C_0, 0x33, I2C_M_SEVEN);
	
	i2c_m_sync_get_io_descriptor(&I2C_1, &I2C_1_io);
	i2c_m_sync_enable(&I2C_1);
	i2c_m_sync_set_slaveaddr(&I2C_1, 0x2c, I2C_M_SEVEN);
	
	i2c_m_sync_get_io_descriptor(&I2C_2, &I2C_2_io);
	i2c_m_sync_enable(&I2C_2);
	i2c_m_sync_set_slaveaddr(&I2C_2, 0x12, I2C_M_SEVEN);
	
	 adc_sync_enable_channel(&ADC_0, 0);
/*	
////////////////////////////////////////////////////////////////////////////////////////////
  // setFeedbackResistor(FIRST, 254);
  
  //1 and 2nd stage Rf = 1.5M ohm
  //1st stage amplifier R1. Values = 1 to 1023
   uint16_t returnValue = setR1(FIRST,2);
   
   returnValue = setR1(SECOND,1000);

    uint8_t str[10];
    uint8_t buffer[2];
    uint16_t adcData[1];
	
   while(1)
   {
	    
	    sprintf((char*)str, "%d", (uint16_t)(1.8*readADC()));
	    io_write(uart, str, strlen((char*)str)+1);
	    io_write(uart, (uint8_t*)"\r\n", 2);
		delay_ms(50);
   }
  
////////////////////////////////////////////////////////////////////////////////////////// 
 */  
   
 int status;
 uint16_t eeMLX90640[832];
 status = MLX90640_DumpEE(eeMLX90640);
 if (status != 0)
 {
	  uart_write((char*)"Failed to load system parameters\r\n",34);
 }

 //status = MLX90640_ExtractParameters(eeMLX90640, &mlx90640);
 //if (status != 0)
 //uart_write("Parameter extraction failed\r\n",29);

 
 //MLX90640_SetRefreshRate(0x01); //Set rate to 1Hz
 //MLX90640_SetRefreshRate(0x02); //Set rate to 2Hz
 //MLX90640_SetRefreshRate(0x03); //Set rate to 4Hz
 MLX90640_SetRefreshRate(0x04); //Set rate to 8Hz
  //MLX90640_SetRefreshRate(0x05); //Set rate to 16Hz
 //MLX90640_SetRefreshRate(0x06); //Set rate to 32Hz
 //MLX90640_SetRefreshRate(0x07); //Set rate to 64Hz
 
	uint16_t mlx90640Frame[835];
	uint16_t sendPacket[451];
	
	uint8_t receiveBuffer[] = {0,0,0};
	
	while(receiveBuffer[0]!=0x01)
	{
		io_read(uart, receiveBuffer, 2);   //Wait for 0x01
	}
	//	if (receiveBuffer[0] == 0x1)
		{
			//Send EEPROM data
		    io_write(uart, ((uint8_t*)eeMLX90640), 1664);
			io_write(uart, (uint8_t*)"\r\n", 2);
			
		}
	
	   receiveBuffer[0] = 0x00;
       while(receiveBuffer[0]!=0x02)
       {
	       io_read(uart, receiveBuffer, 2);   //Wait for 0x02
       }
	       
       if (receiveBuffer[0] == 0x2)
       {
	   while (1) 
	    {	
			int status = MLX90640_GetFrameData(mlx90640Frame);
					
			if (mlx90640Frame[833] == 0)		//Sub frame 0
			{
				for (int i=0; i<384; i++)
				{
					int k = (i*2)+((i/16)%2);
					sendPacket[i] = mlx90640Frame[k];
				}
			}
			else	                             //Sub frame 1
			{
				for (int i=0; i<384; i++)
				{
					int k = (i*2)+1-((i/16)%2);
					sendPacket[i] = mlx90640Frame[k];
				}

			}
			int j = 384;
			for (int i=768; i<834; i++)
			{
				sendPacket[j++] = mlx90640Frame[i];
			}
            sendPacket[450] = readADC();
			io_write(uart,(uint8_t*)sendPacket, 451*2 );
			
	   }
	 }

}
