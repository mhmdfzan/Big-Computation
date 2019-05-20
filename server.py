import socket
import threading, multiprocessing
import signal,time
from functools import partial

host = ''
port = 12345
s = socket.socket(type=socket.SOCK_DGRAM)
s.bind((host, port))

def tambah(a,b, address):
    reply('Hasil penjumlahan '+str(a)+' dengan '+str(b)+' adalah '+str(a+b)+'\n', address)

def kurang(a,b, address):
    reply('Hasil pengurangan '+str(a)+' dengan '+str(b)+' adalah '+str(a-b)+'\n', address)

def kali(a,b, address):
    reply('Hasil perkalian '+str(a)+' dengan '+str(b)+' adalah '+str(a*b)+'\n', address)

def bagi(a,b, address):
    reply('Hasil pembagian '+str(a)+' dengan '+str(b)+' adalah '+str(a/b)+'\n', address)

def FPB(a, b, address):
    a = int(a)
    b = int(b) 
    if a > b: 
        small = b 
    else:
        small = a 
    for i in range(1, small+1): 
        if((a % i == 0) and (b % i == 0)): 
            gcd = i 
    reply('FPB dari '+str(a)+' dan '+str(b)+' adalah '+str(gcd)+'\n', address)

def KPK(a,b, address):
    
    try:
        finished = False
        i = 0
        while not finished:
            x = 1
            y = 1
            p = a*x
            q = b*y
            while(p!=q):
                while(p>q):
                    y += 1
                    q = b * y
                while(p<q):
                    x += 1
                    p = a*x
            if(p==q):
                reply('KPK dari '+str(a)+' dan '+str(b)+' adalah '+str(p)+'\n', address)
                finished = True
    except Exception as errors:
        print(errors)

# ---------------- fitur yang ditambahkan --------------------
def faktorial(n):
    if n == 0: #jika nilai sama dengan 0
        return 1 #maka akan mengembalikan hasil dengan nilai 1
    else: #jika lebih dari 0
        return n * faktorial(n-1) #maka akan melakukan pemanggilan fungsi rekursif dari faktorial

def Permutasi(a, b, address):
    a1 = int(a); b1 = int(b) #untuk menjadikan nilai float menjadi integer
    R1 = 'Error!, Kedua angka harus lebih dari 0. Silahkan ulangi kembali' #membuat notifikasi pertama
    R2 = 'Error!, Angka pertama harus lebih besar atau sama dengan angka kedua. Silahkan ulangi kembali' #membuat notifikasi kedua
    if(a1==0 or b1==0): #jika kedua nilai bernilai 0
        reply(R1, address) #mengirimkan notifikasi pertama ke client
    elif a1<b1: #jika pembilang lebih kecil dari penyebut
        reply(R2, address) #mengirimkan notifikasi kedua ke client
    else:
        pembilang = faktorial(a1) #mencari nilai pembilang
        penyebut = faktorial(a1-b1) #mencari nilai penyebut
        reply('Hasil kombinasi dari '+str(a1)+' dan '+str(b1)+' adalah '+str(pembilang/penyebut)+'\n', address) #mengirimkan hasil kombinasi ke client

# ---------------- akhir fitur yang ditambahkan --------------------

def switch(a, address):
    # fungsi untuk mengecek fungsi mana yang akan dipanggil
    if a[0] == '1':
        tambah(a[1], a[2], address)
    elif a[0] == '2':
        kurang(a[1], a[2], address)
    elif a[0] == '3':
        kali(a[1], a[2], address)
    elif a[0] == '4':
        bagi(a[1], a[2], address)
    elif a[0] == '5':
        FPB(a[1], a[2], address)
    elif a[0] == '6':
        KPK(a[1], a[2], address)
    elif a[0] == '7':
        Permutasi(a[1], a[2], address)
    else:
        # mengembalikan pesan error kepada user
        reply('Error: Operasi nomor - '+str(a[0])+' tidak ditemukan.\n ', address)
    
def reply(result, address):
    # fungsi untuk mengembalikan data kepada client yang meminta request
    s.sendto(bytes(result,"utf-8"), (address[0], address[1]))
    print('Replying:', result)

if __name__ == "__main__":
    pass
    menu = "1. Tambah \n2. Pengurangan \n3. Perkalian \n4. Pembagian \n5. FPB \n6. KPK \n7. Permutasi \n0. Exit\n"
    process = {}
    while True:
        # menunggu data dari client
        data, addr = s.recvfrom(1024)
        print ("Request from -",addr[0],'on port',addr[1],' : ', data.decode())
        
        # jika data yang data yang dikirim adalah 'New Instance', kirim list menu ke client
        if(data.decode()=="New Instance"):
            s.sendto(bytes(menu,"utf-8"), (addr[0], addr[1]))
        else:
            # parsing data dari user, misal: 1|2|3, menjadi angka[0] = 1, angka[1] = 2, angka[3] = 3
            angka = data.decode().split("|")
            a = float(angka[1])
            b = float(angka[2])

            # membuat instance thread baru, menargetkan fungsi switch() untuk menentukan fungsi operasional mana yang akan di prosses
            # dengan argumen (array[], address), dimana array[] berisi: [nomor operasi, angka pertama, angka kedua], dan addr adalah
            # [ipAddress, port]
            process[str(addr[0])+'|'+str(addr[1])] = threading.Thread(target=switch, args=([str(angka[0]), a, b], addr, ))

            # memulai instance tersebut tanpa menunggu prosesnya sampai selesai
            process[str(addr[0])+'|'+str(addr[1])].start()
            
