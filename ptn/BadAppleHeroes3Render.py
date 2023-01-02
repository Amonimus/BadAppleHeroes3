import json
import os
import random

from PIL import Image, ImageOps

import BadAppleJsoner


def pil_convert(paths_arr):
    tiles_img = map(Image.open, paths_arr)
    tiles_img = [ImageOps.fit(image, (32, 32), Image.LANCZOS) for image in tiles_img]
    return tiles_img


def load_tiles(folder):
    tiles = {}

    black_paths = [os.path.join(folder, f) for f in os.listdir(folder) if 'B' in f]
    tiles["black"] = pil_convert(black_paths)

    white0_paths = [os.path.join(folder, f) for f in os.listdir(folder) if 'W0' in f]
    tiles["white0"] = pil_convert(white0_paths)

    white1_paths = [os.path.join(folder, f) for f in os.listdir(folder) if 'W1' in f]
    tiles["white1"] = pil_convert(white1_paths)

    corner_paths = [os.path.join(folder, f) for f in os.listdir(folder) if 'C' in f]
    tiles["corner"] = pil_convert(corner_paths)

    gray_paths = [os.path.join(folder, f) for f in os.listdir(folder) if 'G' in f]
    gray_names = [f.split("G_")[1].split(".png")[0] for f in os.listdir(folder) if 'G' in f]
    tiles["gray"] = {gray_names[i]: pil_convert(gray_paths)[i] for i in range(len(gray_paths))}

    return tiles


def randomtile(arr):
    return random.choice(arr)


def if_relative_is_dark(frame, coor, rel):
    y = coor[1] + rel[1]
    x = coor[0] + rel[0]
    if y >= len(frame):
        y = len(frame) - 1
    elif y <= 0:
        y = 0
    if x >= len(frame[0]):
        x = len(frame[0]) - 1
    elif x <= 0:
        x = 0
    p = frame[y][x]
    return p == 1


def check_neighbours(frame, coor):
    d = 0
    if if_relative_is_dark(frame, coor, (0, 1)):
        d += 1
    if if_relative_is_dark(frame, coor, (1, 0)):
        d += 2
    if if_relative_is_dark(frame, coor, (-1, 0)):
        d += 4
    if if_relative_is_dark(frame, coor, (0, -1)):
        d += 8
    return "{:04b}".format(d)


def get_tiles_white(tiles):
    return randomtile(randomtile(
        [tiles["white0"], tiles["white0"], tiles["white0"], tiles["white0"], tiles["white0"], tiles["white0"],
         tiles["white0"], tiles["white0"], tiles["white0"], tiles["white0"], tiles["white0"], tiles["white0"],
         tiles["white0"], tiles["white0"], tiles["white0"], tiles["white0"], tiles["white0"], tiles["white0"],
         tiles["white0"], tiles["white0"], tiles["white0"], tiles["white0"], tiles["white0"], tiles["white0"],
         tiles["white0"], tiles["white0"], tiles["white0"], tiles["white0"], tiles["white0"], tiles["white0"],
         tiles["white0"], tiles["white0"], tiles["white0"], tiles["white0"], tiles["white0"], tiles["white0"],
         tiles["white0"], tiles["white0"], tiles["white0"], tiles["white0"], tiles["white0"], tiles["white1"]]))


def test_corners(image, frame, coor, tiles):
    if not if_relative_is_dark(frame, coor, (-1, -1)):
        image.alpha_composite(tiles["corner"][0], (coor[0] * 32, coor[1] * 32))
    if not if_relative_is_dark(frame, coor, (1, -1)):
        image.alpha_composite(tiles["corner"][1], (coor[0] * 32, coor[1] * 32))
    if not if_relative_is_dark(frame, coor, (-1, 1)):
        image.alpha_composite(tiles["corner"][3], (coor[0] * 32, coor[1] * 32))
    if not if_relative_is_dark(frame, coor, (1, 1)):
        image.alpha_composite(tiles["corner"][2], (coor[0] * 32, coor[1] * 32))


def place_black_tile(frame, coor, image, tiles, x, y):
    tile = randomtile(tiles["black"]).convert('RGBA')
    image.alpha_composite(tile, (x * 32, y * 32))
    test_corners(image, frame, coor, tiles)


def place_tile(frame, image, col, coor, tiles) -> None:
    x, y = coor
    if col == 0:
        white_tile = get_tiles_white(tiles)
        tile = white_tile.convert('RGBA')
        image.alpha_composite(tile, (x * 32, y * 32))
    else:
        if col == "1111":
            place_black_tile(frame, coor, image, tiles, x, y)
        else:
            find_gray = []
            for i in tiles["gray"].keys():
                if i.find(col) != -1:
                    find_gray.append(tiles["gray"][i])
            if len(find_gray) != 0:
                white_tile = get_tiles_white(tiles)
                tile = white_tile.convert('RGBA')
                image.alpha_composite(tile, (x * 32, y * 32))
                tile = randomtile(find_gray).convert('RGBA')
                image.alpha_composite(tile, (x * 32, y * 32))
            else:
                place_black_tile(frame, coor, image, tiles, x, y)


def process_frame(work_path, height, width, frame_bitmap, tiles, frame_counter, f_debug) -> None:
    image = Image.new('RGBA', (width * 32, height * 32))
    for y in range(height):
        for x in range(width):
            if frame_bitmap[y][x] == 1:
                check_autotiler = check_neighbours(frame_bitmap, (x, y))
                place_tile(frame_bitmap, image, check_autotiler, (x, y), tiles)
            else:
                place_tile(frame_bitmap, image, 0, (x, y), tiles)
    if f_debug is False:
        image.save(work_path + '/render/f' + str(frame_counter) + '.png')
    else:
        if f_debug == frame_counter:
            image.show()
            input("A")


def process_video(work_path, frame_bitmap, tiles, f_debug):
    frames = len(frame_bitmap)
    height = len(frame_bitmap[0])
    width = len(frame_bitmap[0][0])
    frame_counter = 0
    for i in range(frames):
        print('Render: Frame:', frame_counter, '/', frames)
        frame = frame_bitmap[i]
        process_frame(work_path, height, width, frame, tiles, frame_counter, f_debug)
        frame_counter += 1


def reset_export(work_folder):
    if os.path.exists(work_folder + '/render'):
        for f in os.listdir(work_folder + '/render'):
            os.remove(os.path.join(work_folder + '/render', f))
    else:
        os.mkdir(work_folder + '/render')


def main():
    work_path = 'C:/GitHub/BadAppleHeroes3'
    if not os.path.isfile(work_path + '/badapple.json'):
        BadAppleJsoner.badappleconvert([work_path, 20, 17])
    badapple_json = open(work_path + '/badapple.json')
    badapple_array = json.load(badapple_json)
    tiles = load_tiles(work_path + '/res/tiles')
    f_debug = 200
    reset_export(work_path)
    process_video(work_path, badapple_array, tiles, f_debug)


if __name__ == '__main__':
    main()
