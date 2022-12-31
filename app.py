from kivy.lang import Builder

from kivymd.app import MDApp

KV = '''
MDBoxLayout:
    orientation: "vertical"

 

    MDLabel:
        text: "Content"
        halign: "center"
        
    MDTopAppBar:
        title: "MDTopAppBar"
        right_action_items: [["dots-vertical", lambda x: app.callback_1()], ["clock", lambda x: app.callback_2()]]
        "
'''


class Test(MDApp):
    def build(self):
        return Builder.load_string(KV)


Test().run()