# Name 		: Kuldeep Singh Bhandari
# Roll No.  : 111601009
# Aim       : To find the number of words in a given file
# Idea     : Initialise begin to be False. Loop through each character in the
            # the file and as you find a character which is not ' ' or '\n' ,
            # set begin True, then keep it true until you find something ' ' or 
            # '\n', then set begin False, and increment c which is number of
            # words in the file.

f = open("test.txt", "r")
begin = False
c = 0
while(True) :
	x = f.read(1)
	if(x == '') :
		break
	if(not begin and x != '\n' and x != ' ') :
		begin = True
	if(begin and (x == ' ' or x == '\n')) :	
		c += 1
		begin = False

print((c+1) if begin else c)