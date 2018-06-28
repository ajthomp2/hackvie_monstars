import time
import smbus
import numpy as np
import sys
import os

bus = smbus.SMBus(1)

def write(val):
  bus.write_byte_data(addr, 0x40, int(val))

def read():
  try:
    bus.write_byte(addr, 0x40)
    bus.read_byte(addr)
  except Exception as e:
    print e
  return bus.read_byte(addr)

if __name__ == "__main__":
  global addr
  addr = 0x48

  results = []
  times = []
  rounds = 2800
  count = 0

  try:
    start = time.time()
    while count < rounds:
      value = read()
      print(value)
      results.append(value)
      now = time.time()
      times.append(now)
      count = count + 1
    
    end = time.time()
    times2 = times[:]
    for i in range(1, rounds - 1):
      times[i] = times[i] - times2[i - 1]
    times[0] = times[0] - start
    times[-1] = end - times[-1]
    avg = np.mean(times)
    print(avg)
    results = [avg] + results
    if len(sys.argv) == 2:
      filename = sys.argv[1]
      with open("num.txt", "r+") as f:
        num = int(f.read().strip())
        np.save(filename + str(num), results)
        os.system("scp -i hackvie_pswrd.txt " + filename + str(num) + ".npy ec2-user@18.191.114.207:~/hackvie/data/raw/" + filename)
        os.system("rm " + filename + str(num)+ ".npy")
        os.system("ssh -i hackvie_pswrd.txt ec2-user@18.191.114.207 sudo python /home/ec2-user/hackvie/preprocess.py")
        f.seek(0)
        newnum = str(num + 1)
        f.write(newnum)
        f.truncate()
  except KeyboardInterrupt:
    write(0)
    
  

