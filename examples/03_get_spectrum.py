from artist_pythonlib import API
import numpy as np
from matplotlib import pyplot as plt
from xraydb import mu_elam


def scrap_spectrum(artist_spectrum: str):
    try:
        spectrum_dict = artist_spectrum.split('# [degrees]} ')[1].split('{# Avg:')[0]
        spectrum_dict = spectrum_dict.replace('{', '')
        spectrum_dict = spectrum_dict.replace('}', '')
        spectrum_dict = spectrum_dict.replace('\t', ' ')
        spectrum_dict = spectrum_dict.split(' ')[:-1]
        spectrum = np.array(spectrum_dict, np.float32)
        return spectrum.reshape((-1, 2))
    except IndexError:
        raise ValueError('Ploychromatic Source must be set in aRTist!')


def get_current_artist_spcectrum(api: API) -> np.ndarray:
    return scrap_spectrum(api.rc.send('[Engine::GetSpectrum]'))


def main():
    api = API()
    current_spectrum = get_current_artist_spcectrum(api)
    energy_keV = current_spectrum[:, 0]
    photons_n = current_spectrum[:, 1]

    plt.plot(energy_keV, photons_n)
    plt.title('aRTist Source Spectrum')
    plt.ylabel('Photons (n)')
    plt.xlabel('Energy (keV)')
    plt.show()

    energy = np.arange(500, 120000, 10)  # energy in eV
      
    for elem in ('C', 'Cu', 'Au'):
        mu = mu_elam(elem, energy)
        plt.plot(energy / 1000., mu, label=elem)
    
    plt.title('X-ray Mass Attenuation')
    plt.xlabel('Energy (keV)')
    plt.ylabel(r'$\mu/\rho \rm\, (cm^2/gr)$')
    plt.legend()
    plt.yscale('log')
    plt.xscale('log')
    plt.show()

if __name__ == '__main__':
    main()