import os
import random
import shutil

import cv2
from PIL import Image, ImageOps


def convertPIL(paths_arr):
    tiles_img = map(Image.open, paths_arr)
    tiles_img = [ImageOps.fit(image, (32, 32), Image.LANCZOS) for image in tiles_img]
    return tiles_img


def loadTiles(folder):
    tiles = {}

    black_paths = [os.path.join(folder, f) for f in os.listdir(folder) if 'B' in f]
    tiles["black"] = convertPIL(black_paths)

    white0_paths = [os.path.join(folder, f) for f in os.listdir(folder) if 'W0' in f]
    tiles["white0"] = convertPIL(white0_paths)

    white1_paths = [os.path.join(folder, f) for f in os.listdir(folder) if 'W1' in f]
    tiles["white1"] = convertPIL(white1_paths)

    corner_paths = [os.path.join(folder, f) for f in os.listdir(folder) if 'C' in f]
    tiles["corner"] = convertPIL(corner_paths)

    gray_paths = [os.path.join(folder, f) for f in os.listdir(folder) if 'G' in f]
    gray_names = [f.split("G_")[1].split(".png")[0] for f in os.listdir(folder) if 'G' in f]
    tiles["gray"] = {gray_names[i]: convertPIL(gray_paths)[i] for i in range(len(gray_paths))}

    return tiles


def randomtile(arr):
    return random.choice(arr)


def ifTileDark(tile):
    return tile < 127


def ifRelativeIsDark(frame, coor, rel):
    y = coor[1] + rel[1]
    x = coor[0] + rel[0]
    if y >= len(frame):
        y = len(frame) - 1
        # return ifTileDark(frame_bitmap[coor[1]][coor[0]])
    elif y <= 0:
        y = 0
        # return ifTileDark(frame_bitmap[coor[1]][coor[0]])
    if x >= len(frame[0]):
        x = len(frame[0]) - 1
        # return ifTileDark(frame_bitmap[coor[1]][coor[0]])
    elif x <= 0:
        x = 0
        # return ifTileDark(frame_bitmap[coor[1]][coor[0]])
    p = frame[y][x]
    return ifTileDark(p)


def checkNeighbours(frame, coor):
    d = 0
    if ifRelativeIsDark(frame, coor, (0, 1)):
        d += 1
    if ifRelativeIsDark(frame, coor, (1, 0)):
        d += 2
    if ifRelativeIsDark(frame, coor, (-1, 0)):
        d += 4
    if ifRelativeIsDark(frame, coor, (0, -1)):
        d += 8
    return "{:04b}".format(d)


def getWhite(tiles):
    return randomtile(randomtile(
        [tiles["white0"], tiles["white0"], tiles["white0"], tiles["white0"], tiles["white0"], tiles["white0"],
         tiles["white0"], tiles["white0"], tiles["white0"], tiles["white0"], tiles["white0"], tiles["white0"],
         tiles["white0"], tiles["white0"], tiles["white0"], tiles["white0"], tiles["white0"], tiles["white0"],
         tiles["white0"], tiles["white0"], tiles["white0"], tiles["white0"], tiles["white0"], tiles["white0"],
         tiles["white0"], tiles["white0"], tiles["white0"], tiles["white0"], tiles["white0"], tiles["white0"],
         tiles["white0"], tiles["white0"], tiles["white0"], tiles["white0"], tiles["white0"], tiles["white0"],
         tiles["white0"], tiles["white0"], tiles["white0"], tiles["white0"], tiles["white0"], tiles["white1"]]))


def testCorners(image, frame, coor, tiles):
    if not ifRelativeIsDark(frame, coor, (-1, -1)):
        image.alpha_composite(tiles["corner"][0], (coor[0] * 32, coor[1] * 32))
    if not ifRelativeIsDark(frame, coor, (1, -1)):
        image.alpha_composite(tiles["corner"][1], (coor[0] * 32, coor[1] * 32))
    if not ifRelativeIsDark(frame, coor, (-1, 1)):
        image.alpha_composite(tiles["corner"][3], (coor[0] * 32, coor[1] * 32))
    if not ifRelativeIsDark(frame, coor, (1, 1)):
        image.alpha_composite(tiles["corner"][2], (coor[0] * 32, coor[1] * 32))

def placeBlack(frame, coor, image, tiles, x, y):
    tile = randomtile(tiles["black"]).convert('RGBA')
    image.alpha_composite(tile, (x * 32, y * 32))
    testCorners(image, frame, coor, tiles)

def placeTile(frame, image, col, coor, tiles) -> None:
    x, y = coor
    if col == 0:
        white_tile = getWhite(tiles)
        tile = white_tile.convert('RGBA')
        image.alpha_composite(tile, (x * 32, y * 32))
    else:
        if col == "1111":
            placeBlack(frame, coor, image, tiles, x, y)
        else:
            find_gray = []
            for i in tiles["gray"].keys():
                if (i.find(col) != -1):
                    find_gray.append(tiles["gray"][i])
            if len(find_gray) != 0:
                white_tile = getWhite(tiles)
                tile = white_tile.convert('RGBA')
                image.alpha_composite(tile, (x * 32, y * 32))
                tile = randomtile(find_gray).convert('RGBA')
                image.alpha_composite(tile, (x * 32, y * 32))
            else:
                placeBlack(frame, coor, image, tiles, x, y)


def processFrame(work_path, frame_bitmap, frame_counter, tiles) -> None:
    image = Image.new('RGBA', (render_sizes[0] * 32, render_sizes[1] * 32), (255, 255, 255, 255))
    for y in range(len(frame_bitmap)):
        for x in range(len(frame_bitmap[y])):
            if ifTileDark(frame_bitmap[y][x]):
                c = checkNeighbours(frame_bitmap, (x, y))
                placeTile(frame_bitmap, image, c, (x, y), tiles)
            else:
                placeTile(frame_bitmap, image, 0, (x, y), tiles)
    if F_DEBUG is False:
        image.save(work_path+'/result/f' + str(frame_counter) + '.png')
    else:
        image.show()
        input("A")


def workVideo(work_path, render_sizes) -> None:
    tiles = loadTiles(work_path + '/tiles')
    cv2_cap = cv2.VideoCapture(work_path + '/ref/BadApple.mp4')
    cv2_cap.set(3, render_sizes[0])
    cv2_cap.set(4, render_sizes[1])
    frame_counter = 0
    vid_length = int(cv2_cap.get(cv2.CAP_PROP_FRAME_COUNT))
    while frame_counter < vid_length-1:
        ret_flag, frame_bitmap = cv2_cap.read()
        try:
            frame_bitmap = cv2.cvtColor(frame_bitmap, cv2.COLOR_BGR2GRAY)
            frame_bitmap = cv2.resize(frame_bitmap, render_sizes, interpolation=cv2.INTER_AREA)
            if F_DEBUG is not False:
                cv2.imshow('frame_bitmap', frame_bitmap)
                if frame_counter == F_DEBUG:
                    processFrame(work_path, frame_bitmap, frame_counter, tiles)
            else:
                processFrame(work_path, frame_bitmap, frame_counter, tiles)
            print(frame_counter, '/', vid_length)
            frame_counter += 1
            if cv2.waitKey(1) & 0xFF == ord('q') or ret_flag is False:
                cv2_cap.release()
                cv2.destroyAllWindows()
                break
        except cv2.error:
            cv2_cap.release()
            cv2.destroyAllWindows()
            break
    cv2_cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    F_DEBUG = False
    work_path = 'C:/GitHub/BadAppleHeroes3'
    render_sizes = (20, 17)
    for f in os.listdir(work_path+'/result'):
        os.remove(os.path.join(work_path+'/result', f))
    workVideo(work_path, render_sizes)
