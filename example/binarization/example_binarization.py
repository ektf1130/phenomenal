# -*- python -*-
#
#       example_binarization.py : 
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
import cv2

#       ========================================================================
#       Local Import
from alinea.phenomenal.binarization import binarization, get_mean_image
from alinea.phenomenal.configuration import loadconfig, binarization_config
from alinea.phenomenal.result_viewer import show_images

from phenomenal.example.example_tools import (
    load_files, load_images, write_images)

#       ========================================================================
#       Code


def run_example(data_directory):

    pot_ids = load_files(data_directory)

    for pot_id in pot_ids:
        for date in pot_ids[pot_id]:

            files = pot_ids[pot_id][date]

            images = load_images(files, cv2.IMREAD_UNCHANGED)

            # images_binarize_adaptive_threshold = \
            #     example_binarization_adaptive_threshold(images)
            images_binarize_mean_shift = example_binarization_mean_shift(images)
            # images_binarize_elcom = example_binarization_elcom(images)
            # images_binarize_hsv = example_binarization_hsv(images)
            #
            # print pot_id, date
            # for angle in images:
            #     show_images(
            #         [images[angle],
            #          images_binarize_adaptive_threshold[angle],
            #          images_binarize_mean_shift[angle],
            #          images_binarize_elcom[angle],
            #          images_binarize_hsv[angle]], str(angle))

            write_images(data_directory + '/binarization/',
                         files,
                         images_binarize_mean_shift)


def example_binarization_adaptive_threshold(images):

    load_configuration = loadconfig('configuration_side_image_michael.cfg')
    configuration_side = binarization_config(load_configuration)

    load_configuration = loadconfig('configuration_top_image.cfg')
    configuration_top = binarization_config(load_configuration)

    images_binarize = dict()
    for angle in images:

        if angle == -1:
            images_binarize[angle] = binarization(
                images[angle],
                configuration_top,
                is_top_image=True,
                methods='hsv')
        else:
            images_binarize[angle] = binarization(
                images[angle],
                configuration_side,
                methods='adaptive_threshold')

    return images_binarize


def example_binarization_mean_shift(images):

    load_configuration = loadconfig('configuration_image_basic.cfg')
    configuration_side = binarization_config(load_configuration)

    top_image = images.pop(-1)
    mean_image = get_mean_image(images.values())
    images[-1] = top_image

    load_configuration = loadconfig('configuration_top_image.cfg')
    configuration_top = binarization_config(load_configuration)

    images_binarize = dict()
    for angle in images:

        if angle == -1:
            images_binarize[angle] = binarization(
                images[angle],
                configuration_top,
                is_top_image=True,
                methods='hsv')
        else:
            images_binarize[angle] = binarization(
                images[angle],
                configuration_side,
                methods='mean_shift',
                mean_image=mean_image)

    return images_binarize


def example_binarization_elcom(images):

    load_configuration = loadconfig('configuration_cubicle_6_elcom.cfg')
    configuration_side = binarization_config(load_configuration)

    top_image = images.pop(-1)
    mean_image = get_mean_image(images.values())
    images[-1] = top_image


    load_configuration = loadconfig('configuration_top_image.cfg')
    configuration_top = binarization_config(load_configuration)

    images_binarize = dict()
    for angle in images:

        if angle == -1:
            images_binarize[angle] = binarization(
                images[angle],
                configuration_top,
                is_top_image=True,
                methods='hsv')
        else:
            images_binarize[angle] = binarization(
                images[angle][0:2448, 0:2048],
                configuration_side,
                methods='elcom',
                mean_image=mean_image[0:2448, 0:2048])

    return images_binarize


def example_binarization_hsv(images):

    load_configuration = loadconfig('configuration_side_image_michael.cfg')
    configuration_side = binarization_config(load_configuration)

    load_configuration = loadconfig('configuration_top_image.cfg')
    configuration_top = binarization_config(load_configuration)

    images_binarize = dict()
    for angle in images:

        if angle == -1:
            images_binarize[angle] = binarization(
                images[angle],
                configuration_top,
                is_top_image=True,
                methods='hsv')
        else:
            images_binarize[angle] = binarization(
                images[angle],
                configuration_side,
                methods='hsv',)

    return images_binarize

#       ========================================================================
#       LOCAL TEST

if __name__ == "__main__":
    run_example('../../local/data_set_0962_A310_ARCH2013-05-13/')
    # run_example('../../local/B73/')

    # run_example('../../local/Figure_3D/')