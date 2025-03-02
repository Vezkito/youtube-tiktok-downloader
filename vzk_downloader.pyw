import yt_dlp
import os
import re
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pygame
import subprocess

def touch_file(file_path):
    """Atualiza a data e hora de modificação do arquivo para o momento atual."""
    try:
        os.utime(file_path, None)
    except Exception as e:
        print(f"Erro ao atualizar a data/hora do arquivo: {e}")

class VideoDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vzk Downloader")
        self.root.configure(bg='#2e2e2e')
        self.root.attributes('-fullscreen', False)
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)

        self.title_bar = tk.Frame(self.root, bg='#1c1c1c', relief='raised', bd=0, highlightthickness=0)
        self.title_bar.pack(side='top', fill='x')

        self.close_button = tk.Button(self.title_bar, text='X', command=self.root.destroy, bg='#1c1c1c', fg='#ffffff', bd=0, font=('Arial Black', 12))
        self.close_button.pack(side='right')

        self.title_label = tk.Label(self.title_bar, text="VZK Downloader", bg='#1c1c1c', fg='#ffffff', font=('Arial Black', 12))
        self.title_label.pack(side='left', padx=10)

        self.title_bar.bind('<ButtonPress-1>', self.start_move)
        self.title_bar.bind('<B1-Motion>', self.do_move)

        self.style = ttk.Style(self.root)
        self.style.theme_use('clam')

        self.init_styles()
        self.create_widgets()

        self.x = 0
        self.y = 0
        self.sound_file = "download_complete.mp3"

        pygame.mixer.init()

        if not self.check_ffmpeg():
            messagebox.showerror("Erro", "FFmpeg não encontrado. Instale o FFmpeg e adicione ao PATH.")
            self.root.destroy()

    def check_ffmpeg(self):
        """Verifica se o FFmpeg está instalado e acessível."""
        try:
            result = subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            print(f"FFmpeg encontrado: {result.stdout.decode('utf-8').splitlines()[0]}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"FFmpeg não encontrado: {e}")
            return False

    def init_styles(self):
        self.style.configure("TFrame", background='#2e2e2e')
        self.style.configure("TLabel", background='#2e2e2e', foreground='#ffffff', font=('Arial Black', 10))
        self.style.configure("TEntry", background='#4d4d4d', foreground='#ffffff', fieldbackground='#4d4d4d', font=('Arial Black', 10))
        self.style.configure("TButton", background='#4d4d4d', foreground='#ffffff', font=('Arial Black', 10))
        self.style.configure("TCheckbutton", background='#2e2e2e', foreground='#ffffff', font=('Arial Black', 10))
        self.style.configure("TRadiobutton", background='#2e2e2e', foreground='#ffffff', font=('Arial Black', 10), indicatorbackground='#2e2e2e')
        self.style.configure("TNotebook", background='#2e2e2e', foreground='#ffffff', font=('Arial Black', 10))
        self.style.configure("TNotebook.Tab", background='#4d4d4d', foreground='#ffffff', font=('Arial Black', 10))
        self.style.map("TButton", background=[('active', '#6c6c6c')], foreground=[('active', '#ffffff')])
        self.style.map("TCheckbutton", background=[('active', '#2e2e2e'), ('!active', '#2e2e2e')], foreground=[('active', '#ffffff'), ('!active', '#ffffff')])
        self.style.map("TRadiobutton", background=[('active', '#2e2e2e'), ('!active', '#2e2e2e')], foreground=[('active', '#ffffff'), ('!active', '#ffffff')], indicatorcolor=[('selected', '#ffffff')])

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        self.download_frame = ttk.Frame(self.notebook, padding="10")
        self.settings_frame = ttk.Frame(self.notebook, padding="10")

        self.notebook.add(self.download_frame, text='Download')
        self.notebook.add(self.settings_frame, text='Configurações')

        self.create_download_tab()
        self.create_settings_tab()

    def create_download_tab(self):
        caminho_label = ttk.Label(self.download_frame, text="Selecione o caminho para salvar os vídeos:")
        caminho_label.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=5)

        self.caminho_entry = ttk.Entry(self.download_frame, width=50)
        self.caminho_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)

        predefinido1_button = ttk.Button(self.download_frame, text="Vídeo para Edição", command=lambda: self.definir_caminho('C:/Users/Vezkalin/Desktop/Trabalhos/videosparaedicao'))
        predefinido1_button.grid(row=2, column=0, sticky=tk.W, pady=5)

        predefinido2_button = ttk.Button(self.download_frame, text="Downloads", command=lambda: self.definir_caminho('C:/Users/Vezkalin/Downloads'))
        predefinido2_button.grid(row=2, column=1, sticky=tk.W, pady=5)

        predefinido3_button = ttk.Button(self.download_frame, text="Escolher Caminho", command=self.escolher_caminho)
        predefinido3_button.grid(row=3, column=0, sticky=tk.W, pady=5)

        url_label = ttk.Label(self.download_frame, text="Insira os links dos vídeos (um por vez):")
        url_label.grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=5)

        self.url_entry = ttk.Entry(self.download_frame, width=50)
        self.url_entry.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=5)

        self.adicionar_button = ttk.Button(self.download_frame, text="Adicionar e Baixar", command=self.adicionar_url)
        self.adicionar_button.grid(row=5, column=1, sticky=tk.W, pady=5)

        self.status_label = ttk.Label(self.download_frame, text="Nada está sendo baixado", background='#2e2e2e', foreground='#ffffff')
        self.status_label.grid(row=6, column=0, columnspan=2, pady=5)

        self.download_audio_var = tk.BooleanVar(value=False)
        download_audio_check = ttk.Checkbutton(self.download_frame, text='Baixar apenas áudio(.mp3)', variable=self.download_audio_var)
        download_audio_check.grid(row=7, column=0, columnspan=2, pady=5)

    def create_settings_tab(self):
        self.mode_var = tk.StringVar(value='dark')
        self.always_on_top_var = tk.BooleanVar(value=True)

        modo_label = ttk.Label(self.settings_frame, text="Modo de exibição:")
        modo_label.grid(row=0, column=0, sticky=tk.W, pady=5)

        dark_mode_radio = ttk.Radiobutton(self.settings_frame, text='Modo Escuro', variable=self.mode_var, value='dark', command=self.change_mode)
        dark_mode_radio.grid(row=1, column=0, sticky=tk.W, pady=5)
        light_mode_radio = ttk.Radiobutton(self.settings_frame, text='Modo Claro', variable=self.mode_var, value='light', command=self.change_mode)
        light_mode_radio.grid(row=1, column=1, sticky=tk.W, pady=5)

        always_on_top_check = ttk.Checkbutton(self.settings_frame, text='Always on Top', variable=self.always_on_top_var, command=self.toggle_always_on_top)
        always_on_top_check.grid(row=2, column=0, sticky=tk.W, pady=5)

    def definir_caminho(self, caminho):
        self.caminho_entry.delete(0, tk.END)
        self.caminho_entry.insert(0, caminho)

    def escolher_caminho(self):
        caminho = filedialog.askdirectory()
        if caminho:
            self.caminho_entry.delete(0, tk.END)
            self.caminho_entry.insert(0, caminho)

    def adicionar_url(self):
        url = self.url_entry.get().strip()
        caminho = self.caminho_entry.get().strip()
        if not caminho:
            messagebox.showerror("Erro", "Por favor, selecione um caminho para salvar os vídeos bobo.")
            return
        self.url_entry.delete(0, tk.END)
        if url.lower() == "sair":
            self.root.quit()
        elif url.lower() == "retornar":
            self.caminho_entry.delete(0, tk.END)
        elif url:
            self.status_label.config(text="Baixando...")
            self.adicionar_button.config(state=tk.DISABLED)
            threading.Thread(target=self.baixar_video, args=(url, caminho)).start()
        else:
            messagebox.showerror("Erro", "Por favor, insira um link de vídeo.")

    def baixar_video(self, url, caminho):
        ydl_opts = {
            'cookiefile': 'cookies.txt',
            'outtmpl': os.path.join(caminho, '%(title)s.temp.%(ext)s'),  # Arquivo temporário
            'verbose': True,
            'ignoreconfig': True,
            'format': 'bestvideo[vcodec=avc1]+bestaudio/best',  # Tenta H.264 primeiro
            'merge_output_format': 'mp4',
            'prefer_ffmpeg': True,
        }

        try:
            # Baixa o vídeo
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                temp_file = ydl.prepare_filename(info_dict)

            # Define o arquivo final
            final_file = temp_file.replace('.temp.', '.')

            # Converte manualmente com FFmpeg sem abrir CMD
            print(f"Convertendo {temp_file} para {final_file} com H.264...")
            ffmpeg_cmd = [
                'ffmpeg',
                '-i', temp_file,
                '-c:v', 'libx264',
                '-c:a', 'aac',
                '-f', 'mp4',
                '-movflags', '+faststart',
                final_file
            ]
            result = subprocess.run(
                ffmpeg_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                creationflags=subprocess.CREATE_NO_WINDOW  # Impede a abertura do CMD no Windows
            )
            print(f"FFmpeg saída: {result.stdout.decode('utf-8')}")
            print(f"FFmpeg erros (se houver): {result.stderr.decode('utf-8')}")

            # Remove o arquivo temporário após conversão
            if os.path.exists(final_file):
                os.remove(temp_file)
                print(f"Arquivo temporário {temp_file} removido.")
            else:
                raise Exception("Arquivo final não foi criado.")

            touch_file(final_file)
            self.show_status_message("✅ Download e conversão finalizados!")
        except yt_dlp.utils.ExtractorError as e:
            self.show_status_message(f"❌ Erro no download: {e}")
            self.list_available_formats(url)
        except subprocess.CalledProcessError as e:
            self.show_status_message(f"❌ Erro na conversão FFmpeg: {e.stderr.decode('utf-8')}")
            print(f"Erro detalhado FFmpeg: {e}")
        except Exception as e:
            self.show_status_message(f"❌ Erro inesperado: {e}")
            print(f"Erro detalhado: {e}")

    def list_available_formats(self, url):
        """Lista os formatos disponíveis para o vídeo."""
        ydl_opts = {'listformats': True}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.extract_info(url, download=False)
            self.show_status_message("Verifique os formatos disponíveis no console.")
        except Exception as e:
            self.show_status_message(f"❌ Erro ao listar formatos: {e}")

    def show_status_message(self, message):
        self.status_label.config(text=message)
        self.adicionar_button.config(state=tk.NORMAL)
        self.root.update_idletasks()
        pygame.mixer.music.load(self.sound_file)
        pygame.mixer.music.play()
        self.root.after(2500, self.clear_status_message)

    def clear_status_message(self):
        self.status_label.config(text="Nada está sendo baixado")

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        x = self.root.winfo_x() + (event.x - self.x)
        y = self.root.winfo_y() + (event.y - self.y)
        self.root.geometry(f"+{x}+{y}")

    def change_mode(self):
        if self.mode_var.get() == 'dark':
            self.root.configure(bg='#2e2e2e')
            self.title_bar.configure(bg='#1c1c1c')
            self.title_label.configure(bg='#1c1c1c', fg='#ffffff')
            self.close_button.configure(bg='#1c1c1c', fg='#ffffff')
            self.style.configure("TRadiobutton", background='#2e2e2e', foreground='#ffffff', indicatorbackground='#2e2e2e')
            self.init_styles()
        else:
            self.root.configure(bg='#ffffff')
            self.title_bar.configure(bg='#e0e0e0')
            self.title_label.configure(bg='#e0e0e0', fg='#000000')
            self.close_button.configure(bg='#e0e0e0', fg='#000000')
            self.style.configure("TFrame", background='#ffffff')
            self.style.configure("TLabel", background='#ffffff', foreground='#000000', font=('Arial Black', 10))
            self.style.configure("TEntry", background='#ffffff', foreground='#000000', fieldbackground='#ffffff', font=('Arial Black', 10))
            self.style.configure("TButton", background='#e0e0e0', foreground='#000000', font=('Arial Black', 10))
            self.style.configure("TCheckbutton", background='#ffffff', foreground='#000000', font=('Arial Black', 10))
            self.style.configure("TRadiobutton", background='#ffffff', foreground='#000000', indicatorbackground='#ffffff')
            self.style.configure("TNotebook", background='#ffffff', foreground='#000000', font=('Arial Black', 10))
            self.style.configure("TNotebook.Tab", background='#e0e0e0', foreground='#000000', font=('Arial Black', 10))
            self.style.map("TButton", background=[('active', '#c0c0c0')], foreground=[('active', '#000000')])
            self.style.map("TCheckbutton", background=[('active', '#ffffff'), ('!active', '#ffffff')], foreground=[('active', '#000000'), ('!active', '#000000')])
            self.style.map("TRadiobutton", background=[('active', '#ffffff'), ('!active', '#ffffff')], foreground=[('active', '#000000'), ('!active', '#000000')], indicatorcolor=[('selected', '#000000')])

    def toggle_always_on_top(self):
        self.root.attributes('-topmost', self.always_on_top_var.get())

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoDownloaderApp(root)
    root.mainloop()
