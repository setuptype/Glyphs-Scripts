#MenuTitle: Kernpolate
# -*- coding: utf-8 -*-

__doc__="""
Calculates and applies kerning to all masters based on the kerning in the boldest weight. The script uses glyph widths and masters weight values for calculations.

Only works if actual glyph names are used to name groups.
"""

import math
font = Glyphs.font

def getWidth(g, id):
	g = getName(g)
	if g:
		return font.glyphs[g].layers[id].width
	else:
		return 0

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

for master in font.masters:
	if master.id != Master.id:
		print master.name + ' Exceptions:'
		print ''
		for L in Kerning:
			for R in Kerning[L]:
				Width = getWidth(L, Master.id) + getWidth(R, Master.id)
				width = getWidth(L, master.id) + getWidth(R, master.id)
				multiplier = (width / Width + master.weightValue / Master.weightValue)/2
								
				kerning = math.floor(Kerning[L][R] * multiplier)
				try:
					current = font.kerning[master.id][L][R]
				except KeyError:
					current = None
					pass
				if current != kerning and current != None:
					print '/' + getName(L) + '/' + getName(R)
				if current == None:	
					font.setKerningForPair(master.id, getKernName(L), getKernName(R), kerning)

		print ''

Glyphs.clearLog()