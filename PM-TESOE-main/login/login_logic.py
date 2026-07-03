import ssl
# Asegura la descarga de recursos por HTTPS de forma segura
ssl._create_default_https_context = ssl._create_unverified_context

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import AsyncImage
from kivy.uix.progressbar import ProgressBar
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.clock import Clock
from kivy.animation import Animation

# Estado global de sesión del usuario actual
CURRENT_USER = {"username": "", "role": "client"}

# --- COMPONENTES MÓVILES PREMIUM ---

class ModernTextInput(BoxLayout):
    """Contenedor que dibuja una tarjeta blanca redondeada con sombra y un TextInput limpio adentro"""
    def __init__(self, hint_text="", password=False, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = (15, 6, 15, 6)
        self.size_hint_y = None
        self.height = 55
        
        with self.canvas.before:
            # Sombra sutil
            Color(0.85, 0.82, 0.8, 0.5) 
            self.shadow = RoundedRectangle(pos=(self.x, self.y - 3), size=self.size, radius=[14])
            # Fondo blanco puro
            Color(1, 1, 1, 1)  
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[14])
            
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        self.input = TextInput(
            hint_text=hint_text,
            password=password,
            multiline=False,
            background_normal='',
            background_active='',
            background_color=(0, 0, 0, 0),  # Transparente para usar el RoundedRectangle
            foreground_color=(0.2, 0.2, 0.2, 1),
            hint_text_color=(0.6, 0.6, 0.6, 1),
            cursor_color=(0.3, 0.15, 0.05, 1),
            font_name="Roboto",
            font_size=16,
            padding=(0, 10, 0, 10) # Centrado vertical mejorado
        )
        self.add_widget(self.input)

    def update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.shadow.pos = (self.x, self.y - 3)
        self.shadow.size = self.size

    @property
    def text(self):
        return self.input.text


class ModernButton(Button):
    """Botón con esquinas suavizadas, sombras y feedback de presión"""
    def __init__(self, bg_color=(0.92, 0.45, 0.55, 1), text_color=(1, 1, 1, 1), **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0, 0, 0, 0)
        self.color = text_color
        self.bold = True
        self.font_size = 16
        self.font_name = "Roboto"
        self.custom_bg = bg_color
        
        with self.canvas.before:
            # Sombra del botón
            Color(0.8, 0.75, 0.75, 0.5)
            self.shadow = RoundedRectangle(pos=(self.x, self.y - 4), size=self.size, radius=[14])
            # Fondo del botón
            self.bg_color_inst = Color(*self.custom_bg)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[14])
            
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.bind(state=self.on_state_change)

    def update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.shadow.pos = (self.x, self.y - 4)
        self.shadow.size = self.size

    def on_state_change(self, instance, value):
        # Animación visual al presionar (reduce ligeramente la opacidad)
        if value == 'down':
            self.bg_color_inst.a = 0.8
            self.shadow.pos = (self.x, self.y - 1) # Efecto de hundimiento
        else:
            self.bg_color_inst.a = 1.0
            self.shadow.pos = (self.x, self.y - 4)


# --- PANTALLAS ---

class SplashScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        
        with self.canvas.before:
            # Fondo crema cálido
            Color(0.99, 0.97, 0.95, 1)
            self.rect_bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)
        
        from kivy.uix.floatlayout import FloatLayout
        layout = FloatLayout()
        
        # Logotipo vectorial
        self.logo_galleta = AsyncImage(
            source="https://cdn-icons-png.flaticon.com/512/541/541732.png", 
            size_hint=(None, None),
            size=(140, 140),
            pos_hint={'center_x': 0.5, 'center_y': 0.6}
        )
        layout.add_widget(self.logo_galleta)
        
        # Animación de flotación más suave
        anim_movimiento = Animation(pos_hint={'center_y': 0.63}, duration=1.5, t='in_out_sine') + \
                          Animation(pos_hint={'center_y': 0.57}, duration=1.5, t='in_out_sine')
        anim_movimiento.repeat = True
        anim_movimiento.start(self.logo_galleta)
        
        lbl_title = Label(
            text="Tesoe Pop", 
            font_size=38, 
            bold=True, 
            color=(0.35, 0.2, 0.1, 1),  # Chocolate oscuro
            font_name="Roboto",
            size_hint=(None, None),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        layout.add_widget(lbl_title)
        
        self.progress = ProgressBar(
            max=100, 
            value=0, 
            size_hint=(0.6, None), 
            height=15,
            pos_hint={'center_x': 0.5, 'center_y': 0.22}
        )
        layout.add_widget(self.progress)
        
        self.add_widget(layout)
        
        self.progreso_actual = 0
        Clock.schedule_interval(self.actualizar_carga, 0.03)

    def actualizar_carga(self, dt):
        self.progreso_actual += 1
        self.progress.value = self.progreso_actual
        if self.progreso_actual >= 100:
            Clock.unschedule(self.actualizar_carga)
            Animation.cancel_all(self.logo_galleta)
            self.manager.current = 'login'

    def update_bg(self, instance, value):
        self.rect_bg.pos = self.pos
        self.rect_bg.size = self.size


class LoginScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        
        with self.canvas.before:
            Color(0.99, 0.97, 0.95, 1)
            self.rect_bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)
        
        # Ajuste de espaciado para mejor respiración visual
        layout = BoxLayout(orientation='vertical', padding=[35, 50, 35, 40], spacing=20)
        
        layout.add_widget(Label(
            text="¡Bienvenido a\nTesoe Pop!", 
            font_size=30, 
            bold=True, 
            halign="center",
            color=(0.35, 0.2, 0.1, 1), 
            font_name="Roboto", 
            size_hint_y=0.25
        ))
        
        self.username_input = ModernTextInput(hint_text="Nombre de Usuario")
        self.password_input = ModernTextInput(hint_text="Contraseña", password=True)
        
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        
        self.error_label = Label(text="", color=(0.9, 0.3, 0.3, 1), font_size=14, bold=True, font_name="Roboto", size_hint_y=0.05)
        layout.add_widget(self.error_label)
        
        btn_login = ModernButton(text="Iniciar Sesión", bg_color=(0.92, 0.45, 0.55, 1), size_hint_y=None, height=55)
        btn_login.bind(on_press=self.verify_login)
        
        btn_go_register = ModernButton(text="¿No tienes cuenta? Regístrate", bg_color=(0.85, 0.78, 0.73, 1), text_color=(0.3, 0.15, 0.05, 1), size_hint_y=None, height=55)
        btn_go_register.bind(on_press=lambda x: setattr(self.manager, 'current', 'register'))
        
        layout.add_widget(btn_login)
        layout.add_widget(btn_go_register)
        layout.add_widget(Label(size_hint_y=0.15))
        
        self.add_widget(layout)

    def verify_login(self, instance):
        user = self.username_input.text.strip()
        password = self.password_input.text.strip()
        
        # CREDENCIALES ADMINISTRADOR
        if user == "admin" and password == "1234":
            CURRENT_USER["username"] = "admin"
            CURRENT_USER["role"] = "admin"
            self.manager.current = 'admin_panel'
        elif user != "" and password != "":
            CURRENT_USER["username"] = user
            CURRENT_USER["role"] = "client"
            self.manager.current = 'catalog'
        else:
            self.error_label.text = "Campos incompletos. Intente de nuevo."

    def update_bg(self, instance, value):
        self.rect_bg.pos = self.pos
        self.rect_bg.size = self.size


class RegisterScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        
        with self.canvas.before:
            Color(0.99, 0.97, 0.95, 1)
            self.rect_bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)
        
        layout = BoxLayout(orientation='vertical', padding=[35, 40, 35, 30], spacing=15)
        
        layout.add_widget(Label(
            text="Crear Cuenta", 
            font_size=28, 
            bold=True, 
            color=(0.35, 0.2, 0.1, 1), 
            font_name="Roboto", 
            size_hint_y=0.15
        ))
        
        self.name_in = ModernTextInput(hint_text="Nombre Completo")
        self.email_in = ModernTextInput(hint_text="Correo Electrónico")
        self.phone_in = ModernTextInput(hint_text="Teléfono Celular")
        self.user_in = ModernTextInput(hint_text="Nombre de Usuario")
        self.pass_in = ModernTextInput(hint_text="Contraseña", password=True)
        
        layout.add_widget(self.name_in)
        layout.add_widget(self.email_in)
        layout.add_widget(self.phone_in)
        layout.add_widget(self.user_in)
        layout.add_widget(self.pass_in)
        
        # Espacio extra antes de los botones
        layout.add_widget(Label(size_hint_y=0.05))
        
        btn_create = ModernButton(text="Crear Cuenta", bg_color=(0.4, 0.65, 0.5, 1), size_hint_y=None, height=55)
        btn_create.bind(on_press=self.register_user)
        
        btn_back = ModernButton(text="Volver al Login", bg_color=(0.7, 0.65, 0.65, 1), size_hint_y=None, height=50)
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'login'))
        
        layout.add_widget(btn_create)
        layout.add_widget(btn_back)
        
        self.add_widget(layout)

    def register_user(self, instance):
        if self.user_in.text.strip():
            CURRENT_USER["username"] = self.user_in.text.strip()
            CURRENT_USER["role"] = "client"
            self.manager.current = 'catalog'

    def update_bg(self, instance, value):
        self.rect_bg.pos = self.pos
        self.rect_bg.size = self.size


class ProfileScreen(Screen):
    def on_enter(self):
        self.update_profile()

    def update_profile(self):
        self.clear_widgets()
        
        with self.canvas.before:
            Color(0.99, 0.97, 0.95, 1)
            self.rect_bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)
        
        layout = BoxLayout(orientation='vertical', padding=[35, 40, 35, 40], spacing=20)
        
        layout.add_widget(Label(text="Mi Perfil", font_size=28, bold=True, color=(0.35, 0.2, 0.1, 1), font_name="Roboto", size_hint_y=0.15))
        
        # Tarjeta de perfil más estilizada
        data_box = BoxLayout(orientation='vertical', padding=25, spacing=10, size_hint_y=0.3)
        with data_box.canvas.before:
            Color(0.85, 0.82, 0.8, 0.4) 
            self.card_shadow = RoundedRectangle(pos=(data_box.x, data_box.y - 4), size=data_box.size, radius=[16])
            Color(1, 1, 1, 1)
            self.card_rect = RoundedRectangle(pos=data_box.pos, size=data_box.size, radius=[16])
        data_box.bind(pos=self.update_card, size=self.update_card)
        
        data_box.add_widget(Label(text=f"@{CURRENT_USER['username']}", font_size=22, color=(0.2, 0.2, 0.2, 1), font_name="Roboto", bold=True))
        data_box.add_widget(Label(text=f"Tipo de cuenta: {CURRENT_USER['role'].capitalize()}", font_size=15, font_name="Roboto", color=(0.5, 0.5, 0.5, 1)))
        layout.add_widget(data_box)
        
        layout.add_widget(Label(size_hint_y=0.05)) # Espaciador
        
        btn_orders = ModernButton(text="Ver Mis Pedidos", bg_color=(0.92, 0.45, 0.55, 1), size_hint_y=None, height=55)
        btn_orders.bind(on_press=lambda x: setattr(self.manager, 'current', 'client_orders'))
        
        btn_catalog = ModernButton(text="Ir al Catálogo", bg_color=(0.45, 0.3, 0.2, 1), size_hint_y=None, height=55)
        btn_catalog.bind(on_press=lambda x: setattr(self.manager, 'current', 'catalog'))
        
        btn_logout = ModernButton(text="Cerrar Sesión", bg_color=(0.85, 0.35, 0.35, 1), size_hint_y=None, height=50)
        btn_logout.bind(on_press=self.logout)
        
        layout.add_widget(btn_orders)
        layout.add_widget(btn_catalog)
        layout.add_widget(btn_logout)
        layout.add_widget(Label(size_hint_y=0.1))
        
        self.add_widget(layout)

    def logout(self, instance):
        CURRENT_USER["username"] = ""
        CURRENT_USER["role"] = "client"
        self.manager.current = 'login'

    def update_bg(self, instance, value):
        self.rect_bg.pos = self.pos
        self.rect_bg.size = self.size

    def update_card(self, instance, value):
        if hasattr(self, 'card_rect'):
            self.card_rect.pos = instance.pos
            self.card_rect.size = instance.size
            self.card_shadow.pos = (instance.x, instance.y - 4)
            self.card_shadow.size = instance.size