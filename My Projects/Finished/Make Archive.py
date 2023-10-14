"""
Created on Tue 15 Sep 10:40 2020
Finished on ue 15 Sep 10:50 2020
@author: Cpt.Ender

Make a .zip file of all the Python packages
for safe keeping
                                             """
import shutil

root_drctr = 'C:\\Users\\plabc\\AppData\\Roaming\\Python\\'
dst_drctr = 'D:\\plabc\\Desktop\\packages'

shutil.make_archive(dst_drctr, 'zip', root_dir=root_drctr)
