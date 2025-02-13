import os
import shutil

music_dir = "C:/Users/aldai/Music/Music/"
source_dir = "./bpmsupreme"
practice_dir = "./practice_dir"
artist_cache = {}
files = os.listdir(source_dir)

def make_song_path_to_folder(song, practice_setting):
    if practice_setting is True:
        song_path = os.path.join(practice_dir, song)
    else:
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
    return artist

def strip_artist_name(source, song):
    new_name = song.partition("-")[2].lstrip()
    try:
        os.rename(f"./{source}/{song}", f"./{source}/{new_name}")
    except:
        pass
    return new_name


def make_dir_in_folder(cache, practice_setting):
    for name in cache:
        if practice_setting is True:
            dir_path = os.path.join(f"{practice_dir}/", name)
        else:
            dir_path = os.path.join(f"{music_dir}/", name)

        if os.path.exists(dir_path):
            pass
        else:
            os.mkdir(dir_path)

def move_song_to_dir(source, path):
    try:
        shutil.move(source, path)
    except:
        pass

def do_tasks(song_list, source, practice_setting=True):

    for song in song_list:
        artist = make_artist_cache(song)
        new_name = strip_artist_name(source, song)

        make_dir_in_folder(artist_cache, practice_setting)

        source_path = f"{source}/{new_name}"
        if practice_setting is True:
            destination_path = f"{practice_dir}/{artist}"
        else:
            destination_path = f"{music_dir}/{artist}"

        move_song_to_dir(source_path, destination_path)

def check_for_empty_folders(path):
    dirs = list_of_dirs(path)
    dir_files = list_of_files(path)
    if(len(dirs) == 0 and len(dir_files) == 0):
        print(f'DELETING: {path}')
        os.rmdir(path)
        return

    for d in dirs:
        dir_path = f'{path}/{d}'
        check_for_empty_folders(dir_path)


def list_of_dirs(path):
    return [x.name for x in os.scandir(path) if x.is_dir()]

def list_of_files(path):
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]


# do_tasks(files, source_dir, False)
check_for_empty_folders(music_dir)
