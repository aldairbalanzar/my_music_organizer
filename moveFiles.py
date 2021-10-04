import os
import shutil

music_dir = "C:/Users/aldai/Music/Music/"
source = "./djcity"
practice_dir = "./practiceDir"
artist_cache = {}
files = os.listdir(source)

def make_song_path_to_music(song):
    song_path = os.path.join(music_dir, song)
    return song_path

def make_artist_cache(song):
    artist = song.partition("-")[0]
    artist = artist.rstrip()
    artist = artist.partition("ft")[0]
    artist = artist.rstrip()
    if artist not in artist_cache:
        artist_cache[artist] = []
        return artist
    if song not in artist_cache[artist]:
        song_path = make_song_path_to_music(song)
        artist_cache[artist].append(song_path)
        return artist

def strip_artist_name(source, song):
    new_name = song.partition("-")[2].lstrip()
    os.rename("./{}/{}".format(source, song), "./{}/{}".format(source, new_name))
    return new_name


def make_dir_in_music(cache):
    for name in cache:
        dir_path = os.path.join("./renamed/", name)
        if os.path.exists(dir_path):
            print("EXISTS")
        else:
            print("{} DOES NOT exist".format(name))
            os.mkdir(dir_path)

def move_song_to_dir(source, path):
    shutil.move(source, path)

for song in files:
    artist = make_artist_cache(song)
    new_name = strip_artist_name(source, song)
    make_dir_in_music(artist_cache)
    move_song_to_dir("./{}/{}".format(source, new_name), "{}/{}".format(music_dir, artist))
    




# for f in files:
#     source_path = os.path.join(source, f)

#     if os.path.exists(path):
#         print('this dir exists')
#     else:
#         print("this path doesnt exist")
#         os.mkdir(path)
#         shutil.move("./djcity/{}".format(f), "./practiceDir/{}".format(f))
