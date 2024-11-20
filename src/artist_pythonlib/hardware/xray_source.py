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

from ..common_types import SOURCETYPES


class XraySource(BaseHardware):
    def __init__(self, remote_control: Junction | API = None) -> None:
        """Xray source objet. Needs a remote control connection.

        Args:
            remote_control (Junction | API, optional): remote connection to communicate with aRTist. Defaults to None.
        """
        super().__init__(remote_control)

    @property
    def voltage_kv(self) -> float:
        """Current voltage setting of the XRay source.

        Returns:
            float: Voltage value in [kV].
        """
        return_value = self.rc.send("array get Xsource Voltage")
        return_value = return_value.split(" ")[1]
        return float(return_value)

    @voltage_kv.setter
    def voltage_kv(self, voltage_kv: float) -> None:
        self.rc.send(f"set ::Xsource(Voltage) {voltage_kv}")
        self.rc.send("::XSource::ComputeSpectrum")

    @property
    def exposure_ma(self) -> float:
        """Current set exposure of the XRay source

        Returns:
            float: Exposure in [µA].
        """
        return_value = self.rc.send("array get Xsource Exposure")
        return_value = return_value.split(" ")[1]
        return float(return_value)

    @exposure_ma.setter
    def exposure_ma(self, exposure_ma: float) -> None:
        self.rc.send(f"set ::Xsource(Exposure) {exposure_ma}")

    @property
    def filter_material(self) -> str:
        """Filter Material of the XRay source.

        Returns:
            str: Filter material of the XRay source.
        """
        return_value = self.rc.send("array get Xsource FilterMaterial")
        return_value = return_value.split(" ")[1]
        return str(return_value)

    @filter_material.setter
    def filter_material(self, filter_material: float) -> None:
        self.rc.send(f"set ::Xsource(FilterMaterial) {filter_material}")
        self.rc.send("::XSource::ComputeSpectrum")

    @property
    def filter_thickness_mm(self) -> float:
        """Thickness of the filter in [mm].

        Returns:
            float: Filter thickness in [mm].
        """
        return_value = self.rc.send("array get Xsource FilterThickness")
        return_value = return_value.split(" ")[1]
        return float(return_value)

    @filter_thickness_mm.setter
    def filter_thickness_mm(self, filter_thickness_mm: float) -> None:
        self.rc.send(f"set ::Xsource(FilterThickness) {filter_thickness_mm}")
        self.rc.send("::XSource::ComputeSpectrum")

    @property
    def source_type(self) -> int:
        """Source type of the XRay source. Types are Monocromatic or General. See SOURCETYPES.

        Returns:
            int: Source type as integer. Use SOURCETYPES.
        """
        return_value = self.rc.send("array get Xsource Tube")
        return_value = return_value.split(" ")[1]

        if str(return_value).startswith("Mono"):
            return SOURCETYPES.MONOCHROMATIC
        elif str(return_value).startswith("General"):
            return SOURCETYPES.GENERAL

    @source_type.setter
    def source_type(self, source_type: SOURCETYPES) -> None:
        if source_type == SOURCETYPES.MONOCHROMATIC:
            self.rc.send("set ::Xsource(Tube) Mono")
        elif source_type == SOURCETYPES.GENERAL:
            self.rc.send("set ::Xsource(Tube) General")
        self.rc.send("::XSource::ComputeSpectrum")
