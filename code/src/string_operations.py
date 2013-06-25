'''
Created on 18 Jun 2013

@author: J. J. Martin
'''

def string_concatination(a,b):
	'''	Adds two strings 
	Takes 2 parameters a, b both strings '''
	if(type(a) != str):
		return
	if(type(b) != str):
		return
	return a+b

def string_int_concatination(a,b):
	'''	Adds a string and a int at the end
	Takes 2 parameters a, String and b, integer'''
	if(type(a) != str):
		return
	if(type(b) != int):
		return 
	return a+str(b)
