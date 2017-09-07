#MenuTitle: List Combinations of Selected Glyphs
# -*- coding: utf-8 -*-

__doc__="""
Lists all combinations of glyphs used in kerning group names of selected glyphs.

Pairs consisting of glyphs with both left and right kerning are displayed as triplets, e.g. AVA.

Only works if actual glyph names are used to name kerning groups.
"""


def string(g):
	return 'HN' if g[0].isupper() else 'nu'

left = []
right = []

# get kerning groups of selected glyphs

for glyph in Glyphs.font.selection:
	L = glyph.rightKerningGroup
	if L != None and not (L in left):
		left.append(L)
	R = glyph.leftKerningGroup
	if R != None and not (R in right):
		right.append(R)

#generate output

skip	= []
output	= ''

for L in left:
	for R in right:
		pair = '/' + L + '/' + R
		if R + L not in skip:
			output += string(L) + pair + ' ' + string(R) + '\n'
			if L in right:
				skip.append(L + R)
				output += string(L) + pair + '/' + L + ' ' + string(L) + '\n'
		
#display result

from PyObjCTools.AppHelper import callAfter
callAfter(Glyphs.currentDocument.windowController().addTabWithString_, output)

# Glyphs.showMacroWindow()
# Glyphs.clearLog()