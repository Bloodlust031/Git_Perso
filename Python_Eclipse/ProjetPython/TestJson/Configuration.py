'''
Created on 26 nov. 2020

@author: blood
'''


to_integrate_Msg_bin = True
to_integrate_Msg_raw = True
to_integrate_Msg_cnt = True
to_integrate_Msg_decompose = True
to_integrate_Msg_non_decompose_D2Hub = True

Chemin_json = 'H:/Boulot/TempDownAWSS3'
#Chemin_json = 'H:/Boulot/Boulot Jeje/Main/Ican/Extract_traces_FTP/TempDownAWSS3'
#Chemin_json = 'H:/Boulot/Boulot Jeje/Main/Ican/Extract_traces_FTP/TempDownAWSS3_gros'
#Chemin_json = 'C:\TempDownAWSS3'
#Chemin_json = 'D:\Boulot\Main\Ican\Extract_traces_FTP\TempDownAWSS3'
#Chemin_json = 'D:\temp\DWLD msg Bastides'
Chemin_json = 'H:\Jeje\json_iCAN'

lbl_msg_Dic_Params_D2Hub_cnt = 'Msg_Params_decompose_D2Hub_cnt'  #decomposition du message en param�tre r�alis� par D2Hub - Sous forme de dictionnaire
lbl_msg_Dic_Params_D2Hub_raw = 'Msg_Params_decompose_D2Hub_raw'             #decomposition du message en param�tre r�alis� par D2Hub - Sous forme de texte
lbl_msg_Dic_Params_Python = 'Msg_Params_decompose_Python'
lbl_msg_Dic_Params_NonD2Hub = 'Msg_Params_non_decompose_D2Hub'

distribution_delais_GSM = [10, 60, 120, 180, 300, 600, 1200, 3600]    #Distribution des d�lais de r�ception en secondes
 
if __name__ == '__main__':
    pass