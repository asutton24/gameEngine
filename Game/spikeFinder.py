import os

for i in range(1, 5):
    folder = 'Rooms\\Level{}'.format(i)
    files = os.listdir(folder)
    files.remove('Specials')
    for f in files:
        if f[1] != str(i):
            with open(folder + '\\' + f, 'r') as file:
                lines = file.readlines()
                for l in lines:
                    if 'spike.spr' in l:
                        print(f)