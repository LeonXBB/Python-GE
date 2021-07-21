from engine.JSONFile import JSONFile
from gfx.py.Widget import Widget

from kivy.uix.gridlayout import GridLayout, GridLayoutException

from kivy.graphics import *

from math import sqrt, ceil

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
        if not hasattr(self, 'maxXYRatio'): self.maxXYRatio = 8 # TODO change from hard-coding to settings, probably?
        if not hasattr(self, 'minXYRatio'): self.minXYRatio = 1

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

        def getTextLength(self):
               
            dividedText = self.text.split(self.separator)
                
            textLength = (len(dividedText) - 1) * len(self.separator)
            for i in range(len(dividedText)):
                textLength += len(dividedText[i])
                
            return textLength

        def applyPadding(self):

            def convertPadding(self):
                for i in range(len(self.widgetPadding)):
                    if self.widgetPadding[i] is None: self.widgetPadding[i] = 0

            def expandPadding(self): 
                if len(self.widgetPadding) == 1:
                    self.widgetPadding = [self.widgetPadding[0], self.widgetPadding[0], self.widgetPadding[0], self.widgetPadding[0]]
                elif len(self.widgetPadding) == 2:
                    self.widgetPadding = [self.widgetPadding[0], self.widgetPadding[1], self.widgetPadding[0], self.widgetPadding[1]]
                elif len(self.widgetPadding) not in (1, 2, 4):
                    raise GridLayoutException

            def getPaddingInPercentage(self):
                return self.switchCoordinates(self.widgetPadding, 'pixels', 'percentage')

            def _applyPadding(self):

                for i in range(2):
                    
                    self.widgetPos[i] += getPaddingInPercentage(self)[i]
                    self.widgetSize[i] -= (self.widgetPadding[i] + self.widgetPadding[i+2])

            convertPadding(self)
            expandPadding(self)
            _applyPadding(self)

        def getPossibleGrids(self, textLength):
            
            def checkPossibleGridExists(self, textLength):

                if (None not in self.maxGrid) and ((self.maxGrid[0] * self.maxGrid[1]) < textLength): raise GridLayoutException
                if (None not in self.minGrid) and ((self.minGrid[0] * self.minGrid[1]) > textLength): raise GridLayoutException

            def checkGirdForLimits(self, grid):

                for i in range(2):
                    
                    _min = (self.minGrid[i] if self.minGrid[i] is not None else 1)
                    _max = (self.maxGrid[i] if self.maxGrid[i] is not None else grid[i])

                    if not (_min <= grid[i] <= _max): return False 

                return True

            def checkGridForRatios(self, grid, textLength):
                
                if self.minXYRatio is None: self.minXYRatio = 1
                if self.maxXYRatio is None: self.maxXYRatio = textLength

                return self.minXYRatio <= (grid[0] / grid[1]) <= self.maxXYRatio

            def _getPossibleGrids(self, textLength):
                
                possibleGrids = []
                for x in range(1, int(sqrt(textLength)+1)):
                    if not (textLength % x):
                        possibleGrids.append([x,textLength//x])
                        possibleGrids.append([textLength//x, x])

                return possibleGrids

            def filterPossibleGrids(self, possibleGrids):
                
                rv = []

                for grid in possibleGrids:
                    if not checkGirdForLimits(self, grid):
                        continue
                    if not checkGridForRatios(self, grid, textLength):
                        continue

                    rv.append(grid)

                return rv

            def sortFunction(arg):
                return arg[0] / arg[1]

            checkPossibleGridExists(self, textLength)
            possibleGrids= _getPossibleGrids(self, textLength)
            rv = filterPossibleGrids(self, possibleGrids)

            return sorted(rv, key=sortFunction, reverse=True)

        def tryGrid(self, grid):

            def getGridSize(self):
                
                rv = []

                for i in range(2):
                    divValue = self.widgetSize[i] / grid[i]
                    maxValue = (self.maxSize[i] if self.maxSize[i] is not None else divValue)
                    rv.append(min(divValue, maxValue))

                return rv

            def convertSpacing(self):
                
                if len(self.widgetSpacing) == 1: self.widgetSpacing = (self.widgetSpacing[0], self.widgetSpacing[0])
                for i in range(2):     
                    if self.widgetSpacing[i] is None: self.widgetSpacing[i] = 0

            def checkWidgetForLimits(self, gridSize):

                for i in range(2):
                    
                    _min = (self.minSize[i] if self.minSize[i] is not None else 1)
                    #_max = (self.maxSize[i] if self.maxSize[i] is not None else gridSize[i])                       

                    if _min > gridSize[i]: return False

                return True

            def checkAxisForLimitsWithSpacing(self, grid, gridSize):

                posInPixels = self.switchCoordinates(self.widgetPos, 'percentage', 'pixels')

                for i in range(2):            

                    if (posInPixels[i] + (gridSize[i] * grid[i]) + (self.widgetSpacing[i] * (grid[i] - 1))) > self.widgetSize[i]: 
                        return False

                return True

            gridSize = getGridSize(self)
            convertSpacing(self)
            if not checkWidgetForLimits(self, gridSize): return False
            if not checkAxisForLimitsWithSpacing(self, grid, gridSize): return False

            return grid[0], grid[1], gridSize

        def execute(self, widgetSize, textLength):
            
            currentCoordinates = [0, ceil(len(self.text) / (self.widget.cols)) - 1]

            for i in range(textLength):
                
                posX = ((widgetSize[0] + self.widgetSpacing[0]) * currentCoordinates[0] + self.widget.pos[0])
                posY = ((widgetSize[1] + self.widgetSpacing[1]) * currentCoordinates[1] + self.widget.pos[1])

                self.widget.add_widget(Widget(engine=self.engine, size=widgetSize, pos=(posX, posY)), canvas='before')

                currentCoordinates[0] += 1
                if currentCoordinates[0] >= self.widget.cols: 
                    currentCoordinates[1] -= 1
                    currentCoordinates[0] = 0

            self.add_widget(self.widget)

        def mainLoop(self, textLength):
            
            for i in range(textLength, self.widgetSize[0] * self.widgetSize[1]):

                possibleGrids = getPossibleGrids(self, i)
                
                for grid in possibleGrids:
                    try:
                        self.widget.cols, self.widget.rows, widgetSize = tryGrid(self, grid)
                        execute(self, widgetSize, i)
                        return None
                    except:
                        continue

            raise GridLayoutException

        applyPadding(self)
        init(self)
        mainLoop(self, getTextLength(self))

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