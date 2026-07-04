import ssl
import os
import json
ssl._create_default_https_context = ssl._create_unverified_context

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.image import AsyncImage
from kivy.graphics import Color, Rectangle, RoundedRectangle
import random

# Importamos Plyer para abrir la galería nativa del teléfono
from plyer import filechooser

# --- PERSISTENCIA DE DATOS REAL ---
PEDIDOS_FILE = "pedidos.json"

def cargar_pedidos_locales():
    if os.path.exists(PEDIDOS_FILE):
        try:
            with open(PEDIDOS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def guardar_pedidos_locales():
    try:
        with open(PEDIDOS_FILE, "w", encoding="utf-8") as f:
            json.dump(ORDERS_PREPARED, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error al guardar pedidos: {e}")

CART_ITEMS = []
ORDERS_PREPARED = cargar_pedidos_locales()
ULTIMO_PEDIDO = {}

# --- COMPONENTES MODERNOS CON ICONOS REALES ---

class CartButton(Button):
    """Botón móvil plano con radio de curvatura ajustable"""
    def __init__(self, bg_color=(0.9, 0.55, 0.65, 1), text_color=(1, 1, 1, 1), radius=[10], **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0, 0, 0, 0)
        self.color = text_color
        self.bold = True
        self.font_size = 14
        self.font_name = "Roboto"
        self.custom_bg = bg_color
        self.radius = radius
        
        with self.canvas.before:
            Color(*self.custom_bg)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=self.radius)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size


class IconButton(BoxLayout):
    """Un botón que contiene un ícono gráfico real en lugar de texto o emojis"""
    def __init__(self, icon_url, bg_color=(0.75, 0.25, 0.25, 1), radius=[0, 10, 10, 0], on_press_callback=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 12
        
        # Botón invisible de fondo para capturar el click
        self.btn = Button(background_normal='', background_color=(0,0,0,0))
        if on_press_callback:
            self.btn.bind(on_press=on_press_callback)
            
        with self.canvas.before:
            Color(*bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=radius)
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        # Ícono real de alta definición
        self.icon_img = AsyncImage(source=icon_url, allow_stretch=True, keep_ratio=True)
        
        self.add_widget(self.btn)
        self.btn.add_widget(self.icon_img)
        self.btn.bind(pos=self.sync_icon, size=self.sync_icon)

    def update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def sync_icon(self, instance, value):
        self.icon_img.pos = instance.pos
        self.icon_img.size = instance.size


class CardRow(BoxLayout):
    """Fila estilizada con fondo personalizable y esquinas curvas"""
    def __init__(self, bg_color=(1, 1, 1, 1), radius=[10], **kwargs):
        super().__init__(**kwargs)
        self.radius = radius
        with self.canvas.before:
            Color(*bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=self.radius)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size


class ModernSpinner(Spinner):
    """Selector desplegable con esquinas curvas mejorado"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0, 0, 0, 0)
        self.color = (1, 1, 1, 1)
        self.bold = True
        self.font_name = "Roboto"
        
        with self.canvas.before:
            Color(0.25, 0.45, 0.65, 1)  # Azul elegante para el método de pago
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[12])
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size


# --- PANTALLAS ---

class CartScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        
        with self.canvas.before:
            Color(0.98, 0.96, 0.95, 1)
            self.rect_bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)

        self.main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        self.main_layout.add_widget(Label(
            text="Tu Carrito de Compras", font_size=24, font_name="Roboto",
            color=(0.3, 0.15, 0.05, 1), size_hint_y=0.1, bold=True
        ))
        
        scroll = ScrollView(size_hint_y=0.55)
        self.list_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=12, padding=(5, 5, 5, 5))
        self.list_layout.bind(minimum_height=self.list_layout.setter('height'))
        
        total_price = 0.0
        for idx, item in enumerate(CART_ITEMS):
            subtotal = item['price'] * item['qty']
            total_price += subtotal
            
            item_box = CardRow(orientation='horizontal', size_hint_y=None, height=60, spacing=8, padding=(12, 5, 0, 5))
            
            item_box.add_widget(Label(
                text=f"{item['name']}", size_hint_x=0.35, font_name="Roboto",
                color=(0.25, 0.2, 0.2, 1), font_size=15, halign="left", bold=True
            ))
            item_box.add_widget(Label(
                text=f"${item['price']:.2f}", size_hint_x=0.15, font_name="Roboto",
                color=(0.4, 0.2, 0.1, 1), font_size=14
            ))
            
            qty_layout = BoxLayout(size_hint_x=0.35, spacing=4, padding=(0, 4, 0, 4))
            
            btn_minus = IconButton(
                icon_url="https://cdn-icons-png.flaticon.com/512/43/43625.png",
                bg_color=(0.85, 0.6, 0.6, 1), radius=[8],
                on_press_callback=lambda inst, i=idx: self.modify_qty(i, -1)
            )
            
            lbl_qty = Label(text=str(item['qty']), color=(0.3, 0.15, 0.05, 1), font_name="Roboto", bold=True, font_size=15, size_hint_x=0.3)
            
            btn_plus = IconButton(
                icon_url="https://cdn-icons-png.flaticon.com/512/748/748113.png",
                bg_color=(0.6, 0.8, 0.6, 1), radius=[8],
                on_press_callback=lambda inst, i=idx: self.modify_qty(i, 1)
            )
            
            qty_layout.add_widget(btn_minus)
            qty_layout.add_widget(lbl_qty)
            qty_layout.add_widget(btn_plus)
            item_box.add_widget(qty_layout)
            
            btn_delete = IconButton(
                icon_url="https://cdn-icons-png.flaticon.com/512/1214/1214428.png", 
                bg_color=(0.85, 0.3, 0.3, 1), 
                size_hint_x=0.15, 
                radius=[0, 10, 10, 0],
                on_press_callback=lambda instance, i=idx: self.remove_item(i)
            )
            item_box.add_widget(btn_delete)
            
            self.list_layout.add_widget(item_box)
            
        scroll.add_widget(self.list_layout)
        self.main_layout.add_widget(scroll)
        
        pago_box = CardRow(orientation='vertical', padding=15, spacing=8, size_hint_y=0.25, bg_color=(0.94, 0.92, 0.9, 1))
        
        self.label_total = Label(
            text=f"Total a Pagar: ${total_price:.2f}", font_size=22, font_name="Roboto",
            color=(0.15, 0.45, 0.25, 1), size_hint_y=0.4, bold=True
        )
        pago_box.add_widget(self.label_total)

        pago_box.add_widget(Label(
            text="Selecciona Método de Pago:", color=(0.4, 0.2, 0.1, 1), font_name="Roboto",
            size_hint_y=0.2, font_size=14, bold=True
        ))
        
        self.spinner_pago = ModernSpinner(
            text='Efectivo en Caja',
            values=('Efectivo en Caja', 'Transferencia Bancaria', 'Tarjeta de Crédito / Débito'),
            size_hint_y=0.4
        )
        pago_box.add_widget(self.spinner_pago)
        self.main_layout.add_widget(pago_box)
        
        actions = BoxLayout(size_hint_y=0.1, spacing=15)
        
        btn_back = CartButton(text="Seguir Comprando", bg_color=(0.7, 0.6, 0.5, 1), radius=[12])
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'catalog'))
        actions.add_widget(btn_back)
        
        if CART_ITEMS:
            btn_checkout = CartButton(text="Realizar Pedido", bg_color=(0.25, 0.55, 0.75, 1), radius=[12])
            btn_checkout.bind(on_press=lambda x: self.checkout(total_price))
            actions.add_widget(btn_checkout)
            
        self.main_layout.add_widget(actions)
        self.add_widget(self.main_layout)

    def update_bg(self, instance, value):
        self.rect_bg.pos = self.pos
        self.rect_bg.size = self.size

    def modify_qty(self, index, amount):
        CART_ITEMS[index]["qty"] += amount
        if CART_ITEMS[index]["qty"] <= 0:
            CART_ITEMS.pop(index)
        self.on_enter()

    def remove_item(self, index):
        CART_ITEMS.pop(index)
        self.on_enter()

    def checkout(self, total):
        global CART_ITEMS, ULTIMO_PEDIDO
        if CART_ITEMS:
            try:
                from login.login_logic import CURRENT_USER
                user = CURRENT_USER["username"]
            except ImportError:
                user = "Invitado"

            resumen_productos = [f"{item['name']} (x{item['qty']})" for item in CART_ITEMS]
            
            pedido = {
                "id": random.randint(1000, 9999),
                "usuario": user,
                "productos": resumen_productos,
                "total": total,
                "metodo": self.spinner_pago.text,
                "status": "⏳ En Cola",
                "comprobante_path": None
            }
            ORDERS_PREPARED.append(pedido)
            ULTIMO_PEDIDO = pedido
            
            guardar_pedidos_locales()
            CART_ITEMS.clear()
            
            self.manager.get_screen('order_summary').on_enter()
            self.manager.current = 'order_summary'


class OrderSummaryScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        
        with self.canvas.before:
            Color(0.98, 0.96, 0.95, 1)
            self.rect_bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)

        layout = BoxLayout(orientation='vertical', padding=25, spacing=20)
        
        layout.add_widget(Label(
            text="¡TICKET GENERADO EXITOSAMENTE!", font_size=19, font_name="Roboto",
            color=(0.2, 0.55, 0.2, 1), bold=True, size_hint_y=0.1
        ))
        
        if ULTIMO_PEDIDO:
            ticket_box = CardRow(orientation='vertical', padding=20, spacing=8, size_hint_y=0.45, radius=[15])
            
            ticket_box.add_widget(Label(text=f"Pedido #{ULTIMO_PEDIDO['id']}", font_size=24, color=(0.3, 0.15, 0.05, 1), font_name="Roboto", bold=True))
            ticket_box.add_widget(Label(text=f"Total: ${ULTIMO_PEDIDO['total']:.2f}", font_size=20, color=(0.4, 0.2, 0.1, 1), font_name="Roboto", bold=True))
            ticket_box.add_widget(Label(text=f"Método: {ULTIMO_PEDIDO['metodo']}", font_size=15, font_name="Roboto", color=(0.5, 0.5, 0.5, 1)))
            
            if ULTIMO_PEDIDO['metodo'] == 'Transferencia Bancaria':
                ticket_box.add_widget(Label(
                    text="DATOS DE TRANSFERENCIA:\nCLABE: 123456789012345678\nConcepto: Tesoe Pop", 
                    color=(0.2, 0.4, 0.6, 1), halign="center", font_name="Roboto", font_size=14, bold=True
                ))
            else:
                ticket_box.add_widget(Label(
                    text="Tu pedido está en proceso.\nPor favor anexa tu comprobante abajo.", 
                    color=(0.6, 0.4, 0.2, 1), halign="center", font_name="Roboto", font_size=14, bold=True
                ))
                
            layout.add_widget(ticket_box)

        # SECCIÓN DE SUBIDA DE COMPROBANTE NATIVO (Habilitada para todos los métodos de pago)
        upload_box = CardRow(orientation='vertical', padding=15, spacing=10, size_hint_y=0.3, bg_color=(0.92, 0.94, 0.96, 1))
        
        upload_btn_layout = BoxLayout(orientation='horizontal', size_hint_y=0.4, spacing=10)
        
        self.btn_upload = CartButton(text="Abrir Galería...", bg_color=(0.4, 0.5, 0.7, 1), radius=[8])
        # Vinculamos al nuevo método compatible con teléfonos móviles
        self.btn_upload.bind(on_press=self.open_file_chooser)
        
        camera_icon = AsyncImage(source="https://cdn-icons-png.flaticon.com/512/685/685655.png", size_hint_x=0.2)
        
        upload_btn_layout.add_widget(camera_icon)
        upload_btn_layout.add_widget(self.btn_upload)
        
        upload_box.add_widget(Label(
            text="Adjunta una foto de tu comprobante o factura:", 
            color=(0.2, 0.3, 0.4, 1), font_size=13, font_name="Roboto", bold=True, size_hint_y=0.3
        ))
        upload_box.add_widget(upload_btn_layout)
        
        self.lbl_file_status = Label(
            text="Ningún archivo seleccionado", 
            color=(0.5, 0.5, 0.5, 1), font_size=12, font_name="Roboto", size_hint_y=0.3
        )
        upload_box.add_widget(self.lbl_file_status)
        
        layout.add_widget(upload_box)
        
        btn_finish = CartButton(
            text="Volver al Catálogo", bg_color=(0.4, 0.25, 0.15, 1), 
            size_hint_y=0.15, radius=[12]
        )
        btn_finish.bind(on_press=lambda x: setattr(self.manager, 'current', 'catalog'))
        layout.add_widget(btn_finish)
        
        self.add_widget(layout)

    def open_file_chooser(self, instance):
        """Llama a la Galería o Explorador de Archivos Nativo del Sistema Operativo móvil"""
        try:
            # plyer.filechooser abre la interfaz nativa de Android/iOS/Windows/Mac de forma transparente
            filechooser.open_file(
                title="Selecciona tu comprobante",
                filters=[("Imágenes", "*.png", "*.jpg", "*.jpeg"), ("Documentos", "*.pdf")],
                on_selection=self.process_file_selection
            )
        except Exception as e:
            # En caso de error o falta de permisos, muestra el estado de falla en el Label
            self.lbl_file_status.text = f"Error al abrir la galería: {str(e)}"
            self.lbl_file_status.color = (0.8, 0.2, 0.2, 1)

    def process_file_selection(self, selection):
        """Procesa de manera asíncrona la respuesta del archivo seleccionado desde la galería"""
        if selection:
            # Plyer devuelve una lista con las rutas de archivos elegidos
            file_path = selection[0]
            file_name = os.path.basename(file_path)
            
            if ULTIMO_PEDIDO:
                ULTIMO_PEDIDO['comprobante_path'] = file_path
                guardar_pedidos_locales()
            
            self.lbl_file_status.text = f"Archivo cargado exitosamente:\n{file_name}"
            self.lbl_file_status.color = (0.2, 0.6, 0.2, 1)
            self.btn_upload.text = "Cambiar Archivo"

    def update_bg(self, instance, value):
        self.rect_bg.pos = self.pos
        self.rect_bg.size = self.size