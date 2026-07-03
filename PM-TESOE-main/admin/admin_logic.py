from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle, RoundedRectangle
from products.products_logic import PRODUCTS_LIST
from cart.cart_logic import ORDERS_PREPARED

# --- VARIABLES GLOBALES DEL SISTEMA ---
PRODUCTO_A_EDITAR = None
ORDERS_HISTORY = []  
TIENDA_ABIERTA = True 

# --- PALETA DE COLORES DE LA TIENDA (REPOSTERÍA PREMIUM) ---
COLOR_FONDO = (0.98, 0.97, 0.95, 1)        # Crema suave / Vainilla
COLOR_SIDEBAR = (0.22, 0.14, 0.12, 1)      # Marrón Chocolate Profundo
COLOR_PRIMARIO = (0.88, 0.44, 0.52, 1)     # Rosa Fresa / Frambuesa (Botones clave)
COLOR_TEXTO_OSCURO = (0.25, 0.18, 0.16, 1) # Café oscuro para textos legibles
COLOR_CARD_BG = (1, 1, 1, 1)               # Blanco puro para las tarjetas
COLOR_GRIS_SUAVE = (0.65, 0.60, 0.58, 1)   # Gris arcilla para cancelar/secundarios

# --- COMPONENTES ESTILIZADOS ---

class AdminTextInput(BoxLayout):
    """Entrada de texto moderna con bordes muy suaves y limpios"""
    def __init__(self, hint_text="", text="", **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = (12, 4, 12, 4)
        self.size_hint_y = None
        self.height = 45 
        with self.canvas.before:
            # Sombra sutil difuminada
            Color(0.2, 0.1, 0.1, 0.06)
            self.shadow = RoundedRectangle(pos=(self.x, self.y - 2), size=self.size, radius=[10])
            # Fondo del campo
            Color(1, 1, 1, 1)  
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[10])
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.input = TextInput(
            text=text, hint_text=hint_text, multiline=False, background_normal='',
            background_active='', background_color=(0, 0, 0, 0), foreground_color=COLOR_TEXTO_OSCURO,
            hint_text_color=(0.65, 0.6, 0.58, 1), cursor_color=COLOR_PRIMARIO,
            font_name="Roboto", font_size=14, padding=(0, 9, 0, 6)
        )
        self.add_widget(self.input)

    def update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.shadow.pos = (self.x, self.y - 2)
        self.shadow.size = self.size

    @property
    def text(self): return self.input.text

    @text.setter
    def text(self, value): self.input.text = value


class AdminButton(Button):
    """Botón con diseño curvo premium y feedback visual al presionar"""
    def __init__(self, bg_color=COLOR_PRIMARIO, text_color=(1, 1, 1, 1), radius=[10], **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0, 0, 0, 0)
        self.color = text_color
        self.bold = True
        self.font_size = 13
        self.font_name = "Roboto"
        self.custom_bg = bg_color
        self.radius = radius
        with self.canvas.before:
            Color(0.2, 0.1, 0.1, 0.1)
            self.shadow = RoundedRectangle(pos=(self.x, self.y - 2), size=self.size, radius=self.radius)
            self.bg_color_inst = Color(*self.custom_bg)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=self.radius)
        self.bind(pos=self.update_rect, size=self.update_rect, state=self.on_state_change)

    def update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.shadow.pos = (self.x, self.y - 2)
        self.shadow.size = self.size
        
    def on_state_change(self, instance, value):
        if value == 'down':
            self.bg_color_inst.a = 0.85
            self.shadow.pos = (self.x, self.y - 1)
        else:
            self.bg_color_inst.a = 1.0
            self.shadow.pos = (self.x, self.y - 2)


class CardRow(BoxLayout):
    """Tarjetas contenedoras blancas para listas del inventario e historial"""
    def __init__(self, bg_color=COLOR_CARD_BG, radius=[10], **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.2, 0.1, 0.1, 0.05)
            self.shadow = RoundedRectangle(pos=(self.x, self.y - 2), size=self.size, radius=radius)
            Color(*bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=radius)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.shadow.pos = (self.x, self.y - 2)
        self.shadow.size = self.size


class MetricCard(BoxLayout):
    """Tarjetas superiores para mostrar estadísticas de forma elegante"""
    def __init__(self, title, value, color_text, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = (12, 10, 12, 10)
        with self.canvas.before:
            Color(0.2, 0.1, 0.1, 0.05)
            self.shadow = RoundedRectangle(pos=(self.x, self.y - 2), size=self.size, radius=[12])
            Color(1, 1, 1, 1)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[12])
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.add_widget(Label(text=title.upper(), font_size=11, color=(0.55, 0.5, 0.48, 1), bold=True, font_name="Roboto", size_hint_y=0.35))
        self.add_widget(Label(text=value, font_size=20, color=color_text, bold=True, font_name="Roboto", size_hint_y=0.65))

    def update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.shadow.pos = (self.x, self.y - 2)
        self.shadow.size = self.size


# --- INTERFAZ PRINCIPAL DEL PANEL ---

class AdminPanelScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        self.vista_actual = "dashboard"
        
        # Fondo general estilo vainilla
        with self.canvas.before:
            Color(*COLOR_FONDO) 
            self.rect_bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)

        # Contenedor de doble columna (Escritorio / POS)
        self.main_layout = BoxLayout(orientation='horizontal')
        
        # 1. MENÚ LATERAL (Chocolate elegante)
        self.sidebar = BoxLayout(orientation='vertical', size_hint_x=0.22, padding=(12, 20, 12, 20), spacing=8)
        with self.sidebar.canvas.before:
            Color(*COLOR_SIDEBAR) 
            self.sidebar_bg = Rectangle(pos=self.sidebar.pos, size=self.sidebar.size)
        self.sidebar.bind(pos=self.update_sidebar_bg, size=self.update_sidebar_bg)
        
        self.sidebar.add_widget(Label(text="DULCE CONTROL", font_size=16, bold=True, color=(0.98, 0.92, 0.88, 1), size_hint_y=None, height=40))
        self.sidebar.add_widget(Label(size_hint_y=None, height=10)) # Separador
        
        # Botones del menú lateral usando caracteres tipográficos estables e impecables
        self.btn_dash = AdminButton(text="  Resumen", bg_color=(0.28, 0.19, 0.17, 1), size_hint_y=None, height=45)
        self.btn_dash.bind(on_press=lambda x: self.cambiar_vista("dashboard"))
        
        self.btn_inv = AdminButton(text="  Inventario", bg_color=(0.28, 0.19, 0.17, 1), size_hint_y=None, height=45)
        self.btn_inv.bind(on_press=lambda x: self.cambiar_vista("inventario"))
        
        self.btn_orders = AdminButton(text="  Pedidos en Cola", bg_color=(0.28, 0.19, 0.17, 1), size_hint_y=None, height=45)
        self.btn_orders.bind(on_press=lambda x: self.cambiar_vista("pedidos"))
        
        self.btn_hist = AdminButton(text="  Historial Ventas", bg_color=(0.28, 0.19, 0.17, 1), size_hint_y=None, height=45)
        self.btn_hist.bind(on_press=lambda x: self.cambiar_vista("historial"))
        
        self.btn_set = AdminButton(text="  Ajustes Local", bg_color=(0.28, 0.19, 0.17, 1), size_hint_y=None, height=45)
        self.btn_set.bind(on_press=lambda x: self.cambiar_vista("ajustes"))

        self.sidebar.add_widget(self.btn_dash)
        self.sidebar.add_widget(self.btn_inv)
        self.sidebar.add_widget(self.btn_orders)
        self.sidebar.add_widget(self.btn_hist)
        self.sidebar.add_widget(self.btn_set)
        self.sidebar.add_widget(Label(size_hint_y=1.0)) # Empuja el botón de salida al fondo
        
        btn_logout = AdminButton(text="Cerrar Sesión", bg_color=(0.65, 0.25, 0.25, 1), size_hint_y=None, height=42)
        btn_logout.bind(on_press=self.logout)
        self.sidebar.add_widget(btn_logout)

        self.main_layout.add_widget(self.sidebar)

        # 2. ÁREA DE CONTENIDO PRINCIPAL (Derecha)
        self.content_area = BoxLayout(orientation='vertical', size_hint_x=0.78, padding=[25, 20, 25, 20], spacing=15)
        self.main_layout.add_widget(self.content_area)
        
        self.add_widget(self.main_layout)
        self.cambiar_vista("dashboard") 

    def update_bg(self, instance, value):
        self.rect_bg.pos = self.pos
        self.rect_bg.size = self.size

    def update_sidebar_bg(self, instance, value):
        self.sidebar_bg.pos = self.sidebar.pos
        self.sidebar_bg.size = self.sidebar.size

    def cambiar_vista(self, vista):
        """Maneja la transición visual limpia entre secciones"""
        self.content_area.clear_widgets()
        self.vista_actual = vista
        
        # Resetear colores de enfoque en el menú
        for btn in [self.btn_dash, self.btn_inv, self.btn_orders, self.btn_hist, self.btn_set]:
            btn.bg_color_inst.rgb = (0.28, 0.19, 0.17)
            
        if vista == "dashboard":
            self.btn_dash.bg_color_inst.rgb = COLOR_PRIMARIO[:3]
            self.render_dashboard()
        elif vista == "inventario":
            self.btn_inv.bg_color_inst.rgb = COLOR_PRIMARIO[:3]
            self.render_inventory()
        elif vista == "pedidos":
            self.btn_orders.bg_color_inst.rgb = COLOR_PRIMARIO[:3]
            self.render_orders()
        elif vista == "historial":
            self.btn_hist.bg_color_inst.rgb = COLOR_PRIMARIO[:3]
            self.render_history()
        elif vista == "ajustes":
            self.btn_set.bg_color_inst.rgb = COLOR_PRIMARIO[:3]
            self.render_settings()

    # --- PANELES INTERNOS DE CONTENIDO ---

    def render_dashboard(self):
        self.content_area.add_widget(Label(
            text="Resumen Operativo", font_size=24, color=COLOR_TEXTO_OSCURO, 
            bold=True, size_hint_y=None, height=35, halign="left"
        ))
        
        total_ganancias = sum(float(order.get("total", 0)) for order in ORDERS_HISTORY)
        pedidos_activos = len(ORDERS_PREPARED)
        
        dash_box = BoxLayout(size_hint_y=None, height=90, spacing=15)
        dash_box.add_widget(MetricCard(title="Ventas Totales", value=f"${total_ganancias:.2f}", color_text=(0.2, 0.55, 0.3, 1)))
        dash_box.add_widget(MetricCard(title="Pedidos Activos", value=f"{pedidos_activos} en cola", color_text=COLOR_PRIMARIO))
        dash_box.add_widget(MetricCard(title="Productos", value=f"{len(PRODUCTS_LIST)} ítems", color_text=(0.25, 0.45, 0.65, 1)))
        
        self.content_area.add_widget(dash_box)
        self.content_area.add_widget(Label(size_hint_y=1.0)) # Espacio limpio inferior

    def render_inventory(self):
        global PRODUCTO_A_EDITAR
        form_title = "Editar Postre Seleccionado" if PRODUCTO_A_EDITAR else "Añadir Nuevo Postre al Catálogo"
        
        self.content_area.add_widget(Label(
            text=form_title, font_size=16, color=COLOR_TEXTO_OSCURO, bold=True, size_hint_y=None, height=25
        ))
        
        # Grid ordenado de entradas de texto
        form_row1 = BoxLayout(size_hint_y=None, height=45, spacing=12)
        self.name_in = AdminTextInput(hint_text="Nombre del postre (Ej: Cupcake Vainilla)")
        self.price_in = AdminTextInput(hint_text="Precio de venta ($)")
        form_row1.add_widget(self.name_in)
        form_row1.add_widget(self.price_in)
        
        form_row2 = BoxLayout(size_hint_y=None, height=45, spacing=12)
        self.category_in = AdminTextInput(hint_text="Categoría (Ej: Tortas, Galletas)")
        self.stock_in = AdminTextInput(hint_text="Stock Inicial disponible")
        form_row2.add_widget(self.category_in)
        form_row2.add_widget(self.stock_in)
        
        self.content_area.add_widget(form_row1)
        self.content_area.add_widget(form_row2)
        
        if PRODUCTO_A_EDITAR:
            self.name_in.text = PRODUCTO_A_EDITAR.get("name", "")
            self.price_in.text = str(PRODUCTO_A_EDITAR.get("price", ""))
            self.category_in.text = PRODUCTO_A_EDITAR.get("category", "")
            self.stock_in.text = str(PRODUCTO_A_EDITAR.get("stock", "10"))
        
        # Acciones del Formulario
        btn_layout = BoxLayout(size_hint_y=None, height=42, spacing=12)
        if PRODUCTO_A_EDITAR:
            btn_save = AdminButton(text="Actualizar Cambios", bg_color=COLOR_PRIMARIO)
            btn_save.bind(on_press=self.actualizar_producto)
            btn_cancel = AdminButton(text="Cancelar", bg_color=COLOR_GRIS_SUAVE)
            btn_cancel.bind(on_press=self.cancelar_edicion)
            btn_layout.add_widget(btn_save)
            btn_layout.add_widget(btn_cancel)
        else:
            btn_add = AdminButton(text="Registrar en Inventario", bg_color=COLOR_PRIMARIO)
            btn_add.bind(on_press=self.agregar_producto)
            btn_layout.add_widget(btn_add)
            
        self.content_area.add_widget(btn_layout)
        
        # Lista del Catálogo
        self.content_area.add_widget(Label(text="Catálogo de Productos Disponibles", font_size=15, color=COLOR_TEXTO_OSCURO, bold=True, size_hint_y=None, height=25))
        scroll_inv = ScrollView(size_hint_y=1.0)
        inv_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=8, padding=(2, 2, 2, 10))
        inv_layout.bind(minimum_height=inv_layout.setter('height'))
        
        for prod in PRODUCTS_LIST:
            if "stock" not in prod: prod["stock"] = 10
            if "active" not in prod: prod["active"] = True
            
            p_box = CardRow(orientation='horizontal', size_hint_y=None, height=52, spacing=6, padding=(15, 0, 0, 0))
            estado = "[color=44aa66]Visible[/color]" if prod["active"] else "[color=aa5555]Oculto[/color]"
            
            p_box.add_widget(Label(
                text=f"[b]{prod['name']}[/b]  -  ${prod['price']:.2f}\n[size=12]Stock: {prod['stock']} | Estado: {estado}[/size]", 
                markup=True, color=COLOR_TEXTO_OSCURO, font_size=13, halign="left", size_hint_x=0.55
            ))
            
            btn_toggle = AdminButton(text="Pausar" if prod["active"] else "Activar", size_hint_x=0.15, bg_color=(0.45, 0.5, 0.55, 1))
            btn_toggle.bind(on_press=lambda inst, p=prod: self.toggle_producto(p))
            
            btn_edit = AdminButton(text="Editar", size_hint_x=0.15, bg_color=(0.85, 0.62, 0.3, 1))
            btn_edit.bind(on_press=lambda inst, p=prod: self.cargar_para_editar(p))
            
            btn_del = AdminButton(text="Borrar", size_hint_x=0.15, bg_color=(0.78, 0.3, 0.3, 1), radius=[0, 10, 10, 0])
            btn_del.bind(on_press=lambda inst, p=prod: self.eliminar_producto(p))
            
            p_box.add_widget(btn_toggle)
            p_box.add_widget(btn_edit)
            p_box.add_widget(btn_del)
            inv_layout.add_widget(p_box)
            
        scroll_inv.add_widget(inv_layout)
        self.content_area.add_widget(scroll_inv)

    def render_orders(self):
        self.content_area.add_widget(Label(
            text="Pedidos Entrantes y Producción", font_size=18, color=COLOR_TEXTO_OSCURO, bold=True, size_hint_y=None, height=30
        ))
        
        if not ORDERS_PREPARED:
            self.content_area.add_widget(Label(text="No tienes pedidos pendientes en este momento.", color=COLOR_GRIS_SUAVE, font_size=14))
            return
            
        scroll_orders = ScrollView(size_hint_y=1.0)
        orders_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10, padding=(2, 2, 2, 10))
        orders_layout.bind(minimum_height=orders_layout.setter('height'))
        
        for idx, order in enumerate(ORDERS_PREPARED):
            o_box = CardRow(orientation='horizontal', size_hint_y=None, height=65, spacing=8, padding=(15, 0, 0, 0))
            status = order.get("status", "Nuevo")
            
            txt_pedido = f"[b]Pedido #{order.get('id', '?')}[/b] - Cliente: @{order.get('usuario', 'Usuario')}\nEstado actual: [color=cc6677][b]{status}[/b][/color]"
            
            o_box.add_widget(Label(
                text=txt_pedido, markup=True, color=COLOR_TEXTO_OSCURO, font_size=13, halign="left", size_hint_x=0.65
            ))
            
            if "⏳" in status or status == "Nuevo" or "Pendiente" in status:
                btn = AdminButton(text="Preparar", size_hint_x=0.35, bg_color=(0.25, 0.5, 0.7, 1), radius=[0, 10, 10, 0])
                btn.bind(on_press=lambda inst, i=idx: self.cambiar_estado_pedido(i, "En Cocina"))
            elif "Cocina" in status:
                btn = AdminButton(text="Terminar", size_hint_x=0.35, bg_color=(0.3, 0.65, 0.4, 1), radius=[0, 10, 10, 0])
                btn.bind(on_press=lambda inst, i=idx: self.cambiar_estado_pedido(i, "Listo para retirar"))
            else:
                btn = AdminButton(text="Entregar y Cerrar", size_hint_x=0.35, bg_color=COLOR_PRIMARIO, radius=[0, 10, 10, 0])
                btn.bind(on_press=lambda inst, i=idx: self.despachar_pedido(i))
                
            o_box.add_widget(btn)
            orders_layout.add_widget(o_box)
            
        scroll_orders.add_widget(orders_layout)
        self.content_area.add_widget(scroll_orders)

    def render_history(self):
        self.content_area.add_widget(Label(
            text="Historial Cronológico de Ventas Concluidas", font_size=18, color=COLOR_TEXTO_OSCURO, bold=True, size_hint_y=None, height=30
        ))
        
        if not ORDERS_HISTORY:
            self.content_area.add_widget(Label(text="El historial está vacío. Las ventas aparecerán aquí cuando despaches pedidos.", color=COLOR_GRIS_SUAVE, font_size=14))
            return
            
        scroll = ScrollView(size_hint_y=1.0)
        layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=8, padding=(2, 2, 2, 10))
        layout.bind(minimum_height=layout.setter('height'))
        
        for order in reversed(ORDERS_HISTORY): 
            box = CardRow(orientation='horizontal', size_hint_y=None, height=45, padding=(15, 0, 15, 0))
            box.add_widget(Label(text=f"Pedido #{order.get('id','?')}  |  Cliente: {order.get('usuario','')}  |  Total Facturado: [b]${order.get('total','0')}[/b]", markup=True, color=COLOR_TEXTO_OSCURO, halign="left"))
            layout.add_widget(box)
            
        scroll.add_widget(layout)
        self.content_area.add_widget(scroll)

    def render_settings(self):
        self.content_area.add_widget(Label(
            text="Configuración Operativa de la Tienda", font_size=18, color=COLOR_TEXTO_OSCURO, bold=True, size_hint_y=None, height=30
        ))
        
        box = CardRow(orientation='horizontal', size_hint_y=None, height=65, padding=(20, 0, 20, 0))
        box.add_widget(Label(text="Recepción automática de pedidos en la aplicación", color=COLOR_TEXTO_OSCURO, font_size=14, halign="left", size_hint_x=0.7))
        
        estado_txt = "TIENDA ABIERTA" if TIENDA_ABIERTA else "TIENDA CERRADA"
        color_btn = (0.25, 0.6, 0.35, 1) if TIENDA_ABIERTA else (0.75, 0.25, 0.25, 1)
        
        btn_toggle = AdminButton(text=estado_txt, bg_color=color_btn, size_hint_x=0.3)
        btn_toggle.bind(on_press=self.toggle_tienda)
        box.add_widget(btn_toggle)
        
        self.content_area.add_widget(box)
        self.content_area.add_widget(Label(size_hint_y=1.0))

    # --- LÓGICA DE CONTROL (RESPETADA AL 100%) ---

    def toggle_tienda(self, instance):
        global TIENDA_ABIERTA
        TIENDA_ABIERTA = not TIENDA_ABIERTA
        self.cambiar_vista("ajustes")

    def cambiar_estado_pedido(self, index, nuevo_estado):
        ORDERS_PREPARED[index]["status"] = nuevo_estado
        self.cambiar_vista("pedidos")

    def despachar_pedido(self, index):
        pedido = ORDERS_PREPARED.pop(index)
        pedido["status"] = "Entregado"
        ORDERS_HISTORY.append(pedido)
        self.cambiar_vista("pedidos")

    def agregar_producto(self, instance):
        if self.name_in.text and self.price_in.text:
            try:
                new_p = {
                    "id": len(PRODUCTS_LIST) + 1,
                    "name": self.name_in.text,
                    "price": float(self.price_in.text),
                    "category": self.category_in.text if self.category_in.text else "General",
                    "stock": int(self.stock_in.text) if self.stock_in.text else 10,
                    "active": True
                }
                PRODUCTS_LIST.append(new_p)
                self.cambiar_vista("inventario")
            except ValueError:
                self.price_in.text = "Error numérico"

    def cargar_para_editar(self, producto):
        global PRODUCTO_A_EDITAR
        PRODUCTO_A_EDITAR = producto
        self.cambiar_vista("inventario")

    def actualizar_producto(self, instance):
        global PRODUCTO_A_EDITAR
        if PRODUCTO_A_EDITAR and self.name_in.text and self.price_in.text:
            try:
                PRODUCTO_A_EDITAR["name"] = self.name_in.text
                PRODUCTO_A_EDITAR["price"] = float(self.price_in.text)
                PRODUCTO_A_EDITAR["category"] = self.category_in.text
                PRODUCTO_A_EDITAR["stock"] = int(self.stock_in.text)
                PRODUCTO_A_EDITAR = None
                self.cambiar_vista("inventario")
            except ValueError:
                self.price_in.text = "Error numérico"

    def cancelar_edicion(self, instance):
        global PRODUCTO_A_EDITAR
        PRODUCTO_A_EDITAR = None
        self.cambiar_vista("inventario")

    def toggle_producto(self, producto):
        if "active" in producto:
            producto["active"] = not producto["active"]
        else:
            producto["active"] = False
        self.cambiar_vista("inventario")

    def eliminar_producto(self, producto):
        if producto in PRODUCTS_LIST:
            PRODUCTS_LIST.remove(producto)
            self.cambiar_vista("inventario")

    def logout(self, instance):
        global PRODUCTO_A_EDITAR
        PRODUCTO_A_EDITAR = None
        self.manager.current = "login"