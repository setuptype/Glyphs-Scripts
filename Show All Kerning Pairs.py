#MenuTitle: Show All Kerning Pairs
# -*- coding: utf-8 -*-

__doc__="""
Displays all kerning pairs found in a font in a new tab.

Pairs consisting of glyphs with both left and right kerning are displayed as triplets, e.g. AVA, OTO.
"""


def s(g):
	return 'HN' if g.isupper() else 'nu'


Font	= Glyphs.font
kerning	= Font.kerning[Font.selectedFontMaster.id]
output	= ''
skip	= []


for A in kerning:
	for B in kerning[A]:
		a = A[7:] if A[0] == '@' else Font.glyphForId_(A).name
		b = B[7:] if B[0] == '@' else Font.glyphForId_(B).name
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