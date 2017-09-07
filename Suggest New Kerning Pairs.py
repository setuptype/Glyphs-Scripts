#MenuTitle: Suggest New Kerning Pairs
# -*- coding: utf-8 -*-

__doc__="""
Displays pairs that aren't kerned, but the glyphs of the pair are in a kerning group OR are kerned with other glyphs OR are usually kerned.
Example: If pairs AV and LT are kerned, the script will suggest pairs AT and LV.

Pairs consisting of glyphs with both left and right kerning are displayed as triplets, e.g. AVA, OTO.

Only works if actual glyph names are used to name kerning groups.
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

# get existing kerning pairs
# add glyphs with kerning that are not in a group to the left or right list

kerning	= font.kerning[font.selectedFontMaster.id]
existing = []

for L in kerning:
	for R in kerning[L]:
		l = getName(L)
		r = getName(R)
		existing.append(l + r)
		if l not in left:
			left.append(l)
		if r not in right:
			right.append(r)


#generate output

skip	= []
output	= ''

for L in left:
	for R in right:
		pair = '/' + L + '/' + R
		if L + R not in existing and R + L not in skip:
			output += string(L) + pair + ' ' + string(R) + '\n'
			if L in right:
				skip.append(L + R)
				output += string(L) + pair + '/' + L + ' ' + string(L) + '\n'


#display result

from PyObjCTools.AppHelper import callAfter
callAfter(Glyphs.currentDocument.windowController().addTabWithString_, output)

# Glyphs.showMacroWindow()
# Glyphs.clearLog()