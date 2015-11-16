# -*- python -*-
#
#       scipt.py :
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
import glob


#       ========================================================================
#       Local Import
import alinea.phenomenal.chessboard
#       ========================================================================
#       Code
#
data_directory = '../../local/CHESSBOARD_ELCOM_5_1/'


# Load files
files_path = glob.glob(data_directory + '*_side_*.png')
angles = map(lambda x: int((x.split('_side_')[1]).split('.png')[0]), files_path)

image_path = dict()
for i in range(len(files_path)):
    image_path[angles[i]] = files_path[i]

    img = cv2.imread(image_path[angles[i]], cv2.IMREAD_GRAYSCALE)

    size_image = img.shape

print size_image
# # Define Chessboard size
# chessboard = alinea.phenomenal.chessboard.Chessboard(47, (8, 6))
#
# # Load image and find chessboard corners in each image
# chessboard_corners = dict()
# for angle in image_path:
#     print angle
#     img = cv2.imread(image_path[angle], cv2.IMREAD_GRAYSCALE)
#     chessboard.find_and_add_corners(angle, img)
#
# print chessboard
#
# chessboard.write('corners_points_elcom_5')

chessboard = alinea.phenomenal.chessboard.Chessboard.read(
    'corners_points_elcom_5')

import alinea.phenomenal.result_viewer
import alinea.phenomenal.calibration_model

calib = alinea.phenomenal.calibration_model.Calibration()
calib.find_model_parameters(chessboard, size_image)
calib.write_calibration('my_calibration_elcom_5')

calib = alinea.phenomenal.calibration_model.Calibration.read_calibration(
    'my_calibration_elcom_5')


for angle in image_path:
    img = cv2.imread(image_path[angle], cv2.IMREAD_UNCHANGED)

    alinea.phenomenal.result_viewer.show_chessboard_3d_projection_on_image(
        img, angle, chessboard, calib, name_windows=str(angle))
# Define size of chessboard



