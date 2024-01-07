import random

from mn_wifi.cli import CLI
from mininet.log import setLogLevel, info
from mn_wifi.net import Mininet_wifi
from mininet.node import Controller
from mn_wifi.node import UserAP, Car, Station
from mn_wifi.link import wmediumd, ITSLink, mesh
from mn_wifi.wmediumdConnector import interference
from mn_wifi.vanet import vanet
from mn_wifi.sumo.runner import sumo

def file_transfer_topology():
    "Create a WiFi topology with vehicles, access points, and servers."
    net = Mininet_wifi(controller=Controller, accessPoint=UserAP, link=wmediumd, wmediumd_mode=interference)

    #### Add controllers ####
    c0 = net.addController('c0')

    kwargs = {'ssid': 'vanet-ssid', 'mode': 'g', 'passwd': '123456789a',
              'encrypt': 'wpa2', 'failMode': 'standalone', 'datapath': 'user', 'ieee80211r': 'yes'}
    aps = []
    positions = [(100, 450, 0), (500, 450, 0), (100, 150, 0), (500, 150, 0)]

    channels = ['1', '6', '11', '1', '6', '11']

    info('***Creating access Points...\n')
    for i in range(1, 5):
        ap = net.addAccessPoint(f'ap{i}', mac=f'00:00:00:11:00:0{i}', channel=channels[i-1],
                                position=positions[i-1],range = 300, **kwargs,mobility_domain = 'a1b2')
        aps.append(ap)

    info('***Creating Cars ...\n')
    cars = []
    for i in range(1, 6):
        car = net.addStation(f'car{i}', wlans=2, encrypt=['wpa2', ''],
                 bgscan_threshold=-60, s_interval=5, l_interval=10,bgscan_module = "simple")
        cars.append(car)

    info('***Adding a switch ...\n')
    switch = net.addSwitch("sw1",mac='00:00:00:00:00:80')

    info('***Adding a Server ...\n')
    server1 = net.addHost("server1",mac='00:00:00:00:01:01',ip='192.168.1.1/24')


    info('***Setting propagation model...\n')
    net.setPropagationModel(model='logDistance', exp=3.0)

    info('***Configuring nodes...\n')
    net.configureNodes() 

    net.addLink(switch,server1)

    for i in range(len(aps)-1):
        net.addLink(aps[i], aps[i+1])
        net.addLink(aps[i],switch)

    for car in cars:
        net.addLink(car, intf=car.params['wlan'][1], cls= mesh, ssid='meshV2V', channel='5')

    
    net.plotGraph(max_x=600, max_y=600)

    for i in range(5):
        cars[i].coord = ['0,0,0','0,0,0','0,0,0']

    net.setMobilityModel(time=0, model='RandomDirection', nodes=cars, max_x=600, max_y=600)
    net.startMobility(time=0, mob_rep=1, reverse=False)
    
    p = [{},{},{},{},{},{}]
    p[0] = {'position': '40,30,0'}
    p[1] = {'position': '40,30,0'}
    p[2] = {'position': '40,30,0'}
    p[3] = {'position': '40,30,0'}
    p[4] = {'position': '40,30,0'}
    p[5] = {'position': '500,500,00'}
    for i in range(5):
        net.mobility(cars[i],'start',time=i,**p[i])
        net.mobility(cars[i],'stop',time=20,**p[5])
    net.stopMobility(time=26)

    
    for i,ap in enumerate(aps,start=1):
        ap_ip = f'192.168.0.{i}/24'
        ap.setIP(ap_ip)
        ap.cmd(f'route add default gw 192.168.0.{i}/24')

    info('***Starting network...\n')
    net.useExternalProgram(program=sumo, port=8813,extra_params=["--start --delay 1000"],clients=1, exec_order=0) # config_file='map.sumocfg')

    net.build()
    c0.start()

    for ap in aps:
        ap.start([c0])
        


    for i,car in enumerate(cars,start=1):

        car.setIP(f'192.168.0.{int(cars.index(car)) + len(aps) + 1}/24', intf=f'{car}-wlan0')
        car.cmd(f'route add default gw 192.168.0.{len(aps)+ i}/24')

        # Setting another interface for V2V
        car.setIP(f'192.168.1.{int(cars.index(car)) + 1}/24', intf=f'{car}-mp1')

    info('***Running CLI\n')



    
    CLI(net)

    info('***Stopping network\n')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    file_transfer_topology()
