#MenuTitle: List Existing Kerning Pairs
# -*- coding: utf-8 -*-

__doc__="""
Lists all kerning pairs containing the selected glyphs.
"""

Glyphs.clearLog()

def context(g):
	return 'HN' if g[0].isupper() else 'nu'
def getName(g):
	if g[0] == '@':
		return g[7:]
	else:
		return font.glyphForId_(g).name
def getClass(g, side):
	return '@MMK_' + side + '_' + g
def string(g):
	name = font.glyphs[g].string
	if name != None:
		return name
	else:
		return '[' + g + ']'
def getValue(dictionary, chain):
	_key = chain.pop(0)
	if _key in dictionary:
		return getValue(dictionary[_key], chain) if chain else dictionary[_key]


font = Glyphs.font
left = []
right = []
selLeft = []
selRight = []
existing = []
skip	= []
assymetry = []
text = ''
output	= ''
count = 0
assymetryCount = 0

# get kerning groups from all glyphs

for glyph in font.glyphs:
	L = glyph.rightKerningGroup
	R = glyph.leftKerningGroup
	if L != None and not (L in left):
		left.append(L)
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

kerning	= font.kerning[font.selectedFontMaster.id]

for L in kerning:
	for R in kerning[L]:
		l = getName(L)
		r = getName(R)
		if l in selLeft or r in selRight:
			count += 1
			if r + l not in skip:
				kern = getValue(kerning, [getClass(l, 'L'), getClass(r, 'R')])
				kernX = getValue(kerning, [getClass(r, 'L'), getClass(l, 'R')])
				if l in right and r in left and kern != None and kern != kernX:
					warning = ' <!>'
					assymetryCount += 1
					assymetry.append(string(l) + string(r) + string(l))
				else:
					warning = ''
				text += context(l) + '/' + l + '/' + r + ' ' + context(r) + '\n'
				if l in right:
					skip.append(l + r)
					text += context(l) + '/' + l + '/' + r + '/' + l + ' ' + context(l) + warning + '\n'

output += '\n'
output += str(count) + ' kerning pairs found for selected glyphs.\n\n'

# display result

from PyObjCTools.AppHelper import callAfter
callAfter(Glyphs.currentDocument.windowController().addTabWithString_, text)

# show macro window if there are any assymetric kerning triplets
if assymetryCount > 0:
	output += str(assymetryCount) + ' assymetric triplets found:\n' + '\n'.join(assymetry)
	Glyphs.showMacroWindow()
	
output += '\n'
print output
