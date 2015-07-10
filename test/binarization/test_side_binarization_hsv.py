# -*- python -*-
#
#       test_side_binarization_hsv: Module Description
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
#       =======================================================================

"""
Write the doc here...
"""

__revision__ = ""

#       =======================================================================
#       External Import
import glob

#       =======================================================================
#       Local Import
import alinea.phenomenal.binarization as binarization
import alinea.phenomenal.configuration as configuration
import tools_test

#       =======================================================================

def check_side_binarization_hsv(data_directory,
                                refs_directory,
                                rewrite=False):
    """
    :param data_directory:
    :param refs_directory:
    :param rewrite:
    :return:
    """
    images_path = glob.glob(data_directory + '*sv*.png')
    images = tools_test.load_images(images_path)

    config = configuration.loadconfig('configuration_side_image_michael.cfg')
    bin_config = configuration.binarization_config(config)

    list_binarize_image = []
    for image in images:
        list_binarize_image.append(
            binarization.side_binarization_hsv(image, bin_config))

    tools_test.check_result_with_ref(list_binarize_image,
                                     refs_directory,
                                     "side_binarization_hsv",
                                     rewrite)


def check_top_binarization_hsv(data_directory,
                                refs_directory,
                                rewrite=False):
    """
    :param data_directory:
    :param refs_directory:
    :param rewrite:
    :return:
    """
    images_path = glob.glob(data_directory + '*tv*.png')
    images = tools_test.load_images(images_path)

    config = configuration.loadconfig('configuration_top_image.cfg')
    bin_config = configuration.binarization_config(config)

    list_binarize_image = []
    for image in images:
        list_binarize_image.append(
            binarization.top_binarization_hsv(image, bin_config))

    tools_test.check_result_with_ref(list_binarize_image,
                                     refs_directory,
                                     "top_binarization_hsv",
                                     rewrite)

def test_suite_generator():
    tools_test.print_check(check_side_binarization_hsv.__name__)
    for directory in tools_test.directories:
        yield (check_side_binarization_hsv,
               directory[0],
               directory[1])

    for directory in tools_test.directories:
        yield (check_top_binarization_hsv,
               directory[0],
               directory[1],
               True)