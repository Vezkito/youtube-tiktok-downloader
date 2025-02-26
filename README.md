Video Downloader
Este é um aplicativo de desktop para baixar vídeos de várias plataformas usando yt-dlp. O aplicativo possui uma interface gráfica amigável construída com tkinter e permite que os usuários escolham entre diferentes modos de exibição (Dark Mode/Light Mode) e caminhos predefinidos para salvar os vídeos. Além disso, o aplicativo toca um som de notificação quando o download é concluído.

Funcionalidades
Baixar vídeos de várias plataformas usando yt-dlp.
Escolher entre modos de exibição Dark Mode e Light Mode.
Selecionar caminhos predefinidos para salvar os vídeos.
Opção para baixar apenas o áudio dos vídeos.
Notificação sonora quando o download é concluído.
Requisitos
Python 3.7 ou superior
yt-dlp
tkinter
pygame
Instalação
Clone o repositório para o seu ambiente local:

git clone https://github.com/seu-usuario/video-downloader.git
cd video-downloader
Instale as dependências necessárias:

pip install yt-dlp pygame
Certifique-se de que o ffmpeg está instalado e disponível no PATH do sistema. Você pode baixar o ffmpeg aqui.

Uso
Execute o script Python:

python vzk_downloader.pyw
Use a interface gráfica para inserir URLs de vídeos, escolher o caminho para salvar e iniciar os downloads.

Empacotamento com PyInstaller
Para empacotar o aplicativo em um arquivo executável usando PyInstaller, siga estas etapas:

Instale o PyInstaller:

pip install pyinstaller
Crie o executável:

pyinstaller --onefile --noconsole vzk_downloader.pyw
Copie os arquivos adicionais (ffmpeg, ytdl, download_complete.mp3) para a pasta dist onde o executável foi gerado.

Exemplo:

dist/
├── vzk_downloader.exe
├── ffmpeg.exe
├── ytdl
│   └── yt-dlp.exe
├── download_complete.mp3
Execute o arquivo vzk_downloader.exe na pasta dist.
