#see license.txt for license details
#history http://cvs.sourceforge.net/cgi-bin/cvsweb.cgi/reportlab/graphics/widgets/flags.py?cvsroot=reportlab
#$Header: /tmp/reportlab/reportlab/graphics/widgets/flags.py,v 1.11 2001/10/02 19:43:53 rgbecker Exp $
# Flag Widgets - a collection of flags as widgets
# author: John Precedo (johnp@reportlab.com)

"""This file is a collection of flag graphics as widgets.

All flags are represented at the ratio of 1:2, even where the official ratio for the flag is something else
(such as 3:5 for the German national flag). The only exceptions are for where this would look _very_ wrong,
such as the Danish flag whose (ratio is 28:37), or the Swiss flag (which is square).

Unless otherwise stated, these flags are all the 'national flags' of the countries, rather than their
state flags, naval flags, ensigns or any other variants. (National flags are the flag flown by civilians
of a country and the ones usually used to represent a country abroad. State flags are the variants used by
the government and by diplomatic missions overseas).

To check on how close these are to the 'official' representations of flags, check the World Flag Database at
http://www.flags.ndirect.co.uk/

The flags this file contains are:

EU Members:
United Kingdom, Austria, Belgium, Denmark, Finland, France, Germany, Greece, Ireland, Italy, Luxembourg,
Holland (The Netherlands), Spain, Sweden

Others:
USA, Czech Republic, European Union, Switzerland, Turkey
"""

from reportlab.lib import colors
from reportlab.lib.validators import *
from reportlab.lib.attrmap import *
from reportlab.graphics.shapes import Line, Rect, Polygon, Drawing, Group, String, Circle
from reportlab.graphics.widgetbase import Widget
from reportlab.graphics import renderPDF
from signsandsymbols import _Symbol
import copy

validFlag=OneOf(None,
				'UK',
				'USA',
				'Austria',
				'Belgium',
				'Denmark',
				'Finland',
				'France',
				'Germany',
				'Greece',
				'Ireland',
				'Italy',
				'Luxembourg',
				'Holland',
				'Portugal',
				'Spain',
				'Sweden',
				'Norway',
				'CzechRepublic',
				'Turkey',
				'Switzerland',
				'EU',
				)

class Star(_Symbol):
	"""This draws a 5-pointed star.

		possible attributes:
		'x', 'y', 'size', 'fillColor', 'strokeColor'

		"""
	_attrMap = AttrMap(BASE=_Symbol,
			angle = AttrMapValue(isNumber, desc='angle'),
			)

	def __init__(self):
		_Symbol.__init__(self)
		self.size = 100
		self.fillColor = colors.yellow
		self.strokeColor = None
		self.angle = 0

	def demo(self):
		D = Drawing(200, 100)
		et = Star()
		et.x=50
		et.y=0
		D.add(et)
		labelFontSize = 10
		D.add(String(et.x+(et.size/2),(et.y-(1.2*labelFontSize)),
							et.__class__.__name__, fillColor=colors.black, textAnchor='middle',
							fontSize=labelFontSize))
		return D

	def draw(self):
		# general widget bits
		s = float(self.size)  #abbreviate as we will use this a lot
		g = Group()

		# star specific bits
		h = s/5
		z = s/2
		star = Polygon(points = [
					h-z,		0-z,
					h*1.5-z,	h*2.05-z,
					0-z,		h*3-z,
					h*1.95-z,	h*3-z,
					z-z,		s-z,
					h*3.25-z,	h*3-z,
					s-z,		h*3-z,
					s-h*1.5-z,	h*2.05-z,
					s-h-z,		0-z,
					z-z,		h-z,
					],
					fillColor = self.fillColor,
					strokeColor = self.strokeColor,
					strokeWidth=s/50)
		g.rotate(self.angle)
		g.shift(self.x+self.dx,self.y+self.dy)
		g.add(star)

		return g

class Flag(_Symbol):
	"""This is a generic flag class that all the flags in this file use as a basis.

		This class basically provides edges and a tidy-up routine to hide any bits of
		line that overlap the 'outside' of the flag

		possible attributes:
		'x', 'y', 'size', 'fillColor'
	"""

	_attrMap = AttrMap(BASE=_Symbol,
			fillColor = AttrMapValue(isColor, desc='Background color'),
			border = AttrMapValue(isBoolean, 'Whether a background is drawn'),
			kind = AttrMapValue(validFlag, desc='Which flag'),
			)

	def __init__(self):
		_Symbol.__init__(self)
		self.kind = None
		self.size = 100
		self.fillColor = colors.white
		self.border=1

	def availableFlagNames(self):
		'''return a list of the things we can display'''
		return filter(lambda x: x is not None, self._attrMap['kind'].validate._enum)

	def _Flag_None(self):
		# general widget bits
		s = self.size  # abbreviate as we will use this a lot
		g = Group()
		g.add(Rect(self.x+self.dx, self.y+self.dy, s*2, s, fillColor = colors.purple, strokeColor = colors.black, strokeWidth=0))
		return g

	def _borderDraw(self,g):
		# general widget bits
		s = self.size  # abbreviate as we will use this a lot
		x, y, sW = self.x+self.dx, self.y+self.dy, self.strokeWidth/2.
		g.insert(0,Rect(x-sW, y-sW, width=getattr(self,'_width',2*s)+2*sW, height=getattr(self,'_height',s)+2*sW,
				fillColor = None, strokeColor = self.strokeColor, strokeWidth=sW*2))
		return g

	def draw(self):
		kind = self.kind or 'None'
		return self._borderDraw(getattr(self,'_Flag_'+kind)())

	def clone(self):
		return copy.copy(self)

	def demo(self):
		D = Drawing(200, 100)
		name = self.availableFlagNames()
		import time
		name = name[int(time.time()) % len(name)]
		fx = Flag()
		fx.kind = name
		fx.x = 0
		fx.y = 0
		D.add(fx)
		labelFontSize = 10
		D.add(String(fx.x+(fx.size/2),(fx.y-(1.2*labelFontSize)),
							name, fillColor=colors.black, textAnchor='middle',
							fontSize=labelFontSize))
		labelFontSize = int(fx.size/4)
		D.add(String(fx.x+(fx.size),(fx.y+((fx.size/2))),
							"SAMPLE", fillColor=colors.gold, textAnchor='middle',
							fontSize=labelFontSize, fontName="Helvetica-Bold"))
		return D

	def _Flag_UK(self):
		s = float(self.size)
		g = Group()
		x, y = self.x+self.dx, self.y+self.dy
		w = s*2
		g.add(Rect(x, y, w, s, fillColor = colors.navy, strokeColor = colors.black, strokeWidth=0))
		g.add(Polygon([x,y, x+s*.225,y, x+w,y+s*(1-.1125), x+w,y+s, x+w-s*.225,y+s, x, y+s*.1125], fillColor = colors.mintcream, strokeColor=None, strokeWidth=0))
		g.add(Polygon([x,y+s*(1-.1125), x, y+s, x+s*.225,y+s, x+w, y+s*.1125, x+w,y, x+w-s*.225,y], fillColor = colors.mintcream, strokeColor=None, strokeWidth=0))
		g.add(Polygon([x, y+s-(s/15), x+(s-((s/10)*4)), y+(s*0.65), x+(s-(s/10)*3), y+(s*0.65), x, y+s], fillColor = colors.red, strokeColor = None, strokeWidth=0))
		g.add(Polygon([x, y, x+(s-((s/10)*3)), y+(s*0.35), x+(s-((s/10)*2)), y+(s*0.35), x+(s/10), y], fillColor = colors.red, strokeColor = None, strokeWidth=0))
		g.add(Polygon([x+w, y+s, x+(s+((s/10)*3)), y+(s*0.65), x+(s+((s/10)*2)), y+(s*0.65), x+w-(s/10), y+s], fillColor = colors.red, strokeColor = None, strokeWidth=0))
		g.add(Polygon([x+w, y+(s/15), x+(s+((s/10)*4)), y+(s*0.35), x+(s+((s/10)*3)), y+(s*0.35), x+w, y], fillColor = colors.red, strokeColor = None, strokeWidth=0))
		g.add(Rect(x+((s*0.42)*2), y, width=(0.16*s)*2, height=s, fillColor = colors.mintcream, strokeColor = None, strokeWidth=0))
		g.add(Rect(x, y+(s*0.35), width=w, height=s*0.3, fillColor = colors.mintcream, strokeColor = None, strokeWidth=0))
		g.add(Rect(x+((s*0.45)*2), y, width=(0.1*s)*2, height=s, fillColor = colors.red, strokeColor = None, strokeWidth=0))
		g.add(Rect(x, y+(s*0.4), width=w, height=s*0.2, fillColor = colors.red, strokeColor = None, strokeWidth=0))
		return g

	def _Flag_USA(self):
		# general widget bits
		s = self.size  # abbreviate as we will use this a lot
		g = Group()
		x, y = self.x+self.dx, self.y+self.dy

		# flag specific bits
		box = Rect(x, y, s*2, s, fillColor = colors.mintcream, strokeColor = colors.black, strokeWidth=0)
		g.add(box)

		for stripecounter in range (13,0, -1):
			stripeheight = s/13.0
			if not (stripecounter%2 == 0):
				stripecolor = colors.red
			else:
				stripecolor = colors.mintcream
			redorwhiteline = Rect(x, y+(s-(stripeheight*stripecounter)), width=s*2, height=stripeheight,
				fillColor = stripecolor, strokeColor = None, strokeWidth=20)
			g.add(redorwhiteline)

		bluebox = Rect(x, y+(s-(stripeheight*7)), width=0.8*s, height=stripeheight*7,
			fillColor = colors.darkblue, strokeColor = None, strokeWidth=0)
		g.add(bluebox)

		lss = s*0.045
		lss2 = lss/2
		s9 = s/9
		s7 = s/7
		for starxcounter in range(5):
			for starycounter in range(4):
				ls = Star()
				ls.size = lss
				ls.x = x-s/22+lss/2+s7+starxcounter*s7
				ls.fillColor = colors.mintcream
				ls.y = y+s-(starycounter+1)*s9+lss2
				g.add(ls)

		for starxcounter in range(6):
			for starycounter in range(5):
				ls = Star()
				ls.size = lss
				ls.x = x-(s/22)+lss/2+s/14+starxcounter*s7
				ls.fillColor = colors.mintcream
				ls.y = y+s-(starycounter+1)*s9+(s/18)+lss2
				g.add(ls)
		return g

	def _Flag_Austria(self):
		# general widget bits
		s = self.size  # abbreviate as we will use this a lot
		g = Group()
		x, y = self.x+self.dx, self.y+self.dy

		# flag specific bits
		box = Rect(x, y, s*2, s, fillColor = colors.mintcream,
			strokeColor = colors.black, strokeWidth=0)
		g.add(box)


		redbox1 = Rect(x, y, width=s*2.0, height=s/3.0,
			fillColor = colors.red, strokeColor = None, strokeWidth=0)
		g.add(redbox1)

		redbox2 = Rect(x, y+((s/3.0)*2.0), width=s*2.0, height=s/3.0,
			fillColor = colors.red, strokeColor = None, strokeWidth=0)
		g.add(redbox2)
		return g

	def _Flag_Belgium(self):
		# general widget bits
		s = self.size  # abbreviate as we will use this a lot
		g = Group()
		x, y = self.x+self.dx, self.y+self.dy

		# flag specific bits
		box = Rect(x, y, s*2, s,
			fillColor = colors.black, strokeColor = colors.black, strokeWidth=0)
		g.add(box)


		box1 = Rect(x, y, width=(s/3.0)*2.0, height=s,
			fillColor = colors.black, strokeColor = None, strokeWidth=0)
		g.add(box1)

		box2 = Rect(x+((s/3.0)*2.0), y, width=(s/3.0)*2.0, height=s,
			fillColor = colors.gold, strokeColor = None, strokeWidth=0)
		g.add(box2)

		box3 = Rect(x+((s/3.0)*4.0), y, width=(s/3.0)*2.0, height=s,
			fillColor = colors.red, strokeColor = None, strokeWidth=0)
		g.add(box3)
		return g

	def _Flag_Denmark(self):
		# general widget bits
		s = self.size  # abbreviate as we will use this a lot
		g = Group()
		x, y = self.x+self.dx, self.y+self.dy
		self._width = w = s*1.4

		# flag specific bits
		box = Rect(x, y, w, s,
			fillColor = colors.red, strokeColor = colors.black, strokeWidth=0)
		g.add(box)

		whitebox1 = Rect(x+((s/5)*2), y, width=s/6, height=s,
			fillColor = colors.mintcream, strokeColor = None, strokeWidth=0)
		g.add(whitebox1)

		whitebox2 = Rect(x, y+((s/2)-(s/12)), width=w, height=s/6,
			fillColor = colors.mintcream, strokeColor = None, strokeWidth=0)
		g.add(whitebox2)
		return g

	def _Flag_Finland(self):
		# general widget bits
		s = self.size  # abbreviate as we will use this a lot
		g = Group()
		x, y = self.x+self.dx, self.y+self.dy

		# crossbox specific bits
		box = Rect(x, y, s*2, s,
			fillColor = colors.ghostwhite, strokeColor = colors.black, strokeWidth=0)
		g.add(box)

		blueline1 = Rect(x+(s*0.6), y, width=0.3*s, height=s,
			fillColor = colors.darkblue, strokeColor = None, strokeWidth=0)
		g.add(blueline1)

		blueline2 = Rect(x, y+(s*0.4), width=s*2, height=s*0.3,
			fillColor = colors.darkblue, strokeColor = None, strokeWidth=0)
		g.add(blueline2)
		return g

	def _Flag_France(self):
		# general widget bits
		s = self.size  # abbreviate as we will use this a lot
		g = Group()
		x, y = self.x+self.dx, self.y+self.dy

		# flag specific bits
		box = Rect(x, y, s*2, s, fillColor = colors.navy, strokeColor = colors.black, strokeWidth=0)
		g.add(box)

		bluebox = Rect(x, y, width=((s/3.0)*2.0), height=s,
			fillColor = colors.blue, strokeColor = None, strokeWidth=0)
		g.add(bluebox)

		whitebox = Rect(x+((s/3.0)*2.0), y, width=((s/3.0)*2.0), height=s,
			fillColor = colors.mintcream, strokeColor = None, strokeWidth=0)
		g.add(whitebox)

		redbox = Rect(x+((s/3.0)*4.0), y, width=((s/3.0)*2.0), height=s,
			fillColor = colors.red,
			strokeColor = None,
			strokeWidth=0)
		g.add(redbox)
		return g

	def _Flag_Germany(self):
		# general widget bits
		s = self.size  # abbreviate as we will use this a lot
		g = Group()
		x, y = self.x+self.dx, self.y+self.dy

		# flag specific bits
		box = Rect(x, y, s*2, s,
				fillColor = colors.gold, strokeColor = colors.black, strokeWidth=0)
		g.add(box)

		blackbox1 = Rect(x, y+((s/3.0)*2.0), width=s*2.0, height=s/3.0,
			fillColor = colors.black, strokeColor = None, strokeWidth=0)
		g.add(blackbox1)

		redbox1 = Rect(x, y+(s/3.0), width=s*2.0, height=s/3.0,
			fillColor = colors.orangered, strokeColor = None, strokeWidth=0)
		g.add(redbox1)
		return g

	def _Flag_Greece(self):
		# general widget bits
		s = self.size  # abbreviate as we will use this a lot
		g = Group()
		x, y = self.x+self.dx, self.y+self.dy

		# flag specific bits
		box = Rect(x, y, s*2, s, fillColor = colors.gold,
						strokeColor = colors.black, strokeWidth=0)
		g.add(box)

		for stripecounter in range (9,0, -1):
			stripeheight = s/9.0
			if not (stripecounter%2 == 0):
				stripecolor = colors.deepskyblue
			else:
				stripecolor = colors.mintcream

			blueorwhiteline = Rect(x, y+(s-(stripeheight*stripecounter)), width=s*2, height=stripeheight,
				fillColor = stripecolor, strokeColor = None, strokeWidth=20)
			g.add(blueorwhiteline)

		bluebox1 = Rect(x, y+((s)-stripeheight*5), width=(stripeheight*5), height=stripeheight*5,
			fillColor = colors.deepskyblue, strokeColor = None, strokeWidth=0)
		g.add(bluebox1)

		whiteline1 = Rect(x, y+((s)-stripeheight*3), width=stripeheight*5, height=stripeheight,
			fillColor = colors.mintcream, strokeColor = None, strokeWidth=0)
		g.add(whiteline1)

		whiteline2 = Rect(x+(stripeheight*2), y+((s)-stripeheight*5), width=stripeheight, height=stripeheight*5,
			fillColor = colors.mintcream, strokeColor = None, strokeWidth=0)
		g.add(whiteline2)

		return g

	def _Flag_Ireland(self):
		# general widget bits
		s = self.size  # abbreviate as we will use this a lot
		g = Group()
		x, y = self.x+self.dx, self.y+self.dy

		# flag specific bits
		box = Rect(x, y, s*2, s,
			fillColor = colors.forestgreen, strokeColor = colors.black, strokeWidth=0)
		g.add(box)

		whitebox = Rect(x+((s*2.0)/3.0), y, width=(2.0*(s*2.0)/3.0), height=s,
				fillColor = colors.mintcream, strokeColor = None, strokeWidth=0)
		g.add(whitebox)

		orangebox = Rect(x+((2.0*(s*2.0)/3.0)), y, width=(s*2.0)/3.0, height=s,
			fillColor = colors.darkorange, strokeColor = None, strokeWidth=0)
		g.add(orangebox)
		return g

	def _Flag_Italy(self):
		# general widget bits
		s = self.size  # abbreviate as we will use this a lot
		g = Group()
		x, y = self.x+self.dx, self.y+self.dy

		# flag specific bits
		box = Rect(x, y, s*2, s,
				fillColor = colors.forestgreen, strokeColor = colors.black, strokeWidth=0)
		g.add(box)

		whitebox = Rect(x+((s*2.0)/3.0), y, width=(2.0*(s*2.0)/3.0), height=s,
				fillColor = colors.mintcream, strokeColor = None, strokeWidth=0)
		g.add(whitebox)

		redbox = Rect(x+((2.0*(s*2.0)/3.0)), y, width=(s*2.0)/3.0, height=s,
				fillColor = colors.red, strokeColor = None, strokeWidth=0)
		g.add(redbox)
		return g

	def _Flag_Luxembourg(self):
		# general widget bits
		s = self.size  # abbreviate as we will use this a lot
		g = Group()
		x, y = self.x+self.dx, self.y+self.dy

		# flag specific bits
		box = Rect(x, y, s*2, s,
			fillColor = colors.mintcream, strokeColor = colors.black, strokeWidth=0)
		g.add(box)

		redbox = Rect(x, y+((s/3.0)*2.0), width=s*2.0, height=s/3.0,
				fillColor = colors.red, strokeColor = None, strokeWidth=0)
		g.add(redbox)

		bluebox = Rect(x, y, width=s*2.0, height=s/3.0,
				fillColor = colors.dodgerblue, strokeColor = None, strokeWidth=0)
		g.add(bluebox)
		return g

	def _Flag_Holland(self):
		# general widget bits
		s = self.size  # abbreviate as we will use this a lot
		g = Group()
		x, y = self.x+self.dx, self.y+self.dy

		# flag specific bits
		box = Rect(x, y, s*2, s,
			fillColor = colors.mintcream, strokeColor = colors.black, strokeWidth=0)
		g.add(box)

		redbox = Rect(x, y+((s/3.0)*2.0), width=s*2.0, height=s/3.0,
				fillColor = colors.red, strokeColor = None, strokeWidth=0)
		g.add(redbox)

		bluebox = Rect(x, y, width=s*2.0, height=s/3.0,
				fillColor = colors.darkblue, strokeColor = None, strokeWidth=0)
		g.add(bluebox)
		return g

	def _Flag_Portugal(self):
		return Group()

	def _Flag_Spain(self):
		# general widget bits
		s = self.size  # abbreviate as we will use this a lot
		g = Group()
		x, y = self.x+self.dx, self.y+self.dy

		# flag specific bits
		box = Rect(x, y, s*2, s,
				fillColor = colors.yellow, strokeColor = colors.black, strokeWidth=0)
		g.add(box)

		redbox1 = Rect(x, y+((s/4)*3), width=s*2, height=s/4,
			fillColor = colors.red, strokeColor = None, strokeWidth=0)
		g.add(redbox1)

		redbox2 = Rect(x, y, width=s*2, height=s/4,
			fillColor = colors.red,
			strokeColor = None,
			strokeWidth=0)
		g.add(redbox2)
		return g

	def _Flag_Sweden(self):
		# general widget bits
		s = self.size  # abbreviate as we will use this a lot
		g = Group()
		x, y = self.x+self.dx, self.y+self.dy
		# flag specific bits
		self._width = s*1.4
		box = Rect(x, y, self._width, s,
			fillColor = colors.dodgerblue, strokeColor = colors.black, strokeWidth=0)
		g.add(box)

		box1 = Rect(x+((s/5)*2), y, width=s/6, height=s,
				fillColor = colors.gold, strokeColor = None, strokeWidth=0)
		g.add(box1)

		box2 = Rect(x, y+((s/2)-(s/12)), width=self._width, height=s/6,
			fillColor = colors.gold,
			strokeColor = None,
			strokeWidth=0)
		g.add(box2)
		return g

	def _Flag_Norway(self):
		s = self.size  # abbreviate as we will use this a lot
		g = Group()
		x, y = self.x+self.dx, self.y+self.dy
		self._width = s*1.4

		box = Rect(x, y, self._width, s,
				fillColor = colors.red, strokeColor = colors.black, strokeWidth=0)
		g.add(box)

		box = Rect(x, y, self._width, s,
				fillColor = colors.red, strokeColor = colors.black, strokeWidth=0)
		g.add(box)

		whiteline1 = Rect(x+((s*0.2)*2), y, width=s*0.2, height=s,
				fillColor = colors.ghostwhite, strokeColor = None, strokeWidth=0)
		g.add(whiteline1)

		whiteline2 = Rect(x, y+(s*0.4), width=self._width, height=s*0.2,
				fillColor = colors.ghostwhite, strokeColor = None, strokeWidth=0)
		g.add(whiteline2)

		blueline1 = Rect(x+((s*0.225)*2), y, width=0.1*s, height=s,
				fillColor = colors.darkblue, strokeColor = None, strokeWidth=0)
		g.add(blueline1)

		blueline2 = Rect(x, y+(s*0.45), width=self._width, height=s*0.1,
				fillColor = colors.darkblue, strokeColor = None, strokeWidth=0)
		g.add(blueline2)
		return g

	def _Flag_CzechRepublic(self):
		# general widget bits
		s = self.size  # abbreviate as we will use this a lot
		g = Group()
		x, y = self.x+self.dx, self.y+self.dy
		# flag specific bits
		box = Rect(x, y, s*2, s,
			fillColor = colors.mintcream,
						strokeColor = colors.black,
			strokeWidth=0)
		g.add(box)

		redbox = Rect(x, y, width=s*2, height=s/2,
			fillColor = colors.red,
			strokeColor = None,
			strokeWidth=0)
		g.add(redbox)

		bluewedge = Polygon(points = [ x, y, x+s, y+(s/2), x, y+s],
					fillColor = colors.darkblue, strokeColor = None, strokeWidth=0)
		g.add(bluewedge)
		return g

	def _Flag_Turkey(self):
		# general widget bits
		s = float(self.size)  # abbreviate as we will use this a lot
		g = Group()
		x, y = self.x+self.dx, self.y+self.dy

		# flag specific bits
		box = Rect(x, y, s*2, s,
			fillColor = colors.red,
						strokeColor = colors.black,
			strokeWidth=0)
		g.add(box)

		whitecircle = Circle(cx=x+((s*0.35)*2), cy=y+s/2, r=s*0.3,
			fillColor = colors.mintcream,
			strokeColor = None,
			strokeWidth=0)
		g.add(whitecircle)

		redcircle = Circle(cx=x+((s*0.39)*2), cy=y+s/2, r=s*0.24,
			fillColor = colors.red,
			strokeColor = None,
			strokeWidth=0)
		g.add(redcircle)

		ws = Star()
		ws.angle = 15
		ws.size = s/5
		ws.x = x+(s*0.5)*2+ws.size/2
		ws.y = y+(s*0.5)
		ws.fillColor = colors.mintcream
		ws.strokeColor = None
		g.add(ws)
		return g

	def _Flag_Switzerland(self):
		# general widget bits
		s = float(self.size)  # abbreviate as we will use this a lot
		g = Group()
		x, y = self.x+self.dx, self.y+self.dy
		self._width = s

		# flag specific bits
		g.add(Rect(x, y, s, s, fillColor = colors.red, strokeColor = colors.black, strokeWidth=0))
		g.add(Line(x+(s/2), y+(s/5.5), x+(s/2), y+(s-(s/5.5)),
			fillColor = colors.mintcream, strokeColor = colors.mintcream, strokeWidth=(s/5)))
		g.add(Line(x+(s/5.5), y+(s/2), x+(s-(s/5.5)), y+(s/2),
			fillColor = colors.mintcream, strokeColor = colors.mintcream, strokeWidth=s/5))
		return g

	def _Flag_EU(self):
		# general widget bits
		s = float(self.size)  # abbreviate as we will use this a lot
		g = Group()
		x, y = self.x+self.dx, self.y+self.dy
		w = self._width = 1.5*s

		# flag specific bits
		g.add(Rect(x, y, w, s, fillColor = colors.darkblue, strokeColor = None, strokeWidth=0))
		centerx=x+w/2
		centery=y+s/2
		radius=s/3
		yradius = radius
		xradius = radius
		nStars = 12
		from math import sin, cos, pi
		delta = 2*pi/nStars
		for i in range(nStars):
			rad = i*delta
			gs = Star()
			gs.x=cos(rad)*radius+centerx
			gs.y=sin(rad)*radius+centery
			gs.size=s/10
			gs.fillColor=colors.gold
			g.add(gs)
		return g

def makeFlag(name):
	flag = Flag()
	flag.kind = name
	return flag

def test():
	"""This function produces two pdf files with examples of all the signs and symbols from this file.
	"""
# page 1

	labelFontSize = 10

	X = (20,245)

	flags = [
			'UK',
			'USA',
			'Austria',
			'Belgium',
			'Denmark',
			'Finland',
			'France',
			'Germany',
			'Greece',
			'Ireland',
			'Italy',
			'Luxembourg',
			'Holland',
			'Portugal',
			'Spain',
			'Sweden',
			'Norway',
			'CzechRepublic',
			'Turkey',
			'Switzerland',
			'EU',
			]
	y = Y0 = 530
	f = 0
	D = None
	for name in flags:
		if not D: D = Drawing(450,650)
		flag = makeFlag(name)
		i = flags.index(name)
		flag.x = X[i%2]
		flag.y = y
		D.add(flag)
		D.add(String(flag.x+(flag.size/2),(flag.y-(1.2*labelFontSize)),
				name, fillColor=colors.black, textAnchor='middle', fontSize=labelFontSize))
		if i%2: y = y - 125
		if (i%2 and y<0) or name==flags[-1]:
			renderPDF.drawToFile(D, 'flags%02d.pdf'%f, 'flags.py - Page #%d'%(f+1))
			y = Y0
			f = f+1
			D = None

if __name__=='__main__':
	test()
