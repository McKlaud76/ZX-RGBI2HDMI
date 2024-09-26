#pragma once
#include "stdio.h"
#include "v_buf.h"
#include "inttypes.h"
#include "stdbool.h"
#include "pico.h"
//#define FW_VER "0.5A"

#define BOARD_CODE_36LJU22 // to be used with RP2040 Zero
//#define BOARD_CODE_09LJV23

//конфигурация под конкретные платы - configuration for specific boards
#ifdef BOARD_CODE_36LJU22
    #define HDMI_PIN_invert_diffpairs (0)
    #define HDMI_PIN_RGB_notBGR (0)

    #define beginHDMI_PIN_data (8)
    #define beginHDMI_PIN_clk (14)

    #define beginVGA_PIN (8)

    #define F_CAP_PIN (6)
 
    #define D0_CAP_PIN (0)
    #define HS_PIN (D0_CAP_PIN+4)
#else

#ifdef BOARD_CODE_09LJV23
    //начальный пин VGA - VGA start pin
    #define beginVGA_PIN (7)

    //определение пинов и настроек HDMI - HDMI pin and settings definition
    //09LJV23
    #define HDMI_PIN_invert_diffpairs (0)
    #define HDMI_PIN_RGB_notBGR (0)

    #define beginHDMI_PIN_data (7)
    #define beginHDMI_PIN_clk (13)
#else

    //по умолчанию - by default
     //начальный пин VGA - VGA start pin
    #define beginVGA_PIN (7)

    //определение пинов и настроек HDMI - HDMI pin and settings definition
    //09LJV23
    #define HDMI_PIN_invert_diffpairs (0)
    #define HDMI_PIN_RGB_notBGR (0)

    #define beginHDMI_PIN_data (7)
    #define beginHDMI_PIN_clk (13)
    
#endif
#endif

extern uint8_t pallete8[];

enum p_clk_mode_t{SELF_SYNC_MODE,EXT_SYNC_MODE,Z80_FREQ_MODE};
enum video_out_mode_t{VGA,HDMI,RGB,COMP};
enum in_sync_mode_t{S_SYNC,C_SYNC};
enum c_mode_t{PAL,NTSC,SECAM};

typedef struct cap_set_t cap_set_t;
struct cap_set_t {
  int16_t shX;
  int16_t shY;
  enum p_clk_mode_t p_clk_mode;
  enum video_out_mode_t video_out_mode;
  enum in_sync_mode_t in_sync_mode;
  bool is_3X_Buf;
  uint32_t int_freq;
  uint ext_freq_div;
  uint capture_delay;
  uint capture_delay_rise;
  uint capture_delay_fall;
  uint inv_capture_pin_mask;
  uint16_t len_VS;

  enum c_mode_t c_mode;
  bool is_wide_mode;
};

//определение PIO и SM для задачи VGA - defining PIO and SM for VGA task
#define PIO_VGA (pio0)
#define SM_VGA (0)
//определение PIO и SM для задачи HDMI - defining PIO and SM for HDMI task

#define pio_HDMI0 (pio0)
#define sm_HDMI0 (0)

//определение PIO для захвата - defining PIO for capture
#define PIO_CAP (pio1)
//номера SM для захвата - SM numbers for capture
#define SM_CAP  (0)

//значения пинов захвата по умолчанию - default capture pin values
#ifndef D0_CAP_PIN
#define D0_CAP_PIN (0)
#endif

#ifndef F_CAP_PIN
#define F_CAP_PIN (D0_CAP_PIN+6)
#endif

#ifndef HS_PIN
#define HS_PIN (D0_CAP_PIN+4)
#endif

#define V_BUF_W (320)
#define V_BUF_H (320)
#define V_BUF_SZ ((V_BUF_H+1)*V_BUF_W/2)

extern uint8_t g_gbuf[];

#define G_PRINTF  printf
#define G_PRINTF_INFO  printf
#define G_PRINTF_DEBUG  printf
#define G_PRINTF_ERROR  printf
