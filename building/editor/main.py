import PyInstaller.__main__

if __name__ == '__main__':
    PyInstaller.__main__.run([
        '../../editor/main.py',
        '--onefile',
        '--paths=../;../game',
        '--distpath=../../editor',
        '--name=Editor',
    ])
