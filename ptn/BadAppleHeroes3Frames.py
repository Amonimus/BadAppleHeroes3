import os
from itertools import cycle

from PIL import Image


def paste_locations(work_folder, canvas, locations):
    for loc_i in range(len(locations)):
        s_icon = Image.open(work_folder + '/res/portraits/S_' + locations[loc_i] + '.png')
        canvas.paste(s_icon, (749, 213 + (32 * loc_i)), s_icon)


def place_health(work_folder, canvas, x, amount):
    health = Image.open(work_folder + '/res/health.png')
    v_crop = 30 - amount
    health = health.crop((0, v_crop, health.size[0], health.size[1]))
    canvas.paste(health, (611, 213 + (32 * x) + v_crop), health)


def place_mana(work_folder, canvas, x, amount):
    mana = Image.open(work_folder + '/res/mana.png')
    v_crop = 30 - amount
    health = mana.crop((0, v_crop, mana.size[0], mana.size[1]))
    canvas.paste(health, (667, 213 + (32 * x) + v_crop), health)


def place_small_portrait(work_folder, canvas, x, char):
    portrait_s = Image.open(work_folder + '/res/portraits/S_' + char + '.png')
    canvas.paste(portrait_s, (619, 213 + (32 * x)), portrait_s)


def paste_herobox(work_folder, canvas):
    herobox = Image.open(work_folder + '/res/Herobox.png')
    canvas.paste(herobox, (615, 400), herobox)


def place_large_portrait(work_folder, canvas, char):
    portrait_l = Image.open(work_folder + '/res/portraits/L_' + char + '.png')
    canvas.paste(portrait_l, (618, 402), portrait_l)


def place_spirit(work_folder, canvas, ini_lvl, luck_lvl):
    init_s = Image.open(work_folder + '/res/Init_' + str(ini_lvl) + '.png')
    canvas.paste(init_s, (621, 475), init_s)
    luck_s = Image.open(work_folder + '/res/Luck_' + str(luck_lvl) + '.png')
    canvas.paste(luck_s, (621, 492), luck_s)


def place_frame(work_folder, canvas, select):
    frame = Image.open(work_folder + '/res/portraits/Frame_Active.png')
    canvas.paste(frame, (618, 212 + (32 * select)), frame)


def place_select(work_folder, canvas, visible_heroes, select):
    place_large_portrait(work_folder, canvas, visible_heroes[select][0])
    place_spirit(work_folder, canvas, visible_heroes[select][3], visible_heroes[select][4])
    place_frame(work_folder, canvas, select)


def work_image(work_folder, visible_heroes, locations, step, select):
    print(visible_heroes)
    canvas = Image.open(work_folder + '/res/Template_C.png')
    paste_locations(work_folder, canvas, locations)
    paste_herobox(work_folder, canvas)
    for i in range(len(visible_heroes)):
        place_small_portrait(work_folder, canvas, i, visible_heroes[i][0])
        place_health(work_folder, canvas, i, visible_heroes[i][1])
        place_mana(work_folder, canvas, i, visible_heroes[i][2])
    place_select(work_folder, canvas, visible_heroes, select)
    canvas.save(work_folder + '/pil/' + str(step) + '_' + str(select) + '.png')


def forward(hero_loop, step):
    if step > 0:
        for s in range(step):
            next(hero_loop)


def process_queue(work_folder, hero_params, locations):
    for step in range(len(hero_params) - 2):
        hero_loop = cycle(hero_params)
        forward(hero_loop, step)
        heroes_visible = []
        for i in range(5):
            heroes_visible.append(next(hero_loop))
        if step == 0:
            select = 0
            work_image(work_folder, heroes_visible, locations, step, select)
            select = 1
            work_image(work_folder, heroes_visible, locations, step, select)
        elif step == len(hero_params) - 3:
            select = 3
            work_image(work_folder, heroes_visible, locations, step, select)
            select = 4
            work_image(work_folder, heroes_visible, locations, step, select)
        select = 2
        work_image(work_folder, heroes_visible, locations, step, select)


def reset_export(work_folder):
    if os.path.exists(work_folder + '/pil'):
        for f in os.listdir(work_folder + '/pil'):
            os.remove(os.path.join(work_folder + '/pil', f))
    else:
        os.mkdir(work_folder + '/pil')


def main():
    work_folder = 'C:/GitHub/BadAppleHeroes3'
    reset_export(work_folder)
    hero_params = [("Reimu", 20, 25, 2, 1),
                   ("Marisa", 15, 21, 0, 2),
                   ("Patchouli", 12, 29, 1, 1),
                   ("Remilia", 17, 22, 2, 1),
                   ("Sakuya", 17, 22, 2, 2),
                   ("Flandre", 12, 24, 2, 3),
                   ("Youmu", 16, 20, 2, 2),
                   ("Yuyuko", 18, 29, 2, 1),
                   ("Komachi", 18, 21, 2, 1),
                   ("Eiki", 22, 21, 1, 0),
                   ("Mokou", 22, 19, 3, 1),
                   ("Keine", 16, 23, 1, 1),
                   ("HKeine", 19, 22, 1, 2),
                   ("Eirin", 30, 22, 1, 2),
                   ("Kaguya", 28, 19, 1, 0),
                   ("Lunasa", 21, 20, 1, 3),
                   ("Merlin", 19, 16, 2, 1),
                   ("Lyrica", 20, 18, 1, 1),
                   ("Chen", 15, 17, 2, 2),
                   ("Ran", 17, 20, 1, 2),
                   ("Tewi", 19, 22, 2, 1),
                   ("Reisen", 16, 19, 1, 3),
                   ("Momiji", 15, 22, 2, 1),
                   ("Sanae", 21, 19, 1, 0),
                   ("Hina", 18, 18, 0, 1),
                   ("Kanako", 22, 23, 2, 1),
                   ("Suwako", 22, 21, 1, 2),
                   ("Yukari", 22, 27, 3, 2),
                   ("Tenshi", 15, 18, 2, 1),
                   ("Aya", 15, 21, 0, 2),
                   ("Suika", 26, 22, 1, 0),
                   ("Alice", 16, 22, 2, 1),
                   ("Nitori", 15, 18, 1, 0),
                   ("Yuuka", 20, 21, 2, 1),
                   ("Elly", 20, 20, 1, 1),
                   ]
    locations = ['Shrine', 'Ayakashi', 'Mansion', 'Moon', 'Village']
    process_queue(work_folder, hero_params, locations)


if __name__ == '__main__':
    main()
