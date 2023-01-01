import sqlite3
import hashlib
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang import Builder
from kivymd.uix.textfield import MDTextFieldRect, MDTextField
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

Window.size = (300, 500)


class FirstScreen(Screen):
    pass


class LoginScreen(Screen):
    pass


class SignupScreen(Screen):
    pass


class ClosestWorkoutScreen(Screen):
    pass


class ThisWeekWorkoutScreen(Screen):
    pass


class ProfileScreen(Screen):
    pass



class WorkoutApp(MDApp):
    dialog = None
    def build(self):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute(
            'CREATE TABLE IF NOT EXISTS users (username text, password text, bench integer, squat integer, deadlift integer)')
        c.execute("CREATE TABLE IF NOT EXISTS now_logged (username text, password text)")
        conn.commit()
        conn.close()
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepOrange"

        Builder.load_file("my.kv")

        sm = ScreenManager()
        sm.add_widget(FirstScreen(name='first'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(SignupScreen(name='signup'))
        sm.add_widget(ClosestWorkoutScreen(name='closest_workout'))
        sm.add_widget(ThisWeekWorkoutScreen(name='this_week_workout'))
        sm.add_widget(ProfileScreen(name='profile'))

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('SELECT username, password FROM now_logged')
        data = c.fetchone()
        print(data)
        if data:
            print("here")

            sm.current = 'profile'
        else:
            sm.current = 'first'
        conn.commit()
        conn.close()
        return sm


    def login(self, username, password):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        password = hashlib.sha256(password.encode()).hexdigest()
        c.execute('SELECT username, password FROM users WHERE username = ? AND password = ?', (username, password))
        data = c.fetchone()

        if data:
            self.root.current = 'profile'
        else:
            self.root.current = 'login'
        c.execute("CREATE TABLE IF NOT EXISTS now_logged (username text, password text)")
        c.execute("INSERT INTO now_logged VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()



    def signup(self, username, password, password2, bench, squat, deadlift):
        if password != password2:
            if not self.dialog:
                self.dialog = MDDialog(
                    title="Error",
                    text="Passwords do not match",
                    size_hint=(0.8, 1),
                    buttons=[
                        MDFlatButton(
                            text="Close", text_color=self.theme_cls.primary_color, on_release=self.close_dialog
                        ),
                    ],
                )
            self.dialog.open()
        try:
            bench = int(bench)
            squat = int(squat)
            deadlift = int(deadlift)
        except ValueError:
            if not self.dialog:
                self.dialog = MDDialog(
                    title="Error",
                    text="Lifts must be numbers only",
                    size_hint=(0.8, 1),
                    buttons=[
                        MDFlatButton(
                            text="Close", text_color=self.theme_cls.primary_color, on_release=self.close_dialog
                        ),
                    ],
                )
            self.dialog.open()
        if username == '' or password == '' or password2 == '' or bench == '' or squat == '' or deadlift == '':
            if not self.dialog:
                self.dialog = MDDialog(
                    title="Error",
                    text="Please fill out all fields",
                    size_hint=(0.8, 1),
                    buttons=[
                        MDFlatButton(
                            text="Close", text_color=self.theme_cls.primary_color, on_release=self.close_dialog
                        ),
                    ],
                )
            self.dialog.open()
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('SELECT username FROM users WHERE username = ?', (username,))
        data = c.fetchone()
        if data:
            if not self.dialog:
                self.dialog = MDDialog(
                    title="Error",
                    text="Username already exists",
                    size_hint=(0.8, 1),
                    buttons=[
                        MDFlatButton(
                            text="Close", text_color=self.theme_cls.primary_color, on_release=self.close_dialog
                        ),
                    ],
                )
            self.dialog.open()

        else:
            conn = sqlite3.connect('users.db')
            password = hashlib.sha256(password.encode()).hexdigest()
            c = conn.cursor()
            c.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?)', (username, password, bench, squat, deadlift))
            conn.commit()
            conn.close()
            self.root.current = 'login'

    def close_dialog(self, obj):
        self.dialog.dismiss()
        self.dialog = None

    def change_root(self, screen):
        self.root.current = screen

    def logout(self):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('DROP TABLE now_logged')
        conn.commit()
        conn.close()
        self.root.current = 'first'


WorkoutApp().run()
