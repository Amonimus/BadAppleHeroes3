from itertools import cycle

from PIL import Image


def place_health(template, x, amount):
    health = Image.open(work_folder+'/res/health.png')
    v_crop = 30 - amount
    health = health.crop((0, v_crop, health.size[0], health.size[1]))
    template.paste(health, (611, 213 + (32 * x) + v_crop), health)


def place_mana(template, x, amount):
    mana = Image.open(work_folder+'/res/mana.png')
    v_crop = 30 - amount
    health = mana.crop((0, v_crop, mana.size[0], mana.size[1]))
    template.paste(health, (667, 213 + (32 * x) + v_crop), health)


def place_small_portrait(template, x, char):
    portrait_s = Image.open(work_folder+'/portraits/S_' + char + '.png')
    template.paste(portrait_s, (619, 213 + (32 * x)), portrait_s)


def paste_locations(template):
    S_Shrine = Image.open(work_folder+'/portraits/S_Shrine.png')
    S_Ayakashi = Image.open(work_folder+'/portraits/S_Ayakashi.png')
    S_Mansion = Image.open(work_folder+'/portraits/S_Mansion.png')
    S_Moon = Image.open(work_folder+'/portraits/S_Moon.png')
    S_Village = Image.open(work_folder+'/portraits/S_Village.png')
    template.paste(S_Shrine, (749, 213 + (32 * 0)), S_Shrine)
    template.paste(S_Ayakashi, (749, 213 + (32 * 1)), S_Ayakashi)
    template.paste(S_Mansion, (749, 213 + (32 * 2)), S_Mansion)
    template.paste(S_Moon, (749, 213 + (32 * 3)), S_Moon)
    template.paste(S_Village, (749, 213 + (32 * 4)), S_Village)


def paste_herobox(template):
    Herobox = Image.open(work_folder+'/res/Herobox.png')
    template.paste(Herobox, (615, 400), Herobox)


def place_large_portrait(template, char):
    portrait_l = Image.open(work_folder+'/portraits/L_' + char + '.png')
    template.paste(portrait_l, (615, 400), portrait_l)


# def place_luck():
#     luck1 = Image.open("C:/GitHub/BadAppleHeroes3/portraits/L_" + char + ".png")

def work_image(current):
    print(current)
    template = Image.open(work_folder+'/res/Template_C.png')
    paste_locations(template)
    paste_herobox(template)
    for i in range(len(current)):
        place_small_portrait(template, i, current[i][0])
        place_health(template, i, current[i][1])
        place_mana(template, i, current[i][2])
    return template


def process(work_folder, values):
    for step in range(len(values) - 2):
        pool = cycle(values)
        if step > 0:
            for s in range(step):
                next(pool)
        current = []
        for i in range(5):
            current.append(next(pool))
        image = work_image(current)
        image.save(work_folder+'/pil/' + str(step) + '.png')


if __name__ == '__main__':
    work_folder = 'C:/GitHub/BadAppleHeroes3/'
    values = [("Reimu", 20, 25, 3, 2),
              ("Marisa", 15, 21, 1, 3),
              ("Patchouli", 12, 29, 2, 2),
              ("Remilia", 17, 22, 3, 2),
              ("Sakuya", 17, 22, 3, 3),
              ("Flandre", 12, 24, 3, 4),
              ("Youmu", 16, 20, 3, 3),
              ("Yuyuko", 18, 29, 3, 2),
              ("Komachi", 18, 21, 3, 2),
              ("Eiki", 22, 21, 2, 1),
              ("Mokou", 22, 19, 4, 2),
              ("Keine", 16, 23, 2, 2),
              ("HKeine", 19, 22, 2, 3),
              ("Eirin", 30, 22, 2, 3),
              ("Kaguya", 28, 19, 2, 1),
              ("Lunasa", 21, 20, 2, 4),
              ("Merlin", 19, 16, 3, 2),
              ("Lyrica", 20, 18, 2, 2),
              ("Chen", 15, 17, 3, 3),
              ("Ran", 17, 20, 2, 3),
              ("Tewi", 19, 22, 3, 2),
              ("Reisen", 16, 19, 2, 4),
              ("Momiji", 15, 22, 3, 2),
              ("Sanae", 21, 19, 2, 1),
              ("Hina", 18, 18, 1, 2),
              ("Kanako", 22, 23, 3, 2),
              ("Suwako", 22, 21, 2, 3),
              ("Yukari", 22, 27, 4, 3),
              ("Tenshi", 15, 18, 3, 2),
              ("Aya", 15, 21, 1, 3),
              ("Suika", 26, 22, 2, 1),
              ("Alice", 16, 22, 3, 2),
              ("Nitori", 15, 18, 2, 1),
              ("Yuuka", 20, 21, 3, 2),
              ("Elly", 20, 20, 2, 2),
              ]
    process(work_folder, values)
