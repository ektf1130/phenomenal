# -*- python -*-
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
import os
import cv2
import openalea.deploy.shared_data

import alinea.phenomenal.configuration
import alinea.phenomenal.misc
import alinea.phenomenal.calibration_model
import alinea.phenomenal.multi_view_reconstruction
import alinea.phenomenal.binarization_routine
import alinea.phenomenal.binarization_post_processing
import alinea.phenomenal.data_transformation
import alinea.phenomenal.mesh
import alinea.phenomenal.viewer
import alinea.phenomenal.plant_1
from alinea.phenomenal.binarization_routine import (top_binarization_hsv,
                                            side_binarization_mean_shift)
from alinea.phenomenal.binarization_algorithm import get_mean_image


# ==============================================================================


def binarization(images, images_directory, images_path):
    factor = alinea.phenomenal.configuration.\
        binarization_factor('factor_image_basic.cfg')

    if (-1) in images:
        top_image = images.pop((-1))
        mean_image = get_mean_image(images.values())
        images[(-1)] = top_image
    else:
        mean_image = get_mean_image(images.values())

    binarize_images = dict()
    for angle in images:
        if angle < 0:
            binarize_images[angle] = top_binarization_hsv(images[angle], factor)
        else:
            binarize_images[angle] = side_binarization_mean_shift(
                images[angle], mean_image, factor)

    alinea.phenomenal.misc.write_images(
        images_directory + '/binarization/',
        images_path,
        binarize_images)

    return binarize_images


def binarization_post_processing(binarize_images,
                                 images_directory,
                                 images_path):

    share_data_directory = openalea.deploy.shared_data. \
        shared_data(alinea.phenomenal)

    mask_path = os.path.join(share_data_directory, 'roi_stem.png')
    mask_image = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

    post_processing_images = dict()
    for angle in binarize_images:
        if angle == -1:
            mask = None
        else:
            mask = mask_image

        post_processing_images[angle] = alinea.phenomenal.\
            binarization_post_processing.morphology_close(
            binarize_images[angle], mask=mask)

    alinea.phenomenal.misc.write_images(
        images_directory + 'post_processing_images/',
        images_path,
        post_processing_images)

    return post_processing_images


def multi_view_reconstruction(images_binarize, file_path):

    radius = 5
    # Load camera model parameters
    params_camera_path, _ = alinea.phenomenal.plant_1.\
        plant_1_calibration_params_path()

    cam_params = alinea.phenomenal.calibration_model.CameraModelParameters.read(
        params_camera_path)

    # Create model projection object
    projection = alinea.phenomenal.calibration_model.ModelProjection(cam_params)

    images_selected = dict()
    for angle in images_binarize:
        if 0 <= angle <= 360:
            images_selected[angle] = images_binarize[angle]

    points_3d = alinea.phenomenal.multi_view_reconstruction.reconstruction_3d(
        images_selected, projection, radius, verbose=True)

    # Write
    alinea.phenomenal.misc.write_xyz(points_3d, file_path)

    # Viewing
    alinea.phenomenal.viewer.show_points_3d(points_3d, scale_factor=2)

    return points_3d, radius


def mesh(points_3d, radius, file_path):

    matrix, index, origin = alinea.phenomenal.data_transformation.\
        points_3d_to_matrix(points_3d, radius)

    vertices, faces = alinea.phenomenal.mesh.meshing(matrix, origin, radius)

    # Normals and centers
    normals = alinea.phenomenal.mesh.compute_normal(vertices, faces)
    centers = alinea.phenomenal.mesh.center_of_vertices(vertices, faces)

    # Write
    alinea.phenomenal.misc.write_mesh(vertices, faces, file_path)

    # Viewing
    alinea.phenomenal.viewer.show_mesh(
        vertices, faces, normals=normals, centers=centers)

    return vertices, faces


def main():

    images_directory = '../../local/data_set_0962_A310_ARCH2013-05-13/'
    file_images = alinea.phenomenal.misc.load_files(images_directory)

    for pot_id in file_images:
        for date in file_images[pot_id]:
            images_path = file_images[pot_id][date]

            images = alinea.phenomenal.misc.load_images(
                images_path, cv2.IMREAD_UNCHANGED)

            # ==================================================================
            # Binarization

            images_binarize = binarization(
                images, images_directory, images_path)

            # ==================================================================
            # Binarization - Post Processing - Remove Plant Support

            post_processing_images = binarization_post_processing(
                images_binarize, images_directory, images_path)

            # ==================================================================

            file_name = images_path[0].split('\\')[-1].split('_vis_')[0]
            file_path = os.path.join(images_directory, 'points_3d', file_name)

            # ==================================================================
            # Multi-view Reconstruction

            points_3d, radius = multi_view_reconstruction(
                post_processing_images, file_path)

            # ==================================================================
            # Mesh
            # file_path = os.path.join(images_directory, 'mesh', file_name)
            # vertices, faces = mesh(points_3d, radius, file_path)

#       ========================================================================
#       LOCAL TEST

if __name__ == "__main__":
    main()
