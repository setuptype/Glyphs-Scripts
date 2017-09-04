#MenuTitle: Show Pairs With Selected Glyphs
# -*- coding: utf-8 -*-

__doc__="""
Lists all combinations of glyphs used in kerning group names of selected glyphs. Only works if actual glyph names are used to name groups.

Pairs consisting of glyphs with both left and right kerning are displayed as triplets, e.g. AVA.
"""


def s(g):
	return 'HN' if g.isupper() else 'nu'


Font = Glyphs.font
glyphs = Font.selectedLayers

# get kerning groups

for glyph in Font.glyphs:
	a = glyph.rightKerningGroup
	if a != None and not (a in left):
		left.append(a)
	b = glyph.leftKerningGroup
	if b != None and not (b in right):
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