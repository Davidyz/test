#!/usr/bin/python3
import music, UnixIO, sys, os, multiprocessing
arguments = sys.argv

overwrite = '-s' in arguments
bitrate = 320
if overwrite:
    arguments.remove('-s')


if '-b' in arguments:
    bitrate = int(arguments.pop(arguments.index('-b') + 1))
    arguments.remove('-b')

black_list = ('Chopin', 'Kotaro', 'Pacific', 'Vivaldi', 'Andrew')   # add keywords of songs that should not be converted to this tuple.

def skip(song):
    '''
    Return True if the song should not be converted.
    '''
    for i in black_list:
        if i in song:
            return True
    return False

if len(arguments) == 3:
    for i in arguments[1:]:
        if (not os.path.isfile(i)) and (not os.path.isdir(i)):
            raise music.InputError('The input {} is not valid!'.format(i))

    args = {'original':arguments[1],'destination':arguments[2]}

elif len(arguments) == 2 and (os.path.isfile(arguments[1]) or os.path.isdir(arguments[1])):
    args = {'original':arguments[1],'destination':False}

songs = [music.Music(i) for i in UnixIO.listdir(args['original']) if music.is_music(i) and (not skip(i))]

def execute(song, to, overwrite, br=320):
    if os.path.isfile(to) and (not overwrite):
        # when 'to' is a file
        return

    elif os.path.isfile(to) and (not overwrite) and (song.path.split('/')[-1].replace(song.form, 'mp3') in os.listdir(to)):
        # when 'to' is a directory
        return
    print('Converting {}'.format(str(song)))
    song.format(target=to, form='mp3', overwrite=overwrite, bitrate=br)

for song in songs:
    execute(song, args['destination'], overwrite, bitrate)

if args['destination']:
    lyrics = (j for j in UnixIO.listdir(args['original']) if 'lrc' in j)
    for i in lyrics:
        UnixIO.cp(i, args['destination'])
