import random
import sys
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

def simple_file(args):

    # Create Network
    net = Mininet_wifi(controller=Controller, accessPoint=UserAP, link=wmediumd, wmediumd_mode=interference)

    # Add Controllers
    c0 = net.addController('c0')
    info("*** Creating nodes ***\n")
    
    ## Add hosts
    h1 = net.addHost('h1', mac='00:00:00:00:00:01', ip='10.0.0.1/8')
    
    # Add Stations
    sta1 = net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.2/8',position = '150,150,0')
    sta2 = net.addStation('sta2', mac='00:00:00:00:00:03', ip='10.0.0.3/8',position = '40,40,0')

    # Add AP
    ap1 = net.addAccessPoint('ap1', ssid='ssid-AP1', mode='a', channel='36', position='50,40,0')
   
    info("*** Setting Propagation Model ***\n")
    net.setPropagationModel(model='logDistance', exp=3)

    net.configureNodes()
    net.addLink(ap1,h1)

    if '-p' not in args:
        net.plotGraph(max_x=300, max_y=300)

    # Set mobility model for stations
    net.startMobility(time=0, mob_rep=1, reverse=False)

    p1, p2, p3, p4 = {}, {}, {}, {}
    if '-c' not in args:
        p1 = {'position': '50.0,50.0,0.0'}
        p2 = {'position': '40.0,40.0,0.0'}
        p3 = {'position': '250.0,250,0.0'}
        p4 = {'position': '289.0,31.0,0.0'}

    while True:
    
    	net.mobility(sta1, 'start', time=0, **p1)
    	net.mobility(sta2, 'start', time=0, **p2)
    	net.mobility(sta1, 'stop', time=25, **p3)
    	net.mobility(sta2, 'stop', time=25, **p4)
    	net.stopMobility(time=23)
    	print(sta1.wintfs[0].rssi)
    	time = time+1
    	if time = 25
    	
   	 
    
    
    info("*** Starting Network ***\n")
    net.build()
    c0.start()
    ap1.start([c0])
    
    # Start stations
    
    

    info("*** Running CLI ***\n")
    CLI(net)

    info("*** Stopping Network ***\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    simple_file(sys.argv)
