from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.clock import Clock
import sqlite3
from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.animation import Animation

Window.size = (350, 580)
class GrupoAguia(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None

    def build(self):
        global screen_manager
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file('pre-splash.kv'))
        screen_manager.add_widget(Builder.load_file('login.kv'))
        screen_manager.add_widget(Builder.load_file('signup.kv'))
        screen_manager.add_widget(Builder.load_file('home.kv'))

        return screen_manager

    def on_start(self):
        Clock.schedule_once(self.login, 6)
    def login(self, *args):
        screen_manager.current = 'login'

    def signup(self, *args):
        screen_manager.current = 'signup'

    def validate_login(self, username, password):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()

        conn.close()

        if user:
            print("Login efetuado com sucesso!")
            self.user_info = user
            self.update_home_screen()
            screen_manager.current = 'home'
        else:
            print("Senha inválida, tente novamente!")
            self.not_dialog()
            screen_manager.current = 'login'

    def update_home_screen(self):
        global screen_manager
        home_screen = screen_manager.get_screen('home')
        if home_screen:
            welcome_label = home_screen.ids.welcome_label
            if self.user_info:
                username = self.user_info[1]  # Supondo que o nome de usuário esteja na segunda coluna do banco de dados
                welcome_label.text = f"Seja bem-vindo(a), {username}!"

    def register_user(self, username, password, telefone):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, telefone) VALUES (?, ?, ?)", (username, password, telefone))
        conn.commit()
        conn.close()

        print('Usuário registrado com sucesso!')
        self.show_success_dialog()
        screen_manager.current = 'login'

    def show_success_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                text="Usuário registrado com sucesso!",
                md_bg_color=(0, 255, 127),
                buttons=[
                    MDFlatButton(
                        text="OK",
                        text_color=(1, 1, 1, 1),
                        md_bg_color=(211, 211, 211),
                    on_release=self.close_dialog
                    ),
                ],
            )
        self.dialog.open()

    def close_dialog(self, *args):
        self.dialog.dismiss(force=True)
    def not_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                text="Senha inválida, tente novamente!",
                md_bg_color=(226/255, 0, 48/255, 1),
                buttons=[
                    MDFlatButton(
                        text="OK",
                        text_color=(1, 1, 1, 1),
                        md_bg_color=(211, 211, 211),
                    on_release=self.close_dialog
                    ),
                ],
            )
            self.dialog.open()
            self.dialog.ids.text.color = (1, 1, 1, 1)
        else:
            self.dialog.open()
        self.shake_dialog()
    def shake_dialog(self):
        if self.dialog:
            dialog_content = self.dialog.ids.container
            anim = Animation(x=dialog_content.x + 10, duration=0.05) + \
                   Animation(x=dialog_content.x - 20, duration=0.1) + \
                   Animation(x=dialog_content.x + 20, duration=0.1) + \
                   Animation(x=dialog_content.x - 20, duration=0.1) + \
                   Animation(x=dialog_content.x + 20, duration=0.1) + \
                   Animation(x=dialog_content.x + 10, duration=0.05)

            anim.start(dialog_content)
    def close_dialog(self, *args):
        self.dialog.dismiss(force=True)

    def logout(self):
        self.user_info = None  # Limpa as informações do usuário ao sair
        self.screen_manager.current = 'login'

if __name__ == "__main__":
    GrupoAguia().run()
