# -*- python -*-
#
#       calibration_2_script.py :
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
# ==============================================================================

# ==============================================================================
# Load Chessboard

import alinea.phenomenal.chessboard

chessboard_1 = alinea.phenomenal.chessboard.Chessboard.read(
    'chessboard_1')

chessboard_2 = alinea.phenomenal.chessboard.Chessboard.read(
    'chessboard_2')

# ==============================================================================
# Calibration
import alinea.phenomenal.calibration_model

# # Create Object
calib = alinea.phenomenal.calibration_model.Calibration(
    [chessboard_1, chessboard_2], (2056, 2454), verbose=True)
#
res = calib.find_model_parameters_2_chess()
cam_params, chess_params_1, chess_params_2 = res
print cam_params
print chess_params_1
print chess_params_2

cam_params.write('n_camera_parameters')
chess_params_1.write('n_chessboard_parameters_1')
chess_params_2.write('n_chessboard_parameters_2')

cam_params = alinea.phenomenal.calibration_model.CameraModelParameters.read(
    'n_camera_parameters')

chess_params_1 = alinea.phenomenal.calibration_model.ChessboardModelParameters.\
    read('n_chessboard_parameters_1')

chess_params_2 = alinea.phenomenal.calibration_model.ChessboardModelParameters.\
    read('n_chessboard_parameters_2')

print cam_params
print chess_params_1
print chess_params_2

guess = list()
guess[0:6] = chess_params_1.get_parameters()
guess[6:12] = chess_params_2.get_parameters()
guess[12:19] = cam_params.get_parameters()[1:]

print guess

err = calib.fit_function_2(guess)
print err

# ==============================================================================
# Viewing
import alinea.phenomenal.viewer

import cv2
import glob

data_directory = '../../local/CHESSBOARD_1/'

projection = alinea.phenomenal.calibration_model.ModelProjection(cam_params)

# Load files
files_path = glob.glob(data_directory + '*.png')
angles = map(lambda x: int((x.split('_sv')[1]).split('.png')[0]), files_path)

for i in range(len(files_path)):
    img = cv2.imread(files_path[i], cv2.IMREAD_UNCHANGED)

    alinea.phenomenal.viewer.show_chessboard_3d_projection_on_image(
        img,
        angles[i],
        chessboard_1,
        chess_params_1,
        projection,
        name_windows=str(angles[i]))



# Define size of chessboard
#
#
# [  2.43752236e+02   1.70997995e+02  -1.67389666e+02  -2.18081296e+00
#   -3.15465685e+00  -2.53989672e+02  -1.40843310e+02   1.29963186e+02
#    2.18972083e+00   2.07212563e-02   4.49953083e+03   4.46805669e+03
#    5.78332647e+03   6.01170494e+00  -4.44821223e+00]



# [ -1.56104907e+02  -1.84313925e+02   3.45337483e+02  -3.95135546e+01
#    3.43241542e-02   1.92667812e+02   1.87918586e+02   3.05153661e+02
#    9.61008491e+01   2.10449048e+02   4.28812150e+03   4.26745143e+03
#    5.00512535e+03   2.42628401e+02   1.83057881e+02]

#       ========================================================================
#       LOCAL TEST

if __name__ == "__main__":
    pass