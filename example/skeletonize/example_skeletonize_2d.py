# -*- python -*-
#
#       example_skeletonize_2d.py.py : 
#
#       Copyright 2015 INRIA - CIRAD - INRA
#
#       File author(s): Simon Artzet <simon.artzet@gmail.com>
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
#       ========================================================================

#       ========================================================================
#       External Import
import glob
import os

import cv2


#       ========================================================================
#       Local Import
from alinea.phenomenal.skeletonize_2d import skeletonize_thinning
from phenomenal.test.tools_test import show_images


#       ========================================================================
#       Code

def load_files(data_directory):

    images_names = glob.glob(data_directory + '*.png')

    pot_ids = dict()
    for i in range(len(images_names)):

        pot_id = images_names[i].split('\\')[-1].split('_')[0]
        if pot_id not in pot_ids:
            pot_ids[pot_id] = dict()

        date = images_names[i].split(' ')[0].split('_')[-1]
        data = 10
        if date not in pot_ids[pot_id]:
            pot_ids[pot_id][date] = dict()

        result = images_names[i].split('_sv')
        if len(result) == 2:
            angle = result[1].split('.png')[0]
        else:
            result = images_names[i].split('_tv')
            if len(result) == 2:
                angle = -1
            else:
                continue

        pot_ids[pot_id][date][int(angle)] = images_names[i]

    return pot_ids


def load_images(files, cv2_flag):
    images = dict()
    for angle in files:
        images[angle] = cv2.imread(files[angle], flags=cv2_flag)

    return images


def write_images(data_directory, files, images):

    if not os.path.exists(data_directory):
        os.makedirs(data_directory)

    for angle in images:

        path = files[angle]
        filename = path.split('\\')[-1]
        path = data_directory + filename

        cv2.imwrite(path, images[angle])


def run_example(data_directory):
    pot_ids = load_files(data_directory + 'repair_processing/')

    for pot_id in pot_ids:
        for date in pot_ids[pot_id]:

            files = pot_ids[pot_id][date]

            images = load_images(files, cv2.IMREAD_UNCHANGED)

            skeleton_images = example_skeletonize(images)

            # print pot_id, date
            # for angle in skeleton_images:
            #     show_images([images[angle], skeleton_images[angle]],
            #                 str(angle))

            write_images(data_directory + 'skeletonize_2d/',
                         files,
                         skeleton_images)


def example_skeletonize(images):
    skeleton_images = dict()
    for angle in images:
        skeleton_images[angle] = skeletonize_thinning(images[angle])

    return skeleton_images

#       ========================================================================
#       LOCAL TEST

if __name__ == "__main__":
    # run_example('../../local/data_set_0962_A310_ARCH2013-05-13/')
    # run_example('../../local/B73/')
    run_example('../../local/Figure_3D/')