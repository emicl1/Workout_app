from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.list import ILeftBody, OneLineAvatarListItem

root_kv = """
#:import NavigationLayout kivymd.uix.navigationdrawer.NavigationLayout


<ContentNavigationDrawer@MDNavigationDrawer>
    drawer_logo: "demos/kitchen_sink/assets/drawer_logo.png"

    NavigationDrawerSubheader:
        text: "Menu:"


<CustomNavigationDrawerIconButton>

    AvatarSampleWidget:
        source: root.source


NavigationLayout:
    id: nav_layout

    ContentNavigationDrawer:
        id: nav_drawer

    BoxLayout:
        orientation: "vertical"

        MDToolbar:
            id: toolbar
            title: app.title
            md_bg_color: app.theme_cls.primary_color
            background_palette: "Primary"
            background_hue: "500"
            elevation: 10
            left_action_items:
                [["menu", lambda x: app.root.toggle_nav_drawer()]]

        BoxLayout:
            id: content
            orientation: "vertical"
"""


class AvatarSampleWidget(ILeftBody, Image):
    pass


class CustomNavigationDrawerIconButton(OneLineAvatarListItem):
    source = StringProperty()

    def _set_active(self, active, nav_drawer):
        pass


class MainApp(MDApp):
    def __init__(self, **kwargs):
        self.title = "KivyMD Examples - Navigation Drawer with Custom Buttons"
        self.theme_cls.primary_palette = "Orange"
        super().__init__(**kwargs)

    def build(self):
        self.root = Builder.load_string(root_kv)

    def on_start(self):
        for i in range(15):
            self.root.ids.nav_drawer.add_widget(
                CustomNavigationDrawerIconButton(
                    text=f"Item {i}",
                    source="data/logo/kivy-icon-128.png",
                    on_press=lambda x, y=i: self.callback(x, y),
                )
            )

    def callback(self, instance, value):
        toast("Pressed item menu %d" % value)


if __name__ == "__main__":
    MainApp().run()