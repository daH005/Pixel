pyinstaller --onefile ^
            --console ^
            --paths=../../../game;../../../;../../../editor ^
            --distpath=../../../editor ^
            --name=Editor ^
            ../../../editor/main.py