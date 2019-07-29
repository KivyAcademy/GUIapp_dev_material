
from kivy.app import App
from kivy.lang.builder import Builder

kv = '''
BoxLayout:
    orientation: 'vertical'
    
    Label: 
        text: 'top'
        
    BoxLayout:
        orientation: 'vertical'
        
        Button:
            id: btn
            text: 'DropDown'
            on_release: dropdown.open(self)
            size_hint_y: None
            background_normal: ''
            background_color: 0,.5,1,1
            height: '48dp'
    
        Widget:
            on_parent: dropdown.dismiss()
    
        DropDown:
            id: dropdown
            on_select: btn.text = 'Selected value: {}'.format(args[1])
    
            Button:
                text: 'Value A'
                size_hint_y: None
                height: '48dp'
                background_normal: ''
                background_color: 0,0,1,1
                on_release: dropdown.select('A')
    
            Button:
                text: 'Value B'
                size_hint_y: None
                height: '48dp'
                background_normal: ''
                background_color: 1,0,0,1
                on_release: dropdown.select('B')
    
            Button:
                text: 'Value C'
                size_hint_y: None
                height: '48dp'
                background_normal: ''
                background_color: 0,1,0,1
                on_release: dropdown.select('C')
                
        Label:
            text:'Bottom'

'''


class DDTestApp(App):
    def build(self):
        return Builder.load_string(kv)


if __name__ == '__main__':
    DDTestApp().run()

## Reference: https://groups.google.com/forum/#!topic/kivy-users/4X3Ao7oH860
