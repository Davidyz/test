#!/usr/bin/python3
import music, UnixIO, sys, os, multiprocessing
arguments = sys.argv

replaced = '-r' in arguments
bitrate = None
if replaced:
    arguments.remove('-r')

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

def execute(song, replace, to):
    if replace:
        song.format('mp3', True, bitrate)
        return
    song.format('mp3', False, bitrate)
    if to and song.is_lossless():
        UnixIO.mv(song.path().replace(song.form, 'mp3'), to)
    elif to and (not song.is_lossless()):
        UnixIO.cp(song.path().replace(song.form, 'mp3'), to)

pool = multiprocessing.Pool(processes = 3)
pool.starmap_async(execute, ([i, replaced, args['destination']] for i in songs)).get()
pool.close()
pool.join()

if args['destination']:
    lyrics = (j for j in UnixIO.listdir(args['original']) if 'lrc' in j)
    for i in lyrics:
        UnixIO.cp(i, args['destination'])
