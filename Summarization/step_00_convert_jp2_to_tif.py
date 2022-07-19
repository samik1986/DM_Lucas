from multiprocessing import Pool
import sys
import os


def get_date(filename):
    index = filename.index(YEAR_STRING)
    date = filename[index: index + 11]
    return date


def remove_dups(filenames):
    valid_names = {}
    for image_filename in filenames:
        num = image_filename[image_filename.index(INDEX_STRING) - 4: image_filename.index(INDEX_STRING)]
        if num not in valid_names:
            valid_names[num] = image_filename
            continue
        current_filename = valid_names[num]
        current_date = get_date(current_filename)
        current_month = int(current_date[5:7])
        current_day = int(current_date[8:10])

        image_date = get_date(image_filename)
        image_month = int(image_date[5:7])
        image_day = int(image_date[8:10])

        if (image_month > current_month) or (image_month == current_month and image_day > current_day):
            valid_names[num] = image_filename

    no_dups = list(valid_names.values())
    no_dups.sort()
    return no_dups


def function(image_filename):
    input_filename = os.path.join(input_dir, image_filename)
    input_filename_command = input_filename.replace('&', '\&')
    print('working on', input_filename)
    num = image_filename[image_filename.index(INDEX_STRING) - 4: image_filename.index(INDEX_STRING)]
    print('working on', num, 'out of', len(image_filenames))
    kdu_command = "kdu_expand -i " + input_filename_command + " -o " + output_dir + num + ".tif -num_threads 16"
    os.system(kdu_command)


THREADS = 64
INDEX_STRING = '.jp2'
YEAR_STRING = '2013'

input_dir = sys.argv[1]
output_dir = sys.argv[2]

if not os.path.exists(output_dir):
    os.mkdir(output_dir)

image_filenames = [listing for listing in os.listdir(input_dir) if listing != 'Likelihood']
print(len(image_filenames))
image_filenames = remove_dups(image_filenames)
print(len(image_filenames))

pool = Pool(THREADS)
pool.map(function, image_filenames)

