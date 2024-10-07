import tkinter as tk
from tkinter import ttk
import tkinter as tk
from tkinter import LabelFrame
import json
import serial.tools.list_ports
import serial
from tkinter import messagebox
import subprocess
import os
from typing import Optional, Dict

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.frames = {}
        # PageOne
        page_one = PageOne(parent=self)
        self.frames["PageOne"] = page_one
        page_one.grid(row=0, column=0, sticky="nsew")
        # PageTwo
        page_two = PageTwo(parent=self)
        self.frames["PageTwo"] = page_two
        page_two.grid(row=0, column=0, sticky="nsew")
        # Set Initial Page
        self.show_frame("PageOne")        
    def setup_window(self):
        '''Window Settings'''      
        self.title("Calibration Test Setup")
        #self.resizable(False, False)# Disable window resizing
        
        window_width = 950
        window_height = 790
        # Calculate the x and y coordinates to center the window on the screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)+100
        
        # Update the window geometry to include the calculated coordinates for centering
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")# Top-left corner position at (x, y)
    def show_frame(self, page_name):
        '''Show Specified Page'''
        frame = self.frames[page_name]
        frame.tkraise()  # Bring the specified page to the foreground
    def change_frame_and_update_language(self,this_page,next_page):
        '''Bring the specified page to the foreground and synchronize the language settings of the first page with the second page.'''
        this_frame = self.frames[this_page]
        next_frame = self.frames[next_page]
        language_set = this_frame.buttons['SELECT_LANGUAGE'].get()
        next_frame.page_two_language_set = language_set
        next_frame.update_language(language_set)
        next_frame.tkraise()  # Bring the specified page to the foreground
        
class ButtonTemplate(ttk.Frame):
    translations = {
            'en': {
                'FILENAME_PREFIX': 'FILENAME PREFIX',
                'PUMP_CHANNEL': 'PUMP CHANNEL',
                'SYRING_TYPE': 'SYRING TYPE',
                'AUTO_VERIFY': 'AUTO VERIFY',
                'FILENAME_PREFIX_COMMENT': 'Please enter the file name prefix (e.g., calibrateResult_).',
                'PUMP_CHANNEL_COMMENT': 'Please select the pump channel number.',
                'SYRING_TYPE_COMMENT': 'Please select the syringe type.',
                'SAVE': 'Save',
                'SELECT_LANGUAGE': 'SELECT LANGUAGE',
                'PUMP_PORT':'PUMP PORT',
                'CONTROLLER_PORT':'CONTROLLER PORT',
                'BALANCE_PORT':'BALANCE PORT',
                'CONNECT_BUTTON':'Connect',
                'RESCAN':'Rescan Ports',
                'NEXT':'Next',
                'GO_BACK':'Go back',
                'EXECUTE':' Execute',
                'FLOW_RATE':['flow rate\n（ul/min） ','flow rate'],
                'PREPARE_TIME':['prepare time\n（sec）','prepare time'],
                'TEST_TIME':['test time\n（sec）','test time'],
                'ADD':'add',
                'DELETE':'Delete Selected',
                'OK':'ok',
                'TEST_POINTS_SETTING':'TEST POINTS SETTING',
                'CONFIG_FILENAME':'CONFIG FILENAME',
                'CONFIG_FILENAME_COMMENT':'',
                'SELECTED_CONFIG_FILE':'SELECTED CONFIG FILE',
                'SELECTED_CONFIG_FILE_COMMENT':'Please select the config file',
                'settings_saved': 'Settings have been saved to {config_filename}.json',
                'filename_used': 'The filename has already been used.\nPlease re-enter a different filename.',
                'insufficient_data': 'Must have at least three sets of data.',
                'volume_exceeds': 'The total volume exceeds the selected syringe\'s maximum capacity.\n\nTotal volume: {total_volume}\nAvailable volume: {max_volume}',
                'input_empty': 'The input can\'t be EMPTY.',
                "SELECT_CONFIGURATION_FILE": "Select Configuration File",
                "PARAMETER_SETTINGS": "Parameter Settings",
                "SAVE_SETTINGS": "Save Settings",
                "EXECUTE_PROGRAM": "Execute Program",
                "SWITCH_PAGES": "Switch Pages",
                "PLEASE_ENTER_A_NUMBER": "Please enter a number.",
                "PLEASE_ENSURE_THERE_IS_ONLY_ONE_DECIMAL_POINT": "Please ensure input number  is only one decimal point.",
                "MAX_VOLUME": "Max volume",
                "TOTAL_VOLUME": "total volume",
                "FILENAME_ALREADY_EXISTS_PLEASE_ENTER_A_DIFFERENT_NAME": "The filename already exists.",
                "ARE_YOU_SURE_YOU_WANT_TO_OVERWRITE_THE_EXISTING_FILE": "Are you sure you want to overwrite the existing file?",
                "RESERVE_VOLUME":'reserve volume',
                "INVALID_INPUT":'Invalid input. Please check your entry and try again'
            },
            'zh': {
                'FILENAME_PREFIX': '文件名前綴',
                'PUMP_CHANNEL': '幫浦通道',
                'SYRING_TYPE': '注射器類型',
                'RATE_LIST': '流速列表（ul/min）',
                'TIME_LIST': '時間列表（秒）',
                'COLLECT_TIME_AFTER_STOP': '停止後收集時間（秒）',
                'AUTO_VERIFY': '自動驗證',
                'FILENAME_PREFIX_COMMENT': '請輸入文件名前綴（例如：calibrateResult_）。',
                'PUMP_CHANNEL_COMMENT': '請選擇幫浦通道編號。',
                'SYRING_TYPE_COMMENT': '請選擇注射器類型。',
                'SAVE': '儲存設定',
                'SELECT_LANGUAGE': '選擇語言',
                'PUMP_PORT': '幫浦埠',
                'CONTROLLER_PORT': '控制器埠',
                'BALANCE_PORT': '電子秤埠',
                'CONNECT_BUTTON': '連接',
                'RESCAN':'重新掃描',
                'NEXT':'下一頁',
                'GO_BACK':'上一頁',
                'EXECUTE':' 執行',
                'FLOW_RATE':['流速\n(ul/min)','流速'],
                'PREPARE_TIME':['準備時間\n     (秒)','準備時間'],
                'TEST_TIME':['測試時間\n     (秒)','測試時間'],
                'FLOW_DATA_LABEL':'流量資料',
                'ADD':'新增',
                'DELETE':'刪除所選項目',
                'OK':'確認',
                'TEST_POINTS_SETTING':'測試點設定',
                'CONFIG_FILENAME':'設定檔之檔名',
                'CONFIG_FILENAME_COMMENT':'請輸入設定檔的檔名',
                'SELECTED_CONFIG_FILE':'選擇設定檔',
                'SELECTED_CONFIG_FILE_COMMENT':'可選擇已儲存的設定檔',
                'GO_TO_THE_PAGE_ONE':'回到上一頁',
                'settings_saved': '設定檔已儲存到{config_filename}.json',
                'filename_used': '檔名已被使用。\n請重新輸入不同的檔名。',
                'insufficient_data': '必須至少有三組數據。',
                'volume_exceeds': '總體積超過所選注射器的最大容量。\n\n總體積: {total_volume}\n可用容量: {max_volume}',
                'input_empty': '輸入不能為空。',
                "SELECT_CONFIGURATION_FILE": "選擇設定檔",
                "PARAMETER_SETTINGS": "參數設定",
                "SAVE_SETTINGS": "儲存設定",
                "EXECUTE_PROGRAM": "執行程式",
                "SWITCH_PAGES": "切換頁面",
                "PLEASE_ENTER_A_NUMBER": "請輸入數字。",
                "PLEASE_ENSURE_THERE_IS_ONLY_ONE_DECIMAL_POINT": "請確保輸入的數字只包含一個小數點。",
                "MAX_VOLUME": "最大容量",
                "TOTAL_VOLUME": "累計容量",
                "FILENAME_ALREADY_EXISTS_PLEASE_ENTER_A_DIFFERENT_NAME": "檔名已存在。",
                "ARE_YOU_SURE_YOU_WANT_TO_OVERWRITE_THE_EXISTING_FILE": "確定要覆蓋現有檔案嗎？",
                "RESERVE_VOLUME":'保留容量',
                "INVALID_INPUT":'輸入無效。請檢查您的輸入並重試'
            }
    }     
    defalut_settings_dict = {
            'FILENAME_PREFIX': "calibrateResult_",
            'PUMP_CHANNEL': 2, 
            'SYRING_TYPE': 'steel_L (10 ml)',
            'RATE_LIST': "0",
            'TIME_LIST': "0", 
            'TEST_INTERVAL': 30, 
            'COLLECT_TIME_AFTER_STOP': 30, 
            'CALIBRATE': True,
            'AUTO_VERIFY': True, 
            'REPEAT_TIMES_OF_JUST_COLLECT_DATA': 10,
            'CONFIG_FILENAME':'',
            'SELECTED_CONFIG_FILE':'setting.json'
    }   
    syringe_types = {
        "steel_S (8 ml)": 8.0,   # steel_S : 8 ml
        "steel_L (10 ml)": 10.0,  # steel_L : 10 ml
        "glass_S (2.5 ml)": 2.5, # glass_S : 2.5 ml
        "glass_M (5 ml)": 5.0,   # glass_M : 5 ml
        "glass_L (10 ml)": 10.0   # glass_L : 10 ml
    }
    def __init__(self, parent):
        super().__init__(parent)
        self.grid_columnconfigure(0, minsize=30) # Configure the first column (index 0) to have a minimum width of 300 pixels
        self.grid_columnconfigure(1, minsize=0)
        self.tk_vars = {}# Dictionary to store Tkinter variables
        self.labels = {}# Dictionary to store labels
        self.buttons = {}# Dictionary to store buttons
        self.comments = {}# Dictionary to store comments
        self.padding_x = 10
        self.padding_y = 5
    def create_language_selector(self,frame,r,c):#TODO
        label = ttk.Label(frame, text=ButtonTemplate.translations['en']['SELECT_LANGUAGE'])
        label.grid(row=r, column=c, padx=self.padding_x, pady=self.padding_y, sticky=tk.E)

        combobox = ttk.Combobox(frame, values=['en', 'zh'], state='readonly', width=2)
        combobox.set('en')
        combobox.bind('<<ComboboxSelected>>', self.change_language)
        combobox.grid(row=r, column=1, padx=self.padding_x, pady=self.padding_y,sticky='nsew')
        
        self.labels['SELECT_LANGUAGE'] = label
        self.buttons['SELECT_LANGUAGE'] = combobox
    def create_entry(self,frame,r, key):
        label = ttk.Label(frame, text=ButtonTemplate.translations['en'][key])
        label.grid(row=r, column=0, padx=self.padding_x, pady=self.padding_y, sticky=tk.E)

        commet = ttk.Label(frame, text=ButtonTemplate.translations['en']["{}_COMMENT".format(key)])
        commet.grid(row=r, column=2, padx=self.padding_x, pady=self.padding_y, sticky=tk.W)

        default_value = tk.StringVar(value=self.defalut_settings_dict[key])
        entry = ttk.Entry(frame, textvariable=default_value,width=27)
        entry.grid(row=r, column=1, padx=self.padding_x, pady=self.padding_y, sticky='nsew')

        self.tk_vars[key] = default_value
        self.labels[key] = label
        self.buttons[key] = entry
        self.comments[key] = commet   
    def create_selector(self,frame,r,key,options_list):
        label = ttk.Label(frame, text=ButtonTemplate.translations['en'][key])
        label.grid(row=r, column=0, padx=self.padding_x, pady=self.padding_y, sticky=tk.E)
        
        commet = ttk.Label(frame, text=ButtonTemplate.translations['en']["{}_COMMENT".format(key)])
        commet.grid(row=r, column=2, padx=self.padding_x, pady=self.padding_y, sticky=tk.W)

        default_value = tk.StringVar(value=ButtonTemplate.defalut_settings_dict[key])
        combobox = ttk.Combobox(frame, textvariable=default_value, values=options_list,state='readonly', width=25)
        combobox.grid(row=r, column=1, padx=self.padding_x, pady=self.padding_y, sticky='nsew')   
        
        self.tk_vars[key] = default_value
        self.labels[key] = label
        self.buttons[key] = combobox
        self.comments[key] = commet
    def create_checkbutton(self,frame,r,key,com):
        label = ttk.Label(frame, text=ButtonTemplate.translations['en'][key])
        label.grid(row=r, column=0, padx=10, pady=5, sticky=tk.E)

        default_value = tk.BooleanVar(value=self.defalut_settings_dict[key])
        
        checkbutton = ttk.Checkbutton(frame,text="     ",variable=default_value,command=com)
        checkbutton.grid(row=r, column=1, padx=10, pady=5, sticky=tk.W)      
        
        self.tk_vars[key] = default_value
        self.buttons[key] = checkbutton
        self.labels[key] = label   
    def create_button(self,frame,r,c,key,com,button_state=tk.NORMAL):
        button = ttk.Button(frame, text=ButtonTemplate.translations['en'][key],command=com, width=20,state=button_state)
        button.grid(row=r, column=c, padx=self.padding_x, pady=self.padding_y,sticky='nsew')
        self.buttons[key] = button   
    def change_language(self, event):
        selected_language = self.buttons['SELECT_LANGUAGE'].get()
        self.update_language(selected_language) 
    def update_language(self, lang):
        self.labels['SELECT_LANGUAGE'].config(text=ButtonTemplate.translations[lang]['SELECT_LANGUAGE'])
    def update_button_clickable(self,key,button_state):
        if button_state :
            self.buttons[key].config(state=tk.NORMAL)
        else:
            self.buttons[key].config(state=tk.DISABLED)
            
class PageOne(ButtonTemplate):
    def __init__(self, parent):
        super().__init__(parent)
        self.port_connect_states = {}
        self.port_dict={}# Create a dictionary mapping port descriptions to their corresponding device names
       
        # 設定LabelFrame物件的統一長寬高
        labelframe_width=200
        labelframe_height=100
       
        # 語言設定區域
        self.frame_language = LabelFrame(self, text=PageOne.translations['en']['SELECT_LANGUAGE'], padx=10, pady=10,width=labelframe_width, height=labelframe_height)
        self.create_language_selector(frame=self.frame_language,r=0,c=0)
        
        # 幫浦設定區域
        self.frame_port = LabelFrame(self, text=PageOne.translations['en']['PARAMETER_SETTINGS'], padx=10, pady=10,width=labelframe_width, height=labelframe_height)
        self.create_port_button(frame=self.frame_port,r=0,key='PUMP_PORT',char='CH341')
        self.create_port_button(frame=self.frame_port,r=1,key='CONTROLLER_PORT',char='Uno')
        self.create_port_button(frame=self.frame_port,r=2,key='BALANCE_PORT',char='CH340')
        self.create_button(frame=self.frame_port,r=3,c=1,key='RESCAN',com=self.refresh_update_options)
        
        # 換頁設定區域
        self.frame_switch = LabelFrame(self, text=PageOne.translations['en']['SWITCH_PAGES'], padx=10, pady=10,width=labelframe_width, height=labelframe_height)
        self.create_button(frame=self.frame_switch,r=0,c=1,key='NEXT',com=lambda: parent.change_frame_and_update_language("PageOne","PageTwo"),button_state=tk.NORMAL)
        self.create_button(frame=self.frame_switch,r=0,c=0,key='GO_BACK',com=None,button_state=tk.DISABLED)
        
        # 佈局
        self.frame_language.grid(row=0, column=1, padx=0, pady=5,sticky="nsew")
        self.frame_port.grid(row=1, column=1, padx=0, pady=5,sticky="nsew")
        self.frame_switch.grid(row=2, column=1, padx=0, pady=5,sticky="nsew")
    def get_ports(self) ->list:
        """
        獲取所有可用的串口並返回它們的描述。

        這個方法使用 `serial.tools.list_ports.comports()` 來獲取當前系統中所有可用的串口。
        將每個串口的description與其對應的設備名稱映射到字典 `port_dict` 中。
        然後，提取出字典中的所有description（作為鍵）並將它們返回為一個列表。

        返回:
        list: 包含所有可用串口description的列表。
        """
        ports = serial.tools.list_ports.comports()
        # Create a dictionary mapping port descriptions to their corresponding device names
        self.port_dict = {port.description: port.device for port in ports}
        # Extract the list of port descriptions from the dictionary keys
        port_description_list = list(self.port_dict.keys())
        return port_description_list
    def find_port(self,list:list,key:str):
        """
        在給定的串口列表中查找包含指定關鍵字的端口描述。

        參數:
        list (list): 包含串口描述的列表。
        key (str): 用於匹配串口描述的關鍵字。

        返回:
        str: 匹配的串口描述，或 "No serial port found."。
        """
        default_port_option = None

        for item in list:
            if key in item:
                default_port_option = item
                break  
        default_port_option = default_port_option if default_port_option is not None else "No serial port found."
        return default_port_option
    def create_port_button(self,frame,r,key,char) ->None:
        """
        創建一個port選擇按鈕。
        """
        padding_x = 10
        padding_y = 5
        label = ttk.Label(frame,text=PageOne.translations['en'][key])
        label.grid(row=r, column=0, padx=padding_x, pady=padding_y, sticky=tk.E)
        
        button_list=self.get_ports()
        # 使用 find_port 方法在 button_list 中查找包含指定關鍵字 char 的串口描述，
        # 如果找到匹配的串口描述，將其設置為 StringVar 的初始值（default_value），
        default_value = tk.StringVar(value=self.find_port(button_list,char))
        combobox = ttk.Combobox(frame, textvariable=default_value, values=button_list,state='readonly',width=25)
        combobox.grid(row=r, column=1, padx=padding_x, pady=padding_y ,sticky='nsew')
        
        frame_connect_state = tk.Frame(frame)  
        connect_button = ttk.Button(
            frame_connect_state, 
            text=PageOne.translations['en']['CONNECT_BUTTON'],
            command=lambda: self.port_connect(key, char)
        )

        port_connect_state = tk.IntVar()
        checkbutton = tk.Checkbutton(frame_connect_state, text="Not Ready", variable=port_connect_state,state=tk.DISABLED)
        connect_button.pack(side="left", padx=padding_x)
        checkbutton.pack(side="left", padx=padding_x)
        
        frame_connect_state.grid(row=r, column=2,sticky=tk.W)
          
        self.tk_vars[key] = default_value
        self.labels[key] = label
        self.buttons[key] = combobox
        self.buttons[key + '_CONNECT'] = connect_button
        self.buttons[key + '_CHECKBUTTON'] = checkbutton
        self.port_connect_states[key]=port_connect_state
        return None
    def refresh_update_options(self) ->None:
        # 重新掃描的按鍵功能
        button_list = self.get_ports()
        port_mapping_dict = {'PUMP_PORT':'CH341','CONTROLLER_PORT':'Uno','BALANCE_PORT':'CH340'}
        for key,value in port_mapping_dict.items():
            self.tk_vars[key].set(self.find_port(button_list, value))
            self.buttons[key].config(values=button_list)
            
            self.port_connect_states[key].set(0)
            self.buttons[key+'_CHECKBUTTON'].config(text="Not Ready") 
        self.buttons['NEXT'].config(state=tk.DISABLED) 
    def port_connect(self,key,char):
        """
        CONNECT按鈕的功能函數
        """
        port_des = self.buttons[key].get()
        print(f"Selected port: {port_des}")

        port_device = self.port_dict.get(port_des)
        if port_device is None:
            port_device=char

        response = self.communicate_with(port=port_device)
        if response:
            print("通信測試成功")
        else:
            print("通信測試失敗")
        
        if response:
            self.port_connect_states[key].set(1)
            self.buttons[key+'_CHECKBUTTON'].config(text="On Ready!")
        else:
            self.port_connect_states[key].set(0)
            self.buttons[key+'_CHECKBUTTON'].config(text="Not Ready")
        
        can_next = self.ready_for_next()
        self.update_button_clickable('NEXT',can_next)
    def communicate_with(self,port, baudrate=9600, bytesize=7, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE, timeout=1):
        """
        Communicate with the specified serial device.

        :param port: Serial port name (default is 'COM5')
        :param baudrate: Baud rate (default is 9600)
        :param bytesize: Data bits (default is 7)
        :param parity: Parity bit (default is Even)
        :param stopbits: Stop bits (default is 1)
        :param timeout: Timeout setting in seconds (default is 1 second)
        :return: If communication is successful, return the received response; otherwise, return None
        """
        
        if port == 'COM5':
            try:
                with serial.Serial(port=port, baudrate=baudrate, bytesize=bytesize, 
                                parity=parity, stopbits=stopbits, timeout=timeout) as ser:
                    
                    if ser.is_open:
                        print(f"成功連接到 {port}")
                        
                        # 發送測試命令
                        test_command = b'Q\n'  # 可根據實際需要更改命令
                        ser.write(test_command)
                        print(f"已發送命令: {test_command}")

                        # 讀取回應
                        response = ser.read(100)  # 根據需求調整讀取的字節數
                        if response:
                            print(f"從設備接收到的回應: {response}")
                            return response
                        else:
                            print(f"設備未回應 {port}")
                            return None
                    else:
                        print(f"無法連接到 {port}")
                        return None
                        
            except serial.SerialException as e:
                print(f"通信錯誤: {e}")
                return None
        else:
            try:
                with  serial.Serial(port=port, baudrate=9600, bytesize=7, 
                                parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE, timeout=1) as ser:
                    # 檢查是否已經連接
                    print(ser)
                    if ser.is_open:
                        print("已經連接，正在嘗試重新連接...")
                        # 這裡故意再嘗試打開串口以產生錯誤
                        serial.Serial(port=port, baudrate=9600, bytesize=7, 
                                parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE, timeout=1)
                        
            except serial.SerialException as e:
                print("連接錯誤:", e)
                # 檢查特定的錯誤類型
                if "13" in str(e):
                    print('return True')
                    return True
                else:
                    return False
            return False
        button = ttk.Button(self, text=PageOne.translations['en'][key],command=com, width=20,state=button_state)
        button.grid(row=r, column=1, padx=10, pady=5)
        self.buttons[key] = button   
    def ready_for_next(self) ->bool:
        """
        檢查系統是否準備好進行下一步操作。

        這個方法會檢查三個設備端口的連接狀態，分別是PUMP_PORT、CONTROLLER_PORT、BALANCE_PORT。
        如果所有端口的連接狀態均為 1（表示已連接），則返回 True，否則返回 False。

        返回:
        bool: 如果所有必需的端口都已連接，返回 True；否則返回 False。
        """
        return all([
            self.port_connect_states['PUMP_PORT'].get() == 1,
            self.port_connect_states['CONTROLLER_PORT'].get() == 1,
            self.port_connect_states['BALANCE_PORT'].get() == 1
        ])
    def update_language(self, lang) ->None:
        """
        更新語言
        """
        self.labels['SELECT_LANGUAGE'].config(text=PageOne.translations[lang]['SELECT_LANGUAGE'])
    
        button_list =['RESCAN','NEXT','GO_BACK']
        for key in button_list:
            self.buttons[key].config(text=PageOne.translations[lang][key])
        
        port_keys = ['PUMP_PORT', 'CONTROLLER_PORT', 'BALANCE_PORT']
        for key in port_keys:
            self.labels[key].config(text=PageOne.translations[lang][key])
            self.buttons[f'{key}_CONNECT'].config(text=PageOne.translations[lang]['CONNECT_BUTTON'])
        
        self.frame_language.config(text=PageTwo.translations[lang]['SELECT_LANGUAGE'])
        self.frame_port.config(text=PageTwo.translations[lang]['PARAMETER_SETTINGS'])
        self.frame_switch.config(text=PageTwo.translations[lang]['SWITCH_PAGES'])
        return
class PageTwo(ButtonTemplate):
    def __init__(self, parent):
        super().__init__(parent)
        # 設定檔會先存入 save_settings_dict 字典，然後轉換成 JSON 檔案保存。
        self.save_settings_dict =  {
            'FILENAME_PREFIX':'',
            'PUMP_CHANNEL':-1, 
            'SYRING_TYPE':'',
            'RATE_LIST': [],
            'TIME_LIST': [], 
            'AUTO_VERIFY':False, 
            }
        # 設定檔案會存入setting資料夾folder_name
        self.folder_name='setting'
        self.folder_path = self.find_or_create_folder(folder_name=self.folder_name)
        self.file_list = self.get_json_files(folder_path=self.folder_path)
        self.page_two_language_set ='en'
        self.reserve_volume = 0.002 # 預設的保留容量體積(單位:μL)
        print(f'列出預設資料夾內json檔的檔案清單\n>{self.file_list}')
        
        # 設定LabelFrame物件的統一長寬高
        labelframe_width=20
        labelframe_height=100
        
        # 以LabelFrame物件分區
        # 選擇設定檔區域
        self.frame_select = LabelFrame(self, text=PageTwo.translations['en']['SELECT_CONFIGURATION_FILE'], padx=10, pady=10,width=labelframe_width, height=labelframe_height)
        self.create_selector(frame=self.frame_select,r=0,key='SELECTED_CONFIG_FILE',options_list=self.file_list)
        self.buttons['SELECTED_CONFIG_FILE'].bind('<<ComboboxSelected>>', self.on_config_file_selected)    
        # 將下拉選單 'SELECTED_CONFIG_FILE' 的選擇事件綁定到 on_config_file_selected 方法
        
        # 參數設定區域
        self.frame_settings = LabelFrame(self, text=PageTwo.translations['en']['PARAMETER_SETTINGS'],padx=10, pady=10,width=labelframe_width, height=labelframe_height)
        self.create_entry(frame=self.frame_settings,r=0,key='FILENAME_PREFIX')
        self.create_selector(frame=self.frame_settings,r=1,key='PUMP_CHANNEL',options_list=[1, 2])
        self.create_selector(frame=self.frame_settings,r=2,key='SYRING_TYPE',options_list=list(self.syringe_types.keys()))
        self.create_checkbutton(frame=self.frame_settings,r=3,key='AUTO_VERIFY',com=self.auto_verify_selection)
        self.create_test_points_input_region (frame=self.frame_settings,r=4)  
        self.buttons['SYRING_TYPE'].bind("<<ComboboxSelected>>", self.on_syring_type_selection)
        # 將下拉選單 'SYRING_TYPE' 的選擇事件綁定到 on_syring_type_selection 方法
        
        # 儲存新設定檔區域
        self.frame_save = LabelFrame(self, text=PageTwo.translations['en']['SAVE_SETTINGS'], padx=10, pady=10,width=labelframe_width, height=labelframe_height)
        self.create_entry(frame=self.frame_save,r=1,key='CONFIG_FILENAME')
        self.create_button(frame=self.frame_save,r=1,c=2,key='SAVE',com=self.on_save_button_click)  
        self.create_validation_for_config_name_input(frame=self.frame_save,r=2,button=self.buttons['CONFIG_FILENAME'],key='config name input hint')
        
        # 儲存新設定檔區
        self.frame_execute = LabelFrame(self, text=PageTwo.translations['en']['EXECUTE_PROGRAM'], padx=10, pady=10,width=labelframe_width, height=labelframe_height)
        self.create_button(frame=self.frame_execute,r=0,c=1,key='EXECUTE',com=self.execute_program)
        
        # 儲存新設定檔區
        self.frame_switch = LabelFrame(self, text=PageTwo.translations['en']['SWITCH_PAGES'], padx=10, pady=10,width=labelframe_width, height=labelframe_height)
        self.create_button(frame=self.frame_switch,r=0,c=1,key='GO_BACK',com=lambda: parent.show_frame("PageOne"))
        self.create_button(frame=self.frame_switch,r=0,c=2,key='NEXT',com=None,button_state=tk.DISABLED)
        
        self.frame_select.grid(row=0, column=1, padx=0, pady=5,sticky="nsew")
        self.frame_settings.grid(row=1, column=1, padx=0, pady=5, sticky="nsew")
        self.frame_save.grid(row=2, column=1, padx=0, pady=5, sticky="nsew")
        self.frame_execute.grid(row=3, column=1, padx=0, pady=5, sticky="nsew")
        self.frame_switch.grid(row=4, column=1, padx=0, pady=5, sticky="nsew")
       
        self.update_default_value(selected_filename=self.buttons['SELECTED_CONFIG_FILE'].get(),folder_path=self.folder_path)
    def get_json_files(self,folder_path:str) ->list:
        """
        獲取指定資料夾中的所有 JSON 檔案名稱。

        :param folder_path: 要查詢的資料夾路徑
        :return: 包含所有 JSON 檔案名稱的列表
        """
        json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
        return json_files 
    def find_or_create_folder(self,folder_name:str) -> str:
        """
        在當前工作目錄中查找指定資料夾。如果不存在，則創建它。

        參數:
        folder_name (str): 要查找或創建的資料夾名稱。

        返回:
        str: 資料夾的完整路徑。
        """
        current_directory = os.getcwd()
        folder_path = os.path.join(current_directory, folder_name)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        return folder_path
    def update_default_value(self,selected_filename:str,folder_path:str) -> None:
        """
        根據選擇的檔案名稱和資料夾路徑組合出完整路徑，
        讀取對應的 JSON 檔案並將其內容載入至字典中。
        然後將預設值更新為字典中的相應值。
        
        :param selected_filename: 要讀取的 JSON 檔案名稱
        :param folder_path: 包含該檔案的資料夾路徑
        :return: None (此函數不返回任何值)
        """
        file_path = os.path.join(folder_path, selected_filename)
        try:
            # 打開並讀取選中的 json 文件
            with open(file_path, "r") as file:
                content = json.load(file)
                print(f"Content of {selected_filename}:")
                print(content)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except json.JSONDecodeError:
            print(f"Failed to decode JSON from file: {file_path}")
        
        # 根據content字典內容更改預設值
        list=['FILENAME_PREFIX']
        for key in list:
            self.tk_vars[key] = content[key]
            self.buttons[key].delete(0, tk.END)  # 清空原有文本
            self.buttons[key].insert(0,self.tk_vars[key])
        list2 = ['PUMP_CHANNEL','SYRING_TYPE']
        for key in list2:
            self.tk_vars[key] = content[key]
            self.buttons[key].set(self.tk_vars[key])
        list3 = ['AUTO_VERIFY']
        for key in list3:
            self.tk_vars[key].set(content[key])
            
        flow_rate_list = content['RATE_LIST']
        time_list = content['TIME_LIST']
        # 清空treeview的列表
        for item in self.treeview.get_children():
             # Delete each item
            self.treeview.delete(item)
        # 填入treeview的列表
        for i in range(len(flow_rate_list)):
            self.treeview.insert("", tk.END,values=(flow_rate_list[i], time_list[i][0], time_list[i][1]))
        # 更新顯示的總容量值
        self.update_capacity_display()
        return
    def update_capacity_display(self) ->None:
        # 根據目前的treeview物件值來獲得總容量
        total_volume=self.calculate_treeview_capacity()
        # 獲取最大容量值：首先從 'SYRING_TYPE' 按鈕獲取所選擇的容量計，
        # 然後使用該容量計作為鍵，從 syringe_types 字典中獲得對應的最大容量。
        max_volume_key  = self.buttons['SYRING_TYPE'].get()
        max_volume = self.syringe_types[max_volume_key]
        max_volume = max_volume*1000 # 單位換算從ml到μl
        
        #比較總容量與最大容量更新總容量
        response = self.is_over_capacity(max_volume,total_volume)
        if response:
            self.labels['TOTAL_VOLUME'].config(text=f'{PageTwo.translations[self.page_two_language_set]['TOTAL_VOLUME']}:{total_volume:.5f} µL',fg='red')
        else: 
            self.labels['TOTAL_VOLUME'].config(text=f'{PageTwo.translations[self.page_two_language_set]['TOTAL_VOLUME']}:{total_volume:.5f} µL',fg='blue')
        
        self.labels['MAX_VOLUME'].config(text=f'{PageTwo.translations[self.page_two_language_set]['MAX_VOLUME']}:{max_volume:.5f} µL')
        return
    def auto_verify_selection(self) ->None:
        """
        當自動驗證選項被選中時，呼叫此函數以更新總容量值的顯示。
        """
        self.update_capacity_display()
        return
    def on_syring_type_selection(self,even):
        """
        當用戶選擇新的容量計時，將呼叫此函數以更新顯示內容。
        """
        self.update_capacity_display()
    def process_message(self, key:str, data: Optional[Dict] = None, lang:str='en') -> str:
        """
        根據給定的鍵值和語言，從翻譯字典中獲取相應的訊息並進行格式化。

        :param key: 訊息的鍵，對應翻譯字典中的一個條目，用於查找特定的訊息。
        :param data: 可選的字典，用於格式化訊息中的佔位符。如果為 None，則不進行格式化。
        :param lang: 語言代碼，用於指定使用的語言，預設為英文（'en'）。

        :return: 返回格式化後的訊息字串。如果找不到對應的鍵，返回 'Unknown message'。
        """
        message = self.translations.get(lang, {}).get(key, 'Unknown message')
        if data:
            message = message.format(**data)  # 使用字典中的數據格式化消息
        return message   
    def on_config_file_selected(self, event)->None:
        """
        處理設定檔下拉式選單的選擇事件。

        當用戶從下拉式選單中選擇一個設定檔時，這個函數將被調用。
        函數內部將根據選擇的檔案名稱更新顯示或相應的設定值。
        
        :param event: 事件對象，包含關於選擇的詳細資訊。
        """
        self.update_default_value(selected_filename=self.buttons['SELECTED_CONFIG_FILE'].get(),folder_path=self.folder_path)
        return
    def update_language(self, lang:str) ->None:
        """
        更新介面的語言設置。

        根據傳入的語言代碼更新界面上的所有文本和提示信息。
        
        :param lang: 語言代碼，例如 'zh' 表示中文，'en' 表示英文等。
        """
        setting_keys = ['FILENAME_PREFIX','PUMP_CHANNEL','SYRING_TYPE','CONFIG_FILENAME','SELECTED_CONFIG_FILE'] 
        # 更新標籤和註釋文本
        for key in setting_keys:
            self.labels[key].config(text=PageTwo.translations[lang][key])
            self.comments[key].config(text=PageTwo.translations[lang][f'{key}_COMMENT'])
        
        # 只更新特殊標籤的文本
        special_keys = ['AUTO_VERIFY','TEST_POINTS_SETTING']
        for key in special_keys:
            self.labels[key].config(text=PageTwo.translations[lang][key])
        
        # 更新標籤以及treeview物件的標題文本
        flow_data_keys =['FLOW_RATE','PREPARE_TIME','TEST_TIME',]
        for key in flow_data_keys:
            self.labels[key].config(text=PageTwo.translations[lang][key][0])
            self.treeview.heading(key, text=PageTwo.translations[lang][key][1])
        
        # 更新按鈕上顯示的文本
        button_keys =['SAVE','EXECUTE','DELETE','ADD','GO_BACK','NEXT']
        for key in button_keys:
            self.buttons[key].config(text=PageTwo.translations[lang][key])  
        
        # 更新區域名稱文本
        self.frame_select.config(text=PageTwo.translations[lang]['SELECT_CONFIGURATION_FILE'])
        self.frame_settings.config(text=PageTwo.translations[lang]['PARAMETER_SETTINGS'])
        self.frame_save.config(text=PageTwo.translations[lang]['SAVE_SETTINGS'])
        self.frame_execute.config(text=PageTwo.translations[lang]['EXECUTE_PROGRAM'])
        self.frame_switch.config(text=PageTwo.translations[lang]['SWITCH_PAGES'])
        
        # 更新體積相關標籤的文本以及變數
        self.labels['RESERVE_VOLUME'].config(text=f'{PageTwo.translations[lang]['RESERVE_VOLUME']}:{self.reserve_volume} μL')
        self.labels['TOTAL_VOLUME'].config(text=f'{PageTwo.translations[lang]['TOTAL_VOLUME']}:{self.calculate_treeview_capacity()} μL')
        return
    def get_all_values(self)->list:
        """
        獲取樹狀視圖中所有行的值並儲存到清單中。

        此函數將遍歷樹狀視圖中的所有行，並將每行的值收集到一個清單中。
        
        :return: 包含所有行值的清單，每個元素都是一行的值，格式為列表。
        """
        all_values_list = []
        for item in self.treeview.get_children():
            values = self.treeview.item(item, 'values')
            values_list = list(values)
            all_values_list.append(values_list) 
        return all_values_list
    def split_str_list_to_int_lists(self,data_list:list)->tuple[list, list]:
        """
        將資料分開成兩個列表：
        
        這個方法接受包含多個子列表的列表，每個子列表應至少三個字符串元素，
        每個元素列表的第一個元素表示速率，
        第二和第三個元素表示時間。
        該方法返回一個元組，包含兩個列表：
        一個是速率列表，另一個是時間列表。

        參數:
        data_list (list): 包含多個子列表的列表，每個子列表應包含至少三個字符串元素。

        返回:
        tuple[list, list]: 第一個列表包含轉換後的浮點數利率，第二個列表包含時間範圍列表。
        """
        rate_list = []
        time_list = []
        for item in data_list:
            rate_list.append(float(item[0]))  # 添加第一個元素到 rate_list
            time_list.append([float(item[1]), float(item[2])])  # 將第二和第三個元素合成列表添加到 time_list

        self.save_settings_dict['RATE_LIST'] = rate_list
        self.save_settings_dict['TIME_LIST'] = time_list
        return rate_list,time_list
    def is_over_capacity(self,max_volume:float,total_volume:float) ->bool:
        """
        檢查是否超過最大容量。

        這個方法接受最大容量和當前總容量，並返回一個布林值，
        用於指示當前容量是否超過最大限制。

        參數:
        max_volume (float): 容器的最大容量。
        total_volume (float): 當前的總容量。

        返回:
        bool: 如果當前容量超過最大容量，則返回 True，否則返回 False。
        """
        total_volume=total_volume+self.reserve_volume
        if total_volume > max_volume:
            return True
        else:
            return False
    def calculate_treeview_capacity(self)->float:
        """
        計算樹狀視圖的總容量。

        這個方法從樹狀視圖中獲取所有值，然後計算總容量。
        容量是根據速率和時間計算得出的。

        返回:
        float: 計算出的總容量。
        """
        data_list =self.get_all_values()
        rate_list,time_list=self.split_str_list_to_int_lists(data_list=data_list)
        
        total_volume=0
        for i in range(len(rate_list)):
            volume = rate_list[i]
            pre_time = time_list[i][0]
            post_time = time_list[i][1]
            total_duration = pre_time/60 + post_time/60
            total_volume += volume * total_duration
            
        if  self.tk_vars['AUTO_VERIFY'].get() == True:
            total_volume = total_volume*2
        
        return total_volume           
    def save_settings(self)->dict:
        """
        將參數設定存入字典中並返回該字典。

        這個方法將當前的設定儲存到實例的設定字典中，
        並返回該字典以便於後續使用。

        返回:
        dict: 包含當前設定的字典。
        """
        
        string_fields = ['FILENAME_PREFIX', 'SYRING_TYPE']
        for field in string_fields:
            self.save_settings_dict[field] = self.buttons[field].get()
        
        integer_fields = ['PUMP_CHANNEL']
        for field in integer_fields:
            self.save_settings_dict[field] = int(self.buttons[field].get())      
        
        boolean_fields = ['AUTO_VERIFY']
        for field in boolean_fields:
            self.save_settings_dict[field] = self.tk_vars[field].get()
        
        # 處理從 treeview 獲得的數據，建立速率列表和時間列表。
        data_list = self.get_all_values()
        rate_list,time_list = self.split_str_list_to_int_lists(data_list)

        self.save_settings_dict['RATE_LIST'] = rate_list
        self.save_settings_dict['TIME_LIST'] = time_list
        
        return  self.save_settings_dict
    def on_save_button_click(self)->None:
        """
        按下 Save 按鈕後執行的函數。

        此函數執行以下操作：
        1. 檢查所指定的檔案名稱是否已存在，避免檔案重複。如果檔案已存在，詢問使用者是否要覆蓋該檔案。
        2. 檢查儲存的測試點資料是否包含超過三組數據。
        3. 計算總計容量並檢查是否超過設定的最大容量。
        4. 通過以上檢查後，將資料存入字典，再將字典轉換成json檔案。
        
        """
        config_filename_without_extension = self.buttons['CONFIG_FILENAME'].get()
        config_filename_with_extension = f'{config_filename_without_extension}.json'
        if config_filename_without_extension in self.file_list:
            if not messagebox.askyesno('HINT', self.process_message('ARE_YOU_SURE_YOU_WANT_TO_OVERWRITE_THE_EXISTING_FILE',None,lang=self.page_two_language_set)):
                print('設定檔保存失敗')
                return
        
        data_list = self.get_all_values()
        if len(data_list)<3:
            messagebox.showinfo('HINT', self.process_message('insufficient_data',None, lang=self.page_two_language_set))
            print('設定檔保存失敗')
            return
        
        max_volume_key  = self.buttons['SYRING_TYPE'].get()
        max_volume = self.syringe_types[max_volume_key]
        max_volume =max_volume*1000
        total_volume =self.calculate_treeview_capacity()
        if self.is_over_capacity(max_volume,total_volume) is True:
            messagebox.showinfo('HINT',self.process_message('volume_exceeds', {'total_volume': total_volume, 'max_volume': max_volume}, lang=self.page_two_language_set))
            return
        else:
            self.save_settings()
            # 將save_settings_dict字典存成json_file
            full_path = os.path.join(self.folder_path, config_filename_with_extension)
            with open(full_path, "w") as json_file:
                json.dump(self.save_settings_dict, json_file, indent=4)
                messagebox.showinfo('HINT',self.process_message('settings_saved', {'config_filename': config_filename_with_extension}, lang=self.page_two_language_set))
            print('設定檔保存成功')
            
            # 將新增的設定檔的檔名更新到選擇設定檔的下拉式清單選項中
            self.file_list = self.get_json_files(folder_path=self.folder_path)
            self.buttons['SELECTED_CONFIG_FILE']['values'] = self.file_list
            self.buttons['SELECTED_CONFIG_FILE'].set(config_filename_with_extension)
            
            return
    def create_test_points_input_region (self,frame,r) ->None:
        """
        創建測試點輸入區域。

        此函數負責設置和初始化用於輸入測試點數據的 GUI 元素。
        """
        # 創建測試點區域的父框架
        frame_test_points_region = tk.Frame(frame)

        # 創建錯誤標籤
        self.labels['error_label'] = tk.Label(frame_test_points_region, text="", fg="red")

        # 創建樹狀視圖顯示測試點數據
        self.treeview = ttk.Treeview(frame_test_points_region, columns=("FLOW_RATE", "PREPARE_TIME", "TEST_TIME"), show='headings', height=7)

        # 創建並配置滾動條
        scrollbar = tk.Scrollbar(frame_test_points_region)  # 在頁框中加入捲軸元件
        scrollbar.config(command=self.treeview.yview)  # 設定 scrollbar 的 command = treeview.yview

        # 將元素添加到父容器中 父框架為frame_test_points_region
        self.labels['error_label'].pack(side='top', padx=0, pady=0)
        self.treeview.pack(side='left')
        scrollbar.pack(side='right', fill='y')  # 設定捲軸的位置以及填滿方式

        # 定義欄位
        keys = ['FLOW_RATE', 'PREPARE_TIME', 'TEST_TIME']
        for key in keys:
            self.treeview.heading(key, text=PageTwo.translations['en'][key][1])
            self.treeview.column(key, width=120)

        # 設定輸入框的父容器
        frame_entry = ttk.Frame(frame)
        # 創建測試點的輸入框
        self.create_small_entry_with_label(frame_entry, 'FLOW_RATE')
        self.create_small_entry_with_label(frame_entry, 'PREPARE_TIME')
        self.create_small_entry_with_label(frame_entry, 'TEST_TIME')

        # 創建標籤和按鈕
        self.labels['TEST_POINTS_SETTING'] = ttk.Label(frame, text=PageTwo.translations['en']['TEST_POINTS_SETTING'])
        self.buttons['ADD'] = ttk.Button(frame, text=PageTwo.translations['en']['ADD'], command=self.insert_values)
        self.buttons['DELETE'] = ttk.Button(frame, text=PageTwo.translations['en']['DELETE'], command=self.delete_selected)
        self.labels['TOTAL_VOLUME'] = tk.Label(frame, text="", fg="blue")
        self.labels['RESERVE_VOLUME'] = tk.Label(frame, text=f'{PageTwo.translations[self.page_two_language_set]['RESERVE_VOLUME']}:{self.reserve_volume} μL', fg="blue")

        # 使用 grid 佈局 父框架為frame
        frame_entry.grid(row=r, column=1, sticky=tk.W)
        self.labels['TEST_POINTS_SETTING'].grid(row=r, column=0, padx=10, sticky=tk.E)
        self.buttons['ADD'].grid(row=r, column=2, sticky=tk.W)
        frame_test_points_region.grid(row=r+1, column=1)
        self.buttons['DELETE'].grid(row=r+1, column=2, sticky=tk.W)
        self.labels['TOTAL_VOLUME'].grid(row=r+2, column=1, sticky=tk.W)
        self.labels['RESERVE_VOLUME'].grid(row=r+3, column=1, sticky=tk.W)

            
        frame_volume = ttk.Frame(frame)
        self.labels['MAX_VOLUME'] = tk.Label(frame_volume, text="", fg="blue")
        self.labels['MAX_VOLUME'].pack(side=tk.TOP, anchor=tk.W)
        frame_volume.grid(row=r+1,column=0,sticky=tk.W)
        return        
    def create_small_entry_with_label(self,frame,key:str) ->None: 
        # test_points_input˙輸入框創建函式
        # 使用 register 來將函式轉換為 Tkinter 可以使用的 callback
        validate_command = (self.register(self.validate_input), '%S', '%P')
        
        padding_x=5
        padding_y=0
        label = ttk.Label(frame, text=PageTwo.translations['en'][key][0])  # 設定寬度
        label.pack(side='left', padx=padding_x,pady=padding_y)
        entry = ttk.Entry(frame,validate='key', validatecommand=validate_command, width=5)  # 設定寬度
        entry.pack(side='left', padx=padding_x,pady=padding_y)
    
        self.labels[key]=label
        self.buttons[key]=entry   
    def insert_values(self) ->None:
        """
        處理 ADD 按鈕的功能，將用戶輸入的值插入到測試點列表中。
        """
        def pad_zero_if_starts_with_dot(s:str) ->str:# 在點前補零
            if s.startswith('.'):
                return '0' + s  
            return s
        def pad_zero_if_ends_with_dot(s:str) ->str:# 在點後補零
            if s.endswith('.'):
                return  s+'0'  
            return s

        # 獲取輸入的值
        flow_rate = self.buttons['FLOW_RATE'].get()
        pre_time = self.buttons['PREPARE_TIME'].get()
        post_time = self.buttons['TEST_TIME'].get()
        
        if flow_rate.strip() == "" or pre_time.strip() == "" or post_time.strip() == "":# 檢查輸入值是否只有空格
            messagebox.showinfo('HINT',self.process_message('input_empty',None, lang=self.page_two_language_set))
            return
        if flow_rate.count('.') > 1 or pre_time.count('.') > 1 or post_time.count('.') > 1:
            messagebox.showinfo('HINT',self.process_message('PLEASE_ENSURE_THERE_IS_ONLY_ONE_DECIMAL_POINT',None, lang=self.page_two_language_set))
            return
        else:
            flow_rate = pad_zero_if_starts_with_dot(flow_rate)
            pre_time = pad_zero_if_starts_with_dot(pre_time)
            post_time = pad_zero_if_starts_with_dot(post_time)
            flow_rate = pad_zero_if_ends_with_dot(flow_rate)
            pre_time = pad_zero_if_ends_with_dot(pre_time)
            post_time = pad_zero_if_ends_with_dot(post_time)
            
            # 插入到 Treeview 中
            self.treeview.insert("", tk.END, values=(flow_rate, pre_time, post_time))
        # 每次按下add鍵變會更新總容量顯示值
        self.update_capacity_display()
        return
    def delete_selected(self) ->None:
        """
        處理 delete按鈕的功能，刪除選中的項目。
        """
        # 獲取選中的項目
        selected_items = self.treeview.selection()
        for item in selected_items:
            self.treeview.delete(item)  # 刪除選中的項目
        # 每次刪除實會更新總容量顯示值
        self.update_capacity_display()
        return
    def validate_input(self, char:str, current:str) ->bool:
        """
        驗證函式，檢查是否輸入的是否是數字(可有小數點)
        """
        if char.isdigit():  # 允許數字
            self.labels['error_label'].config(text="")  # 清空錯誤提示
            return True
        elif char == ".":  # 允許小數點
            if len(current)>=1 and current.count(".")<=1 : # 只允許一個小數點
                self.labels['error_label'].config(text="")  # 清空錯誤提示
                return True
            else:
                self.labels['error_label'].config(text=PageTwo.translations[self.page_two_language_set]['PLEASE_ENSURE_THERE_IS_ONLY_ONE_DECIMAL_POINT'])
                return True
        elif char ==" ":
            self.labels['error_label'].config(text=PageTwo.translations[self.page_two_language_set]['input_empty'])
            return False
        else:
            self.labels['error_label'].config(text=PageTwo.translations[self.page_two_language_set]['PLEASE_ENTER_A_NUMBER'])
            return False
    def execute_program(self) ->None:
        """
        EXECUTE功能，按下按鈕後先驗證輸入後啟動校正程式。
        """
        if not self.Confirm_data():
            messagebox.showinfo('HINT',self.process_message('INVALID_INPUT',None,self.page_two_language_set))
        else:
            self.save_settings()
            with open(f"autoCalibration_setting.json", "w") as json_file:
                json.dump(self.save_settings_dict, json_file, indent=4)
                messagebox.showinfo('HINT',self.process_message('settings_saved', {'config_filename': 'autoCalibration_setting'}, lang=self.page_two_language_set))
            try:
                subprocess.Popen(['python', 'autoCalibration.py'])  
                print("程式已啟動")
            except Exception as e:
                print(f"啟動程式時出錯: {e}")
    def Confirm_data(self):
        data_list = self.get_all_values()
        rate_list,time_list = self.split_str_list_to_int_lists(data_list)
        max_volume_key  = self.buttons['SYRING_TYPE'].get()
        max_volume = self.syringe_types[max_volume_key]
        max_volume = max_volume*1000
        total_volume = self.calculate_treeview_capacity()
        if self.is_over_capacity(max_volume,total_volume):
            print("1")
            return False
        if not isinstance(self.buttons['FILENAME_PREFIX'].get(), (str)):
            print("2")
            return False
        if not int(self.buttons['PUMP_CHANNEL'].get()) in [1, 2]:
            print("3")
            return False
        if not self.buttons['SYRING_TYPE'].get() in list(self.syringe_types.keys()):
            print("4")
            return False
        
        
        if len(rate_list)!=len(time_list):
            print("5")
            return False
        if len(rate_list)<3:
            print("6")
            return False
        for item in range(len(time_list)):
            if not isinstance(item, (int)):
                print("7")
                return False
        for i in range(len(time_list)):
            if not isinstance(time_list[i][0], (float)):
                print("8")
                return False 
            if not isinstance(time_list[i][1], (float)):
                print("9")
                return False
        if not isinstance(self.tk_vars['AUTO_VERIFY'].get()==1,(bool)):
            print("10")
            return False
        
        return True
    def create_validation_for_config_name_input(self, frame, r:int, button:ttk.Entry ,key:str)->None:
        """
        為配置名稱輸入框創建驗證規則。

        :param frame:
        :param r: 在網格中顯示標籤的行號，類型為整數
        :param button: 與輸入框相關聯的按鈕，類型為 ttk.Entry
        :param key: 用於標識標籤的字符或名稱，類型為字符串
        """
        # 註冊驗證函數，檢查用戶輸入的合法性
        self.validate_command_config_name = (self.register(self.validate_config_name_input), '%S', '%P')
        
        # 將驗證命令應用於指定的按鈕
        button.config(validate='key', validatecommand=self.validate_command_config_name)
        
        # 創建提示標籤以顯示驗證結果
        label = tk.Label(frame, text="", fg="red")
        label.grid(row=r, column=1, padx=1, pady=1, sticky=tk.W)
        
        # 將標籤存儲到字典中，方便後續引用
        self.labels[key] = label
    def validate_config_name_input(self, char, current:str) ->bool:
        """
        驗證函式，檢查輸入設定檔檔案名稱是否重複
        """
        current = f'{current}.json'# 加上附檔名
        if current in self.file_list:  # 允許數字
            self.labels['config name input hint'].config(text=PageTwo.translations[self.page_two_language_set]['FILENAME_ALREADY_EXISTS_PLEASE_ENTER_A_DIFFERENT_NAME'])  # 
            return True
        else:
            self.labels['config name input hint'].config(text="")  # 
            return True 
if __name__ == "__main__":
    app = Application()
    app.mainloop()