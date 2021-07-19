from kivy import graphics
from engine.JSONFile import JSONFile
from gfx.py.Widget import Widget

from kivy.uix.gridlayout import GridLayout, GridLayoutException

from kivy.graphics import *

from math import sqrt

class Text(Widget):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        
        if not hasattr(self, 'text'): self.text = ''
        if not hasattr(self, "texture"): self.texture = 'fontTexture'
        if not hasattr(self, "coordinatesAddress"): self.coordinatesAddress = 'fontCoordinates'
        if not hasattr(self, "minGrid"): self.minGrid = [None, None]
        if not hasattr(self, "maxGrid"): self.maxGrid = [None, None]
        if not hasattr(self, "minSize"): self.minSize = [None, None]
        if not hasattr(self, "maxSize"): self.maxSize = [None, None]
        if not hasattr(self, "separator"): self.separator = ' '

    def unpack(self):

        self.getTexture()
        self.getWidgetReady()

    def getTexture(self): 
            
            if type(self.texture) == str:
                self.texture = JSONFile(self.texture).get_all_values()
            
            elif type(self.texture) == dict:
                pass

            else:
                raise TypeError

    def getInstruction(self, symbol):

            if type(self.coordinatesAddress) == str:
                rv = JSONFile(self.coordinatesAddress).get_value(symbol)
            elif type(self.coordinatesAddress) == dict:
                rv = self.coordinatesAddress.get(symbol)
            else:
                raise TypeError

            return rv

    def getWidgetReady(self):

        def init(self):

            self.widget = GridLayout(size=self.widgetSize, pos=self.switchCoordinates(self.widgetPos, 'percentage','pixels'))

            dividedText = self.text.split(self.separator)

            textLength = (len(dividedText) - 1) * len(self.separator)
            for i in range(len(dividedText)):
                textLength += len(dividedText[i])

            return self.widget, textLength

        def applyPadding(self):

            for i in range(len(self.widgetPadding)):
                if self.widgetPadding[i] is None: self.widgetPadding[i] = 0

            if len(self.widgetPadding) == 1:
                self.widgetPadding = [self.widgetPadding[0], self.widgetPadding[0], self.widgetPadding[0], self.widgetPadding[0]]
            elif len(self.widgetPadding) == 2:
                self.widgetPadding = [self.widgetPadding[0], self.widgetPadding[1], self.widgetPadding[0], self.widgetPadding[1]]
            elif len(self.widgetPadding) not in (1, 2, 4):
                raise GridLayoutException

            paddingInPercentage = self.switchCoordinates(self.widgetPadding, 'pixels', 'percentage')

            for i in range(2):

                self.widgetPos[i] += paddingInPercentage[i]
                self.widgetSize[i] -= (self.widgetPadding[i] + self.widgetPadding[i+2])

        def getPossibleGrids(self, textLength):
            
            def checkValidity(self, textLength):
            
                if None in self.maxGrid: 
                    return True           
                
                else: 
                    return self.maxGrid[0] * self.maxGrid[1] >= textLength

            def sortFunction(arg):
                return arg[0] / arg[1]

            if not checkValidity(self, textLength): raise GridLayoutException

            if textLength % 2 != 0: textLength += 1

            possibleGrids = []
            for x in range(1, int(sqrt(textLength)+1)):
                if not (textLength % x):
                    possibleGrids.append([x,textLength//x])
                    possibleGrids.append([textLength//x, x])

            rv = []

            for possibleGrid in possibleGrids:
                if (self.maxGrid[0] is None or possibleGrid[0] <= self.maxGrid[0]) and (self.maxGrid[1] is None or possibleGrid[1] <= self.maxGrid[1]):
                    if (self.minGrid[0] is None or possibleGrid[0] >= self.minGrid[0]) and (self.minGrid[1] is None or possibleGrid[1] >= self.minGrid[1]):
                        rv.append(possibleGrid)

            rv = sorted(rv, key=sortFunction, reverse=True)

            return rv

        def tryGrid(self, grid):

            gridSize = [0, 0]

            if len(self.widgetSpacing) == 1: self.widgetSpacing = (self.widgetSpacing[0], self.widgetSpacing[0])

            for i in range(2):

                if self.widgetSpacing[i] is None: self.widgetSpacing[i] = 0

                if self.minSize[i] is not None:
                    if (self.widgetSpacing[i] * (grid[i] - 1)) + (grid[i] * self.minSize[i]) > self.widgetSize[i]:
                        return False
              
                if self.maxSize[i] is None:
                    gridSize[i] = (self.widgetSize[i] - self.widgetSpacing[i] * (grid[i] - 1)) / grid[i] 
                else:
                    gridSize[i] = min((self.widgetSize[i] - self.widgetSpacing[i] * (grid[i] - 1)) / grid[i], self.maxSize[i])
            
                if (gridSize[i] * grid[i] + self.widgetSpacing[i] * (grid[i] - 1)) > self.widgetSize[i]: 
                    return False

            return grid, gridSize 

        def execute(self, widgetGrid, widgetSize, textLength):
            
            self.widget.cols = widgetGrid[0]
            self.widget.rows = widgetGrid[1]

            currentCoordinates = [0, widgetGrid[1]-1]

            for i in range(textLength):
                
                posX = ((widgetSize[0] + self.widgetSpacing[0]) * currentCoordinates[0] + self.widget.pos[0])
                posY = ((widgetSize[1] + self.widgetSpacing[1]) * currentCoordinates[1] + self.widget.pos[1])

                self.widget.add_widget(Widget(engine=self.engine, size=(widgetSize[0], widgetSize[1]), pos=(posX, posY)), canvas='before')

                currentCoordinates[0] += 1
                if currentCoordinates[0] >= widgetGrid[0]: 
                    currentCoordinates[1] -= 1
                    currentCoordinates[0] = 0

            self.add_widget(self.widget)

        applyPadding(self)

        self.widget, textLength = init(self)

        possibleGrids = getPossibleGrids(self, textLength)
        
        for grid in possibleGrids:
            try:
                widgetGrid, widgetSize = tryGrid(self, grid)
                execute(self, widgetGrid, widgetSize, textLength)
                return None
            except:
                continue
        
        raise GridLayoutException

    def putSymbol(self, symbol, widgetToPutInto):
        
        with widgetToPutInto.canvas.after:
            Color(1, 0, 0)
            Line(points=[self.switchCoordinates((-1,-1,101,-1,101,101,-1,101,-1,-1), 'percentage', 'pixels', widgetToPutInto.size, widgetToPutInto.pos)])
            Color(0, 0, 1)
            try:
                exec(self.getInstruction(symbol))
            except:
                pass

    def show(self):

        self.unpack()

        for i in range(len(self.text)):
            if self.text[i] != self.separator: self.putSymbol(self.text[i], self.widget.children[len(self.widget.children)-1-i])
            else: self.putSymbol(" " * len(self.separator), self.widget.children[len(self.widget.children)-1-i])