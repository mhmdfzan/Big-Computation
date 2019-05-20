import socket  #import socket
from os import system #import system

host = '192.168.1.15' #inisiasi IP server
port = 12345 #inisiasi nilai Port

print('Target IP:', host)  #print nilai target IP server
print('Target port:', port) #print nilai target Port

c = socket.socket(type=socket.SOCK_DGRAM) #inisiasi socket untuk client

def requestFunction(a): #mendefinisikan fungsi request dengan inputan string(a)
    c.sendto(bytes(a, 'utf-8'), (host, port)) #mengirimkan data inputan client ke server
    c.settimeout(10) #melakukan set timeout untuk client dengan nilai 10 detik
    data = c.recvfrom(1024) #menyimpan data dari server ke dalam variable data
    print(str(data[0].decode())) #melakukan print variable data

def newInstance(): #mendefinisikan fungsi newInstance untuk server mengirimkan menu ke client
    c.sendto(bytes('New Instance', 'utf-8'), (host, port)) #mengirimkan data yang berupa new instance ke server
    data = c.recvfrom(1024) #menyimpan data dari server ke dalam variable data
    print(data[0].decode()) #melakukan print variable data

if __name__ == "__main__": 
    system('clear') #clearscreen yang berfungsi pada os linux
    a = '' #inisiasi variable a dengan nilai data berupa string kosong
    while True: #melakukan perulangan
        newInstance() #memanggil fungsi newInstance
        
        while True: #melakukan perulangan
            try: #error handling
                a = '' #inisiasi variable a dengan nilai data berupa string kosong
                a += str(int(input('Masukkan nomor operasi: '))) #variable ditambahkan dan direplace dengan inputan operasi
                if a == '0': #jika variable a sama dengan 0
                    c.close() #koneksi client ditutup
                    exit() #exit
                a += '|'+str(float(input('Masukkan angka pertama: '))) # nilai a ditambahkan dengan nilai inputan angka pertama + '|'
                a += '|'+str(float(input('Masukkan angka kedua: '))) #nilai a ditambahkan dengan nilai inputan angka kedua + '|'
                requestFunction(a) #memanggil fungsi requestFunction dengan inputan berupa variable a
                input('Press Enter to return...') #System menerima inputan dari client
                system('clear') #clearscreen yang berfungsi pada os linux
                break #stop secara paksa proses program
            except Exception as errors: #untuk menangkap error yang terjadi
                print(errors) #print error
        
