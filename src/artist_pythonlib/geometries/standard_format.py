from __future__ import annotations

import numpy as np
from scipy.spatial.transform import Rotation


def projection_geometry(api) -> dict:
    """Returns the current projection geometry of the scene. All positions are in [mm].

    Returns:
        dict: Dictionary of the projection geometry. Keys are: 'focal_spot_position_mm',
        'focal_spot_orientation_matrix', 'detector_center_position_mm',
        'detector_center_orientation_matrix', 'detector_center_orientation_quat',
        'detector_count_px' and 'detector_resolution_mm'
    """
    source_position = np.array(api.get_position("S"))
    source_orientation = np.array(api.get_rotation_matrix("S"))
    detector_position = np.array(api.get_position("D"))
    detector_orientation = np.array(api.get_rotation_matrix("D"))

    detector_resolution = api.get_detector_resolution()
    detector_pixel_count = api.get_detector_pixel_count()

    data_dict = dict()
    data_dict["focal_spot_position_mm"] = source_position.tolist()
    data_dict["focal_spot_orientation_quat"] = (
        Rotation.from_matrix(source_orientation).as_quat().tolist()
    )
    data_dict["detector_center_position_mm"] = detector_position.tolist()
    data_dict["detector_center_orientation_quat"] = (
        Rotation.from_matrix(detector_orientation).as_quat().tolist()
    )

    data_dict["image_width_px"] = detector_pixel_count.tolist()[0]
    data_dict["pixel_pitch_width_mm"] = detector_resolution.tolist()[0]
    data_dict["image_height_px"] = detector_pixel_count.tolist()[1]
    data_dict["pixel_pitch_height_mm"] = detector_resolution.tolist()[1]

    return data_dict
