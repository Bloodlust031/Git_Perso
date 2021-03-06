# -*-coding:Latin-1 -*

'''
Created on 25 nov. 2020

@author: blood
'''

import datetime
from datetime import date
from datetime import timedelta
from datetime import datetime
import time

def print_temps(fonction_a_executer):
    """Notre d�corateur. C'est lui qui est appel� directement LORS
    DE LA DEFINITION de notre fonction (fonction_a_executer)"""
    
    def fonction_modifiee():
        """Fonction renvoy�e par notre d�corateur. Elle se charge
        de calculer le temps mis par la fonction � s'ex�cuter"""
        
        tps_avant = time.time() # Avant d'ex�cuter la fonction
        valeur_renvoyee = fonction_a_executer() # On ex�cute la fonction
        tps_apres = time.time()
        tps_execution = tps_apres - tps_avant
        print("La fonction {0} a mis {1} pour s'ex�cuter".format( \
                fonction_a_executer, tps_execution))
        return valeur_renvoyee
    return fonction_modifiee

def convert_Hex_decimal(str_raw, bigEndian = False):
    if (bigEndian):
        #if faut retourner la chaine de caract�re
        i = len(str_raw)-2
        st_nombre_input =''
        while (i>=0):
            st_temp = str_raw[i:i+2]
            st_nombre_input = st_nombre_input + st_temp
            i = i - 2
    else:
        st_nombre_input = str_raw

    nombre = int(st_nombre_input,16)
    #print("convert_Hex_decimal " + st_nombre_input + " " + nombre)
    return nombre


def calc_CRC(data):
    #Calcul de CRC16-Modbus 
    crc_table=[0x0000,0xC0C1,0xC181,0x0140,0xC301,0x03C0,0x0280,0xC241,0xC601,0x06C0,0x0780,0xC741,0x0500,0xC5C1,0xC481,0x0440,0xCC01,0x0CC0,0x0D80,0xCD41,0x0F00,0xCFC1,0xCE81,0x0E40,0x0A00,0xCAC1,0xCB81,0x0B40,0xC901,0x09C0,0x0880,0xC841,0xD801,0x18C0,0x1980,0xD941,0x1B00,0xDBC1,0xDA81,0x1A40,0x1E00,0xDEC1,0xDF81,0x1F40,0xDD01,0x1DC0,0x1C80,0xDC41,0x1400,0xD4C1,0xD581,0x1540,0xD701,0x17C0,0x1680,0xD641,0xD201,0x12C0,0x1380,0xD341,0x1100,0xD1C1,0xD081,0x1040,0xF001,0x30C0,0x3180,0xF141,0x3300,0xF3C1,0xF281,0x3240,0x3600,0xF6C1,0xF781,0x3740,0xF501,0x35C0,0x3480,0xF441,0x3C00,0xFCC1,0xFD81,0x3D40,0xFF01,0x3FC0,0x3E80,0xFE41,0xFA01,0x3AC0,0x3B80,0xFB41,0x3900,0xF9C1,0xF881,0x3840,0x2800,0xE8C1,0xE981,0x2940,0xEB01,0x2BC0,0x2A80,0xEA41,0xEE01,0x2EC0,0x2F80,0xEF41,0x2D00,0xEDC1,0xEC81,0x2C40,0xE401,0x24C0,0x2580,0xE541,0x2700,0xE7C1,0xE681,0x2640,0x2200,0xE2C1,0xE381,0x2340,0xE101,0x21C0,0x2080,0xE041,0xA001,0x60C0,0x6180,0xA141,0x6300,0xA3C1,0xA281,0x6240,0x6600,0xA6C1,0xA781,0x6740,0xA501,0x65C0,0x6480,0xA441,0x6C00,0xACC1,0xAD81,0x6D40,0xAF01,0x6FC0,0x6E80,0xAE41,0xAA01,0x6AC0,0x6B80,0xAB41,0x6900,0xA9C1,0xA881,0x6840,0x7800,0xB8C1,0xB981,0x7940,0xBB01,0x7BC0,0x7A80,0xBA41,0xBE01,0x7EC0,0x7F80,0xBF41,0x7D00,0xBDC1,0xBC81,0x7C40,0xB401,0x74C0,0x7580,0xB541,0x7700,0xB7C1,0xB681,0x7640,0x7200,0xB2C1,0xB381,0x7340,0xB101,0x71C0,0x7080,0xB041,0x5000,0x90C1,0x9181,0x5140,0x9301,0x53C0,0x5280,0x9241,0x9601,0x56C0,0x5780,0x9741,0x5500,0x95C1,0x9481,0x5440,0x9C01,0x5CC0,0x5D80,0x9D41,0x5F00,0x9FC1,0x9E81,0x5E40,0x5A00,0x9AC1,0x9B81,0x5B40,0x9901,0x59C0,0x5880,0x9841,0x8801,0x48C0,0x4980,0x8941,0x4B00,0x8BC1,0x8A81,0x4A40,0x4E00,0x8EC1,0x8F81,0x4F40,0x8D01,0x4DC0,0x4C80,0x8C41,0x4400,0x84C1,0x8581,0x4540,0x8701,0x47C0,0x4680,0x8641,0x8201,0x42C0,0x4380,0x8341,0x4100,0x81C1,0x8081,0x4040] 

    crc_hi=0xFF 
    crc_lo=0xFF
     
    str_temp = data
    while len(str_temp) >=2:
        w = int(str_temp[0:2],16)
        index=crc_lo^w 
        crc_val=crc_table[index] 
        crc_temp=int(crc_val/256) 
        crc_val_low=int(crc_val-(crc_temp*256)) 
        crc_lo=crc_val_low ^ crc_hi 
        crc_hi=crc_temp
        str_temp = str_temp[2:]
    crc=crc_hi*256 +crc_lo
    return crc


def is_date_recent(st_date):
    
    #"2021-02-26T13:11:17.683Z"
    #"2021-02-26T13:10:00.236+0000"
    #print("input: " + st_date)
    if type(st_date) == str:
        if len(st_date) == 20:
            date_old = datetime.strptime(st_date,'%Y-%m-%dT%H:%M:%S%z')
        else: 
            if (st_date[-5:] == "+0000"):
                st_date2 = st_date[:-5] + "Z"
            else:
                st_date2 = st_date
            date_old = datetime.strptime(st_date2,'%Y-%m-%dT%H:%M:%S.%f%z')

        today = date.today()
        ecart = today-date_old.date()
        if (ecart > timedelta(days=15)):
            return False
        else:
            return True
    else:
        return False

if __name__ == '__main__':
    
#    convert_Hex_decimal('8C010000', True)
#   convert_Hex_decimal('8C010000')

    crc = calc_CRC('0000000014000B10060D02F5000000990018000F003836343530343033313530343834346C001600060010000B00140064001600060006000D0002000F0018001100565237454359485A524B4A3836383532359D00040001000165001F0008007720C51354EF454066001F000800B35E0CE5447BF43F680002000400000000006700020004000000000069001F0008003333333333236140AB4E1F000800000000000000F03F6A001F00080000000000000000006B001F000800000000000000F03FFF7F040001006413000200040071F3DE007C4E0300020000007D4E030002000100FF2A0400010001FA4E020004000219B25F')
    print(crc)#normalement "31997" (en d�cimal)
    
    is_date_recent("2018-05-09T08:31:55Z")
    is_date_recent("2019-09-10T07:00:57.600Z")
    is_date_recent("2021-02-26T13:10:00.236+0000")
    is_date_recent("2021-02-26T15:27:59.347Z")
    is_date_recent("2020-05-19T12:22:56.053Z")
    is_date_recent("2021-02-26T15:26:21.500+0000")
    
    
    pass