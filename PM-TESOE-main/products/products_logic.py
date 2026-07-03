import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import AsyncImage
from kivy.graphics import Color, Rectangle, RoundedRectangle
from cart.cart_logic import ORDERS_PREPARED
from login.login_logic import CURRENT_USER

# --- LISTA DE PRODUCTOS ---
PRODUCTS_LIST = [
    {"id": 1, "name": "Café Americano", "price": 1.5, "category": "Cafés", "stock": 50, "img": "https://images.unsplash.com/photo-1497935586351-b67a49e012bf?w=400"},
    {"id": 2, "name": "Cappuccino Clásico", "price": 2.5, "category": "Cafés", "stock": 30, "img": "https://images.unsplash.com/photo-1534778101976-62847782c213?w=400"},
    {"id": 3, "name": "Latte Vainilla", "price": 2.8, "category": "Cafés", "stock": 25, "img": "https://images.unsplash.com/photo-1570968915860-54d5c301fa9f?w=400"},
    {"id": 4, "name": "Espresso Doble", "price": 1.8, "category": "Cafés", "stock": 40, "img": "https://images.unsplash.com/photo-1510591509098-f4fdc6d0fd24?w=400"},
    {"id": 5, "name": "Mocaccino", "price": 3.0, "category": "Cafés", "stock": 20, "img": "https://images.unsplash.com/photo-1572442388796-11668a67e53d?w=400"},
    {"id": 6, "name": "Frappuccino Caramelo", "price": 3.5, "category": "Bebidas Frías", "stock": 15, "img": "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=400"},
    {"id": 7, "name": "Iced Latte", "price": 2.5, "category": "Bebidas Frías", "stock": 25, "img": "https://images.unsplash.com/photo-1461023058943-0708e52150fe?w=400"},
    {"id": 8, "name": "Té Helado de Limón", "price": 2.0, "category": "Bebidas Frías", "stock": 35, "img": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=400"},
    {"id": 9, "name": "Jugo Natural Naranja", "price": 2.2, "category": "Bebidas Frías", "stock": 10, "img": "https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=400"},
    {"id": 10, "name": "Sándwich de Pavo", "price": 4.5, "category": "Salados", "stock": 12, "img": "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=400"},
    {"id": 11, "name": "Croissant de Jamón", "price": 3.5, "category": "Salados", "stock": 8, "img": "https://images.unsplash.com/photo-1549931319-a545dcf3bc73?w=400"},
    {"id": 12, "name": "Tostadas con Aguacate", "price": 4.0, "category": "Salados", "stock": 15, "img": "https://images.unsplash.com/photo-1541519227354-08fa5d50c44d?w=400"},
    {"id": 13, "name": "Empanada de Carne", "price": 1.5, "category": "Salados", "stock": 0, "img": "https://images.unsplash.com/photo-1626074964464-524637ce5aca?w=400"},
    {"id": 14, "name": "Torta de Fresa", "price": 4.0, "category": "Postres", "stock": 3, "img": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=400"},
    {"id": 15, "name": "Cheesecake Frutos Rojos", "price": 4.5, "category": "Postres", "stock": 5, "img": "https://images.unsplash.com/photo-1533134242443-d4fd215305ad?w=400"},
    {"id": 16, "name": "Torta de Chocolate", "price": 4.0, "category": "Postres", "stock": 0, "img": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=400"},
    {"id": 17, "name": "Donas Glaseadas", "price": 1.5, "category": "Postres", "stock": 15, "img": "https://images.unsplash.com/photo-1551024601-bec78aea704b?w=400"},
    {"id": 18, "name": "Brownie con Nuez", "price": 2.5, "category": "Postres", "stock": 8, "img": "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=400"},
    {"id": 19, "name": "Cupcake Vainilla", "price": 2.0, "category": "Postres", "stock": 12, "img": "https://images.unsplash.com/photo-1576618148400-f54bed99fcfd?w=400"},
    {"id": 20, "name": "Galleta Chispas", "price": 1.2, "category": "Postres", "stock": 20, "img": "https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=400"}
]

SELECTED_PRODUCT = {}
CATEGORIA_ACTUAL = "Todas"
TEXTO_BUSQUEDA = ""
NOTAS_CLIENTE_ACTUAL = "" 

# --- COMPONENTES VISUALES MEJORADOS ---

class CatalogButton(Button):
    def __init__(self, bg_color=(0.9, 0.55, 0.65, 1), text_color=(1, 1, 1, 1), radius=[10], **kwargs):
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
            Color(*self.custom_bg)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=self.radius)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size

class PremiumIconButton(BoxLayout):
    def __init__(self, text="", icon_url="", bg_color=(0.4, 0.25, 0.15, 1), text_color=(1, 1, 1, 1), radius=[10], on_press_callback=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.padding = (12, 6, 12, 6)
        self.spacing = 6
        
        self.btn = Button(background_normal='', background_color=(0,0,0,0))
        if on_press_callback:
            self.btn.bind(on_press=on_press_callback)
            
        with self.canvas.before:
            Color(*bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=radius)
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        self.icon_img = AsyncImage(source=icon_url, size_hint_x=0.3 if text else 1, allow_stretch=True, keep_ratio=True)
        self.add_widget(self.icon_img)
        
        if text:
            # Tamaño de fuente reducido para evitar que se desborde del botón
            self.lbl = Label(text=text, color=text_color, font_name="Roboto", bold=True, font_size=12, size_hint_x=0.7)
            self.add_widget(self.lbl)
            
        self.add_widget(self.btn)
        self.btn.bind(pos=self.sync_trigger, size=self.sync_trigger)

    def update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def sync_trigger(self, instance, value):
        self.btn.pos = self.pos
        self.btn.size = self.size

class CardContainer(BoxLayout):
    def __init__(self, bg_color=(1, 1, 1, 1), radius=[12], **kwargs):
        super().__init__(**kwargs)
        self.radius = radius
        with self.canvas.before:
            # Sombra más sutil y limpia
            Color(0.92, 0.90, 0.88, 1)
            self.border_rect = RoundedRectangle(pos=(self.pos[0]-1, self.pos[1]-2), size=(self.size[0]+2, self.size[1]+3), radius=self.radius)
            Color(*bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=self.radius)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, instance, value):
        self.border_rect.pos = (self.pos[0]-1, self.pos[1]-2)
        self.border_rect.size = (self.size[0]+2, self.size[1]+3)
        self.rect.pos = self.pos
        self.rect.size = self.size

class ModernTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_active = ''
        self.background_color = (1, 1, 1, 1) 
        self.font_name = "Roboto"
        self.foreground_color = (0.2, 0.15, 0.1, 1) 
        self.hint_text_color = (0.6, 0.55, 0.5, 1) 
        self.cursor_color = (0.4, 0.25, 0.15, 1) 
        self.multiline = False
        self.padding = [14, 10, 14, 10]
        self.bind(size=self._actualizar_padding)

        with self.canvas.before:
            Color(0.85, 0.82, 0.8, 1)
            self.bg_border = RoundedRectangle(pos=self.pos, size=self.size, radius=[10])
            Color(1, 1, 1, 1)
            self.rect = RoundedRectangle(pos=(self.pos[0]+1.5, self.pos[1]+1.5), size=(self.size[0]-3, self.size[1]-3), radius=[9])
            
        self.bind(pos=self.update_rect, size=self.update_rect)

    def _actualizar_padding(self, instance, size):
        self.padding[1] = (self.height - self.line_height) / 2
        self.padding[3] = self.padding[1]

    def update_rect(self, instance, value):
        self.bg_border.pos = self.pos
        self.bg_border.size = self.size
        self.rect.pos = (self.pos[0]+1.5, self.pos[1]+1.5)
        self.rect.size = (self.size[0]-3, self.size[1]-3)


# --- PANTALLAS ---

class CatalogScreen(Screen):
    def on_enter(self):
        global CATEGORIA_ACTUAL, TEXTO_BUSQUEDA
        self.clear_widgets()
        
        with self.canvas.before:
            Color(0.98, 0.96, 0.95, 1)
            self.rect_bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)

        main_layout = BoxLayout(orientation='vertical', padding=14, spacing=10)
        
        # Navbar Superior
        nav_bar = BoxLayout(size_hint_y=0.07, spacing=10)
        btn_profile = PremiumIconButton(
            text="Mi Perfil", 
            icon_url="https://cdn-icons-png.flaticon.com/512/1077/1077114.png",
            bg_color=(0.4, 0.25, 0.15, 1),
            on_press_callback=lambda x: self.go_profile()
        )
        btn_cart = PremiumIconButton(
            text="Ver Carrito", 
            icon_url="https://cdn-icons-png.flaticon.com/512/1170/1170678.png",
            bg_color=(0.75, 0.45, 0.35, 1),
            on_press_callback=lambda x: setattr(self.manager, 'current', 'cart')
        )
        nav_bar.add_widget(btn_profile)
        nav_bar.add_widget(btn_cart)
        main_layout.add_widget(nav_bar)

        # Buscador
        search_box = BoxLayout(size_hint_y=0.07)
        self.search_input = ModernTextInput(hint_text="Buscar en la cafetería...", multiline=False)
        self.search_input.text = TEXTO_BUSQUEDA 
        self.search_input.bind(text=self.actualizar_busqueda)
        search_box.add_widget(self.search_input)
        main_layout.add_widget(search_box)
        
        # Categorías
        categoria_layout = BoxLayout(size_hint_y=0.06, spacing=5)
        categorias = ["Todas", "Cafés", "Bebidas Frías", "Salados", "Postres"]
        for cat in categorias:
            is_active = (cat == CATEGORIA_ACTUAL)
            b_color = (0.4, 0.25, 0.15, 1) if is_active else (0.9, 0.85, 0.82, 1)
            t_color = (1, 1, 1, 1) if is_active else (0.4, 0.25, 0.15, 1)
            
            btn_cat = CatalogButton(text=cat, font_size=11, bg_color=b_color, text_color=t_color, radius=[8])
            btn_cat.bold = is_active
            btn_cat.bind(on_press=lambda inst, c=cat: self.filtrar_por_categoria(c))
            categoria_layout.add_widget(btn_cat)
        main_layout.add_widget(categoria_layout)
        
        # ScrollView
        scroll = ScrollView(size_hint_y=0.8)
        product_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=15, padding=(2, 6))
        product_layout.bind(minimum_height=product_layout.setter('height'))
        
        for prod in PRODUCTS_LIST:
            if CATEGORIA_ACTUAL != "Todas" and prod["category"] != CATEGORIA_ACTUAL:
                continue
            if TEXTO_BUSQUEDA.lower() not in prod["name"].lower():
                continue
            
            # --- DISEÑO DE TARJETA MEJORADO ---
            # Altura ajustada para dar respiro, espaciado interno equilibrado
            item_box = CardContainer(orientation='horizontal', size_hint_y=None, height=125, spacing=15, padding=12, radius=[12])
            
            # Imagen ocupa estrictamente un 30% del ancho
            img = AsyncImage(source=prod["img"], size_hint_x=0.3, allow_stretch=True, keep_ratio=True)
            item_box.add_widget(img)
            
            # Contenedor derecho (vertical) para organizar los textos y el botón
            right_layout = BoxLayout(orientation='vertical', spacing=2)
            
            # 1. Título (Alineado a la izquierda)
            lbl_name = Label(text=prod["name"], font_size=16, font_name="Roboto", color=(0.2, 0.1, 0.05, 1), bold=True, halign="left", valign="bottom")
            # El bind de size a text_size es obligatorio en Kivy para que halign funcione
            lbl_name.bind(size=lambda inst, size: setattr(inst, 'text_size', size))
            right_layout.add_widget(lbl_name)
            
            # 2. Categoría y Precio (Lado a lado)
            cat_price_box = BoxLayout(orientation='horizontal')
            lbl_cat = Label(text=f"{prod['category']}", font_size=12, font_name="Roboto", color=(0.5, 0.4, 0.3, 1), halign="left", valign="top")
            lbl_cat.bind(size=lambda inst, size: setattr(inst, 'text_size', size))
            
            lbl_price = Label(text=f"${prod['price']:.2f}", font_size=15, font_name="Roboto", color=(0.15, 0.45, 0.25, 1), bold=True, halign="right", valign="top")
            lbl_price.bind(size=lambda inst, size: setattr(inst, 'text_size', size))
            
            cat_price_box.add_widget(lbl_cat)
            cat_price_box.add_widget(lbl_price)
            right_layout.add_widget(cat_price_box)
            
            # 3. Fila Inferior: Stock y Botón
            bottom_row = BoxLayout(orientation='horizontal', spacing=5)
            
            stock_actual = prod.get("stock", 0)
            if stock_actual == 0:
                lbl_stock = Label(text="¡Agotado!", font_size=12, font_name="Roboto", color=(0.85, 0.2, 0.2, 1), bold=True, halign="left", valign="middle")
            elif stock_actual <= 3:
                lbl_stock = Label(text=f"¡Últimas {stock_actual}!", font_size=12, font_name="Roboto", color=(0.9, 0.45, 0.1, 1), bold=True, halign="left", valign="middle")
            else:
                lbl_stock = Label(text=f"Stock: {stock_actual}", font_size=12, font_name="Roboto", color=(0.5, 0.5, 0.5, 1), halign="left", valign="middle")
            
            lbl_stock.bind(size=lambda inst, size: setattr(inst, 'text_size', size))
            bottom_row.add_widget(lbl_stock)
            
            # Botón estilizado, empaquetado para que no se estire y ocupe solo el espacio necesario
            btn_container = BoxLayout(size_hint_x=0.6, padding=[0, 2, 0, 2])
            p_bg_color = (0.75, 0.45, 0.35, 1) if stock_actual > 0 else (0.75, 0.72, 0.7, 1)
            btn_text = "Pedir" if stock_actual > 0 else "Agotado"
            
            btn_view = PremiumIconButton(
                text=btn_text,
                icon_url="https://cdn-icons-png.flaticon.com/512/4218/4218381.png",
                bg_color=p_bg_color,
                radius=[8],
                on_press_callback=lambda instance, p=prod: self.view_details(p) if p.get("stock", 0) > 0 else None
            )
            btn_container.add_widget(btn_view)
            bottom_row.add_widget(btn_container)
            
            right_layout.add_widget(bottom_row)
            
            # Ensamblar la tarjeta
            item_box.add_widget(right_layout)
            product_layout.add_widget(item_box)
            
        scroll.add_widget(product_layout)
        main_layout.add_widget(scroll)
        self.add_widget(main_layout)

    def update_bg(self, instance, value):
        self.rect_bg.pos = self.pos
        self.rect_bg.size = self.size

    def actualizar_busqueda(self, instance, text):
        global TEXTO_BUSQUEDA
        TEXTO_BUSQUEDA = text
        self.on_enter()
        self.search_input.focus = True 

    def filtrar_por_categoria(self, categoria):
        global CATEGORIA_ACTUAL
        CATEGORIA_ACTUAL = categoria
        self.on_enter()

    def view_details(self, product):
        global SELECTED_PRODUCT, NOTAS_CLIENTE_ACTUAL
        SELECTED_PRODUCT.update(product)
        NOTAS_CLIENTE_ACTUAL = "" 
        self.manager.current = 'product_detail'
        
    def go_profile(self):
        self.manager.get_screen('profile').update_profile()
        self.manager.current = 'profile'


class ProductDetailScreen(Screen):
    def on_enter(self):
        global NOTAS_CLIENTE_ACTUAL
        self.clear_widgets()
        
        with self.canvas.before:
            Color(0.98, 0.96, 0.95, 1)
            self.rect_bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        if SELECTED_PRODUCT:
            # Título (Alineado a la izquierda para mantener la limpieza)
            lbl_title = Label(text=SELECTED_PRODUCT["name"], font_size=24, font_name="Roboto", color=(0.3, 0.15, 0.05, 1), bold=True, halign="center", valign="middle", size_hint_y=0.08)
            lbl_title.bind(size=lambda inst, size: setattr(inst, 'text_size', size))
            layout.add_widget(lbl_title)
            
            layout.add_widget(AsyncImage(source=SELECTED_PRODUCT["img"], size_hint_y=0.32, allow_stretch=True, keep_ratio=True))
            
            # Card de Información
            info_box = CardContainer(orientation='vertical', padding=15, size_hint_y=0.26, spacing=5, radius=[12])
            
            lbl_cat = Label(text=f"Categoría: {SELECTED_PRODUCT['category']}", font_size=13, font_name="Roboto", color=(0.5, 0.4, 0.3, 1), halign="center")
            lbl_cat.bind(size=lambda inst, size: setattr(inst, 'text_size', size))
            info_box.add_widget(lbl_cat)
            
            lbl_price = Label(text=f"${SELECTED_PRODUCT['price']:.2f}", font_size=22, font_name="Roboto", color=(0.15, 0.45, 0.25, 1), bold=True, halign="center")
            lbl_price.bind(size=lambda inst, size: setattr(inst, 'text_size', size))
            info_box.add_widget(lbl_price)
            
            stock_actual = SELECTED_PRODUCT.get("stock", 0)
            txt_stock = f"Disponibles: {stock_actual} unidades" if stock_actual > 3 else f"¡Sólo quedan {stock_actual} unidades!"
            color_stock = (0.15, 0.45, 0.25, 1) if stock_actual > 3 else (0.9, 0.3, 0.1, 1)
            
            lbl_stock = Label(text=txt_stock, font_size=12, font_name="Roboto", color=color_stock, bold=True, halign="center")
            lbl_stock.bind(size=lambda inst, size: setattr(inst, 'text_size', size))
            info_box.add_widget(lbl_stock)
            
            desc_lbl = Label(
                text=f"Disfruta de nuestro {SELECTED_PRODUCT['name']} preparado de forma artesanal con los mejores ingredientes de nuestra cafetería.",
                font_size=12, font_name="Roboto", color=(0.4, 0.35, 0.3, 1), halign="center", valign="top"
            )
            desc_lbl.bind(size=lambda inst, size: setattr(inst, 'text_size', size))
            info_box.add_widget(desc_lbl)
            layout.add_widget(info_box)
            
            # Textos de Especificación alineados
            lbl_especif = Label(text="¿Cómo deseas tu pedido? (Especificaciones)", font_size=13, font_name="Roboto", color=(0.4, 0.25, 0.15, 1), bold=True, halign="left", valign="middle", size_hint_y=0.04)
            lbl_especif.bind(size=lambda inst, size: setattr(inst, 'text_size', size))
            layout.add_widget(lbl_especif)
            
            self.input_notas = ModernTextInput(hint_text="Ej: Leche deslactosada, sin azúcar...", size_hint_y=0.08)
            self.input_notas.bind(text=self.guardar_especificacion)
            layout.add_widget(self.input_notas)
            
            btn_box = BoxLayout(orientation='vertical', spacing=8, size_hint_y=0.22)
            btn_add = PremiumIconButton(
                text="Añadir al Carrito",
                icon_url="https://cdn-icons-png.flaticon.com/512/3514/3514491.png",
                bg_color=(0.35, 0.6, 0.4, 1), radius=[10],
                on_press_callback=self.add_to_cart
            )
            btn_back = CatalogButton(text="Volver al Menú", bg_color=(0.6, 0.55, 0.55, 1), radius=[10])
            btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'catalog'))
            
            btn_box.add_widget(btn_add)
            btn_box.add_widget(btn_back)
            layout.add_widget(btn_box)
            
        self.add_widget(layout)

    def update_bg(self, instance, value):
        self.rect_bg.pos = self.pos
        self.rect_bg.size = self.size

    def guardar_especificacion(self, instance, value):
        global NOTAS_CLIENTE_ACTUAL
        NOTAS_CLIENTE_ACTUAL = value

    def add_to_cart(self, instance):
        from cart.cart_logic import CART_ITEMS
        global NOTAS_CLIENTE_ACTUAL
        encontrado = False
        
        for item in CART_ITEMS:
            if item["id"] == SELECTED_PRODUCT["id"] and item.get("notas", "") == NOTAS_CLIENTE_ACTUAL:
                item["qty"] += 1
                encontrado = True
                break
        if not encontrado:
            nuevo_item = SELECTED_PRODUCT.copy()
            nuevo_item["qty"] = 1
            nuevo_item["notas"] = NOTAS_CLIENTE_ACTUAL 
            CART_ITEMS.append(nuevo_item)
            
        self.manager.current = 'cart'

class ClientOrdersScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        
        with self.canvas.before:
            Color(0.98, 0.96, 0.95, 1)
            self.rect_bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)

        layout = BoxLayout(orientation='vertical', padding=15, spacing=12)
        
        lbl_title = Label(text="Mis Pedidos Solicitados", font_size=22, font_name="Roboto", bold=True, color=(0.3, 0.15, 0.05, 1), halign="center", valign="middle", size_hint_y=0.08)
        lbl_title.bind(size=lambda inst, size: setattr(inst, 'text_size', size))
        layout.add_widget(lbl_title)

        scroll = ScrollView(size_hint_y=0.82)
        orders_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        orders_layout.bind(minimum_height=orders_layout.setter('height'))
        
        mis_pedidos = [o for o in ORDERS_PREPARED if o['usuario'] == CURRENT_USER['username']]

        if not mis_pedidos:
            lbl_empty = Label(text="Aún no tienes pedidos registrados en tu historial.", font_name="Roboto", color=(0.5, 0.5, 0.5, 1), font_size=14, halign="center")
            lbl_empty.bind(size=lambda inst, size: setattr(inst, 'text_size', size))
            orders_layout.add_widget(lbl_empty)
        else:
            for pedido in reversed(mis_pedidos):
                box = CardContainer(orientation='vertical', size_hint_y=None, padding=12, radius=[10], spacing=6)
                
                detalles = f"Ticket #{pedido.get('id', 'N/A')}  |  Total: ${pedido['total']:.2f}\nMétodo: {pedido.get('metodo', 'N/A')}  |  Estado: {pedido['status']}"
                
                lbl_detalles = Label(text=detalles, font_name="Roboto", color=(0.25, 0.2, 0.2, 1), font_size=13, bold=True, halign='left', size_hint_y=None)
                lbl_detalles.bind(texture_size=lambda instance, size: setattr(instance, 'height', size[1]))
                box.bind(width=lambda inv, w: setattr(lbl_detalles, 'text_size', (w - 24, None)))
                box.add_widget(lbl_detalles)
                
                texto_productos = "Detalle:\n"
                if "productos" in pedido:
                    items_desc = [f"• {p['name']} (x{p['qty']}) { '['+p['notas']+']' if p.get('notas') else '' }" for p in pedido["productos"]]
                    texto_productos += "\n".join(items_desc)
                else:
                    texto_productos += "Productos procesados correctamente."
                    
                lbl_productos = Label(text=texto_productos, font_name="Roboto", color=(0.4, 0.35, 0.3, 1), font_size=12, halign='left', size_hint_y=None)
                lbl_productos.bind(texture_size=lambda instance, size: setattr(instance, 'height', size[1]))
                box.bind(width=lambda inv, w: setattr(lbl_productos, 'text_size', (w - 24, None)))
                box.add_widget(lbl_productos)
                
                box.bind(minimum_height=box.setter('height'))
                orders_layout.add_widget(box)

        scroll.add_widget(orders_layout)
        layout.add_widget(scroll)

        btn_back = CatalogButton(text="Volver al Perfil", bg_color=(0.4, 0.25, 0.15, 1), size_hint_y=0.08, radius=[10])
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'profile'))
        layout.add_widget(btn_back)
        self.add_widget(layout)

    def update_bg(self, instance, value):
        self.rect_bg.pos = self.pos
        self.rect_bg.size = self.size