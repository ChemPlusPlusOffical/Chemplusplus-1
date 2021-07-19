'''

This is the backend for my chemistry helper
'''
import string

import re

def add_space(s):
	temp = re.sub('([A-Z])', r' \1', s)
				
	return temp

ELECTRON_CONFIG = dict()
LEVELS = {'1':1, '2':8, '3':8, '4':16, '5':16, '6':16}
S, P, D= 2, 6, 10
LETTERS = {'s':2, 'p':6, 'd':10}

import json 
table = dict()
temp2 = json.load(open("ptable.json", 'r'))['Table']['Columns']['Column']
print(temp2, type(temp2))
for i in range(len(temp2)):
	temp2[i] = add_space(temp2[i])
temp = json.load(open("ptable.json", "r"))["Table"]["Row"]
print(type(temp[0]))
for i in temp:
	table[i['Cell'][2]] = i['Cell']
	ELECTRON_CONFIG[i['Cell'][1]] = i['Cell'][5]
print(table)

class ec:
	def __init__(self, ec):
		temp = ec.split(ec[1])
		self.e = int(temp[1])
		self.level = int(temp[0])
		self.letter = ec[1]

class element:
	def __init__(self, name, ecs, br):
		self.ec = ecs
		self.br = br
		self.name = name



def sub_bohr_config(x):
	for i in ELECTRON_CONFIG:
		if i == x:
			t = ELECTRON_CONFIG[x]
			t = t.split(' ')

			#recursion
			for i in t:
				if i[0] == '[':
					
					for e in (sub_bohr_config(i.split(']')[0][1:])):
						t.append(e)
					r = i[4:]
					t.remove(i)
					t.append(r)

			return t




def config(x):
	name = x
	for i in ELECTRON_CONFIG:
		if i == x:
			x = ELECTRON_CONFIG[i]
			break

	prev = ''
	if x[0] == '[':
		x = x.split(']')
		prev = x[0][1:]
		
		x = x[1:][0]
		for i in ELECTRON_CONFIG:
			if i == prev:
				x+= ' '+ELECTRON_CONFIG[i]
	x = x.split(" ")
	for i in x:
		if i[0] == '(':
			x.remove(i)

	for i in x:
		if i[0] == '[':
			for e in sub_bohr_config(i.split(']')[0][1:]):
				x.append(e)
			t = i[4:]
			x.remove(i)
			x.append(t)
	br = 0
	for i in x:
		if int(i[0]) > br:
			br = int(i[0])

	x = element(name, x, br)
	return x 
