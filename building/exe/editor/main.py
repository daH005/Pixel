import PyInstaller.__main__

if __name__ == '__main__':
    PyInstaller.__main__.run([
        '../../../editor/main.py',
        '--onefile',
        '--paths=../../../game;../../../;../../../editor',
        '--distpath=../../../editor',
        '--name=Editor',
    ])
