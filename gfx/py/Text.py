from engine.JSONFile import JSONFile

from kivy.uix.gridlayout import GridLayout, GridLayoutException

from kivy.graphics import *

class Text():

    def __init__(self, engine, widget, text, texture='fontTexture', coordinatesAddress='fontCoordinates', minGrid=(None, None), maxGrid=(None,None), separator=' ') -> None:

        self.engine = engine

        self.widget = widget
        self.text = text
        self.texture = texture
        self.coordinatesAddress = coordinatesAddress
        self.minGrid = minGrid
        self.maxGrid = maxGrid
        self.separator = separator

        self.texture = self.getTexture()
        self.widget = self.getGrid()

    def getTexture(self): 
            
            if type(self.texture) == str:
                self.texture = JSONFile(self.texture).get_all_values()
            
            elif type(self.texture) == dict:
                pass

            else:
                raise TypeError

            return self.texture

    def getCoordinate(self, symbol):

            if type(self.coordinatesAddress) == str:
                rv = JSONFile(self.coordinatesAddress).get_value(symbol)
            elif type(self.coordinatesAddress) == dict:
                rv = self.coordinatesAddress.get(symbol)
            else:
                raise TypeError

            return rv

    def getGrid(self):

        
        dividedText = self.text.split(self.separator)

        textLength = (len(dividedText) - 1) * len(self.separator)
        for i in range(len(dividedText)):
            textLength += len(dividedText[i])

        xLimit = (self.minGrid[0] if self.minGrid[0] is not None else 0, self.maxGrid[0] if self.maxGrid[0] is not None else 1000)
        yLimit = (self.minGrid[1] if self.minGrid[1] is not None else 0, self.maxGrid[1] if self.maxGrid[1] is not None else 1000)

        if textLength > (xLimit[1] * yLimit[1]):
            raise GridLayoutException
        else:

            rv = [xLimit[0], yLimit[0]]

            stopFlag = False

            while not stopFlag:
                while rv[0] < xLimit[1]:
                    while rv[1] < yLimit[1]:
                        if rv[0]*rv[1] >= textLength:
                            stopFlag = True
                            break
                        else:
                            rv[1] +=1
                
                    if not stopFlag:
                        rv[1] = yLimit[0]
                        rv[0] += 1
                    else:
                        break

            self.widget.cols = rv[0]
            self.widget.rows = rv[1] 

            dSizeX = self.widget.size[0] / rv[0]
            dSizeY = self.widget.size[1] / rv[1]

            currentCoordinates = [0, rv[1]-1]

            for i in range(textLength):

                self.widget.add_widget(GridLayout(size=(dSizeX, dSizeY), pos=(dSizeX * currentCoordinates[0] + self.widget.pos[0], dSizeY * currentCoordinates[1] + self.widget.pos[1])))

                currentCoordinates[0] += 1
                if currentCoordinates[0] >= rv[0]: 
                    currentCoordinates[1] -= 1
                    currentCoordinates[0] = 0


            return self.widget

    def putSymbol(self, symbol, widgetToPutInto):

        with widgetToPutInto.canvas.before:
            letterCoordinates = self.getCoordinate(symbol)
            exec(letterCoordinates)

    def show(self):
        
        for i in range(len(self.text)):
            self.putSymbol(self.text[i], self.widget.children[len(self.widget.children)-1-i])