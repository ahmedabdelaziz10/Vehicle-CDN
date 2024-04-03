import random
import sys
import time
from mn_wifi.cli import CLI
from mininet.log import setLogLevel, info
from mn_wifi.net import Mininet_wifi
from mininet.node import Controller
from mn_wifi.node import UserAP, Car, Station
from mn_wifi.link import wmediumd, ITSLink, mesh
from mn_wifi.wmediumdConnector import interference
from mn_wifi.vanet import vanet
from mn_wifi.telemetry import telemetry
from mn_wifi.sumo.runner import sumo

def simple_file():

    # Create Network
    net = Mininet_wifi(controller=Controller, accessPoint=UserAP, link=wmediumd, wmediumd_mode=interference)

    # Add Controllers
    c0 = net.addController('c0')
    info("*** Creating nodes ***\n")
    
    ## Add hosts
    h1 = net.addHost('h1', mac='00:00:00:00:00:01', ip='10.0.0.1/8')
    
    # Add Stations
    sta1 = net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.2/8', min_x=0, max_x=300, min_y=0, max_y=300, min_v=25, max_v=50)
    sta2 = net.addStation('sta2', mac='00:00:00:00:00:03', ip='10.0.0.3/8', min_x=0, max_x=300, min_y=0, max_y=300, min_v=30, max_v=70)

    # Add AP
    ap1 = net.addAccessPoint('ap1', ssid = 'ssid-AP1', mode='g', channel='1', position='50,40,0')
    ap2 = net.addAccessPoint('ap2', ssid = 'ssid-AP2', mode = 'g', channel = '6', position = '100,100,0')
    ap3 = net.addAccessPoint('ap3', ssid = 'ssid-AP3', mode = 'g', channel = '11', position = '150,200,0')
   
    info("*** Setting Propagation Model ***\n")
    net.setPropagationModel(model='logDistance', exp=3)

    net.configureNodes()
    net.addLink(ap1,h1)
    net.addLink(ap2,h1)
    net.addLink(ap3,h1)

 
    net.plotGraph(max_x=300, max_y=300)

    # Set mobility model for stations
    net.setMobilityModel(time=0, model='RandomDirection',max_x=300, max_y=300, seed=20)
    #net.startMobility(time=0, mob_rep=1, reverse=False)
    #net.stopMobility(time=26)
    
    
    
    	

    
    info("*** Starting Network ***\n")
    net.build()
    c0.start()
    ap1.start([c0])
    last_time = time.time() ##setting up time before starting loop
    last_RSSI_sta1 = sta1.wintfs[0].rssi ##setting up RSSI at sta1 before starting loop
    last_RSSI_sta2 = sta2.wintfs[0].rssi## setting up RSSI at sta2 before starting loop
    while True:
    	print(f'RSSI of station 1 is {sta1.wintfs[0].rssi}')
    	print(f'RSSI of station 2 is {sta2.wintfs[0].rssi}')
    	current_time = time.time()##current time after loop
    	elapsed_time = current_time - last_time ##measuring time from entering loop and before, elapsed time of iter
    	current_RSSI_sta1 = sta1.wintfs[0].rssi
    	current_RSSI_sta2 = sta2.wintfs[0].rssi
    	print(f'last RSSI is {last_RSSI_sta1}')
    	RSSI_diff_sta1 = current_RSSI_sta1 - last_RSSI_sta1 ##same process as time but for RSSI of station 1
    	RSSI_diff_sta2 = current_RSSI_sta2 - last_RSSI_sta2 ##same process as time but for RSSI of station 1
    	RSRQ_sta1 = RSSI_diff_sta1/elapsed_time
    	RSRQ_sta2 = RSSI_diff_sta2/elapsed_time
    	print(f'RSSI diff is {RSSI_diff_sta1}')
    	print(elapsed_time)
    	last_RSSI_sta1 = current_RSSI_sta1 ##updating last RSSI at station1 to be current time before new iter of loop
    	last_RSSI_sta2 = current_RSSI_sta2 ##updating last RSSI at station2 to be current time before new iter of loop
    	last_time = current_time ##updating last time to be current time before new iter of loop
    	time.sleep(max(0,0.5-elapsed_time)) ##cannot sleep for non-negative time, 0.5-elapsed time because otherwise it adds 0.5 
    	##onto elapsed time
    	if current_RSSI_sta1 != 0 or current_RSSI_sta2 !=0:
    		CLI(net,script = "command.txt")
    	if current_RSSI_sta1 !=0 and current_RSSI_sta2:
    		CLI(net,script = "ping2.txt")
    # Start stations
    info("*** Running CLI ***\n")
    CLI(net,script = "command.txt")
    

    info("*** Stopping Network ***\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    simple_file()
