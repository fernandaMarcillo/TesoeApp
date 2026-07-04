import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout  
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import AsyncImage
from kivy.graphics import Color, Rectangle, RoundedRectangle
from cart.cart_logic import ORDERS_PREPARED
from login.login_logic import CURRENT_USER

# --- LISTA DE PRODUCTOS (IMÁGENES DE POSTRES ACTUALIZADAS) ---
PRODUCTS_LIST = [
    {"id": 1, "name": "Café Americano", "price": 1.5, "category": "Cafés", "stock": 50, "img": "imagenes/cafe_americano.jpg"},
    {"id": 2, "name": "Cappuccino Clásico", "price": 2.5, "category": "Cafés", "stock": 30, "img": "imagenes/capuchino_de_vainilla.jpg"},
    {"id": 3, "name": "Latte Vainilla", "price": 2.8, "category": "Cafés", "stock": 25, "img": "imagenes/latte_vainilla.jpg"},
    {"id": 4, "name": "Espresso Doble", "price": 1.8, "category": "Cafés", "stock": 40, "img": "imagenes/espress.jpg"},
    {"id": 5, "name": "Mocaccino", "price": 3.0, "category": "Cafés", "stock": 20, "img": "imagenes/mocaccino.jpg"},
    {"id": 6, "name": "Frappuccino Caramelo", "price": 3.5, "category": "Bebidas Frías", "stock": 15, "img": "imagenes/frape.jpg"},
    {"id": 7, "name": "Iced Latte", "price": 2.5, "category": "Bebidas Frías", "stock": 25, "img": "imagenes/icelate.jpg"},
    {"id": 8, "name": "Té Helado de Limón", "price": 2.0, "category": "Bebidas Frías", "stock": 35, "img": "imagenes/te_helado.jpg"},
    {"id": 9, "name": "Jugo Natural Naranja", "price": 2.2, "category": "Bebidas Frías", "stock": 10, "img": "imagenes/jugo.jpg"},    
    {"id": 10, "name": "Tostadas con Aguacate", "price": 4.0, "category": "Salados", "stock": 15, "img": "imagenes/tostadaAguacate.jpg"},
    {"id": 11, "name": "Empanada de Carne", "price": 1.5, "category": "Salados", "stock": 0, "img": "imagenes/empanada_de_carne.jpg"},
    {"id": 12, "name": "Torta de Fresa", "price": 4.0, "category": "Postres", "stock": 3, "img": "imagenes/tortafresa.jpg"}, 
    {"id": 13, "name": "Cheesecake Frutos Rojos", "price": 4.5, "category": "Postres", "stock": 5, "img": "imagenes/cheesecakeFrutosRojos.jpg"}, 
    {"id": 14, "name": "Torta de Chocolate", "price": 4.0, "category": "Postres", "stock": 0, "img": "imagenes/tortachcocolate.jpg"}, 
    {"id": 15, "name": "Donas Glaseadas", "price": 1.5, "category": "Postres", "stock": 15, "img": "imagenes/DONAS.jpg"},
    {"id": 16, "name": "Brownie con Nuez", "price": 2.5, "category": "Postres", "stock": 8, "img": "imagenes/brownies.jpg"},
    {"id": 17, "name": "Cupcake Vainilla", "price": 2.0, "category": "Postres", "stock": 12, "img": "imagenes/cupcakes.jpg"},
    {"id": 19, "name": "Galleta Chispas", "price": 1.2, "category": "Postres", "stock": 20, "img": "imagenes/galletas.jpg"}
]

SELECTED_PRODUCT = {}
CATEGORIA_ACTUAL = "Todas"
TEXTO_BUSQUEDA = ""
NOTAS_CLIENTE_ACTUAL = "" 

# --- COMPONENTES VISUALES ---

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
        self.padding = (8, 4, 8, 4)
        self.spacing = 4
        
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
            self.lbl = Label(text=text, color=text_color, font_name="Roboto", bold=True, font_size=11, size_hint_x=0.7)
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
    def __init__(self, bg_color=(1, 1, 1, 1), radius=[16], **kwargs):
        super().__init__(**kwargs)
        self.radius = radius
        with self.canvas.before:
            Color(0.88, 0.85, 0.82, 0.6)
            self.shadow_rect = RoundedRectangle(pos=(self.pos[0]-2, self.pos[1]-3), size=(self.size[0]+4, self.size[1]+5), radius=self.radius)
            Color(*bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=self.radius)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, instance, value):
        self.shadow_rect.pos = (self.pos[0]-2, self.pos[1]-3)
        self.shadow_rect.size = (self.size[0]+4, self.size[1]+5)
        self.rect.pos = self.pos
        self.rect.size = self.size

class ModernTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_active = ''
        self.background_color = (0, 0, 0, 0) # Fondo manejado por la tarjeta contenedora
        self.font_name = "Roboto"
        self.foreground_color = (0.2, 0.15, 0.1, 1) 
        self.hint_text_color = (0.6, 0.55, 0.5, 1) 
        self.cursor_color = (0.4, 0.25, 0.15, 1) 
        self.multiline = False
        self.padding = [12, 10, 12, 10]
        self.bind(size=self._actualizar_padding)

    def _actualizar_padding(self, instance, size):
        self.padding[1] = (self.height - self.line_height) / 2
        self.padding[3] = self.padding[1]

class AppNavBar(BoxLayout):
    def __init__(self, screen_manager, active_tab="menu", **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = 0.08
        self.spacing = 8
        self.padding = [10, 6, 10, 6]
        
        with self.canvas.before:
            Color(1, 1, 1, 1) 
            self.bg = Rectangle(pos=self.pos, size=self.size)
            Color(0.9, 0.86, 0.83, 1) 
            self.line = Rectangle(pos=(self.pos[0], self.pos[1] + self.size[1] - 1), size=(self.size[0], 1))
        self.bind(pos=self.update_bg, size=self.update_bg)
        
        c_menu = (0.4, 0.25, 0.15, 1) if active_tab == "menu" else (0.7, 0.65, 0.6, 1)
        c_cart = (0.4, 0.25, 0.15, 1) if active_tab == "cart" else (0.7, 0.65, 0.6, 1)
        c_profile = (0.4, 0.25, 0.15, 1) if active_tab == "profile" else (0.7, 0.65, 0.6, 1)
        
        btn_menu = PremiumIconButton(text="Menú", icon_url="https://cdn-icons-png.flaticon.com/512/2311/2311524.png", bg_color=c_menu, radius=[12], on_press_callback=lambda x: setattr(screen_manager, 'current', 'catalog'))
        btn_cart = PremiumIconButton(text="Carrito", icon_url="https://cdn-icons-png.flaticon.com/512/1170/1170678.png", bg_color=c_cart, radius=[12], on_press_callback=lambda x: setattr(screen_manager, 'current', 'cart'))
        btn_profile = PremiumIconButton(text="Perfil", icon_url="https://cdn-icons-png.flaticon.com/512/1077/1077114.png", bg_color=c_profile, radius=[12], on_press_callback=lambda x: self.go_profile(screen_manager))
        
        self.add_widget(btn_menu)
        self.add_widget(btn_cart)
        self.add_widget(btn_profile)

    def update_bg(self, instance, value):
        self.bg.pos = self.pos
        self.bg.size = self.size
        self.line.pos = (self.pos[0], self.pos[1] + self.size[1] - 1)
        self.line.size = (self.size[0], 1)

    def go_profile(self, manager):
        manager.get_screen('profile').update_profile()
        manager.current = 'profile'


# --- PANTALLAS ---

class CatalogScreen(Screen):
    def on_enter(self):
        global CATEGORIA_ACTUAL, TEXTO_BUSQUEDA
        self.clear_widgets()
        
        with self.canvas.before:
            Color(0.97, 0.95, 0.93, 1) 
            self.rect_bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)

        main_layout = BoxLayout(orientation='vertical')
        content_layout = BoxLayout(orientation='vertical', padding=[14, 14, 14, 4], spacing=10)

        # --- BUSCADOR DENTRO DE UNA TARJETA DE TEXTO PREMIUM ---
        search_card = CardContainer(orientation='horizontal', size_hint_y=0.075, padding=[12, 2, 12, 2], radius=[16], bg_color=(1, 1, 1, 1))
        
        self.search_input = ModernTextInput(hint_text="🔍 Buscar café, postres, salados...")
        self.search_input.text = TEXTO_BUSQUEDA 
        self.search_input.bind(text=self.actualizar_busqueda)
        
        search_card.add_widget(self.search_input)
        content_layout.add_widget(search_card)
        
        # Filtro de Categorías
        categoria_layout = BoxLayout(size_hint_y=0.06, spacing=6)
        categorias = ["Todas", "Cafés", "Bebidas Frías", "Salados", "Postres"]
        for cat in categorias:
            is_active = (cat == CATEGORIA_ACTUAL)
            b_color = (0.4, 0.25, 0.15, 1) if is_active else (1, 1, 1, 1)
            t_color = (1, 1, 1, 1) if is_active else (0.4, 0.25, 0.15, 1)
            
            btn_cat = CatalogButton(text=cat, font_size=11, bg_color=b_color, text_color=t_color, radius=[14])
            btn_cat.bold = is_active
            btn_cat.bind(on_press=lambda inst, c=cat: self.filtrar_por_categoria(c))
            categoria_layout.add_widget(btn_cat)
        content_layout.add_widget(categoria_layout)
        
        # --- CUADRÍCULA DIRECTA USANDO SCROLLVIEW + GRIDLAYOUT ---
        scroll = ScrollView(size_hint_y=0.865)
        
        # Configuración de 2 columnas con redimensionamiento dinámico automático
        grid_products = GridLayout(cols=2, spacing=12, size_hint_y=None, padding=[2, 8, 2, 8])
        grid_products.bind(minimum_height=grid_products.setter('height'))
        
        for prod in PRODUCTS_LIST:
            if CATEGORIA_ACTUAL != "Todas" and prod["category"] != CATEGORIA_ACTUAL:
                continue
            if TEXTO_BUSQUEDA.lower() not in prod["name"].lower():
                continue
            
            # Tarjeta Individual del Producto (Diseño Vertical de Cuadrícula)
            card = CardContainer(orientation='vertical', size_hint_y=None, height=220, padding=10, spacing=6, radius=[16])
            
            # Imagen del producto
            img_box = BoxLayout(size_hint_y=0.55)
            product_img = AsyncImage(source=prod["img"], allow_stretch=True, keep_ratio=True)
            img_box.add_widget(product_img)
            card.add_widget(img_box)
            
            # Textos descriptivos
            lbl_name = Label(text=prod["name"], font_size=13, font_name="Roboto", color=(0.22, 0.13, 0.08, 1), bold=True, halign="center", size_hint_y=0.15)
            lbl_name.bind(size=lambda inst, size: setattr(inst, 'text_size', size))
            card.add_widget(lbl_name)
            
            # Fila de Precio y Stock
            meta_row = BoxLayout(orientation='horizontal', size_hint_y=0.12)
            
            lbl_price = Label(text=f"${prod['price']:.2f}", font_size=13, font_name="Roboto", color=(0.15, 0.48, 0.25, 1), bold=True, halign="left")
            lbl_price.bind(size=lambda inst, size: setattr(inst, 'text_size', size))
            
            stock_actual = prod.get("stock", 0)
            if stock_actual == 0:
                lbl_stock = Label(text="Agotado", font_size=10, font_name="Roboto", color=(0.85, 0.25, 0.25, 1), bold=True, halign="right")
            elif stock_actual <= 3:
                lbl_stock = Label(text="¡Últimos!", font_size=10, font_name="Roboto", color=(0.9, 0.45, 0.1, 1), bold=True, halign="right")
            else:
                lbl_stock = Label(text=f"Cant: {stock_actual}", font_size=10, font_name="Roboto", color=(0.5, 0.45, 0.4, 1), halign="right")
            lbl_stock.bind(size=lambda inst, size: setattr(inst, 'text_size', size))
            
            meta_row.add_widget(lbl_price)
            meta_row.add_widget(lbl_stock)
            card.add_widget(meta_row)
            
            # Botón de acción dentro de la tarjeta
            btn_box = BoxLayout(size_hint_y=0.18)
            p_bg_color = (0.4, 0.25, 0.15, 1) if stock_actual > 0 else (0.78, 0.75, 0.73, 1)
            btn_text = "Pedir" if stock_actual > 0 else "Sin Stock"
            
            btn_action = PremiumIconButton(
                text=btn_text,
                icon_url="https://cdn-icons-png.flaticon.com/512/4218/4218381.png",
                bg_color=p_bg_color,
                radius=[10],
                on_press_callback=lambda instance, p=prod: self.view_details(p) if p.get("stock", 0) > 0 else None
            )
            btn_box.add_widget(btn_action)
            card.add_widget(btn_box)
            
            grid_products.add_widget(card)
            
        scroll.add_widget(grid_products)
        content_layout.add_widget(scroll)
        main_layout.add_widget(content_layout)
        
        main_layout.add_widget(AppNavBar(screen_manager=self.manager, active_tab="menu"))
        self.add_widget(main_layout)

    def update_bg(self, instance, value):
        self.rect_bg.pos = self.pos
        self.rect_bg.size = self.size

    def actualizar_busqueda(self, instance, text):
        global TEXTO_BUSQUEDA
        TEXTO_BUSQUEDA = text
        # Al reconstruir el contenido, guardamos el foco para seguir escribiendo de forma fluida
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


class ProductDetailScreen(Screen):
    def on_enter(self):
        global NOTAS_CLIENTE_ACTUAL
        self.clear_widgets()
        
        with self.canvas.before:
            Color(0.97, 0.95, 0.93, 1)
            self.rect_bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=12)
        
        if SELECTED_PRODUCT:
            lbl_title = Label(text=SELECTED_PRODUCT["name"], font_size=23, font_name="Roboto", color=(0.3, 0.15, 0.05, 1), bold=True, halign="center", valign="middle", size_hint_y=0.08)
            lbl_title.bind(size=lambda inst, size: setattr(inst, 'text_size', size))
            layout.add_widget(lbl_title)
            
            img_box = CardContainer(size_hint_y=0.32, padding=8, radius=[16])
            img_box.add_widget(AsyncImage(source=SELECTED_PRODUCT["img"], allow_stretch=True, keep_ratio=True))
            layout.add_widget(img_box)
            
            info_box = CardContainer(orientation='vertical', padding=15, size_hint_y=0.28, spacing=6, radius=[16])
            
            lbl_cat = Label(text=f"Categoría: {SELECTED_PRODUCT['category']}", font_size=13, font_name="Roboto", color=(0.55, 0.45, 0.4, 1), halign="center")
            lbl_cat.bind(size=lambda inst, size: setattr(inst, 'text_size', size))
            info_box.add_widget(lbl_cat)
            
            lbl_price = Label(text=f"${SELECTED_PRODUCT['price']:.2f}", font_size=24, font_name="Roboto", color=(0.15, 0.48, 0.25, 1), bold=True, halign="center")
            lbl_price.bind(size=lambda inst, size: setattr(inst, 'text_size', size))
            info_box.add_widget(lbl_price)
            
            stock_actual = SELECTED_PRODUCT.get("stock", 0)
            txt_stock = f"Disponibles: {stock_actual} unidades" if stock_actual > 3 else f"¡Sólo quedan {stock_actual} unidades!"
            color_stock = (0.15, 0.48, 0.25, 1) if stock_actual > 3 else (0.85, 0.3, 0.15, 1)
            
            lbl_stock = Label(text=txt_stock, font_size=12, font_name="Roboto", color=color_stock, bold=True, halign="center")
            lbl_stock.bind(size=lambda inst, size: setattr(inst, 'text_size', size))
            info_box.add_widget(lbl_stock)
            
            desc_lbl = Label(
                text=f"Disfruta de nuestro {SELECTED_PRODUCT['name']} preparado de forma artesanal con los mejores ingredientes.",
                font_size=12, font_name="Roboto", color=(0.45, 0.4, 0.35, 1), halign="center", valign="top"
            )
            desc_lbl.bind(size=lambda inst, size: setattr(inst, 'text_size', size))
            info_box.add_widget(desc_lbl)
            layout.add_widget(info_box)
            
            lbl_especif = Label(text="¿Cómo deseas tu pedido?", font_size=13, font_name="Roboto", color=(0.4, 0.25, 0.15, 1), bold=True, halign="left", size_hint_y=0.04)
            lbl_especif.bind(size=lambda inst, size: setattr(inst, 'text_size', size))
            layout.add_widget(lbl_especif)
            
            # Input de especificaciones envuelto en su propia tarjeta de texto
            notes_card = CardContainer(orientation='horizontal', size_hint_y=0.08, padding=[12, 2, 12, 2], radius=[14])
            self.input_notas = ModernTextInput(hint_text="Ej: Sin azúcar, extra de chocolate...")
            self.input_notas.bind(text=self.guardar_especificacion)
            notes_card.add_widget(self.input_notas)
            layout.add_widget(notes_card)
            
            btn_box = BoxLayout(orientation='vertical', spacing=8, size_hint_y=0.20)
            btn_add = PremiumIconButton(
                text="Añadir al Carrito",
                icon_url="https://cdn-icons-png.flaticon.com/512/3514/3514491.png",
                bg_color=(0.15, 0.48, 0.25, 1), radius=[12],
                on_press_callback=self.add_to_cart
            )
            btn_back = CatalogButton(text="Volver al Menú", bg_color=(0.55, 0.5, 0.48, 1), radius=[12])
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
            Color(0.97, 0.95, 0.93, 1)
            self.rect_bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)

        main_layout = BoxLayout(orientation='vertical')
        content_layout = BoxLayout(orientation='vertical', padding=15, spacing=12)
        
        lbl_title = Label(text="Mis Pedidos Solicitados", font_size=22, font_name="Roboto", bold=True, color=(0.3, 0.15, 0.05, 1), halign="center", valign="middle", size_hint_y=0.08)
        lbl_title.bind(size=lambda inst, size: setattr(inst, 'text_size', size))
        content_layout.add_widget(lbl_title)

        scroll = ScrollView(size_hint_y=0.92)
        orders_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=12)
        orders_layout.bind(minimum_height=orders_layout.setter('height'))
        
        mis_pedidos = [o for o in ORDERS_PREPARED if o['usuario'] == CURRENT_USER['username']]

        if not mis_pedidos:
            lbl_empty = Label(text="Aún no tienes pedidos registrados en tu historial.", font_name="Roboto", color=(0.5, 0.5, 0.5, 1), font_size=14, halign="center")
            lbl_empty.bind(size=lambda inst, size: setattr(inst, 'text_size', size))
            orders_layout.add_widget(lbl_empty)
        else:
            for pedido in reversed(mis_pedidos):
                box = CardContainer(orientation='vertical', size_hint_y=None, padding=14, radius=[14], spacing=6)
                
                detalles = f"Ticket #{pedido.get('id', 'N/A')}  |  Total: ${pedido['total']:.2f}\nMétodo: {pedido.get('metodo', 'N/A')}  |  Estado: {pedido['status']}"
                
                lbl_detalles = Label(text=detalles, font_name="Roboto", color=(0.22, 0.15, 0.1, 1), font_size=13, bold=True, halign='left', size_hint_y=None)
                lbl_detalles.bind(texture_size=lambda instance, size: setattr(instance, 'height', size[1]))
                box.bind(width=lambda inv, w: setattr(lbl_detalles, 'text_size', (w - 28, None)))
                box.add_widget(lbl_detalles)
                
                texto_productos = "Detalle de Compra:\n"
                if "productos" in pedido:
                    items_desc = [f" • {p['name']} (x{p['qty']}) { '['+p['notas']+']' if p.get('notas') else '' }" for p in pedido["productos"]]
                    texto_productos += "\n".join(items_desc)
                else:
                    texto_productos += "Productos procesados correctamente."
                    
                lbl_productos = Label(text=texto_productos, font_name="Roboto", color=(0.45, 0.4, 0.38, 1), font_size=12, halign='left', size_hint_y=None)
                lbl_productos.bind(texture_size=lambda instance, size: setattr(instance, 'height', size[1]))
                box.bind(width=lambda inv, w: setattr(lbl_productos, 'text_size', (w - 28, None)))
                box.add_widget(lbl_productos)
                
                box.bind(minimum_height=box.setter('height'))
                orders_layout.add_widget(box)

        scroll.add_widget(orders_layout)
        content_layout.add_widget(scroll)
        
        btn_back = CatalogButton(text="Volver al Perfil", bg_color=(0.4, 0.25, 0.15, 1), size_hint_y=0.08, radius=[12])
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'profile'))
        content_layout.add_widget(btn_back)
        
        content_layout.add_widget(scroll)
        main_layout.add_widget(content_layout)
        
        main_layout.add_widget(AppNavBar(screen_manager=self.manager, active_tab="profile"))
        self.add_widget(main_layout)

    def update_bg(self, instance, value):
        self.rect_bg.pos = self.pos
        self.rect_bg.size = self.size