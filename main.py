import serial
import serial.tools.list_ports
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from sklearn.preprocessing import MinMaxScaler
import csv
import os

ports = serial.tools.list_ports.comports()
serialcomm = serial.Serial()
warna = ['Violet', 'Blue', 'Green', 'Yellow', 'Orange', 'Red']
portList = []

for eachport in ports:
    portList.append(str(eachport))
    print(str(eachport))

myport = input('Silahkan pilih angka port board anda!(contoh : 3)')
for x in range(0,len(portList)):
    if portList[x].startswith("COM" + str(myport)):
        portVar = "COM" + str(myport)
        print(portList[x])
        
serialcomm.baudrate = 115200
serialcomm.port = portVar
serialcomm.open()


filename = input('Silahkan masukkan nama file (contoh: myfile.csv): ')

def update(frame):
    if serialcomm.in_waiting:
        serial_monitor = serialcomm.readline()
        nilai = serial_monitor.decode('utf').rstrip('\n').rstrip('\r')
        converted_data = nilai.split(",")
        converted_data = [float(i) for i in converted_data]
        # scaler = MinMaxScaler()
        # converted_data = scaler.fit_transform([[x] for x in converted_data])
        # converted_data = [x[0] for x in converted_data]
        label = ['450nm','500nm','550nm','570nm','600nm','650nm']
        color = ['violet','blue','green','yellow','orange','red']

        try:
            print(converted_data)
            header = label = ['450nm','500nm','550nm','570nm','600nm','650nm']
            data_csv = converted_data
            file_exist = os.path.isfile(filename)
            with open(filename, 'a', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                if not file_exist:
                    csvwriter.writerow(header)
                csvwriter.writerow(data_csv)
            plt.clf()
            plt.bar(label, converted_data, color=color, width=0.6)
            plt.xlabel("Spektrum")
            plt.ylabel("Intensitas Cahaya (AU)")
            plt.title("Basic Reading AS7262")
            plt.tight_layout()
            plt.xticks(size=14)
            plt.yticks(size=14)
            plt.ylim(0, max(converted_data) * 1.1)
        except ValueError or IndexError :
            pass

ani = FuncAnimation(plt.gcf(), update, frames=np.arange(0, 10), repeat=True)
plt.tight_layout()
plt.pause(0.05)
plt.show()