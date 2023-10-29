pyinstaller --onefile ^
            --noconsole ^
            --paths=../../game;../../ ^
            --distpath=../../game ^
            --name=Pixel ^
            --icon=../../assets/images/icons/icon.bmp ^
            ../../game/main.py