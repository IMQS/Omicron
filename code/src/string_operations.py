'''	Adds two strings 
	Takes 2 parameters a, b both strings '''
def string_concatination(a,b):
	if(type(a) != str):
		return
	if(type(b) != str):
		return
	return a+b
'''	Adds a string and a int at the end
	Takes 2 parameters a, String and b, integer'''
def string_int_concatination(a,b):
	if(type(a) != str):
		return
	if(type(b) != int):
		return 
	return a+str(b)
