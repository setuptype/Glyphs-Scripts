#MenuTitle: Kernpolate
# -*- coding: utf-8 -*-

__doc__="""
Adjusts and applies kerning from the boldest master to lighter masters.

If kerning for a given pair already exists in a lighter master, the script skips it and lists the pair.

Only works if actual glyph names are used to name groups.
"""

Glyphs.clearLog()

import math
font = Glyphs.font

def getWidth(g, id):
	g = getName(g)
	try:
		return font.glyphs[g].layers[id].width
	except:
		return None

def getName(g):
	if g[0] == '@':
		return g[7:]
	else:
		return font.glyphForId_(g).name
		
def getKernName(g):
	if g[0] == '@':
		return g
	else:
		return font.glyphForId_(g).name

heaviest = 0
for master in font.masters:
	if master.weightValue > heaviest:
		heaviest = master.weightValue
		Master = master
		
Kerning = font.kerning[Master.id]

output = ''
missing = []

for master in font.masters:
	if master.id != Master.id:
		output += master.name + ' Exceptions:\n\n'
		for L in Kerning:
			if getWidth(L, Master.id):
				for R in Kerning[L]:
					if getWidth(R, Master.id):
						Width = getWidth(L, Master.id) + getWidth(R, Master.id)
						width = getWidth(L, master.id) + getWidth(R, master.id)
						multiplier = (width / Width + master.weightValue / Master.weightValue)/2
										
						kerning = math.floor(Kerning[L][R] * multiplier)
						try:
							current = font.kerning[master.id][L][R]
						except:
							current = None
						if current != kerning and current != None:
							output += '/' + getName(L) + '/' + getName(R) + '\n'
						if current == None:	
							font.setKerningForPair(master.id, getKernName(L), getKernName(R), kerning)
					else:
						if R not in missing:
							missing.append(getName(R))
			else:
				if L not in missing:
					missing.append(getName(L))
		
print output

if len(missing):
	print '\nKerning groups using non-existent glyph names:\n'
	for i in missing:
		print i + '\n'