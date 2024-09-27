import customtkinter as tk
from tkinter import ttk, messagebox, Toplevel
from PIL import Image, ImageTk  # Asegúrate de tener Pillow instalado
from database.db_handler import DatabaseHandler
from utils import validate_float, validate_int, format_currency

class ProductGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Gestión de productos")
        self.master.geometry("600x600")
        self.master.resizable(False, False)

        try:
            self.db = DatabaseHandler()
        except Exception as e:
            messagebox.showerror("Database Error", f"No se pudo conectar a la base de datos: {e}")
            self.master.destroy()
            return

        self.selected_product = None  # Para rastrear el producto seleccionado
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.master, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configuración de columnas y filas
        for i in range(6):
            main_frame.grid_columnconfigure(i, weight=1)
        for i in range(8):
            main_frame.grid_rowconfigure(i, weight=1)

        # Mostrar imagen
        self.show_image(main_frame)

        # Entradas de texto
        ttk.Label(main_frame, text="Name:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.name_entry = ttk.Entry(main_frame, width=30)
        self.name_entry.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)

        ttk.Label(main_frame, text="Brand:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.brand_entry = ttk.Entry(main_frame, width=30)
        self.brand_entry.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)

        ttk.Label(main_frame, text="Reference:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.reference_entry = ttk.Entry(main_frame, width=30)
        self.reference_entry.grid(row=3, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)

        ttk.Label(main_frame, text="Price:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.price_entry = ttk.Entry(main_frame, width=30)
        self.price_entry.grid(row=4, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)

        ttk.Label(main_frame, text="Quantity:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        self.quantity_entry = ttk.Entry(main_frame, width=30)
        self.quantity_entry.grid(row=5, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)

        # Botones para CRUD
        ttk.Button(main_frame, text="Agregar producto", command=self.add_product).grid(row=6, column=0, columnspan=3, pady=10)
        ttk.Button(main_frame, text="Mostrar productos", command=self.show_products).grid(row=7, column=0, columnspan=3, pady=10)
        ttk.Button(main_frame, text="Actualizar producto", command=self.update_product).grid(row=8, column=0, columnspan=3, pady=10)
        ttk.Button(main_frame, text="Eliminar producto", command=self.delete_product).grid(row=9, column=0, columnspan=3, pady=10)

    def show_image(self, parent):
        # Cargar la imagen
        try:
            image_path = "D:\\database.png"  # Ruta de la imagen
            image = Image.open(image_path)
            image = image.resize((100, 100), Image.LANCZOS)  # Cambia ANTIALIAS por LANCZOS
            self.photo = ImageTk.PhotoImage(image)  # Convertir a PhotoImage

            # Crear un Label para mostrar la imagen
            image_label = ttk.Label(parent, image=self.photo)
            image_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))  # Ajusta la posición según sea necesario
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")

    def add_product(self):
        name = self.name_entry.get()
        brand = self.brand_entry.get()
        reference = self.reference_entry.get()
        price = self.price_entry.get()
        quantity = self.quantity_entry.get()

        if name and brand and reference and price and quantity:
            price = validate_float(price)
            quantity = validate_int(quantity)

            if price is not None and quantity is not None:
                try:
                    self.db.insert_product(name, brand, reference, price, quantity)
                    messagebox.showinfo("Success", "Producto agregado exitosamente!")
                    self.clear_entries()
                except Exception as e:
                    messagebox.showerror("Database Error", f"No se pudo agregar el producto: {e}")
            else:
                messagebox.showerror("Error", "Precio o cantidad no válidos!")
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios!")

    def show_products(self):
        try:
            products = self.db.get_all_products()
            if products:
                product_window = Toplevel(self.master)
                product_window.title("Lista de productos")
                product_window.geometry("800x400")

                tree = ttk.Treeview(product_window, columns=("ID", "Name", "Brand", "Reference", "Price", "Quantity"), show="headings")
                tree.heading("ID", text="ID")
                tree.heading("Name", text="Name")
                tree.heading("Brand", text="Brand")
                tree.heading("Reference", text="Reference")
                tree.heading("Price", text="Price")
                tree.heading("Quantity", text="Quantity")

                tree.column("ID", width=50)
                tree.column("Name", width=150)
                tree.column("Brand", width=150)
                tree.column("Reference", width=150)
                tree.column("Price", width=100)
                tree.column("Quantity", width=100)

                for product in products:
                    formatted_product = list(product)
                    formatted_product[4] = format_currency(product[4])
                    tree.insert("", "end", values=formatted_product)

                tree.bind("<<TreeviewSelect>>", self.on_product_select)
                tree.pack(expand=True, fill='both', padx=10, pady=10)

                scrollbar = ttk.Scrollbar(product_window, orient="vertical", command=tree.yview)
                scrollbar.pack(side='right', fill='y')
                tree.configure(yscrollcommand=scrollbar.set)
            else:
                messagebox.showinfo("Info", "No se encontraron productos!")
        except Exception as e:
            messagebox.showerror("Database Error", f"No se pudieron recuperar los productos: {e}")

    def on_product_select(self, event):
        tree = event.widget
        selected_item = tree.selection()
        if selected_item:
            product = tree.item(selected_item)["values"]
            self.selected_product = product[0]  # Guardar ID del producto seleccionado
            print(f"Producto seleccionado con ID: {self.selected_product}")

            # Llenar los campos de texto con la información del producto seleccionado
            self.name_entry.delete(0, 'end')
            self.name_entry.insert(0, product[1])
            self.brand_entry.delete(0, 'end')
            self.brand_entry.insert(0, product[2])
            self.reference_entry.delete(0, 'end')
            self.reference_entry.insert(0, product[3])
            self.price_entry.delete(0, 'end')
            self.price_entry.insert(0, product[4])
            self.quantity_entry.delete(0, 'end')

    def update_product(self):
        if self.selected_product:  # Verifica que haya un producto seleccionado
            name = self.name_entry.get()
            brand = self.brand_entry.get()
            reference = self.reference_entry.get()
            price = self.price_entry.get()
            quantity = self.quantity_entry.get()

            if name and brand and reference and price and quantity:
                price = validate_float(price)
                quantity = validate_int(quantity)

                if price is not None and quantity is not None:
                    try:
                        print(f"Actualizando producto con ID: {self.selected_product}")
                        self.db.update_product(self.selected_product, name, brand, reference, price, quantity)
                        messagebox.showinfo("Success", "Producto actualizado exitosamente!")
                        self.clear_entries()
                    except Exception as e:
                        messagebox.showerror("Database Error", f"No se pudo actualizar el producto: {e}")
                else:
                    messagebox.showerror("Error", "Precio o cantidad no válidos!")
            else:
                messagebox.showerror("Error", "Todos los campos son obligatorios!")
        else:
            messagebox.showerror("Error", "Seleccione un producto para actualizar")

    def delete_product(self):
        if self.selected_product:  # Asegúrate de que haya un producto seleccionado
            try:
                print(f"Eliminando producto con ID: {self.selected_product}")
                self.db.delete_product(self.selected_product)
                messagebox.showinfo("Success", "Producto eliminado exitosamente!")
                self.clear_entries()
                self.selected_product = None  # Restablecer el producto seleccionado
            except Exception as e:
                messagebox.showerror("Database Error", f"No se pudo eliminar el producto: {e}")
        else:
            messagebox.showerror("Error", "Seleccione un producto para eliminar")

    def clear_entries(self):
        self.name_entry.delete(0, 'end')
        self.brand_entry.delete(0, 'end')
        self.reference_entry.delete(0, 'end')
        self.price_entry.delete(0, 'end')
        self.quantity_entry.delete(0, 'end')

    def run(self):
        self.master.mainloop()

    def __del__(self):
        if hasattr(self, 'db'):
            self.db.close()

