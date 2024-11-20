# Copyright 2023 Simon Wittl (Deggendorf Institute of Technology)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import annotations

import numpy as np
from scipy.spatial.transform import Rotation


def circular_trajectory(
    fod_mm: float, fdd_mm: float, number_of_projections: int, opening_angle: float = 0.2
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if fod_mm > fdd_mm:
        raise ValueError("fod > fdd.")

    rotation_angles = np.linspace(
        0.0, np.pi * (1.0 + opening_angle), number_of_projections, endpoint=False
    )
    rotation_object = Rotation.from_euler("Y", rotation_angles, degrees=False)

    source_initial_position = np.array([0.0, 0.0, fod_mm])
    detector_initial_position = np.array([0.0, 0.0, fod_mm - fdd_mm])

    source_positions = rotation_object.apply(source_initial_position)
    detector_positions = rotation_object.apply(detector_initial_position)

    return source_positions, detector_positions, rotation_object.as_matrix()


def look_at_orientation(
    source, detector, up_vector: np.ndarray = np.array([0.0, 0.0, 1.0])
):
    normal = source - detector
    normal = normal / np.linalg.norm(normal)

    up_axis = int(np.argmax(up_vector))

    line = np.cross(normal, up_vector)
    col = np.cross(line, normal)

    if np.sign(col[up_axis]) != np.sign(up_vector[up_axis]):
        col *= -1.0

    line = np.cross(normal, col)

    rotation_matrix = np.eye(3)
    rotation_matrix[:, 0] = line
    rotation_matrix[:, 1] = col
    rotation_matrix[:, 2] = normal

    if np.linalg.det(rotation_matrix) < 0.0:
        rotation_matrix[:, np.argmax(up_vector)] *= -1.0

    return rotation_matrix


def sphere_trajectory(
    fod_mm: float, fdd_mm: float, number_of_projections: int
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    phi = (1.0 + np.sqrt(5.0)) / 2.0
    start = -(number_of_projections - 1.0)
    end = number_of_projections - 1.0
    i = np.linspace(start, end, number_of_projections)
    theta = np.divide(2.0 * i * np.pi, phi)
    sphi = i / number_of_projections
    cphi = (
        np.sqrt((number_of_projections + i) * (number_of_projections - i))
        / number_of_projections
    )

    point_array = np.zeros((number_of_projections, 3))

    point_array[:, 0] = cphi * np.cos(theta)
    point_array[:, 1] = cphi * np.sin(theta)
    point_array[:, 2] = sphi

    source_positions = point_array * fod_mm
    detector_positions = point_array * (fod_mm - fdd_mm)
    orientation = np.array(
        list(map(look_at_orientation, source_positions, detector_positions))
    )

    return source_positions, detector_positions, orientation


def arbitary_circular_trajectory(
    fod_mm: float,
    fdd_mm: float,
    number_of_projections: int,
    transformation: np.ndarray = np.eye(4),
    opening_angle: float = 0.2,
):
    source_positions, detector_positions, orientation = circular_trajectory(
        fod_mm, fdd_mm, number_of_projections, opening_angle
    )

    source_transformation_matrix = np.zeros((number_of_projections, 4, 4))
    source_transformation_matrix[:, 3, 3] = 1.0
    detector_transformation_matrix = source_transformation_matrix.copy()

    source_transformation_matrix[:, :3, 3] = source_positions
    detector_transformation_matrix[:, :3, 3] = detector_positions

    source_transformation_matrix[:, :3, :3] = orientation
    detector_transformation_matrix[:, :3, :3] = orientation

    transformation = np.expand_dims(transformation, 0)
    source_transformation_matrix = transformation @ source_transformation_matrix
    detector_transformation_matrix = transformation @ detector_transformation_matrix

    return (
        source_transformation_matrix[:, :3, 3].reshape((number_of_projections, 3)),
        detector_transformation_matrix[:, :3, 3].reshape((number_of_projections, 3)),
        detector_transformation_matrix[:, :3, :3].reshape(
            (number_of_projections, 3, 3)
        ),
    )
