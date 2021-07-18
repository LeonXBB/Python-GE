from engine.JSONFile import JSONFile

from gfx.py.Widget import Widget

from kivy.uix.gridlayout import GridLayout, GridLayoutException

from kivy.graphics import *

class Text(Widget):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        
        if not hasattr(self, 'engine'): raise EnvironmentError
        if not hasattr(self, "size"): self.size = (self.engine.settings.windowWidth, self.engine.settings.windowHeight)
        if not hasattr(self, "pos"): self.pos = (0, 0)
        if not hasattr(self, 'text'): self.text = ''
        if not hasattr(self, "texture"): self.texture = 'fontTexture'
        if not hasattr(self, "coordinatesAddress"): self.coordinatesAddress = 'fontCoordinates'
        if not hasattr(self, "minGrid"): self.minGrid = (None, None)
        if not hasattr(self, "maxGrid"): self.maxGrid = (None, None)
        if not hasattr(self, "minSize"): self.minSize = (None, None)
        if not hasattr(self, "maxSize"): self.maxSize = (None, None)
        if not hasattr(self, "separator"): self.separator = ' '

    def unpack(self):

        self.getTexture()
        self.getGrid()

    def getTexture(self): 
            
            if type(self.texture) == str:
                self.texture = JSONFile(self.texture).get_all_values()
            
            elif type(self.texture) == dict:
                pass

            else:
                raise TypeError

    def getCoordinate(self, symbol):

            if type(self.coordinatesAddress) == str:
                rv = JSONFile(self.coordinatesAddress).get_value(symbol)
            elif type(self.coordinatesAddress) == dict:
                rv = self.coordinatesAddress.get(symbol)
            else:
                raise TypeError

            return rv

    def getGrid(self):

        self.widget = GridLayout(size=self.size, pos=self.switchCoordinates(self.pos, 'percentage','pixels'))

        dividedText = self.text.split(self.separator)

        textLength = (len(dividedText) - 1) * len(self.separator)
        for i in range(len(dividedText)):
            textLength += len(dividedText[i])

        sizeXLimit = (self.minSize[0] if self.minSize[0] is not None else 1, self.maxSize[0] if self.maxSize[0] is not None else 1) 
        sizeYLimit = (self.minSize[1] if self.minSize[1] is not None else 1, self.maxSize[1] if self.maxSize[1] is not None else 1) 

        colsLimit = (self.minGrid[0] if self.minGrid[0] is not None else 1, self.maxGrid[0] if self.maxGrid[0] is not None else self.size[0])
        rowsLimit = (self.minGrid[1] if self.minGrid[1] is not None else 1, self.maxGrid[1] if self.maxGrid[1] is not None else self.size[1])
       
        if (textLength > (colsLimit[1] * rowsLimit[1])) or (colsLimit[0] > self.size[0] / sizeXLimit[0]) or (colsLimit[1] < self.size[0] / sizeXLimit[1]) \
            or (rowsLimit[0] > self.size[1] / sizeYLimit[0]) or (rowsLimit[1] < self.size[1] / sizeYLimit[1]):
            
            raise GridLayoutException 
        
        else:

            rv = [colsLimit[1], rowsLimit[1]]

            stopFlag = False

            while not stopFlag:
                while rv[0] < colsLimit[1]:
                    while rv[1] < rowsLimit[1]:
                        if rv[0]*rv[1] >= textLength:
                            stopFlag = True
                            break
                        else:
                            rv[1] +=1
                
                    if not stopFlag:
                        rv[1] = rowsLimit[0]
                        rv[0] += 1
                    else:
                        break

            print('RV: ', str(rv))

            self.widget.cols = rv[0]
            self.widget.rows = rv[1] 

            dSizeX = self.widget.size[0] / rv[0]
            dSizeY = self.widget.size[1] / rv[1]

            currentCoordinates = [0, rv[1]-1]

            for i in range(textLength):

                self.widget.add_widget(Widget(engine=self.engine, size=(dSizeX, dSizeY), pos=(dSizeX * currentCoordinates[0] + self.widget.pos[0], dSizeY * currentCoordinates[1] + self.widget.pos[1])), canvas='before')

                currentCoordinates[0] += 1
                if currentCoordinates[0] >= rv[0]: 
                    currentCoordinates[1] -= 1
                    currentCoordinates[0] = 0

            self.add_widget(self.widget)

    def putSymbol(self, symbol, widgetToPutInto):
        
        with widgetToPutInto.canvas.after:
            exec(self.getCoordinate(symbol))
            
    def show(self):

        self.unpack()

        for i in range(len(self.text)):
            self.putSymbol(self.text[i], self.widget.children[len(self.widget.children)-1-i])