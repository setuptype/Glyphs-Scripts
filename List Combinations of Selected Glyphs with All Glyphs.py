#MenuTitle: List Combinations of Selected Glyphs with Other Glyphs
# -*- coding: utf-8 -*-

__doc__="""
Lists all combinations of selected glyphs with glyphs that are already kerned OR are usually kerned.

Pairs consisting of glyphs with both left and right kerning are displayed as triplets, e.g. AVA.
"""


def string(g):
	return 'HN' if g[0].isupper() else 'nu'

def getName(g):
	if g[0] == '@':
		return g[7:]
	else:
		return font.glyphForId_(g).name

font = Glyphs.font


# usually kerned glyphs

left	= ['A','O','F','X','L','P','R','S','T','U','V','Y','Z','f','n','o','r','s','t','v','x','z','period','quotesingle','quoteright','slash','question','hyphen','zero','four','six','seven','nine','space']
right	= ['A','O','J','S','T','U','V','X','Y','Z','f','n','o','s','t','u','v','x','z','period','quotesingle','quoteright','slash','hyphen','question','zero','one','two','three','four','six','seven','nine','space']


# get kerning groups

for glyph in font.glyphs:
	L = glyph.rightKerningGroup
	if L != None and not (L in left):
		left.append(L)
	R = glyph.leftKerningGroup
	if R != None and not (R in right):
		right.append(R)


# add glyphs with kerning that are not in a group to left/right lists

kerning	= font.kerning[font.selectedFontMaster.id]

for L in kerning:
	for R in kerning[L]:
		l = getName(L)
		r = getName(R)
		if l not in left:
			left.append(l)
		if r not in right:
			right.append(r)


#generate output

skip	= []
output	= ''

for glyph in font.selection:
	
	g = glyph.name
	
	for L in left:
		pair = '/' + L + '/' + g
		if g + L not in skip:
			output += string(L) + pair + ' ' + string(g) + '\n'
			if L in right:
				skip.append(L + g)
				output += string(L) + pair + '/' + L + ' ' + string(L) + '\n'
	
	for R in right:
		pair = '/' + g + '/' + R
		if R + g not in skip:
			output += string(g) + pair + ' ' + string(R) + '\n'
			if R in left:
				skip.append(g + R)
				output += string(g) + pair + '/' + g + ' ' + string(g) + '\n'
			
				
# #display result

from PyObjCTools.AppHelper import callAfter
callAfter(Glyphs.currentDocument.windowController().addTabWithString_, output)

# Glyphs.showMacroWindow()
# Glyphs.clearLog()