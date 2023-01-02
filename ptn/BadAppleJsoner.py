import sys
from typing import Union

import cv2
import json

from numpy import ndarray


def is_pixel_dark(pixel: int) -> int:
    """
    Checks if pixel is dark (0 is Black, 255 is White)
    :param pixel: Pixel. (int)
    :return: 1 (Dark) or 0 (Bright) (int)
    :rtype: int
    """
    if pixel < 127:
        return 1
    else:
        return 0


def frame_to_binary(frame_bitmap: ndarray) -> None:
    """
    Converts CV2 bitmap (0 to 255) to a binary (0 to 1) bitmap.
    :param frame_bitmap: CV2 frame. (numpy.ndarray = list[h][w])
    """
    for y in range(len(frame_bitmap)):
        for x in range(len(frame_bitmap[y])):
            frame_bitmap[y][x] = is_pixel_dark(frame_bitmap[y][x])
        frame_bitmap[y] = frame_bitmap[y].tolist()


def frame_compress(frame_bitmap: ndarray, render_sizes: tuple) -> ndarray:
    """
    Converts CV2 Frame (RGB) to monochrome (0 to 255) and resizes.
    :param frame_bitmap: CV2 Frame. (numpy.ndarray = list[h][w])
    :param render_sizes: New size. (tulpe(width (int), height (int))
    :return: Converted frame. (list[h][w])
    :rtype: numpy.ndarray
    """
    frame_bitmap = cv2.cvtColor(frame_bitmap, cv2.COLOR_BGR2GRAY)
    frame_bitmap = cv2.resize(frame_bitmap, render_sizes, interpolation=cv2.INTER_AREA)
    return frame_bitmap


def frame_process(cv2_cap: cv2.cv2.VideoCapture, render_sizes: tuple, frame_counter: int, flag_debug: int = False) -> \
        Union[list, bool]:
    """
    Works on CV2 Frame.
    :param cv2_cap: CV2 Frame. (cv2.cv2.VideoCapture)
    :param render_sizes: New size. (tulpe(width (int), height (int))
    :param frame_counter: Frame counter. (int)
    :param flag_debug: If is in debug. Only processes the specified frame number. Optional. (int)
    :return: 2D Frame's pixel array / False. (list[h (int)][w (int)] / bool)
    :rtype: list or bool
    """
    ret_flag, frame_bitmap = cv2_cap.read()
    try:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Break.")
            return False
        frame_bitmap: ndarray = frame_compress(frame_bitmap, render_sizes)
        if flag_debug is not False:
            cv2.imshow('frame_bitmap', frame_bitmap)
            if flag_debug == frame_counter:
                frame_to_binary(frame_bitmap)
                input("Pause")
        else:
            frame_to_binary(frame_bitmap)
        frame_bitmap: list = frame_bitmap.tolist()
        return frame_bitmap
    except cv2.error:
        print(cv2.error.msg)
        # return False


def cap_release(cv2_cap: cv2.cv2.VideoCapture) -> None:
    """
    Stops CV2 process.
    :param cv2_cap: CV2 Frame. (cv2.cv2.VideoCapture)
    """
    cv2_cap.release()
    cv2.destroyAllWindows()


def json_export(frame_list: list, work_path: str) -> None:
    """
    Writes the converted video into .json.
    :param work_path: Write dir. (str)
    :param frame_list: Converted video. (list[list[h (int)][w (int)]])
    """
    json_object = json.dumps(frame_list)
    with open(work_path + '/badapple.json', 'w') as outfile:
        outfile.write(json_object)


def video_process(work_path: str, render_width: int, render_height: int, flag_debug: int = False) -> None:
    """
    Main work.
    :param work_path: Working directory. (str)
    :param render_width: Converted video width in pixels. (int)
    :param render_height: Converted video height in pixels. (int)
    :param flag_debug: Debug. Shows the video and processes only the specified frame number. Optional. (int)
    """
    cv2_cap = cv2.VideoCapture(work_path + '/BadApple.mp4')
    render_sizes = (render_width, render_height)
    frame_counter = 0
    vid_length = int(cv2_cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_list = []
    while frame_counter <= vid_length:
        print('Jsoner: Frame:', frame_counter, '/', vid_length)
        frame_converted = frame_process(cv2_cap, render_sizes, frame_counter, flag_debug)
        if frame_converted is not False:
            frame_list.append(frame_converted)
            frame_counter += 1
        else:
            print("Error.")
            break
    cap_release(cv2_cap)
    json_export(frame_list, work_path)
    print("Done.")


def badappleconvert(ba_args: list) -> None:
    """
    Main.
    :param ba_args: [DIRECTORY, WIDTH, HEIGHT, (DEBUG_FRAME)]
    """
    work_path = ba_args[0]
    render_width = int(ba_args[1])
    render_height = int(ba_args[2])
    if len(ba_args) == 4:
        flag_debug = int(ba_args[3])
        video_process(work_path, render_width, render_height, flag_debug)
    else:
        video_process(work_path, render_width, render_height)


if __name__ == '__main__':
    args = sys.argv[1:]
    badappleconvert(args)
