# ZX RGB-I to VGA & HDMI Configuration Tool
# (c) Aleks Ekb
# Source: https://github.com/AlexEkb4ever/ZX_RGBI2VGA-HDMI
# ---------------------------------------------------------
# Version: 1.0 - English
# ---------------------------------------------------------
# Change log:
# 1.0 EN:   translation to English by KWF
#           minor changes to layout
# ---------------------------------------------------------
# GPL-3.0 license

# -*- coding: utf-8 -*-

import PySimpleGUI as sg
#import serial.tools.list_ports
import time
import re
import sys
import glob
import serial

def write_ser(ser,key,value):
    return True

def serial_ports():
    """ Lists serial port names
        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result
# default theme
sg.change_look_and_feel('SystemDefaultForReal') #GreenTan

# get list of ports
#dev_TTY=[comport.device for comport in serial.tools.list_ports.comports()]#v1
dev_TTY=serial_ports()#v2
if len(dev_TTY)==0:
    dev_TTY=[""]
    sg.PopupNoButtons("No serial port found !",auto_close=True)
    #exit(0)
    sys.exit()
    
#print([comport.device for comport in serial.tools.list_ports.comports()])

#Draw the button
namesMode=('Self-synchronisation','External Clock','Z80 Clock Signal');

comboBoxMode=sg.Combo(namesMode,default_value=namesMode[0], size=(20, 1),key='modeName',readonly=True)
comboBoxPorts=sg.InputCombo(dev_TTY,default_value=dev_TTY[0], size=(40, 1),key='portName',readonly=True)
sliderX=sg.Frame(layout=[[
     sg.Slider((200, 0), orientation='h', enable_events=True, key='SLIDERX')          
    ]],title=" X offset",title_location=sg.TITLE_LOCATION_TOP,key='settingsBlock')

sliderY=sg.Frame(layout=[[
     sg.Slider((0, 200), orientation='h', enable_events=True, key='SLIDERY')          
    ]],title=" Y offset",title_location=sg.TITLE_LOCATION_TOP,key='settingsBlock')

sliderF=sg.Frame(layout=[[
     sg.Slider((6000, 9000), orientation='h', enable_events=True, key='-SLIDERF-',size=(250,20))          
    ]],title=" Internal Capture Frequency (kHz)",title_location=sg.TITLE_LOCATION_TOP,key='setting_F_Block')

dividerF=sg.Frame(layout=[[
     sg.Slider((1, 5), orientation='h', enable_events=True, key='-SLIDER_f_div-')          
    ]],title=" Divider ",title_location=sg.TITLE_LOCATION_TOP,key='dividerFblock')

slider_VS_LEN=sg.Frame(layout=[[
     sg.Slider((50, 500), orientation='h', enable_events=True, key='-SLIDER_VS_LEN-')          
    ]],title=" KSI Length ",title_location=sg.TITLE_LOCATION_TOP,key='settings_VS_LEN_Block')

invBlock=sg.Frame(layout=[[
     sg.CBox('F', size=(3, 1),key='is_inv_F'),    
     sg.CBox('KSI', size=(3, 1),key='is_inv_VS'),  
     sg.CBox('SSI', size=(3, 1),key='is_inv_HS'),  
     sg.CBox('I', size=(3, 1),key='is_inv_I'),  
     sg.CBox('R', size=(3, 1),key='is_inv_R'),  
     sg.CBox('G', size=(3, 1),key='is_inv_G'),  
     sg.CBox('B', size=(3, 1),key='is_inv_B'),  
    ]],title=" Invert Input Signals",title_location=sg.TITLE_LOCATION_TOP,key='setting_inv_Block')

sliderDelay0= sg.Slider((0, 31), orientation='h', enable_events=True, key='-SLIDER_DELAY_0-')          
   
sliderDelay1=sg.Frame(layout=[[
     sg.Slider((0, 31), orientation='h', enable_events=True, key='-SLIDER_DELAY_1-')          
    ]],title=" along the front ",title_location=sg.TITLE_LOCATION_TOP,key='-SLIDER_DELAY_BLOCK1-')

sliderDelay2=sg.Frame(layout=[[
     sg.Slider((0, 31), orientation='h', enable_events=True, key='-SLIDER_DELAY_2-')          
    ]],title=" on the decline",title_location=sg.TITLE_LOCATION_TOP,key='-SLIDER_DELAY_BLOCK2-')

syncSelect=sg.Frame(layout=[[sg.Radio('Separated ', "SYNCMODE", default=True,key="isVS_HS"),
                           sg.Radio('Composite', "SYNCMODE",key="isVHS")],[sg.Push(),slider_VS_LEN,sg.Push()]],title=" Synchronisation ",title_location=sg.TITLE_LOCATION_TOP)

btn1=sg.Button('Apply', size=(10,1),key="btn1Click")

block0=[
         [sg.Frame(layout=[[sg.Radio('VGA ', "VIDEOMODE", default=True, size=(5, 1),key="isVGAout",disabled=False),
                           sg.Radio('HDMI ', "VIDEOMODE", key="isHDMIout",disabled=False)],[
                           sg.Radio('RGB ', "VIDEOMODE", size=(5, 1),key="isRGBout",disabled=True),
                           sg.Radio('COMP', "VIDEOMODE", key="isCOMPout",disabled=True)],
                           [
                               sg.Push(),sg.Frame(layout=[[sg.CBox('widescreen', key='is_widescreen',disabled=True)]], title=" Proportions ",title_location=sg.TITLE_LOCATION_TOP,key="WIDE_MODE_BLOCK"),sg.Push()],[
                               
                            sg.Frame(layout=[[sg.Radio(' PAL (50Hz) ', "SYS_COLOR_MODE", default=True,key="isPAL",disabled=False),
                                              sg.Radio(' NTSC (60Hz) ', "SYS_COLOR_MODE",key="isNTSC",disabled=False)]], title=" Standard ",title_location=sg.TITLE_LOCATION_TOP,key="C_MODE_BLOCK")
                               ]], title=" Video Output ",title_location=sg.TITLE_LOCATION_TOP),
          sg.Frame(layout=[[sg.Radio(' 1X ', "BUFMODE", default=True, size=(5, 1),key="is1X_BUFMODE",disabled=False),
                                     sg.Radio(' 3X ', "BUFMODE",key="is3X_BUFMODE",disabled=False)]], title=" Buffer ",title_location=sg.TITLE_LOCATION_TOP)
          ],
    
         [sg.Frame(layout=[[comboBoxPorts]],title=" Serial Port",title_location=sg.TITLE_LOCATION_TOP,key='portNameBlock')]]

block1=[[
         syncSelect,
         sg.Frame(layout=[[comboBoxMode],[dividerF]],title=" Pixel Clock Source",title_location=sg.TITLE_LOCATION_TOP)],
        [sliderF]
        ]

block2=[[sg.Frame(layout=[
    
  
    [sg.Push(),sliderX, sliderY,sg.Push()],
    [sg.Push(),sg.Frame(layout=[[sliderDelay1,sliderDelay2],[sg.Push(),sliderDelay0,sg.Push()]],title=" Capture Delay ",title_location=sg.TITLE_LOCATION_TOP,key='delay_cap_block'),sg.Push()],
    [sg.Push(),invBlock,sg.Push()],
    
     #[sg.Push(),sg.Column( layout=[[sliderF]] , element_justification='c'),sg.Push()]
    
    ],title="",title_location=sg.TITLE_LOCATION_TOP,key='settingsBlock')]]

blockBTN=[[btn1]]

layout = [
     [sg.Push(),sg.Column( layout=block0 , element_justification='c'),sg.Push()],
     [sg.Push(),sg.Column( layout=block1 , element_justification='c'),sg.Push()],
     [sg.Push(),sg.Column( layout=block2 , element_justification='c'),sg.Push()],
     [sg.Push(),sg.Column( layout=blockBTN , element_justification='c'),sg.Push()],
        ]

#Draw the window

window = sg.Window('ZX RGB-I to VGA & HDMI ConfigGUI by Alex Ekb', layout, font=('',12), margins=(10,0), size=(600,650), default_element_size=(40, 1),scaling=True, grab_anywhere=False)
#window.set_icon(red_icon)
#window.set_icon(r'HDMI_icon.png')

ser=None
oldSerName=None
itst=0
x_sh='0'
y_sh='0'
l_mode='read'
while True:
    event, values = window.read(timeout=100)
    if event is None:
        break
    
    # Checking serial port connection
    #print(values)
    
    xnew=int(values['SLIDERX'])
    ynew=int(values['SLIDERY'])    
    
    if event=='__TIMEOUT__':
        # change serial port
        if (comboBoxPorts.get()!=oldSerName):
            if l_mode!='write':
                l_mode='read'
            ser_name=comboBoxPorts.get()
            if ser==None:
                while ser==None:
                    try:
                        ser=serial.Serial(ser_name,115200, timeout=0.001)
                        oldSerName=ser_name
                        
                    except:
                        ser=None
                        print(" Serial "+ser_name+" Connection ERROR!!!")
                        time.sleep(1)
                        
            else:
                ser.close()
                ser=serial.Serial(ser_name,115200, timeout=0.001)
                oldSerName=ser_name            
         
    #print(event)
    # saving the entire block of data
    if event=='btn1Click':
        #print("Saving data")
        sg.PopupNoButtons(" Rebooting the board ... WAIT ...", auto_close=True, no_titlebar=True, text_color='Red', font='Arial 16 italic bold', background_color='Yellow')
                
        l_mode='write'
    #print(btn1.tex)
    #print(values)
    
    # mode selection
    modeName=window['modeName'].get()
    
    #print(modeName)
    if modeName==namesMode[0]: #self-synchronization
        window['dividerFblock'].hide_row()
        window['setting_F_Block'].unhide_row()
        window['-SLIDER_DELAY_0-'].unhide_row() 
        window['-SLIDER_DELAY_BLOCK1-'].hide_row()
        window['-SLIDER_DELAY_BLOCK2-'].hide_row()
        
    if modeName==namesMode[1]: #external clock
        window['dividerFblock'].unhide_row()
        window['setting_F_Block'].hide_row()        
        window['-SLIDER_DELAY_0-'].unhide_row()        
        window['-SLIDER_DELAY_BLOCK1-'].hide_row()
        window['-SLIDER_DELAY_BLOCK2-'].hide_row()

    if modeName==namesMode[2]: #Z80 clock signal
        window['dividerFblock'].hide_row()
        window['setting_F_Block'].hide_row()
        window['-SLIDER_DELAY_0-'].hide_row()        
        window['-SLIDER_DELAY_BLOCK1-'].unhide_row()
        window['-SLIDER_DELAY_BLOCK2-'].unhide_row()
    
    if window['isHDMIout'].get():
        window['C_MODE_BLOCK'].hide_row()
        window['WIDE_MODE_BLOCK'].unhide_row()
        
    if window['isVGAout'].get():
        window['C_MODE_BLOCK'].hide_row() 
        window['WIDE_MODE_BLOCK'].unhide_row()
        
    if window['isRGBout'].get():
        window['C_MODE_BLOCK'].unhide_row()
        window['WIDE_MODE_BLOCK'].hide_row()
        
    if window['isCOMPout'].get():
        window['C_MODE_BLOCK'].unhide_row()  
        window['WIDE_MODE_BLOCK'].hide_row()
   
    if window['isVHS'].get():
        window['settings_VS_LEN_Block'].unhide_row()
    if window['isVS_HS'].get():
        window['settings_VS_LEN_Block'].hide_row()        
   
    # working with serial port
    if event=='__TIMEOUT__':
        if ser!=None:
            try: 
                # hardware mode check
                ser.write("mode\n".encode())
                time.sleep(0.1)
                hw_mode=str(ser.readall())
                #print(hw_mode)
                
                #mode 0 - mode of writing and reading values
                if (hw_mode.find("mode 0")>0):
                    print("H/W Mode 0")
                    #desired mode
                   
                    # save to chip
                    if l_mode=='write':
                        sg.PopupNoButtons("Save Parameters",auto_close=True)
                       
                        ser.write(("wcap_sh_x "+str(int(values['SLIDERX']))+"\n").encode())
                        time.sleep(0.01)                        
                        ser.readall()
                        
                        ser.write(("wcap_sh_y "+str(int(values['SLIDERY']))+"\n").encode())
                        time.sleep(0.01)                        
                        ser.readall()     
                        
                        ser.write(("wcap_ext_f_div "+str(int(values['-SLIDER_f_div-']))+"\n").encode())
                        time.sleep(0.01)                        
                        ser.readall()    
                        
                        ser.write(("wcap_int_f "+str(int(values['-SLIDERF-']))+"000\n").encode())
                        time.sleep(0.01)                        
                        ser.readall()      
                        
                        ser.write(("wcap_delay "+str(int(values['-SLIDER_DELAY_0-']))+"\n").encode())
                        time.sleep(0.01)                        
                        ser.readall()                         
                        
                        ser.write(("wcap_delay_rise "+str(int(values['-SLIDER_DELAY_1-']))+"\n").encode())
                        time.sleep(0.01)                        
                        ser.readall()  
                        
                        ser.write(("wcap_delay_fall "+str(int(values['-SLIDER_DELAY_2-']))+"\n").encode())
                        time.sleep(0.01)                        
                        ser.readall()   
                        
                        ser.write(("wcap_len_VS "+str(int(values['-SLIDER_VS_LEN-']))+"\n").encode())
                        time.sleep(0.01)                        
                        ser.readall()
                        
                        iD=0
                        if values['isHDMIout']:
                            iD=1
                        if values['isRGBout']:
                            iD=2
                        if values['isCOMPout']:
                            iD=3
                        ser.write(("wvideo_out "+str(int(iD))+"\n").encode())
                        time.sleep(0.01)                        
                        ser.readall()
                        
                        iD=0
                        if values['isNTSC']:
                            iD=1
                        
                        ser.write(("wc_mode "+str(int(iD))+"\n").encode())
                        time.sleep(0.01)                        
                        ser.readall()                        
  
                        iD=0
                        if values['is3X_BUFMODE']:
                            iD=1
                        ser.write(("wis_3X_bufmode "+str(int(iD))+"\n").encode())
                        time.sleep(0.01)                        
                        ser.readall()                        
                        
                        iD=0
                        if values['isVHS']:
                            iD=1
                        ser.write(("wcap_sync_mode "+str(int(iD))+"\n").encode())
                        time.sleep(0.01)                        
                        ser.readall() 
                        
                        iD=0
                        if values['is_widescreen']:
                            iD=1
                                                        
                        ser.write(("wwide_mode "+str(int(iD))+"\n").encode())
                        time.sleep(0.01)                        
                        ser.readall()                         
                 
                        iD=0
                        if values['modeName']==namesMode[1]:
                            iD=1
                        if values['modeName']==namesMode[2]:
                            iD=2                              
                          
                        ser.write(("wcap_p_clk_mode "+str(int(iD))+"\n").encode())
                        time.sleep(0.01)                        
                        ser.readall() 
                        
                        iD=0
                        if values['is_inv_F']:
                            iD|=1
                        iD<<=1                         
                        if values['is_inv_VS']:
                            iD|=1
                        iD<<=1 
                        if values['is_inv_HS']:
                            iD|=1
                        iD<<=1 
                        if values['is_inv_I']:
                            iD|=1
                        iD<<=1 
                        if values['is_inv_R']:
                            iD|=1
                        iD<<=1 
                        if values['is_inv_G']:
                            iD|=1
                        iD<<=1 
                        if values['is_inv_B']:
                            iD|=1
                        ser.write(("wcap_in_inv_mask "+str(int(iD))+"\n").encode())
                        time.sleep(0.01)                        
                        ser.readall()                         
                        
                        print("Saving Data")
                        l_mode='user_mode'
                        ser.write("save\n".encode())
                        continue                        
                    #reading from chip
                    if l_mode=='read':
                        #show loading waiting window
                        sg.PopupNoButtons("Loading Parameters ...",auto_close=True)
                        #msg=sg.popup("загрузка параметров",no_titlebar=False,button_type=None,auto_close=True)
                       
                        #setting parameters on the form
                        ser.write("rcap_sh_x\n".encode())
                        time.sleep(0.01)
                        s1=str(ser.readall())
                        i_data = int(''.join(x for x in s1 if x.isdigit()))
                        window['SLIDERX'].update(value=i_data)
                        
                        ser.write("rcap_sh_y\n".encode())
                        time.sleep(0.01)
                        s1=str(ser.readall())
                        i_data = int(''.join(x for x in s1 if x.isdigit()))
                        window['SLIDERY'].update(value=i_data)  
                        
                        ser.write("rcap_ext_f_div\n".encode())
                        time.sleep(0.01)
                        s1=str(ser.readall())
                        i_data = int(''.join(x for x in s1 if x.isdigit()))
                        window['-SLIDER_f_div-'].update(value=i_data)                                    
                        
                        ser.write("rcap_int_f\n".encode())
                        time.sleep(0.01)
                        s1=str(ser.readall())
                        i_data = int(''.join(x for x in s1 if x.isdigit()))
                        window['-SLIDERF-'].update(value=i_data/1000) 
                        
                        ser.write("rcap_delay\n".encode())
                        time.sleep(0.01)
                        s1=str(ser.readall())
                        i_data = int(''.join(x for x in s1 if x.isdigit()))
                        window['-SLIDER_DELAY_0-'].update(value=i_data)                         
                        
                        ser.write("rcap_delay_rise\n".encode())
                        time.sleep(0.01)
                        s1=str(ser.readall())
                        i_data = int(''.join(x for x in s1 if x.isdigit()))
                        window['-SLIDER_DELAY_1-'].update(value=i_data)                         
                        
                        ser.write("rcap_delay_fall\n".encode())
                        time.sleep(0.01)
                        s1=str(ser.readall())
                        i_data = int(''.join(x for x in s1 if x.isdigit()))
                        window['-SLIDER_DELAY_2-'].update(value=i_data)                         
                         
                        ser.write("rcap_len_VS\n".encode())
                        time.sleep(0.01)
                        s1=str(ser.readall())
                        i_data = int(''.join(x for x in s1 if x.isdigit()))
                        window['-SLIDER_VS_LEN-'].update(value=i_data)                             
                        
                        ser.write("rwide_mode\n".encode())
                        time.sleep(0.01)
                        s1=str(ser.readall())
                        i_data = int(''.join(x for x in s1 if x.isdigit()))
                        if i_data==1:
                            window['is_widescreen'].update(True)    
                        else:
                            window['is_widescreen'].update(False)    

                        ser.write("rvideo_out\n".encode())
                        time.sleep(0.01)
                        s1=str(ser.readall())
                        i_data = int(''.join(x for x in s1 if x.isdigit()))
                        if i_data==0:
                            window['isVGAout'].update(True)
                        if i_data==1:
                            window['isHDMIout'].update(True)        
                        if i_data==2:
                            window['isRGBout'].update(True)    
                        if i_data==3:
                            window['isCOMPout'].update(True) 
                        
                        ser.write("rc_mode\n".encode())
                        time.sleep(0.01)
                        s1=str(ser.readall())
                        i_data = int(''.join(x for x in s1 if x.isdigit()))
                        if i_data==0:
                            window['isPAL'].update(True)
                        if i_data==1:
                            window['isNTSC'].update(True)                          
                        
                        ser.write("ris_3X_bufmode\n".encode())
                        time.sleep(0.01)
                        s1=str(ser.readall())
                        i_data = int(''.join(x for x in s1 if x.isdigit()))
                        print("s="+s1+" buf mode="+str(i_data))
                        if i_data==30:
                            window['is1X_BUFMODE'].update(True)
                        if i_data==31:
                            window['is3X_BUFMODE'].update(True)                              
                        
                        ser.write("rcap_sync_mode\n".encode())
                        time.sleep(0.01)
                        s1=str(ser.readall())
                        i_data = int(''.join(x for x in s1 if x.isdigit()))
                        if i_data==0:
                            window['isVS_HS'].update(True)
                        if i_data==1:
                            window['isVHS'].update(True)                             
                        
                        ser.write("rcap_p_clk_mode\n".encode())
                        time.sleep(0.01)
                        s1=str(ser.readall())
                        i_data = int(''.join(x for x in s1 if x.isdigit()))
                        window['modeName'].update(namesMode[i_data])
                        
                        ser.write("rcap_in_inv_mask\n".encode())
                        time.sleep(0.01)
                        s1=str(ser.readall())
                        i_data = int(''.join(x for x in s1 if x.isdigit()))
                        window['is_inv_B'].update(i_data&1)                        
                        i_data>>=1
                        window['is_inv_G'].update(i_data&1)                        
                        i_data>>=1
                        window['is_inv_R'].update(i_data&1)                        
                        i_data>>=1
                        window['is_inv_I'].update(i_data&1)                        
                        i_data>>=1
                        window['is_inv_HS'].update(i_data&1)                        
                        i_data>>=1
                        window['is_inv_VS'].update(i_data&1)                        
                        i_data>>=1
                        window['is_inv_F'].update(i_data&1)
                        l_mode='user_mode'
                        ser.write("exit\n".encode())
                        continue
                       
                #mode 1 - you can only change the offset
                if (hw_mode.find("mode 1")>0):
                    print("H/W Mode 1")
                     
                    if l_mode!='user_mode':
                        #если находимся не в том режиме - рестартуем
                        print("Restart H/W")
                        ser.write("reset\n".encode())
                        time.sleep(0.1)                    
                        continue
                    if x_sh!=xnew:
                        st1="wcap_sh_x "+str(xnew)
                        #print(st1)
                        ser.write(st1.encode())  
                        x_sh=xnew
                        time.sleep(0.1)
                        print(str(ser.readall()))
                        #print(" test "+st1)
                    
                    if y_sh!=ynew:
                        st1="wcap_sh_y "+str(ynew)
                        ser.write(st1.encode())  
                        y_sh=ynew
                        time.sleep(0.1)                
                        print(str(ser.readall()))
                    #print(" test "+st1)
               
            except:
                print("Serial error")
                ser.close()
                time.sleep(0.1)
                ser=None
                oldSerName=None

# end
