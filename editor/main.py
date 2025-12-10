import json
import sys

_FILENAME: str = 'map.txt'
_DELIMITER: str = '\nMultiple cells:'
_MULTIPLE_CELL_SYMBOL: str = 'M'
_BLOCK_W: int = 40
_RESULT_JSON_MAP_FILENAME: str = '../assets/levels/{}.json'

_id_global_count: int = 0

_TREE_X_OFFSETS_FROM_CENTER = {
    0: 100,
    1: 80,
    2: 100,
}
_TREE_Y_OFFSETS_FROM_BOTTOM = {
    0: 200,
    1: 200,
    2: 140,
}
_TOP_WATER_Y_OFFSET_FROM_BOTTOM = 32
_HINT_Y_OFFSET_FROM_BOTTOM = 80
_CHEST_Y_OFFSET_FROM_BOTTOM = 60

_SKELETON_Y_OFFSET_FROM_BOTTOM = 72
_SLUG_Y_OFFSET_FROM_BOTTOM = 52


def main() -> None:
    result_json_map = {
        'objects': [],
        'is_available': True,
        'is_completed': False,
        'w': None,
        'h': None,
        'extra_data': {},
    }

    with open(_FILENAME, 'r', encoding='utf-8') as f:
        map_: str = f.read()

    if _DELIMITER in map_:
        map_, multiple_cells = map_.split(_DELIMITER)
        multiple_cells = multiple_cells.strip().split('\n')
    else:
        multiple_cells = []
    map_ = map_.split('\n')

    multiple_cell_i: int = 0
    max_row_len: int = 0
    for y, row in enumerate(map_):
        max_row_len = max(max_row_len, len(row.strip()))
        for x, cell in enumerate(row):
            symbols = cell
            if cell == _MULTIPLE_CELL_SYMBOL:
                symbols = multiple_cells[multiple_cell_i]
                multiple_cell_i += 1

            _handle_cell(x, y, symbols, result_json_map['objects'])

    result_json_map['w'] = max_row_len * _BLOCK_W
    result_json_map['h'] = len(map_) * _BLOCK_W

    if len(sys.argv) > 1:
        fn = sys.argv[1]
    else:
        fn = 'result'

    path = _RESULT_JSON_MAP_FILENAME.format(fn)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(result_json_map, indent=4, ensure_ascii=False))

    print('The map has been successfully created!')


def _handle_cell(x: int, y: int,
                 symbols: str, 
                 objects: list[dict],
                 ) -> None:
    global _id_global_count

    symbols = symbols.replace('f', '+=')

    for symbol in symbols:
        args = {
            'x': x * _BLOCK_W,
            'y': y * _BLOCK_W,
        }
        if symbol in ('*', '-', '<', '>', '[', ']'):
            t = 'Dirt'
            args = {
                **args,
                'direction': -1 if symbol in ('<', '[') else 1 if symbol in ('>', ']') else None,
                'grass_enabled': True if symbol in ('-', '<', '>') else False,
            }
        elif symbol == 'p':
            t = 'Player'
        elif symbol == '$':
            t = 'Coin'
            args = {
                **args,
                'id_': _id_global_count,
            }
            _id_global_count += 1
        elif symbol == 'c':
            t = 'Chest'
            args = {
                **args,
                'y': args['y'] + _BLOCK_W - _CHEST_Y_OFFSET_FROM_BOTTOM,
                'id_': _id_global_count,
            }
            _id_global_count += 1            
        elif symbol == 'h':
            t = 'Heart'
        elif symbol == 'G':
            t = 'Shield'
        elif symbol in ('w', 't'):
            t = 'Water'
            args = {
                **args,
                'is_top': False if symbol == 'w' else True,
            }
            if symbol == 't':
                args['y'] = args['y'] + _BLOCK_W - _TOP_WATER_Y_OFFSET_FROM_BOTTOM
        elif symbol == '#':
            t = 'Bricks'
        elif symbol == '+':
            t = 'BackgroundBricks'
        elif symbol == '@':
            t = 'BackgroundDirt'
        elif symbol == '=':
            t = 'Ladder'
        elif symbol == '?':
            t = 'Hint'
            args = {
                **args,
                'y': args['y'] + _BLOCK_W - _HINT_Y_OFFSET_FROM_BOTTOM,
                'text': 'Default text... Fill it.',
            }
        elif symbol == '^':
            t = 'Spike'
        elif symbol == 'f':
            t = 'Finish'
        elif symbol in ('S', 'K', 'B'):
            t = 'Slug' if symbol == 'S' else 'Skeleton' if symbol == 'K' else 'Bat'
            args = {
                **args,
                'start_x': 0,
                'end_x': 999999,
            }
            if symbol == 'S':
                args['y'] = args['y'] + _BLOCK_W - _SLUG_Y_OFFSET_FROM_BOTTOM
            elif symbol == 'K':
                args['y'] = args['y'] + _BLOCK_W - _SKELETON_Y_OFFSET_FROM_BOTTOM
        elif symbol == 'P':
            t = 'Spider'
            args = {
                **args,
                'end_y': 999999,
            }
        elif symbol == 'C':
            t = 'Cannon'
            args = {
                **args,
                'end_x': 999999,
            }
        elif symbol in ('/', '\\'):
            t = 'Web'
            args = {
                **args,
                'direction': -1 if symbol == '/' else 1
            }
        elif symbol.isdigit():
            _i = int(symbol)
            t = 'Tree'
            args = {
                **args,
                'x': args['x'] + (_BLOCK_W // 2) - _TREE_X_OFFSETS_FROM_CENTER[_i],
                'y': args['y'] + _BLOCK_W - _TREE_Y_OFFSETS_FROM_BOTTOM[_i],
                'image_index': _i,
            }
        else:
            continue

        obj = {
            'type': t,
            'factory_method': '__call__',
            'args': args,
        }
        objects.append(obj)


if __name__ == '__main__':
    main()
