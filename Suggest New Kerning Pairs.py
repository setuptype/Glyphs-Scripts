#MenuTitle: Kerning: Suggest New Pairs
# -*- coding: utf-8 -*-

__doc__="""
Lists all combinations of selection’s kerning groups with all existing kerning groups.
Only works if actual glyph names are used for kerning groups.
"""

Glyphs.clearLog()

def context(g):
	return 'HN' if g[0].isupper() else 'nu'
def getName(g):
	if g[0] == '@':
		return g[7:]
	else:
		return font.glyphForId_(g).name

font = Glyphs.font
left = []
right = []
selLeft = []
selRight = []
existing = []
skip	= []
output	= ''

# get kerning groups from all glyphs

for glyph in font.glyphs:
	L = glyph.rightKerningGroup
	if L != None and not (L in left):
		left.append(L)
	R = glyph.leftKerningGroup
	if R != None and not (R in right):
		right.append(R)

# get kerning groups from selection

for glyph in font.selection:
	L = glyph.rightKerningGroup
	if L != None and not (L in selLeft):
		selLeft.append(L)
	R = glyph.leftKerningGroup
	if R != None and not (R in selRight):
		selRight.append(R)

# get existing kerning pairs

kerning	= font.kerning[font.selectedFontMaster.id]
for L in kerning:
	for R in kerning[L]:
		l = getName(L)
		r = getName(R)
		existing.append(l + r)


# generate new pairs

for g in selLeft:
	
	for R in right:
		if g + R not in existing:
			pair = '/' + g + '/' + R
			if R + g not in skip:
				output += context(g) + pair + ' ' + context(R) + '\n'
				if g in right:
					skip.append(g + R)
					output += context(g) + pair + '/' + g + ' ' + context(g) + '\n'
			
for g in selRight:
	
	for L in left:
		if L + g not in existing:
			pair = '/' + L + '/' + g
			if g + L not in skip:
				output += context(L) + pair + ' ' + context(g) + '\n'
				if g in left:
					skip.append(L + g)
					output += context(g) + pair + '/' + g + ' ' + context(g) + '\n'
				
				
# display result

from PyObjCTools.AppHelper import callAfter
callAfter(Glyphs.currentDocument.windowController().addTabWithString_, output)

# Glyphs.showMacroWindow()