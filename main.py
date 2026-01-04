import sys
import serial.tools.list_ports
import serial
import customtkinter as ctk
from tkinter import filedialog, messagebox
import esptool
import threading
import time

class ESPFlashTool(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ESP32 Relay X8 - Flash Tool")

        self.title("ESP32 Relay X8 - Suite de Flasheo")
        self.geometry("700x700")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.bin_path = ""
        self.serial_reading = False
        self.serial_thread = None
        self.ser = None


        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1) # El textbox se expande
        



        # --- Header ---
        self.label_title = ctk.CTkLabel(self, text="ESP32 Advanced Flash Tool", font=ctk.CTkFont(size=22, weight="bold"))
        self.label_title.grid(row=0, column=0, padx=20, pady=15)


        # --- Port Config Frame ---
        self.frame_config = ctk.CTkFrame(self)
        self.frame_config.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.frame_config.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.frame_config, text="Puerto COM:").grid(row=0, column=0, padx=10, pady=10)
        self.combo_ports = ctk.CTkComboBox(self.frame_config, values=self.get_ports())
        self.combo_ports.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        self.btn_refresh = ctk.CTkButton(self.frame_config, text="🔄", width=40, command=self.refresh_ports)
        self.btn_refresh.grid(row=0, column=2, padx=10, pady=10)



        ctk.CTkLabel(self.frame_config, text="Velocidad:").grid(row=1, column=0, padx=10, pady=10)
        self.combo_baud = ctk.CTkComboBox(self.frame_config, values=["921600", "460800", "115200"])
        self.combo_baud.grid(row=1, column=1, padx=10, pady=10, sticky="ew")


        # --- File Selection ---
        self.btn_select_file = ctk.CTkButton(self, text="📁 Seleccionar Firmware (.bin)", command=self.select_file)
        self.btn_select_file.grid(row=2, column=0, padx=20, pady=10, sticky="ew")


        self.label_file = ctk.CTkLabel(self, text="Ningún archivo seleccionado", font=ctk.CTkFont(size=10, slant="italic"))
        self.label_file.grid(row=3, column=0, padx=20, pady=0)




        # --- Console / Serial Monitor ---
        self.label_console = ctk.CTkLabel(self, text="Salida de Consola / Monitor Serie", font=ctk.CTkFont(weight="bold"))
        self.label_console.grid(row=4, column=0, padx=20, pady=(10,0), sticky="w")
        




        self.textbox = ctk.CTkTextbox(self, height=250, font=("Courier", 12))
        self.textbox.grid(row=5, column=0, padx=20, pady=10, sticky="nsew")
        
        # --- Control Buttons ---
        self.frame_btns = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_btns.grid(row=6, column=0, padx=20, pady=20, sticky="ew")
        self.frame_btns.grid_columnconfigure((0,1,2), weight=1)

        self.btn_erase = ctk.CTkButton(self.frame_btns, text="🗑️ BORRAR FLASH", command=self.start_erase_thread, 
                                       fg_color="#A93226", hover_color="#7B241C")
        self.btn_erase.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.btn_flash = ctk.CTkButton(self.frame_btns, text="🚀 FLASH", command=self.start_flash_thread, 
                                       fg_color="#1D8348", hover_color="#145A32", font=ctk.CTkFont(weight="bold"))
        self.btn_flash.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.btn_serial = ctk.CTkButton(self.frame_btns, text="📡 MONITOR SERIE", command=self.toggle_serial, 
                                        fg_color="#2E86C1", hover_color="#1B4F72")
        self.btn_serial.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

    def get_ports(self):
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports] if ports else ["No se detectan puertos"]

    def refresh_ports(self):
        self.combo_ports.configure(values=self.get_ports())

        if self.get_ports(): self.combo_ports.set(self.get_ports()[0])

    def select_file(self):
        file = filedialog.askopenfilename(filetypes=[("Binary files", "*.bin")])
        if file:
            self.bin_path = file

            self.label_file.configure(text=file)

    def log(self, message):
        self.textbox.insert("end", message + "\n")
        self.textbox.see("end")

    def start_flash_thread(self):
        if not self.bin_path:

            messagebox.showerror("Error", "Selecciona un archivo .bin")
            return



        self.stop_serial()
        threading.Thread(target=self.flash_firmware, daemon=True).start()














    def start_erase_thread(self):
        if messagebox.askyesno("Confirmar", "¿Seguro que quieres borrar toda la memoria del ESP32?"):
            self.stop_serial()
            threading.Thread(target=self.erase_flash, daemon=True).start()

    def erase_flash(self):
        self.btn_erase.configure(state="disabled")
        self.btn_flash.configure(state="disabled")
        self.log("🧽 Borrando memoria flash...")
        try:



            esptool.main(['--port', self.combo_ports.get(), 'erase_flash'])
            self.log("✅ Memoria borrada con éxito.")
        except Exception as e:


            self.log(f"❌ Error al borrar: {str(e)}")
        finally:
            self.btn_erase.configure(state="normal")
            self.btn_flash.configure(state="normal")

    def flash_firmware(self):
        self.btn_flash.configure(state="disabled")
        self.btn_erase.configure(state="disabled")
        self.log(f"⚡ Flasheando {self.combo_ports.get()}...")
        try:
            esptool.main(['--port', self.combo_ports.get(), '--baud', self.combo_baud.get(), 
                          '--chip', 'esp32', 'write_flash', '--flash_mode', 'dio', '0x10000', self.bin_path])
            self.log("✅ Flasheo completado con éxito.")
            time.sleep(1)
            self.toggle_serial() # Auto-iniciar monitor tras flasheo
        except Exception as e:
            self.log(f"❌ Error: {str(e)}")
        finally:
            self.btn_flash.configure(state="normal")
            self.btn_erase.configure(state="normal")

    def toggle_serial(self):
        if self.serial_reading:
            self.stop_serial()
        else:
            self.start_serial()

    def start_serial(self):
        port = self.combo_ports.get()
        baud = 115200 # Velocidad estándar para logs de ESP32
        try:
            self.ser = serial.Serial(port, baud, timeout=0.1)
            self.serial_reading = True
            self.btn_serial.configure(text="🛑 PARAR MONITOR", fg_color="orange")
            self.log(f"--- Monitor Serie Iniciado ({port} @ 115200) ---")
            self.serial_thread = threading.Thread(target=self.read_serial, daemon=True)
            self.serial_thread.start()
        except Exception as e:
            self.log(f"❌ No se pudo abrir puerto serie: {str(e)}")

    def stop_serial(self):
        self.serial_reading = False
        if self.ser and self.ser.is_open:
            self.ser.close()
        self.btn_serial.configure(text="📡 MONITOR SERIE", fg_color="#2E86C1")
        self.log("--- Monitor Serie Detenido ---")

    def read_serial(self):
        while self.serial_reading:
            if self.ser and self.ser.is_open:
                try:
                    line = self.ser.readline().decode('utf-8', errors='replace')
                    if line:
                        self.textbox.insert("end", line)
                        self.textbox.see("end")
                except:
                    break
            time.sleep(0.01)

if __name__ == "__main__":
    app = ESPFlashTool()
    app.mainloop()