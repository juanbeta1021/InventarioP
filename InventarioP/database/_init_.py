from .db_handler import DatabaseHandler
import tkinter as tk
from tkinter import messagebox
import mysql.connector
import datetime

class AppScreens:
    def __init__(self, root, cursor, conn):
        self.root = root
        self.root.title("APP_PLASTICO")
        self.root.geometry("500x600")  # Ajusta el tamaño aquí
        self.root.resizable(False, False)
        self.root.config(bg="#7FFFD4")
        self.cursor = cursor
        self.conn = conn
        self.current_user_id = None

        # Crear los marcos de las pantallas
        self.frame_register = tk.Frame(root)
        self.frame_login = tk.Frame(root)
        self.frame_recover = tk.Frame(root)
        self.frame_main = tk.Frame(root)
        self.frame_metas = tk.Frame(root)
        self.frame_historial = tk.Frame(root)

        # Mostrar la pantalla de registro al iniciar
        self.show_register_screen()

    def clear_screen(self):
        """Ocultar todos los frames antes de mostrar uno nuevo"""
        self.frame_register.pack_forget()
        self.frame_login.pack_forget()
        self.frame_recover.pack_forget()
        self.frame_main.pack_forget()
        self.frame_metas.pack_forget()
        self.frame_historial.pack_forget()

    def show_register_screen(self):
        self.clear_screen()

        tk.Label(self.frame_register, text="Registro de Usuarios", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.frame_register, text="Nombre:").pack(pady=5)
        self.entry_name = tk.Entry(self.frame_register, width=30)
        self.entry_name.pack(pady=5)

        tk.Label(self.frame_register, text="Correo Electrónico:").pack(pady=5)
        self.entry_email = tk.Entry(self.frame_register, width=30)
        self.entry_email.pack(pady=5)

        tk.Label(self.frame_register, text="Contraseña:").pack(pady=5)
        self.entry_password = tk.Entry(self.frame_register, show='*', width=30)
        self.entry_password.pack(pady=5)

        tk.Button(self.frame_register, text="Registrar", command=self.register_user).pack(pady=10)
        tk.Button(self.frame_register, text="Iniciar Sesión", command=self.show_login_screen).pack(pady=5)
        tk.Button(self.frame_register, text="Recuperar Contraseña", command=self.show_recover_screen).pack(pady=5)

        self.frame_register.pack()

    def show_login_screen(self):
        self.clear_screen()

        tk.Label(self.frame_login, text="Inicio de Sesión", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.frame_login, text="Correo Electrónico:").pack(pady=5)
        self.entry_login_email = tk.Entry(self.frame_login, width=30)
        self.entry_login_email.pack(pady=5)

        tk.Label(self.frame_login, text="Contraseña:").pack(pady=5)
        self.entry_login_password = tk.Entry(self.frame_login, show='*', width=30)
        self.entry_login_password.pack(pady=5)

        tk.Button(self.frame_login, text="Iniciar Sesión", command=self.login_user).pack(pady=10)
        tk.Button(self.frame_login, text="Volver al Registro", command=self.show_register_screen).pack(pady=5)

        self.frame_login.pack()

    def show_recover_screen(self):
        self.clear_screen()

        tk.Label(self.frame_recover, text="Recuperación de Contraseña", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.frame_recover, text="Correo Electrónico:").pack(pady=5)
        self.entry_recover_email = tk.Entry(self.frame_recover, width=30)
        self.entry_recover_email.pack(pady=5)

        tk.Button(self.frame_recover, text="Enviar Enlace de Recuperación", command=self.recover_password).pack(pady=10)
        tk.Button(self.frame_recover, text="Volver al Registro", command=self.show_register_screen).pack(pady=5)

        self.frame_recover.pack()

    def register_user(self):
        name = self.entry_name.get()
        email = self.entry_email.get()
        password = self.entry_password.get()

        if name and email and password:
            try:
                self.cursor.execute('INSERT INTO users (name, email, password) VALUES (%s, %s, %s)',
                                    (name, email, password))
                self.conn.commit()
                messagebox.showinfo("Registro", "Registro exitoso")
                self.show_login_screen()
            except mysql.connector.IntegrityError:
                messagebox.showerror("Error", "El correo electrónico ya está registrado")
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error en el registro: {e}")
        else:
            messagebox.showerror("Error", "Todos los campos deben ser completados")

    def login_user(self):
        email = self.entry_login_email.get()
        password = self.entry_login_password.get()

        if email and password:
            self.cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
            user = self.cursor.fetchone()
            if user:
                self.current_user_id = user[0]  # Guarda el ID del usuario actual
                self.record_action("Inicio de sesión")
                messagebox.showinfo("Inicio de Sesión", "Inicio de sesión exitoso")
                self.show_main_screen()
            else:
                messagebox.showerror("Error", "Credenciales incorrectas")
        else:
            messagebox.showerror("Error", "Todos los campos deben ser completados")

    def recover_password(self):
        email = self.entry_recover_email.get()

        if email:
            # Aquí se debería agregar la lógica para enviar el enlace de recuperación
            messagebox.showinfo("Recuperación", "Enlace de recuperación enviado")
            self.show_register_screen()
        else:
            messagebox.showerror("Error", "El campo de correo electrónico debe ser completado")

    def show_main_screen(self):
        self.clear_screen()

        tk.Label(self.frame_main, text="Pantalla Principal", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.frame_main, text="Registrar Consumo", command=self.show_consumo_screen).pack(pady=5)
        tk.Button(self.frame_main, text="Ver Historial", command=self.show_historial_screen).pack(pady=5)
        tk.Button(self.frame_main, text="Sugerir Alternativas", command=self.show_sugerencias_screen).pack(pady=5)
        tk.Button(self.frame_main, text="Gestionar Metas", command=self.show_metas_screen).pack(pady=5)

        self.frame_main.pack()

    def show_consumo_screen(self):
        self.clear_screen()

        tk.Label(self.frame_main, text="Registrar Consumo", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.frame_main, text="Fecha (YYYY-MM-DD):").pack(pady=5)
        self.entry_fecha = tk.Entry(self.frame_main, width=30)
        self.entry_fecha.pack(pady=5)

        tk.Label(self.frame_main, text="Cantidad:").pack(pady=5)
        self.entry_cantidad = tk.Entry(self.frame_main, width=30)
        self.entry_cantidad.pack(pady=5)

        tk.Label(self.frame_main, text="Descripción:").pack(pady=5)
        self.entry_descripcion = tk.Entry(self.frame_main, width=30)
        self.entry_descripcion.pack(pady=5)

        tk.Button(self.frame_main, text="Guardar Consumo", command=self.save_consumo).pack(pady=10)
        tk.Button(self.frame_main, text="Volver", command=self.show_main_screen).pack(pady=5)

        self.frame_main.pack()

    def save_consumo(self):
        fecha = self.entry_fecha.get()
        cantidad = self.entry_cantidad.get()
        descripcion = self.entry_descripcion.get()

        if fecha and cantidad and descripcion:
            try:
                self.cursor.execute(
                    'INSERT INTO consumo (user_id, fecha, cantidad, descripcion) VALUES (%s, %s, %s, %s)',
                    (self.current_user_id, fecha, cantidad, descripcion))
                self.conn.commit()
                self.record_action(f"Consumo registrado: {fecha} - {cantidad} - {descripcion}")
                messagebox.showinfo("Consumo", "Consumo registrado exitosamente")
                self.clear_screen()  # Limpiar la pantalla antes de mostrar la pantalla principal
                self.show_main_screen()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al registrar el consumo: {e}")
        else:
            messagebox.showerror("Error", "Todos los campos deben ser completados")

    def show_historial_screen(self):
        self.clear_screen()

        tk.Label(self.frame_historial, text="Historial de Acciones", font=("Arial", 16)).pack(pady=10)

        self.cursor.execute('SELECT accion, fecha FROM historial WHERE user_id = %s ORDER BY fecha DESC',
                            (self.current_user_id, ))
        historial = self.cursor.fetchall()

        if historial:
            for accion, fecha in historial:
                tk.Label(self.frame_historial, text=f"{fecha} - {accion}").pack()
        else:
            tk.Label(self.frame_historial, text="No hay historial de acciones.").pack()

        tk.Button(self.frame_historial, text="Volver", command=self.show_main_screen).pack(pady=10)

        self.frame_historial.pack()

    def record_action(self, action):
        fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            self.cursor.execute('INSERT INTO historial (user_id, accion, fecha) VALUES (%s, %s, %s)',
                                (self.current_user_id, action, fecha))
            self.conn.commit()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudo registrar la acción: {e}")

    def show_metas_screen(self):
        self.clear_screen()
        tk.Label(self.frame_metas, text="Gestión de Metas", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.frame_metas, text="Volver", command=self.show_main_screen).pack(pady=10)
        self.frame_metas.pack()

    def show_sugerencias_screen(self):
        self.clear_screen()
        tk.Label(self.frame_main, text="Sugerencias", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.frame_main, text="Aquí van las sugerencias para alternativas al plástico").pack(pady=5)
        tk.Button(self.frame_main, text="Volver", command=self.show_main_screen).pack(pady=5)
        self.frame_main.pack()


