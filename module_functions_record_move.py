# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 12:21:00 2022

@author: kec994
"""
import pandas as pd
import numpy as np
import keyboard
from time import sleep

from module_functions_record_movepydexarm import Dexarm

'''windows'''
#dexarm = Dexarm("COM67")
# Enable Stepper M17 X Y Z
# Disable Stepper M18 X Y Z


def record_move_joints(device, n_joints=3, step_time=0.2):
    device.disable_stepper_all()
    #device.set_color(0 , 0, 255) # RGB
    print('Start Recording..............')
    #device.release_all_servos()
    action=[]
    for i in range(n_joints):
        action.append(0)
    action=np.array(action).reshape(1, -1)
    action2=action.copy()
    
    time_action=np.array([0])
    
    
    cont=False
    i=0 # action_Index, time_Index
    # Have first data
    temp=device.get_mag_encoder()  
    temp=np.array(temp)
    action=temp.reshape(1, -1)
    while cont==False: # Invert Logic
        sleep(step_time)
        time_action[i]=time_action[i]+1
        cont=keyboard.is_pressed('q')
        temp=np.array(device.get_mag_encoder()).reshape(1, -1)
        

        if (temp[0]==action[i]).all():
            pass
        else:
            action=np.append(action, temp, axis=0)
            time_action=np.append(time_action,np.array([0]),axis=0)
            print('Previous Position Coord: {}\nCurrent Time: {}\nTotal Steps: {}'\
                  .format(action[i], time_action[i], len(action)))
            i+=1
            print('New Position: Temp')
            
    # Save Last Step After While
    action=np.append(action, temp, axis=0)
    
    time_action=np.append(time_action,np.array([0]),axis=0)
    print('Previous Position Coord: {}\nCurrent Time: {}\nTotal Steps: {}'\
          .format(action[i], time_action[i], len(action)))
    print('Stop Recording')
    device.enable_stepper_all()
    return action, time_action, step_time
    
#%%
#%%
#%%
#%%
#%%
if __name__ == "__main__":
    port='COM5'
    # Initialize
    device = Dexarm(port)
    n_joints=3
    
    device.g_code('M114') #Get Current Position
    device.go_home()
    
    input('Enter Any Key to Start recording........')
    
    #%% Start Training
    action,time_action, step_time=record_move_joints(device)
    # Converting Into Pandas
    action=pd.DataFrame(action)
    time_action=pd.DataFrame(time_action.reshape(-1, 1))
    step_time=pd.DataFrame([step_time])       
    #%%
    task_name='Task_02.xlsx'
    # Write File
    with pd.ExcelWriter(task_name) as writer:  
        action.to_excel(writer, sheet_name='joint_positions', index=False)
        time_action.to_excel(writer, sheet_name='duration', index=False)
        step_time.to_excel(writer, sheet_name='step_time', index=False)
        

    # Read From Excel File
    with pd.ExcelFile(task_name) as reader:
        action = pd.read_excel(reader, sheet_name='joint_positions')
        time_action = pd.read_excel(reader, sheet_name='duration')
        step_time = pd.read_excel(reader, sheet_name='step_time')
        
    device.disconnect()
