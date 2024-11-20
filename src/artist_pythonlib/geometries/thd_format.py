import numpy as np
from scipy.spatial.transform import Rotation

try:
    from thd_json.header import generate_header
except ModuleNotFoundError:
    from warnings import warn

    warn(
        "The optional modules of `thd` is not installed. THD Json geometry is not available."
    )


def thd_projection_geometry(api) -> dict:
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
    header_dict = dict()
    projection_geometry = dict()
    image = dict()
    detector = dict()

    json_header = generate_header()
    header_dict["uuid"] = json_header.uuid
    header_dict["timestamp"] = json_header.timestamp

    projection_geometry["focal_spot_position_mm"] = source_position.tolist()
    projection_geometry["focal_spot_orientation_quat"] = (
        Rotation.from_matrix(source_orientation).as_quat().tolist()
    )
    projection_geometry["detector_center_position_mm"] = detector_position.tolist()
    projection_geometry["detector_center_orientation_quat"] = (
        Rotation.from_matrix(detector_orientation).as_quat().tolist()
    )

    image["uuid"] = json_header.uuid
    image["timestamp"] = json_header.timestamp
    image["image_path"] = f"{json_header.uuid}.tif"

    detector["image_width_px"] = detector_pixel_count.tolist()[0]
    detector["pixel_pitch_width_mm"] = detector_resolution.tolist()[0]
    detector["image_height_px"] = detector_pixel_count.tolist()[1]
    detector["pixel_pitch_height_mm"] = detector_resolution.tolist()[1]

    data_dict["projection_geometry"] = projection_geometry
    data_dict["image"] = image
    data_dict["detector"] = detector
    data_dict["header"] = header_dict

    return data_dict
