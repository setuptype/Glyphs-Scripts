#MenuTitle: Show Pairs With Selected Glyphs
# -*- coding: utf-8 -*-

__doc__="""
Lists all combinations of glyphs used in kerning group names of selected glyphs. Only works if actual glyph names are used to name groups.

Pairs consisting of glyphs with both left and right kerning are displayed as triplets, e.g. AVA.
"""


def s(g):
	return 'HN' if g.isupper() else 'nu'

left = []
right = []

# get kerning groups of selected glyphs

for glyph in Glyphs.font.selection:
	a = glyph.rightKerningGroup
	if a != None and not (a in left):
		left.append(a)
	b = glyph.leftKerningGroup
	if b != None and not (b in right):
		right.append(b)

#generate output

skip	= []
output	= ''

for a in left:
	for b in right:
		pair = '/' + a + '/' + b
		if b + a not in skip:
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