#MenuTitle: Inspect Metrics
# -*- coding: utf-8 -*-

__doc__="""
Outputs ASCII visualization of metrics of active/selected glyphs.
"""

Glyphs.showMacroWindow()
Glyphs.clearLog()

Font	= Glyphs.font
layers	= Font.selectedLayers

def inspect(glyph, gLength):

	masters = []
	for layer in glyph.layers:
		if layer.associatedMasterId == layer.layerId:
			masters.append(layer)

	w = []
	l = []
	r = []
	strings = []
	
	for i in masters:
		w.append(i.width)
		l.append(i.LSB)
		r.append(i.RSB)
		
	lX = list(l)
	lX.sort(reverse = True)
	
	rX = list(r)
	rX.sort()
	
	wX = list(w)
	wX.sort(reverse = True)
	
	wY = list(w)
	wY.sort()
	
	for i in range(len(masters)):
		
		L	= n(l[i], l+r)
		R	= n(r[i], l+r)
		W	= n(w[i], w)
		y	= len(masters)
		
		lsbSlash	= '|' if l.count(l[i]) > 1 else '\\' if l[i] >= 0 else '/'
		rsbSlash	= '|' if r.count(r[i]) > 1 else '/' if r[i] >= 0 else '\\'
		lmSlash		= '|' if w.count(w[i]) > 1 else '/'
		rmSlash		= '|' if w.count(w[i]) > 1 else '\\'
		
		lsb	= slash(lX.index(l[i]), y, lsbSlash)
		rsb	= slash(rX.index(r[i]), y, rsbSlash)
		lm	= slash(wX.index(w[i]), y, lmSlash)
		rm	= slash(wY.index(w[i]), y, rmSlash)
		
		gName	= glyph.string if glyph.string != None and glyph.name != 'space' else glyph.name
		gName	+= (' ') * (gLength - len(gName))
		if i > 0:
			gName = (' ') * gLength
		
		strings.append( gName+'   '+lsb+' '+L+' | '+R+' '+rsb+'   '+lm+' '+W+' '+rm+' ' )
	
	ruler = ('_') * len(strings[0])
	print ruler
	print ''
	for i in strings:
		print i
	
def slash(x, y, char):
	string = ''
	for i in range(y):
		s = char if i == x else ' '
		string += s
	return string
	
def n(num, array):
	num = str(int(num))
	offset = (' ') * (3 - len(num))
	return offset + num

def longest(array):
	array.sort(reverse = True)
	return len(str(int(array[0])))

gLength = 0
for layer in layers:
	gName = layer.parent.string if layer.parent.string != None and layer.parent.name != 'space' else layer.parent.name
	if(len(gName) > gLength):
		gLength = len(gName)

offset = (' ') * len(Font.masters)
print (' ') * gLength + '  ' + offset + '  LSB | RSB  ' + offset + offset + '  Width'

for layer in layers:
	inspect(layer.parent, gLength)
print ''