# PowerShell: Запустить для обновления .py GUI файлов
Set-Location C:\My\code\Working\pyqt_project\ui
pyuic5 sources/main_window.ui -o main_window_ui.py
pyuic5 sources/video_dialog_ui.ui -o video_dialog_ui.py
pyuic5 sources/video_download_dialog.ui -o video_download_dialog_ui.py