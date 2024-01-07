
# Change to the directory where your Mininet-WiFi script is located
cd /home/wifi/mininet-wifi/examples
# Clean Mininet
sudo mn -c
# Clear the output
clear\
# Print a message indicating the start of the topology
echo "Starting the topology..." 
echo 'Keep calm, it takes time'
# Run the Mininet-WiFi script
sudo python3 project-3.0.py

# Wait for a moment to ensure Mininet-WiFi is ready
sleep 5

# Ping between cars
car1 ping -c 4 car2

# Start HTTP server on car2
car2 python3 -m http.server 80 &

# Create a test file on car2
car2 sh -c 'echo "hello, this is a test file" > test_file.txt'

# Download the test file from car1
car1 wget -O - http://192.168.0.6/test_file.txt