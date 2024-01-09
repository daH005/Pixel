import PyInstaller.__main__

if __name__ == '__main__':
    PyInstaller.__main__.run([
        '../../../game/main.py',
        '--onefile',
        '--noconsole',
        '--paths=../../../game;../../../',
        '--distpath=../../../game',
        '--name=Pixel',
        '--icon=../../../assets/images/icons/icon.bmp',
    ])
