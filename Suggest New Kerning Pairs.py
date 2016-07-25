#MenuTitle: Suggest New Kerning Pairs
# -*- coding: utf-8 -*-

__doc__="""
Displays pairs that aren't kerned, but the glyphs of the pair are in a kerning group OR are kerned with other glyphs OR are usually kerned.
Example: If pairs AV and LT are kerned, the script will suggest pairs AT and LV.

Pairs consisting of glyphs with both left and right kerning are displayed as triplets, e.g. AVA, OTO.

Only works if actual glyph names are used to name groups.
"""


def s(g):
	return 'HN' if g.isupper() else 'nu'


Font = Glyphs.font


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

# get existing kerning pairs
# add glyphs with kerning that are not in a group to the left or right list

kerning	= Font.kerning[Font.selectedFontMaster.id]
pairs = []

for A in kerning:
	for B in kerning[A]:
		a = A[7:] if A[0] == '@' else Font.glyphForId_(A).name
		b = B[7:] if B[0] == '@' else Font.glyphForId_(B).name
		pairs.append(a + b)
		if a not in left:
			left.append(a)
		if b not in right:
			right.append(b)


#generate output

skip	= []
output	= ''

for a in left:
	for b in right:
		pair = '/' + a + '/' + b
		if a + b not in pairs and b + a not in skip:
			string = pair + ' ' + s(b)
			if a in right:
				string = pair + '/' + a + ' ' + s(a)
				skip.append(a + b)
			output += s(a) + string + '\n'


#display result

from PyObjCTools.AppHelper import callAfter
callAfter(Glyphs.currentDocument.windowController().addTabWithString_, output)

# Glyphs.showMacroWindow()
# Glyphs.clearLog()
# print output