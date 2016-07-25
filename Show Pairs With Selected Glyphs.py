#MenuTitle: Show Pairs With Selected Glyphs
# -*- coding: utf-8 -*-

__doc__="""
Combines selected glyphs with glyphs that are in a kerning group OR are kerned with other glyphs OR are usually kerned.

Pairs consisting of glyphs with both left and right kerning are displayed as triplets, e.g. AVA.

Only works if actual glyph names are used to name groups.
"""


def s(g):
	return 'HN' if g.isupper() else 'nu'


Font = Glyphs.font
glyphs = Font.selectedLayers


# usually kerned glyphs

left	= ['A','O','F','X','L','P','R','S','T','U','V','Y','Z','f','n','o','r','s','t','v','x','z','period','quotesingle','quoteright','slash','question','hyphen','zero','four','six','seven','nine','space']
right	= ['A','O','J','S','T','U','V','X','Y','Z','f','n','o','s','t','u','v','x','z','period','quotesingle','quoteright','slash','hyphen','question','zero','one','two','three','four','six','seven','nine','space']


# get kerning groups

for glyph in Font.glyphs:
	a = glyph.rightKerningGroup
	if a != None and not (a in left):
		left.append(a)
	b = glyph.leftKerningGroup
	if b != None and not (b in right):
		right.append(b)


# add glyphs with kerning that are not in a group to left/right lists

kerning	= Font.kerning[Font.selectedFontMaster.id]

for A in kerning:
	for B in kerning[A]:
		a = A[7:] if A[0] == '@' else Font.glyphForId_(A).name
		b = B[7:] if B[0] == '@' else Font.glyphForId_(B).name
		if a not in left:
			left.append(a)
		if b not in right:
			right.append(b)


#generate output

skip	= []
output	= ''

for glyph in glyphs:
	
	g = glyph.parent.name
	
	for a in left:
		pair = '/' + a + '/' + g
		if g + a not in skip:
			string = pair + ' ' + s(g)
			if a in right:
				string = pair + '/' + a + ' ' + s(a)
				skip.append(a + g)
			output += s(a) + string + '\n'
	
	for b in right:
		pair = '/' + g + '/' + b
		if b + g not in skip:
			string = pair + ' ' + s(b)
			if b in left:
				string = pair + '/' + g + ' ' + s(g)
				skip.append(g + b)
			output += s(g) + string + '\n'
			
				
# #display result

from PyObjCTools.AppHelper import callAfter
callAfter(Glyphs.currentDocument.windowController().addTabWithString_, output)

# Glyphs.showMacroWindow()
# Glyphs.clearLog()
# print output