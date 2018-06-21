from argparse import ArgumentParser
from prettytable import PrettyTable
from datetime import datetime, timedelta

parser = ArgumentParser(description="Auth log parser")
parser.add_argument("filename", help="Log file path")
parser.add_argument("-u",help="Summary failed login log and sort log by user .", action="store_true")
parser.add_argument("-after",help="Filter log after date. format YYYY-MM-DD-HH:MM:SS")
parser.add_argument("-before",help="Filter log before date. format YYYY-MM-DD-HH:MM:SS")
parser.add_argument("-n",help="Show only the user of most N-th times")
parser.add_argument("-t",help="Show only the user of attacking equal or more than T times")
parser.add_argument("-r",help="Sort in reverse order", action="store_true")
args = parser.parse_args()

file = open(args.filename,'r')
matrix=[]
x=0
no=0
n1=0

#n
if args.n :
	N=args.n
else:
	N=-1
	
#-after
if args.after :
	af=args.after
	for line in file:
		if(n1==int(N)):
			break
		l=[]
		l=line.split()
		if(len(l[0])==4):
			str=l[0]+'-'+l[1]+'-'+l[2]+'-'+l[3]
		else :
			str='2018-'+l[0]+'-'+l[1]+'-'+l[2]
		after = datetime.strptime(af, '%Y-%m-%d-%H:%M:%S')
		str = datetime.strptime(str, '%Y-%b-%d-%H:%M:%S')
		#before
		if args.before :
			bf=args.before
			before = datetime.strptime(bf, '%Y-%m-%d-%H:%M:%S')
			if(str-after>timedelta(0) and before-str>timedelta(0)) :
				for i in range(len(l)):
					if(l[i]=='Invalid'):
						n1+=1
						usr=l[i+2]
						check=0
						
						#check duplicate
						for j in range(x):
							if(matrix[j][0]==usr):
								matrix[j][1]+=1
								check=1
								
						if(check==0):
							matrix.append([])
							matrix[x].append(usr)
							matrix[x].append(1)
							x+=1
						break
		else :
			if(str-after>timedelta(0)) :
				for i in range(len(l)):
					if(l[i]=='Invalid'):
						usr=l[i+2]
						check=0
						
						#check duplicate
						for j in range(x):
							if(matrix[j][0]==usr):
								matrix[j][1]+=1
								check=1
								
						if(check==0):
							matrix.append([])
							matrix[x].append(usr)
							matrix[x].append(1)
							x+=1
						break

#-before
elif args.before :
	bf=args.before
	for line in file:
		if(n1==int(N)):
			break
		l=[]
		l=line.split()
		if(len(l[0])==4):
			str=l[0]+'-'+l[1]+'-'+l[2]+'-'+l[3]
		else :
			str='2018-'+l[0]+'-'+l[1]+'-'+l[2]
		before = datetime.strptime(bf, '%Y-%m-%d-%H:%M:%S')
		str = datetime.strptime(str, '%Y-%b-%d-%H:%M:%S')
		if(before-str>timedelta(0)) :
			for i in range(len(l)):
				if(l[i]=='Invalid'):
					n1+=1
					usr=l[i+2]
					check=0
					
					#check duplicate
					for j in range(x):
						if(matrix[j][0]==usr):
							matrix[j][1]+=1
							check=1
							
					if(check==0):
						matrix.append([])
						matrix[x].append(usr)
						matrix[x].append(1)
						x+=1
					break

else :
	for line in file:
		if(n1==int(N)):
			break
		l=[]
		l=line.split()
		for i in range(len(l)):
			if(l[i]=='Invalid'):
				n1+=1
				usr=l[i+2]
				check=0
				
				#check duplicate
				for j in range(x):
					if(matrix[j][0]==usr):
						matrix[j][1]+=1
						check=1
						
				if(check==0):
					matrix.append([])
					matrix[x].append(usr)
					matrix[x].append(1)
					x+=1
				break

#sort
for element in matrix:
	element.reverse()
matrix.sort()
matrix.reverse()	
for element in matrix:
	element.reverse()
	
#-u
if args.u :
	matrix.sort()
	
#-r
if args.r :
	for element in matrix:
		element.reverse()
	matrix.sort()	
	for element in matrix:
		element.reverse()
		
"""
if args.n :
	for element in matrix:
		element.reverse()
	matrix.sort()	
	for element in matrix:
		element.reverse()
			
	N=args.n
	table=PrettyTable()
	table.field_names = ["user","count"]
	for j in range(x):
		if(matrix[j][1]<=int(N)):
			table.add_row(matrix[j])
	print(table)
	no=1
"""		
#-t
if args.t :
	for element in matrix:
		element.reverse()
	matrix.sort()	
	matrix.reverse()
	for element in matrix:
		element.reverse()
			
	T=args.t
	table=PrettyTable()
	table.field_names = ["user","count"]
	for j in range(x):
		if(matrix[j][1]>=int(T)):
			table.add_row(matrix[j])
	print(table)
	no=1


#table
if (no==0) :
	table=PrettyTable()
	table.field_names = ["user","count"]
	for element in matrix:
		table.add_row(element)
	print(table)

