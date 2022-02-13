import pyb
from pyb import I2C,Pin
import sys

AFE_ADDR = 0x58

#/* AFE440X registers */

AFE_CONTROL0 = 0x00

#Sample LED2 Start / End
AFE_LED2STC = 0x01
AFE_LED2ENDC = 0x02

#LED1 Start / End
AFE_LED1LEDSTC = 0x03
AFE_LED1LEDENDC = 0x04

#Sample Ambient 2 ( or LED3 ) Start / End
AFE_ALED2STC = 0x05
AFE_ALED2ENDC = 0x06

#Sample LED1 Start / End
AFE_LED1STC  = 0x07
AFE_LED1ENDC = 0x08

#LED2 Start / End
AFE_LED2LEDSTC = 0x09
AFE_LED2LEDENDC = 0x0a

#Sample Ambient 1 Start / End
AFE_ALED1STC = 0x0b
AFE_ALED1ENDC = 0x0c

# LED2 Convert Start / End
AFE_LED2CONVST = 0x0d
AFE_LED2CONVEND = 0x0e

AFE_ALED2CONVST = 0x0f
AFE_ALED2CONVEND = 0x10

#LED1 Convert Start / End
AFE_LED1CONVST = 0x11
AFE_LED1CONVEND = 0x12

#Ambient 1 Convert Start / End
AFE_ALED1CONVST = 0x13
AFE_ALED1CONVEND = 0x14

# ADC Reset Phase 0 Start / End
AFE_ADCRSTSTCT0 = 0x15
AFE_ADCRSTENDCT0 = 0x16

# ADC Reset Phase 1 Start / End
AFE_ADCRSTSTCT1 = 0x17
AFE_ADCRSTENDCT1 = 0x18

# ADC Reset Phase 2 Start / End
AFE_ADCRSTSTCT2=   0x19
AFE_ADCRSTENDCT2=  0x1a

# ADC Reset Phase 3 Start / End
AFE_ADCRSTSTCT3=   0x1b
AFE_ADCRSTENDCT3=  0x1c

# PRPCT ( timer counter )
AFE_PRPCOUNT=      0x1d #/**< Bits 0-15 for writing counter value      */
# Timer Module enable / NUMAV ( # of times to sample and average )
AFE_CONTROL1=      0x1e 

AFE_TIA_GAIN=      0x21
# TIA Gains 2
AFE_TIA_GAIN_SEP=  0x20

# LED Current Control
AFE_LEDCNTRL=      0x22
# /* ********************************************************************
#  * LED current control is a 24 bit register where                     *
#  * LED1: bits 0-5 LED2: bits 6-11 LED3: bits 12-17 and the rest are 0 *
#  * ****************************************************************** *
#  * LED1, LED2, LED3 Register Values | LED Current Setting (mA)        *
#  *                   0              |              0                  *
#  *                   1              |             0.8                 *
#  *                   2              |             1.6                 *
#  *                   3              |             2.4                 *
#  *                  ...             |             ...                 *
#  *                   63             |              50                 *
#  **********************************************************************/

# /**< Settings Address */
AFE_CONTROL2=      0x23

# Clockout Settings
AFE_ALARM=         0x29
# /* *****************************************************************************
#   *  CLKOUT_DIV Register Settings Graph
#   * ****************************************************************************
#   * CLKOUT_DIV Register Settings | Division Ratio | Output Clock Freq. ( MHz ) *
#   *             0                |         1      |             4              *
#   *             1                |         2      |             2              *
#   *             2                |         4      |             1              *
#   *             3                |         8      |            0.5             *
#   *             4                |        16      |           0.25             *
#   *             5                |        32      |          0.125             *
#   *             6                |        64      |         0.0625             *
#   *             7                |       128      |        0.03125             *
#   *         8..15                |    Do not use  |      Do not use            *
#   *****************************************************************************/

# LED2 Output Value
AFE_LED2VAL=       0x2a

# LED3 or Ambient 2 Value
AFE_ALED2VAL=      0x2b

# LED1 Output Value
AFE_LED1VAL=       0x2c

# Ambient 1 Value
AFE_ALED1VAL=      0x2d

# LED2-Ambient 2 Value
AFE_LED2_ALED2VAL= 0x2e

# LED1-Ambient 1 Value
AFE_LED1_ALED1VAL= 0x2f

# PD disconnect / INP, INN settings / EXT clock Division settings
AFE_CONTROL3=      0x31

# PDN_CYCLE Start / End
AFE_PDNCYCLESTC=   0x32
AFE_PDNCYCLEENDC=  0x33

# Programmable Start / End time for ADC_RDY replacement
AFE_PROG_TG_STC=   0x34 #/**< Bits 0-15 Define Start Time              */
AFE_PROG_TG_ENDC=  0x35 #/**< Bits 0-15 Define End Time              */

# LED3C Start / End
AFE_LED3LEDSTC=    0x36
AFE_LED3LEDENDC=   0x37

# PRF Clock Division settings
AFE_CLKDIV_PRF=    0x39
# /* ****************************************************************************
#   *   CLKDIV_PRF Register Settings Graph
#   * ****************************************************************************
#   * CLKDIV_PRF Settings|Division Ratio|Clock Freq(MHz)| Lowest PRF Setting (Hz)*
#   *          0         |       1      |       4       |           61           *
#   *          1         |  Do Not Use  |  Do Not Use   |      Do Not Use        *
#   *          2         |  Do Not Use  |  Do Not Use   |      Do Not Use        *
#   *          3         |  Do Not Use  |  Do Not Use   |      Do Not Use        *
#   *          4         |       2      |       2       |           31           *
#   *          5         |       4      |       1       |           15           *
#   *          6         |       8      |     0.5       |            8           *
#   *          7         |      16      |    0.25       |            4           *
#   *****************************************************************************/

# DAC Settings
AFE_OFFDAC=        0x3a
AFE_DEC = 0x3d
AFE_AVG_LED2_ALED2VAL = 0x3f
AFE_AVG_LED1_ALED1VAL = 0x40


class AFE4404():
    #默认使用引脚X1作为中断引脚，连接模块的INT引脚
    #默认使用TPYBoard v102的i2c(2)接口 SCL=>Y9 SDA=>Y10
    def __init__(self,i2c_id=1,address=0x58, pin='X1'):
        print("intpin: {0}, address: {1}".format(pin, address))
        self.i2c = I2C(i2c_id,I2C.MASTER, baudrate=400000)
        self.address = address
        self.interrupt =Pin(pin,Pin.IN)    #设置中断引脚为输入模式
        # pyb.delay(1000)                              
        # self.reset()                                                     #软复位
        pyb.delay(1000)
        # utime.sleep_ms(5000)
        #reg_data = self.i2c.mem_read(1, self.address, REG_INTR_STATUS_1)
        addr = self.i2c.scan()
        if address not in addr:
            print('AFE4404 device not found')
        elif not self.i2c.is_ready(address):
            print('AFE4404 device not response')
        else:
            # self.AFE_RESETZ_Init()
            self.AFE_Enable_HWPDN()
            self.AFE_Disable_HWPDN()
            self.AFE_Trigger_HWReset()
            # self.AFE_Reg_Init()
            # self.setup()

    def AFE_RESETZ_Init(self):

        self.AFE_Reg_Init()

    def AFE_Trigger_HWReset(self):
        # self.reset()
        # P_out=Pin('Y4')
        p_Trigger_HWReset = Pin('X2', Pin.OUT_PP)
        p_Trigger_HWReset.low()
        pyb.delay(30)
        p_Trigger_HWReset.high()
        pyb.delay(10)

    def AFE_Enable_HWPDN(self):

        p_out = Pin('X2', Pin.OUT_PP)
        p_out.low()
        pyb.delay(10)  #Power Down by setting the RESETZ pin to LOW for more than 200 us
        print('HWPDN Enable')

    def AFE_Disable_HWPDN(self):

        p_out = Pin('X2', Pin.OUT_PP)
        p_out.high()
        pyb.delay(10)  #Power Up the AFE by setting the RESETZ pin to HIGH
        print('HWPDN Disable')


    def AFE_Reg_Init(self):

        self.AFE_Reg_Write(AFE_LEDCNTRL, 0x0033C3)
        print('Reg_Init Finished')

    def AFE_CLK_Init(self):
        AFE_Reg_Write(35, 0x104218)       #Set CLK Mode to internal clock (default Wert: 124218 mit interner CLK)
        AFE_Reg_Write(41, 0x2)            #Don´t set the internal clock to the CLK pin for outside usage
        AFE_Reg_Write(49, 0x000021)       #Division ratio for external clock mode set to fit the Arduino Mega 16MHz
        AFE_Reg_Write(57, 0)              #Set the lowes sampling rate to 61Hz (~17 ms)
        print('Clk_Init Finished')



    def AFE_Reg_Write (self, reg_address, data):

        configData=bytes ([0x00,0x00,0x00])         #bytes型是字节数组
        ConfigData=bytearray(configData)
        ConfigData[0]=(data >>16)
        ConfigData[1]=(data & 0x00FFFF) >>8
        ConfigData[2]=data & 0x0000FF
        # configData=bytes (ConfigData)
        self.i2c.mem_write(ConfigData,self.address, reg_address)

    def AFE_Reg_Read(self, reg_address):

        retVal = None
        configData = bytes(self.i2c.mem_read(3, AFE_ADDR, reg_address))
        retVal = configData[0]
        retVal = (retVal << 8) | configData[1]
        retVal = (retVal << 8) | configData[2]
        if reg_address >= 0x2A and reg_address <= 0x2F:
            if retVal & 0x00200000:  # check if the ADC value is positive or negative
                retVal &= 0x003FFFFF   # convert it to a 22 bit value
                return (retVal^0xFFC00000)
            return retVal
            # print('Read Data successfully')
            # print(retVal)
        else:
            print('Register Address wrong')


    def shutdown(self):
        """
        关闭灯
        """
        self.AFE_Disable_Read() 
        self.AFE_Reg_Write(AFE_LEDCNTRL, 0x000000) #关灯
        self.AFE_Enable_Read()



    # def reset(self, led_mode=b'\x40'):
        """
        Reset the device, this will clear all settings,
        so after running this, run setup() again.
        """
        # self.i2c.mem_write(led_mode, self.address, REG_MODE_CONFIG) #原来是40

    def AFE_Enable_Read(self):       #Prohibit writing to registers

        configData = bytes([0x00,0x00,0x01]) 
        self.i2c.mem_write(configData, self.address, AFE_CONTROL0) 
        print('Enable Read')

    def AFE_Disable_Read(self):        #Permitt writing to registers

        configData = bytes([0x00,0x00,0x00]) 
        self.i2c.mem_write(configData, self.address, AFE_CONTROL0) 
        print('Disable Read')


    def setup(self):
        """置
        模块的初始化设
        """
        self.AFE_Disable_Read() 

        self.AFE_Reg_Write(AFE_LED2STC,100)  #AFE_LED2STC 4MHZ:100 250KHz:7
        self.AFE_Reg_Write(AFE_LED2ENDC, 399)  #AFE_LED2ENDC 4MHZ:399 250KHz:24

        self.AFE_Reg_Write(AFE_LED1LEDSTC, 802)  #AFE_LED1LEDSTC 4MHZ: 802 250KHz: 52
        self.AFE_Reg_Write(AFE_LED1LEDENDC, 1201)  #self.AFE_LED1LEDENDC 4MHZ: 1201 250KHz: 76

        self.AFE_Reg_Write(AFE_ALED2STC, 501)  #self.AFE_ALED2STC 4MHZ: 501 250KHz: 33
        self.AFE_Reg_Write(AFE_ALED2ENDC, 800)  #self.AFE_ALED2ENDC 4MHZ: 800 250KHz: 50

        self.AFE_Reg_Write(AFE_LED1STC, 902)  #self.AFE_LED1STC 4MHZ: 902 250KHz: 59
        self.AFE_Reg_Write(AFE_LED1ENDC, 1201)  #self.AFE_LED1ENDC 4MHZ: 1201 250KHz: 76

        self.AFE_Reg_Write(AFE_LED2LEDSTC, 0)  #self.AFE_LED2LEDSTC 4MHZ: 0 250KHz: 0
        self.AFE_Reg_Write(AFE_LED2LEDENDC, 399)  #self.AFE_LED2LEDENDC 4MHZ: 399 250KHz: 24

        self.AFE_Reg_Write(AFE_ALED1STC, 1303)  #self.AFE_ALED1STC 4MHZ: 1303 250KHz: 85
        self.AFE_Reg_Write(AFE_ALED1ENDC, 1602)  #self.AFE_ALED1ENDC 4MHZ: 1602 250KHz: 102

        self.AFE_Reg_Write(AFE_LED2CONVST, 409)  #self.AFE_LED2CONVST 4MHZ: 409 250KHz: 28
        self.AFE_Reg_Write(AFE_LED2CONVEND, 1468)  #self.AFE_LED2CONVEND 4MHZ: 1468 250KHz: 94

        self.AFE_Reg_Write(AFE_ALED2CONVST, 1478)  #self.AFE_ALED2CONVST 4MHZ: 1478 250KHz: 98
        self.AFE_Reg_Write(AFE_ALED2CONVEND, 2537)  #self.AFE_ALED2CONVEND 4MHZ: 2537 250KHz: 164

        self.AFE_Reg_Write(AFE_LED1CONVST, 2547)  #self.AFE_LED1CONVST 4MHZ: 2547 250KHz: 168
        self.AFE_Reg_Write(AFE_LED1CONVEND, 3606)  #self.AFE_LED1CONVEND 4MHZ: 3606 250KHz: 234

        self.AFE_Reg_Write(AFE_ALED1CONVST, 3616)  #self.AFE_ALED1CONVST 4MHZ: 3616 250KHz: 238
        self.AFE_Reg_Write(AFE_ALED1CONVEND, 4675)  #self.AFE_ALED1CONVEND 4MHZ: 4675 250KHz: 304

        self.AFE_Reg_Write(AFE_ADCRSTSTCT0, 401)  #self.AFE_ADCRSTSTCT0 4MHZ: 401 250KHz: 26
        self.AFE_Reg_Write(AFE_ADCRSTENDCT0, 407)  #self.AFE_ADCRSTENDCT0 4MHZ: 407 250KHz: 26

        self.AFE_Reg_Write(AFE_ADCRSTSTCT1, 1470)  #self.AFE_ADCRSTSTCT1 4MHZ: 1470 250KHz: 96
        self.AFE_Reg_Write(AFE_ADCRSTENDCT1, 1476)  #self.AFE_ADCRSTENDCT1 4MHZ: 1476 250KHz: 96

        self.AFE_Reg_Write(AFE_ADCRSTSTCT2, 2539)  #self.AFE_ADCRSTSTCT2 4MHZ: 2539 250KHz: 166
        self.AFE_Reg_Write(AFE_ADCRSTENDCT2, 2545)  #self.AFE_ADCRSTENDCT2 4MHZ: 2545 250KHz: 166

        self.AFE_Reg_Write(AFE_ADCRSTSTCT3, 3608)  #self.AFE_ADCRSTSTCT3 4MHZ: 3608 250KHz: 236
        self.AFE_Reg_Write(AFE_ADCRSTENDCT3, 3614)  #self.AFE_ADCRSTENDCT3 4MHZ: 3614 250KHz: 236

        self.AFE_Reg_Write(AFE_LED3LEDSTC, 401)  #self.AFE_LED3LEDSTC 4MHZ: 401 250KHz: 26
        self.AFE_Reg_Write(AFE_LED3LEDENDC, 800)  #self.AFE_LED3LEDENDC 4MHZ: 800 250KHz: 50

        self.AFE_Reg_Write(AFE_PRPCOUNT, 39999)  #self.AFE_PRPCOUNT 4MHZ: 39999 250KHz: 2499


        self.AFE_Reg_Write(AFE_CONTROL1, 0x000103)  #AFE_CONTROL1 TimerEN = 1  NUMAV = 3
        self.AFE_Reg_Write(AFE_TIA_GAIN_SEP, 0x008003)  #self.AFE_TIA_SEP_GAIN (LED2) ENSEPGAIN = 1  LED2/LED3 gain = 50K
        self.AFE_Reg_Write(AFE_TIA_GAIN, 0x000003)  #self.AFE_TIA_GAIN (LED1) LED1/LED1AMB gain = 50K
        self.AFE_Reg_Write(AFE_OFFDAC, 0x000000)  #self.AFE_DAC_SETTING_REG
        self.AFE_Reg_Write(AFE_LEDCNTRL, 0x0030CF)  #LED3 - 3.125mA  LED2 - 3.125mA  LED1 - 12.5mA
        self.AFE_Reg_Write(AFE_CONTROL2, 0x020200)  #DYN1, LEDCurr, DYN2, Ext CLK, DYN3, DYN4 #0x000200)  - 0x200 Osc mode #self.AFE_CONTROL2
        self.AFE_Reg_Write(AFE_CONTROL3, 0x000020)  #ENABLE_INPUT_SHORT
        self.AFE_Reg_Write(AFE_CLKDIV_PRF, 0)  #CLKDIV_PRF 4MHz

        self.AFE_Reg_Write(AFE_PDNCYCLESTC, 5475)  #AFE_DPD1STC
        self.AFE_Reg_Write(AFE_PDNCYCLEENDC, 39199)  #AFE_DPD1ENDC

        # self.AFE_Reg_Write(AFE_DEC, 0x13) #decimation factor setted as 8

        self.AFE_Reg_Write(AFE_ALARM, 0X000200)  #0 4MHz

        self.AFE_Enable_Read()


    # def set_config(self, reg, value):
    #     self.i2c.mem_write(value, self.address, reg)

    def AFE_get_led1_val(self,amount):

        LED1_buf = []
        LED2_buf = []
        LED3_buf = []
        Ambient_buf=[]
        for i in range(amount):
            # if self.interrupt.value() == 1:

            #     ADC_Freq=ADC_Freq+1
            # print('huhu')
            while(self.interrupt.value() == 0): #It is a active-low interrupt
                #等待中断信号
                pass

            LED1=self.AFE_Reg_Read(AFE_LED1VAL)
            LED2=self.AFE_Reg_Read(AFE_LED2VAL)
            LED3=self.AFE_Reg_Read(AFE_ALED2VAL)
            Ambient=self.AFE_Reg_Read(AFE_ALED1VAL)
            LED1_buf.append(LED1) #在buf后面添加新的对象LED1
            LED2_buf.append(LED2)
            LED3_buf.append(LED3)
            Ambient_buf.append(Ambient)
            # print('xixi')

        return LED1_buf, LED2_buf, LED3_buf, Ambient_buf

    def AFE_get_led2_val(self):
        return self.AFE_Reg_Read(AFE_LED2VAL)


    def AFE_get_led3_val(self):
        return self.AFE_Reg_Read(AFE_ALED2VAL)


    # def read_fifo(self):
    #     """
    #     读取寄存器的数据
    #     """
    #     red_led = None
    #     ir_led = None

    #     #从寄存器中读取1个字节的数据
    #     reg_INTR1 = self.i2c.mem_read(1, self.address, REG_INTR_STATUS_1) #猜想必须读取才能重新读取新的数据
    #     reg_INTR2 = self.i2c.mem_read(1, self.address, REG_INTR_STATUS_2)

    #     d = self.i2c.mem_read(6, self.address, REG_FIFO_DATA) #读取6 bit 从外设中

    #     # mask MSB [23:18]
    #     red_led = (d[0] << 16 | d[1] << 8 | d[2]) & 0x03FFFF
    #     ir_led = (d[3] << 16 | d[4] << 8 | d[5]) & 0x03FFFF

    #     return red_led, ir_led

    def read_sequential(self, amount=100):
        """
        读取模块上红色LED和红外光LED测量的数据
        """
        red_buf = []
        ir_buf = []
        for i in range(amount):
            while(self.interrupt.value() == 1): #It is a active-low interrupt
                #等待中断信号
                pass

            red, ir = self.read_fifo()

            red_buf.append(red) #在buf后面添加新的对象red
            ir_buf.append(ir)

        return red_buf, ir_buf
