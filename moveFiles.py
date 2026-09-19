import os
import shutil

music_dir = "/Volumes/main_music/_aldair_music"
source_dir = "./bpmsupreme"
practice_dir = "./practice_dir"

artist_cache = {}
files = os.listdir(source_dir)

RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
RESET = '\033[0m'  # Resets the terminal color back to default


def make_song_path_to_folder(song, practice_setting):
    if practice_setting is True:
        song_path = os.path.join(practice_dir, song)
    else:
        song_path = os.path.join(music_dir, song)

    return song_path


def make_artist_cache(song):
    # BPM Supreme format:
    # Artist - Song Title.mp3
    #
    # Split specifically on " - " so artists like
    # Jay-Z and T-Pain don't get split incorrectly.
    parts = song.split(" - ", 1)

    if len(parts) != 2:
        print(f"Could not determine artist from: {song}")
        return None

    artist = parts[0].strip()

    # Remove featured artist from folder name.
    #
    # Example:
    # Icona Pop ft Charli XCX
    # becomes:
    # Icona Pop
    artist = artist.split(" ft ", 1)[0].strip()

    if artist not in artist_cache:
        artist_cache[artist] = []

    return artist


def strip_artist_name(source, song):
    # Split only on BPM Supreme's artist/title separator.
    parts = song.split(" - ", 1)

    if len(parts) != 2:
        print(f"Could not parse filename: {song}")
        return song

    new_name = parts[1].strip()

    old_path = os.path.join(source, song)
    new_path = os.path.join(source, new_name)

    try:
        print(f"{YELLOW}Renaming:{RESET} {song} {YELLOW}->{RESET} {new_name}{RESET}")

        # Don't overwrite an existing file.
        if os.path.exists(new_path):
            print(f"File already exists: {new_path}")
            return new_name

        os.rename(old_path, new_path)

    except Exception as e:
        print(f"Error renaming {song}: {e}")
        return song

    return new_name


def make_dir_in_folder(cache, practice_setting):
    for name in cache:

        if practice_setting is True:
            dir_path = os.path.join(practice_dir, name)
        else:
            dir_path = os.path.join(music_dir, name)

        # print(f"Current dir: {dir_path}")

        # makedirs is safer than mkdir because it can
        # create parent directories if necessary.
        os.makedirs(dir_path, exist_ok=True)


def copy_song_to_dir(source, path):
    destination = os.path.join(
        path,
        os.path.basename(source)
    )

    # Skip the file if it already exists.
    if os.path.exists(destination):
        print(f"{YELLOW}Already exists: {destination}{RESET}")
        return False

    try:
        shutil.copy2(source, path)

        print(f"{YELLOW}Copied:{RESET} {source} {YELLOW}->{RESET} {path}")

        return True

    except Exception as e:
        print(f"{RED}Error copying {source}: {e}{RESET}")
        return False


def do_tasks(song_list, source, practice_setting=True):

    for song in song_list:

        # Ignore folders and other non-file items.
        original_source_path = os.path.join(source, song)

        if not os.path.isfile(original_source_path):
            continue

        artist = make_artist_cache(song)

        # Skip filenames that don't match:
        # Artist - Song.mp3
        if artist is None:
            continue

        new_name = strip_artist_name(source, song)

        make_dir_in_folder(
            artist_cache,
            practice_setting
        )

        source_path = os.path.join(
            source,
            new_name
        )

        if practice_setting is True:
            destination_path = os.path.join(
                practice_dir,
                artist
            )
        else:
            destination_path = os.path.join(
                music_dir,
                artist
            )

        copy_song_to_dir(
            source_path,
            destination_path
        )



# -------------------------------------------
# Empty directory cleanup
# -------------------------------------------

def check_for_empty_folders(path):

    dirs = list_of_dirs(path)
    dir_files = list_of_files(path)

    if len(dirs) == 0 and len(dir_files) == 0:

        print(f"DELETING: {path}")

        os.rmdir(path)

        return

    for d in dirs:

        dir_path = os.path.join(
            path,
            d
        )

        check_for_empty_folders(dir_path)


def list_of_dirs(path):

    return [
        x.name
        for x in os.scandir(path)
        if x.is_dir()
    ]


def list_of_files(path):

    return [
        f
        for f in os.listdir(path)
        if os.path.isfile(
            os.path.join(path, f)
        )
    ]


# -------------------------------------------
# Run
# -------------------------------------------

do_tasks(
    files,
    source_dir,
    False
)

print(f"{GREEN}Done moving files.{RESET}")

# Uncomment when you want to clean up empty folders.
# check_for_empty_folders(music_dir)