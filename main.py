import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import sqlite3
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.app import runTouchApp
from kivy.core.window import Window
from kivy.clock import Clock
import hashlib


class MainWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass



class AddUserWindow(Screen, Widget):
    username = ObjectProperty(None)
    password = ObjectProperty(None)
    benchpress = ObjectProperty(None)
    deadlift = ObjectProperty(None)
    squat = ObjectProperty(None)

    def submit(self):
        username = self.username.text
        password = self.password.text
        benchpress = self.benchpress.text
        deadlift = self.deadlift.text
        squat = self.squat.text
        hash = hashlib.sha256(password.encode())
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute(
            "CREATE TABLE IF NOT EXISTS users (username text, password text, benchpress integer, deadlift integer, "
            "squat integer)")
        c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", (
            username, hash.hexdigest(), benchpress, deadlift, squat))
        conn.commit()
        conn.close()
        self.username.text = ""
        self.password.text = ""
        self.benchpress.text = ""
        self.deadlift.text = ""
        self.squat.text = ""


class LoginWindow(Screen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)

    def login(self):
        username = self.username.text
        password = self.password.text
        passwd = hashlib.sha256(password.encode())
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, passwd.hexdigest()))
        data = c.fetchone()
        if data is not None:
            c.execute("CREATE TABLE IF NOT EXISTS currently_logged_user (username text, password text) ")
            print("gere")
            c.execute("INSERT INTO currently_logged_user VALUES (?, ?)", (username, passwd.hexdigest()))
            conn.commit()
            self.manager.current = "user"
        else:
            print("Invalid username or password")
        conn.close()
        self.username.text = ""
        self.password.text = ""


class UserWindow(Screen):
    def logout(self):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("DROP TABLE currently_logged_user")
        conn.commit()
        self.manager.transition.direction = "right"
        self.manager.current = "main"
        conn.close()


kv = Builder.load_file("my.kv")


class WorkoutApp(App):

    def build(self):
        sm = WindowManager()
        sm.add_widget(MainWindow(name="main"))
        sm.add_widget(AddUserWindow(name="AddUser"))
        sm.add_widget(LoginWindow(name="Login"))
        sm.add_widget(UserWindow(name="user"))
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS currently_logged_user (username text, password text) ")
        c.execute("SELECT * FROM currently_logged_user")
        data = c.fetchone()
        print(kivy.__version__)
        print(data)
        if data:
            sm.current = "user"
        else:
            sm.current = "main"
        conn.close()
        return sm


if __name__ == '__main__':
    WorkoutApp().run()

