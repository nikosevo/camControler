#!python3

import irsdk
import time
import keyboard


# this is our State class, with some helpful variables
class State:
    ir_connected = False
    last_car_setup_tick = -1
    last_dr_tick = -1
    active_driver = 6


    sor_drivers = ['Nikos Vrace',
                   'Ruben Vega',
                   'Jesus J Bohorquez',
                   'Dylan McCarty'
                   ]

    sor_drivers_car_nums = {
        "None" : 0
    }

    def changeActiveDriver(self,select):
        for index, key in enumerate(self.sor_drivers_car_nums):
            if(index == select):
                self.active_driver = self.sor_drivers_car_nums[key]
                return



    
    


# here we check if we are connected to iracing
# so we can retrieve some data
def check_iracing():
    if state.ir_connected and not (ir.is_initialized and ir.is_connected):
        state.ir_connected = False
        # don't forget to reset your State variables
        state.last_car_setup_tick = -1
        # we are shutting down ir library (clearing all internal variables)
        ir.shutdown()
        print('irsdk disconnected')
    elif not state.ir_connected and ir.startup() and ir.is_initialized and ir.is_connected:
        state.ir_connected = True
        print('irsdk connected')

# our main loop, where we retrieve data
# and do something useful with it
def loop():
    # on each tick we freeze buffer with live telemetry
    # it is optional, but useful if you use vars like CarIdxXXX
    # this way you will have consistent data from those vars inside one tick
    # because sometimes while you retrieve one CarIdxXXX variable
    # another one in next line of code could change
    # to the next iracing internal tick_count
    # and you will get incosistent data
    ir.freeze_var_buffer_latest()

    # retrieve live telemetry data
    # check here for list of available variables
    # https://github.com/kutu/pyirsdk/blob/master/vars.txt
    # this is not full list, because some cars has additional
    # specific variables, like break bias, wings adjustment, etc
    # t = ir['SessionTime']
    # print('session time:', t)

    # retrieve CarSetup from session data
    # we also check if CarSetup data has been updated
    # with ir.get_session_info_update_by_key(key)
    # but first you need to request data, before checking if its updated


    drivers = ir['DriverInfo']['Drivers']
    if drivers:
        dr_tick = ir.get_session_info_update_by_key('DriverInfo')
        if(dr_tick != state.last_dr_tick):
            state.last_dr_tick = dr_tick


            for entry_driver in drivers:
                for sor_driver in state.sor_drivers:
                    if(entry_driver['UserName'] == sor_driver):
                        state.sor_drivers_car_nums[entry_driver['UserName']] = entry_driver['CarNumberRaw']
            print(state.sor_drivers_car_nums)
    
    
    # print(usr)


    if drivers:
        drivers_tick = ir.get_session_info_update_by_key('DriverInfo')
        # print(drivers)

    car_setup = ir['CarSetup']
    if car_setup:
        car_setup_tick = ir.get_session_info_update_by_key('CarSetup')
        if car_setup_tick != state.last_car_setup_tick:
            state.last_car_setup_tick = car_setup_tick
            print('car setup update count:', car_setup['UpdateCount'])
            # now you can go to garage, and do some changes with your setup
            # this line will be printed, only when you change something
            # and press apply button, but not every 1 sec
    # note about session info data
    # you should always check if data exists first
    # before do something like ir['WeekendInfo']['TeamRacing']
    # so do like this:
    # if ir['WeekendInfo']:
    #   print(ir['WeekendInfo']['TeamRacing'])

    # and just as an example
    # you can send commands to iracing
    # like switch cameras, rewind in replay mode, send chat and pit commands, etc
    # check pyirsdk.py library to see what commands are available
    # https://github.com/kutu/pyirsdk/blob/master/irsdk.py#L134 (class BroadcastMsg)
    # when you run this script, camera will be switched to P1
    # and very first camera in list of cameras in iracing
    # while script is running, change camera by yourself in iracing
    # and notice how this code changes it back every 1 sec
    # ir.cam_switch_pos(0, 1)

if __name__ == '__main__':
    # initializing ir and state
    ir = irsdk.IRSDK()
    state = State()

    try:
        # infinite loop
        while True:
            # check if we are connected to iracing
            check_iracing()
            # if we are, then process data
            if state.ir_connected:
                loop()
            # sleep for 1 second
            # maximum you can use is 1/60
            # cause iracing updates data with 60 fps
            if keyboard.read_key() == "q":
                ir.replay_set_play_speed(-1)
                ir.cam_switch_num(car_number='64',group=1)
            if keyboard.read_key() == "w":
                ir.replay_set_play_speed(0)
            if keyboard.read_key() == "e":
                ir.replay_set_play_speed(2)


            #changing active driver
            if keyboard.read_key() == "1":
                state.changeActiveDriver(1)
                ir.cam_switch_num(car_number=str(state.active_driver),group=9)
                print(state.active_driver)
            if keyboard.read_key() == "2":
                print(state.active_driver)
                ir.cam_switch_num(car_number=str(state.active_driver),group=9)
                state.changeActiveDriver(2)

            
            if keyboard.read_key() == "a":   #tv1
                ir.cam_switch_num(car_number=str(state.active_driver),group=11)
            if keyboard.read_key() == "s":  #tv3
                ir.cam_switch_num(car_number=str(state.active_driver),group=13)
            if keyboard.read_key() == "d":  #scenic
                ir.cam_switch_num(car_number=str(state.active_driver),group=10)
            if keyboard.read_key() == "f":
                ir.cam_switch_num(car_number=str(state.active_driver),group=16)            
            
            
            if keyboard.read_key() == "z": #choper
                ir.cam_switch_num(car_number=str(state.active_driver),group=19)            
            if keyboard.read_key() == "x": #rear chase
                ir.cam_switch_num(car_number=str(state.active_driver),group=22)            
            if keyboard.read_key() == "c": #rollbar
                ir.cam_switch_num(car_number=str(state.active_driver),group=3)            
            if keyboard.read_key() == "v": #gearbox
                ir.cam_switch_num(car_number=str(state.active_driver),group=2)


            # ime.sleep(0.2)
    except KeyboardInterrupt:
        # press ctrl+c to exit
        pass
