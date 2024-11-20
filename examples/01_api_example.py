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

import matplotlib.pyplot as plt
from pathlib import Path

from artist_pythonlib import API
from artist_pythonlib.hardware import XraySource, XrayDetector


def main():
    # Initialize the api.
    artist_api = API()

    # Move and rotate source to initial position / orientation.
    artist_api.rotate('S', alpha=0., beta=77, gamma=-12.)
    artist_api.translate('S', x=10, y=-129, z=199.4)

    # Get the current position of the source:
    source_position = artist_api.get_position('S')
    source_orientation = artist_api.get_orientation('S')
    
    print(f'Source Position: {source_position}')
    print(f'Source Orientation: {source_orientation}')

    # Create a source object and set the voltage
    source = XraySource()
    source.voltage_kv = 142.
    source.exposure_ma = 10.

    print(f'Source Voltage: {source.voltage_kv} kV')
    print(f'Source Exposure: {source.exposure_ma} mA')
    print(f'Source Type: {source.source_type}')

    # Create a detector object and set the resolution
    detector = XrayDetector()
    detector.detector_resolution_mm = [0.1, 0.15]
    detector.detector_count_px = [1000, 1000]

    print(f'Detector Resolution: {detector.detector_resolution_mm} mm')
    print(f'Detector Pixel Count: {detector.detector_count_px} px')

    # Load .stl part
    new_id = artist_api.load_part(
        Path(r'C:\Program Files\BAM\aRTist 2.12\Data\Library\ExampleParts\Fun\Dog.stl'),  # Plesas check where the aRTist software is installed.
        'Fe',
        'test_object')
    
    # Make a projection an visualize it in python
    image = artist_api.get_image()

    # change material
    artist_api.set_material(new_id, 'Al')

    plt.imshow(image)
    plt.show()

    # Set visibility off
    artist_api.set_visibility(new_id, False)

    # Delete part
    artist_api.delete_part(new_id)

if __name__ == '__main__':
    main()
