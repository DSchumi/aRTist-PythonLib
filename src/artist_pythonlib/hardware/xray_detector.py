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

from artist_pythonlib.api import API
from artist_pythonlib.remote_connection import Junction
from .base_hardware import BaseHardware

import numpy as np


class XrayDetector(BaseHardware):
    def __init__(self, remote_control: Junction | API = None) -> None:
        """XRay detector object. Needs a remote control connection.

        Args:
            remote_control (Junction | API, optional): Remote control connection for the communication with artist. Defaults to None.
        """
        super().__init__(remote_control)

    @property
    def detector_resolution_mm(self) -> np.ndarray:
        """Current detector resolution / pixel pitch in [mm].

        Returns:
            np.ndarray: Detector resolution (u, v) in [mm].
        """
        return_value = self.rc.send("::XDetector::GetResolution")
        return_value = np.array(np.float32(return_value.split(" ")))
        return return_value

    @detector_resolution_mm.setter
    def detector_resolution_mm(self, detector_resolution_mm: np.ndarray) -> None:
        self.rc.send(f"set ::Xsetup_private(DGdx) {detector_resolution_mm[0]}")
        self.rc.send(f"set ::Xsetup_private(DGdy) {detector_resolution_mm[1]}")

    @property
    def detector_count_px(self) -> np.ndarray:
        """Current detector pixel count.

        Returns:
            np.ndarray: Detector pixel count (u, v) in [n].
        """
        return_value = self.rc.send("::XDetector::GetPixelSize")
        return_value = np.array(np.int32(return_value.split(" ")))
        return return_value

    @detector_count_px.setter
    def detector_count_px(self, detector_count_px: np.ndarray) -> None:
        self.rc.send(f"set ::Xsetup(DetectorPixelX) {detector_count_px[0]}")
        self.rc.send(f"set ::Xsetup(DetectorPixelY) {detector_count_px[1]}")

    @property
    def flatfield_correction(self) -> bool:
        """Faltfiled corrected?

        Returns:
            bool: Return wheter the projection is flatfield corrected or not.
        """
        return_value = self.rc.send("array get Xdetector FFCorrRun")
        return_value = return_value.split(" ")[1]
        return bool(return_value)
