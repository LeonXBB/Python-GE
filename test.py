from kivy.app import App 
from kivy.clock import Clock
from kivy.uix.label import Label

class myApp(App):

    def build(self):
        Clock.schedule_interval(self.update, 1)        
        return Label(text="0")

    def update(self, dt):
        self.root.text = str(int(self.root.text) + 1)

if __name__ == '__main__':
    my_app = myApp().run()

Trying to understand the way Kivy's Clock works: will it call its scheduled function if the previous instance of it hasn't been finished yet?

So, basically, the title. I have the following code (sort of MRE):

```
from kivy.app import App 
from kivy.clock import Clock
from kivy.uix.label import Label

class myApp(App):

    def build(self):
        Clock.schedule_interval(self.update, 1)        
        return Label(text="0")

    def update(self, dt):
        self.root.text = str(int(self.root.text) + 1)

if __name__ == '__main__':
    my_app = myApp().run()
```

In the following code everything works as intended (number on the screen increases every second, give or take hardware limitations).
However, I have noticed, that, in case the execution time of the ```update``` function is more than scheduled interval, the clock waits for the previous iteration to finish before starting a new one. This is unwanted behavior. I'd like to both (or multiple) calls to run simultaneously (one finishing, one starting or something like that). Given that there are no thread-unsafe parts in the code of the function itself, is it possible to achieve it by the means of ```kivy.clock```, and if so, how?

My kivy version is ```1.11.1``` and kivy clock type is set to ```free_all```.