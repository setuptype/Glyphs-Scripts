#MenuTitle: List All Kerning Pairs
# -*- coding: utf-8 -*-

__doc__="""
Lists all kerning pairs in active master.

Pairs consisting of glyphs with both left and right kerning are displayed as triplets, e.g. AVA, OTO.
"""


def string(g):
	return 'HN' if g[0].isupper() else 'nu'

def getName(g):
	if g[0] == '@':
		return g[7:]
	else:
		return font.glyphForId_(g).name

font	= Glyphs.font
kerning	= font.kerning[font.selectedFontMaster.id]
output	= ''
skip	= []
left	= []
right	= []


for L in kerning:
	l = getName(L)
	for R in kerning[L]:
		r = getName(R)
		if l not in left:
			left.append(l)
		if r not in right:
			right.append(r)
		

for L in kerning:
	for R in kerning[L]:
		l = getName(L)
		r = getName(R)
		if r + l not in skip:
			output += string(l) + '/' + l + '/' + r + ' ' + string(r) + '\n'
			if l in right:
				skip.append(l + r)
				output += string(l) + '/' + l + '/' + r + '/' + l + ' ' + string(l) + '\n'


#display result

from PyObjCTools.AppHelper import callAfter
callAfter(Glyphs.currentDocument.windowController().addTabWithString_, output)

Glyphs.showMacroWindow()
Glyphs.clearLog()