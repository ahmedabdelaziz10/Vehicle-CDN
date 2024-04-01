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

def simple_file():

    # Create Network
    net = Mininet_wifi(controller=Controller, accessPoint=UserAP, link=wmediumd, wmediumd_mode=interference)

    # Add Controllers
    c0 = net.addController('c0')
    info("*** Creating nodes ***\n")
    
    ##Add hosts
    
    h1 = net.addHost('h1', mac='00:00:00:00:00:01', ip='10.0.0.1/8')
    
    
    # Add Stations
    sta1 = net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.2/8',position = '150,100,0')
    sta2 = net.addStation('sta2', mac='00:00:00:00:00:03', ip='10.0.0.3/8',position = '40,40,0')

    # Add AP
    ap1 = net.addAccessPoint('ap1', ssid='ssid-AP1', mode='g', channel='1', position='50,40,0')
    ap2 = net.addAccessPoint('ap2',ssid = 'ssid-AP2', mode = 'g', channel = '6', position = '100,40,0')
    ap3 = net.addAccessPoint('ap3', ssid = 'ssid-AP3',mode = 'g', channel  = '11', position = '150,40,0')

    info("*** Setting Propagation Model ***\n")
    net.setPropagationModel(model='logDistance', exp=4.5)
    
    net.configureNodes()
    net.addLink(ap1,h1)
    net.addLink(ap2,h1)
    net.addLink(ap3,h1)

    net.plotGraph(max_x=200, max_y=200)

    info("*** Starting Network ***\n")
    net.build()
    c0.start()
    ap1.start([c0])
    ap2.start([c0])
    ap3.start([c0])
    
    #nodes = net.stations
    #telemetry(nodes = nodes, single = True, data_type = 'rssi')
    
    result = sta2.cmd('sta2 iw dev sta2-wlan0 link | grep signal | tr -d signal')
    print(result)
    info("*** Running CLI ***\n")
    CLI(net)
    

    
    


    info("*** Stopping Network ***\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    simple_file()
