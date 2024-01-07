import random
from mn_wifi.cli import CLI
from mininet.log import setLogLevel, info
from mn_wifi.net import Mininet_wifi
from mininet.node import Controller
from mn_wifi.node import UserAP, Car
from mn_wifi.link import *

def file_transfer_topology():
    "Create a WiFi topology with vehicles, access points, and servers."
    net = Mininet_wifi(controller=Controller, accessPoint=UserAP, link=wmediumd)

    # Add controllers
    info('Adding Controller....\n')
    c0 = net.addController('c0')

    kwargs = {'ssid': 'vanet-ssid', 'controller': 'c0', 'mode': 'g', 'passwd': '123456789a', 'range': '200',
              'power': '33', 'mobility_domain': 'a1b2', 'encrypt': 'wpa2', 'failMode': 'standalone',
              'datapath': 'user', 'ieee80211w':'None','ieee80211r':'yes'}

    aps = []
    positions = [(100, 450, 0), (450, 450, 0), (100, 100, 0), (450, 100, 0)]

    channels = ['1', '6', '11', '1', '6', '11']

    info('***Creating access Points...\n')
    aps.append(net.addAccessPoint('ap1',wlans=2, mac='00:00:00:11:00:01', channel=channels[0], position=positions[0], **kwargs))
    aps.append(net.addAccessPoint('ap2',wlans=2, mac='00:00:00:11:00:02', channel=channels[1], position=positions[1], **kwargs))
    aps.append(net.addAccessPoint('ap3',wlans=2, mac='00:00:00:11:00:03', channel=channels[2], position=positions[2], **kwargs))
    aps.append(net.addAccessPoint('ap4',wlans=2, mac='00:00:00:11:00:04', channel=channels[3], position=positions[3], **kwargs))

    info('***Creating Cars ...\n')
    cars = []
    ckwargs = {'bgscan_threshold': '-60','controller': 'c0', 'encrypt': 'wpa2', 's_interval': '5', 'l_interval': '10',
               'bscan_module': 'simple'}
    cars.append(net.addCar('car1', mac='00:00:00:11:00:05', wlans=2, position='10,20,0', **ckwargs))
    cars.append(net.addCar('car2', mac='00:00:00:11:00:06', wlans=2, position='20,20,0', **ckwargs))
    cars.append(net.addCar('car3', mac='00:00:00:11:00:07', wlans=2, position='30,20,0', **ckwargs))
    cars.append(net.addCar('car4', mac='00:00:00:11:00:08', wlans=2, position='40,20,0', **ckwargs))
    cars.append(net.addCar('car5', mac='00:00:00:11:00:09', wlans=2, position='50,20,0', **ckwargs))
    cars.append(net.addCar('car6', mac='00:00:00:11:00:25', wlans=2, position='450,90,0', **ckwargs))
    cars.append(net.addCar('car7', mac='00:00:00:11:00:26', wlans=2, position='90,90,0', **ckwargs))

    #info('***Adding a switch ...\n')
    switch = net.addSwitch("sw1", mac='00:00:00:00:00:80', controller=c0,ip='192.168.1.11/24')

    # Add a server and start HTTP server on port 80
    info('***Adding a Server ...\n')
    server1 = net.addHost("server1", mac='00:00:00:11:00:10', ip='192.168.1.20/24', encrypt='wpa2')
    server2 = net.addHost("server2", mac='00:00:00:11:00:11', ip='192.168.1.21/24', encrypt='wpa2')


    info('***Setting propagation model...\n')
    net.setPropagationModel(model='logDistance', exp=4.0)

    info('***Configuring nodes...\n')
    net.configureNodes()

    net.addLink(switch,server1)
    net.addLink(switch,server2)

    for i in range(len(aps)-1):
        net.addLink(aps[i], aps[i+1])
        net.addLink(aps[i],switch)
    


    #for i, ap in enumerate(aps, start=1):
        #net.addLink(ap,intf = f'ap{i}-wlan2', cls=wmediumd, ssid='wmediumd-ssid')



    #net.addLink(aps[i], switch)
        #net.addLink(aps[i], aps[i + 1])


    
    net.plotGraph(max_x=600, max_y=600)

    net.setMobilityModel(time=0, model='RandomDirection', nodes=cars, max_x=600, max_y=600)
    net.startMobility(time=0, mob_rep=1, reverse=False,ac_method='ssf')

    p = [{}, {}, {}, {}, {}, {}]
    p[0] = {'position': '40,30,0'}
    p[1] = {'position': '40,30,0'}
    p[2] = {'position': '40,30,0'}
    p[3] = {'position': '40,30,0'}
    p[4] = {'position': '40,30,0'}
    p[5] = {'position': '500,500,00'}
    for i in range(5):
        net.mobility(cars[i], 'start', time=i, **p[i])
        net.mobility(cars[i], 'stop', time=(20 + int(i)), **p[5])
    net.stopMobility(time=26)

    for car in cars:
        net.addLink(car, intf= car.wintfs[0].name, cls=mesh, channel=6)
        net.addLink(car, intf= car.wintfs[1].name, cls=adhoc,channel=11)


    info('***Starting network...\n')

    net.build()
    c0.start()
    #switch.start([c0])
    for ap in aps:
        ap.start([c0])

    #for i, ap in enumerate(aps, start=1):
     #   ap_ip = f'192.168.1.{i + 10}/24'
      #  ap.setIP(ap_ip, intf=f'ap{i}-wlan2')
       # ap.cmd(f'route add -net 192.168.0.0/24 dev {ap}-wlan2')

    for i, car in enumerate(cars, start=1):
        car_ip_wlan0= f'192.168.0.{i + len(aps)}/24'
        car.setIP(car_ip_wlan0,intf = car.params['wlan'][0])
        car.cmd(f'route add -net 192.168.0.0/24 dev {car}-wlan0')
        car.cmd(f'route add default gw 192.168.0{len(aps)+ i}/24')
        
        car_ip_wlan1 = f'192.168.1.{i + 10 + len(aps)}/24'
        car.setIP(car_ip_wlan1, intf=car.params['wlan'][1])
        car.cmd(f'route add -net 192.168.1.0/24 dev {car}-wlan1')
        car.cmd(f'route add default gw 192.168.1{len(aps)+ i+10}/24')
        



    
    CLI(net)
    info('***Stopping network\n')
    net.stop()



if __name__ == '__main__':
    setLogLevel('info')
    file_transfer_topology()
