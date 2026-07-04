from kivy.app import App
from ui.ui_logic import build_screen_manager

class TesoePopApp(App):
    def build(self):
        # Configuración  de la ventana principal
        self.title = "Tesoe Pop App"
       
        # Retorna el ScreenManager completamente estilizado y unificado
        return build_screen_manager()

if __name__ == '__main__':
    TesoePopApp().run()