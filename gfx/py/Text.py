from kivy import graphics
from engine.JSONFile import JSONFile
from gfx.py.Widget import Widget

from kivy.uix.gridlayout import GridLayout, GridLayoutException

from kivy.graphics import *

from math import sqrt

class Text(Widget):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        
        if not hasattr(self, 'engine'): raise EnvironmentError
        if not hasattr(self, "size"): self.size = (self.engine.settings.windowWidth, self.engine.settings.windowHeight)
        if not hasattr(self, "pos"): self.pos = (0, 0)
        if not hasattr(self, 'text'): self.text = ''
        if not hasattr(self, "texture"): self.texture = 'fontTexture'
        if not hasattr(self, "coordinatesAddress"): self.coordinatesAddress = 'fontCoordinates'
        if not hasattr(self, "minGrid"): self.minGrid = [None, None]
        if not hasattr(self, "maxGrid"): self.maxGrid = [None, None]
        if not hasattr(self, "minSize"): self.minSize = [None, None]
        if not hasattr(self, "maxSize"): self.maxSize = [None, None]
        if not hasattr(self, "separator"): self.separator = ' '
        if not hasattr(self, "padding"): self.padding = [None, None, None, None]
        if not hasattr(self, "spacing"): self.spacing = [None, None]

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

            self.widget = GridLayout(size=self.size, pos=self.switchCoordinates(self.pos, 'percentage','pixels'))

            dividedText = self.text.split(self.separator)

            textLength = (len(dividedText) - 1) * len(self.separator)
            for i in range(len(dividedText)):
                textLength += len(dividedText[i])

            return self.widget, textLength

        def applyPadding(self):

            for i in range(len(self.padding)):
                if self.padding[i] is None: self.padding[i] = 0

            if len(self.padding) == 1:
                self.padding = [self.padding[0], self.padding[0], self.padding[0], self.padding[0]]
            elif len(self.padding) == 2:
                self.padding = [self.padding[0], self.padding[1], self.padding[0], self.padding[1]]
            elif len(self.padding) not in (1, 2, 4):
                raise GridLayoutException

            paddingInPercentage = self.switchCoordinates(self.padding, 'pixels', 'percentage')

            for i in range(2):

                self.pos[i] += paddingInPercentage[i]
                self.size[i] -= (self.padding[i] + self.padding[i+2])

        def getPossibleGrids(self, textLength):
            
            def checkValidity(self, textLength):
            
                if None in self.maxGrid: 
                    return True
                    '''if self.maxGrid[0] is None:
                        
                        if self.minSize[0] is not None:
                            self.maxGrid[0] = round(self.size[0] / self.minSize[0])
                        else:
                            if self.maxSize[0] is not None:
                                self.maxGrid[0] = round(self.size[0] / self.maxSize[0])
                            else:
                                self.maxGrid[0] = 1
                                self.maxGrid[1] = (self.maxGrid[1] if self.maxGrid[1] is not None else 1)
                                while self.maxGrid[0] * self.maxGrid[1] < textLength:
                                    self.maxGrid[0] += 1
                                    self.maxGrid[1] += 1

                    if self.maxGrid[1] is None:
                        
                        if self.minSize[1] is not None:
                            self.maxGrid[1] = round(self.size[1] / self.minSize[1])
                        else:
                            if self.maxSize[1] is not None:
                                self.maxGrid[1] = round(self.size[1] / self.maxSize[1])
                            else:
                                self.maxGrid[1] = 1
                                self.maxGrid[0] = (self.maxGrid[0] if self.maxGrid[0] is not None else 1)
                                while self.maxGrid[0] * self.maxGrid[1] < textLength:
                                    self.maxGrid[0] += 1
                                    self.maxGrid[1] += 1'''            
                
                else: 
                    return self.maxGrid[0] * self.maxGrid[1] >= textLength

            def sortFunction(arg):
                if arg[0] - arg[1] < 0: return -1000
                else: return arg[1] - arg[0]

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

            if len(self.spacing) == 1: self.spacing = (self.spacing[0], self.spacing[0])

            for i in range(2):

                if self.spacing[i] is None: self.spacing[i] = 0

                if self.minSize[i] is not None:
                    if (self.spacing[i] * (grid[i] - 1)) + (grid[i] * self.minSize[i]) > self.size[i]:
                        return False
              
                if self.maxSize[i] is None:
                    gridSize[i] = (self.size[i] - self.spacing[i] * (grid[i] - 1)) / grid[i] 
                else:
                    gridSize[i] = min((self.size[i] - self.spacing[i] * (grid[i] - 1)) / grid[i], self.maxSize[i])
            
                if (gridSize[i] * grid[i] + self.spacing[i] * (grid[i] - 1)) > self.size[i]: 
                    return False

            return grid, gridSize 

        def execute(self, widgetGrid, widgetSize, textLength):
            
            self.widget.cols = widgetGrid[0]
            self.widget.rows = widgetGrid[1]

            currentCoordinates = [0, widgetGrid[1]-1]

            for i in range(textLength):
                
                posX = ((widgetSize[0] + self.spacing[0]) * currentCoordinates[0] + self.widget.pos[0])
                posY = ((widgetSize[1] + self.spacing[1]) * currentCoordinates[1] + self.widget.pos[1])

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
            exec(self.getInstruction(symbol))
            
    def show(self):

        self.unpack()

        for i in range(len(self.text)):
            if self.text[i] != self.separator: self.putSymbol(self.text[i], self.widget.children[len(self.widget.children)-1-i])
            else: self.putSymbol(" " * len(self.separator), self.widget.children[len(self.widget.children)-1-i])