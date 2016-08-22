# -*- coding: utf-8 -*-
def sub_run(path,n):    #  n 记录每次切片的一组中包含的字符数
	f1=open(path,'rb')
	stxt=f1.read()
	stxt=str(stxt,'utf-8')
	f1.close()
	tmp_str={}
	for i in list(range(len(stxt)-1)):
		tmp_str[stxt[i:i+n]]=0
		
	for i in list(range(len(stxt)-1)):
		tmp_str[stxt[i:i+n]]+=1
	
	tmp_str=sorted(tmp_str.items(),key=lambda d:d[1],reverse = True)
	print('*****'+str(n)+'字符***************')
	print(tmp_str)
	print('*************************')

filepath='文本.txt'    #用于统计用的文本路径
sub_run(filepath,2)
sub_run(filepath,3)
sub_run(filepath,4)