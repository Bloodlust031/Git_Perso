'''
Created on 26 nov. 2020

@author: blood
'''


to_integrate_Msg_bin = False
to_integrate_Msg_raw = False
to_integrate_Msg_cnt = False
to_integrate_Msg_decompose = False
to_integrate_Msg_non_decompose_D2Hub = False

Chemin_json = 'H:/Boulot/TempDownAWSS3'
#Chemin_json = 'H:/Boulot/Boulot Jeje/Main/Ican/Extract_traces_FTP/TempDownAWSS3'
#Chemin_json = 'H:/Boulot/Boulot Jeje/Main/Ican/Extract_traces_FTP/TempDownAWSS3_gros'
#Chemin_json = 'C:\TempDownAWSS3'
#Chemin_json = 'D:\Boulot\Main\Ican\Extract_traces_FTP\TempDownAWSS3'
#Chemin_json = 'D:\temp\DWLD msg Bastides'


lbl_msg_Dic_Params_D2Hub_cnt = 'Msg_Params_decompose_D2Hub_cnt'  #decomposition du message en paramètre réalisé par D2Hub - Sous forme de dictionnaire
lbl_msg_Dic_Params_D2Hub_raw = 'Msg_Params_decompose_D2Hub_raw'             #decomposition du message en paramètre réalisé par D2Hub - Sous forme de texte
lbl_msg_Dic_Params_Python = 'Msg_Params_decompose_Python'
lbl_msg_Dic_Params_NonD2Hub = 'Msg_Params_non_decompose_D2Hub'

distribution_delais_GSM = [10, 60, 120, 180, 300, 600, 1200, 3600]    #Distribution des délais de réception en secondes
 
if __name__ == '__main__':
    pass