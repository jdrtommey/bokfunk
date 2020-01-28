"""
INSERT FUNCTION TO PLOT HERE WITH NAME def my_function(dictionary):
"""

import keygen

link_dict = {
    'time':360,
    'loss':-30,
    'bg_power':-110,
    'wavelength':1550,
    'wavelength_range':0.1
}
hardware_dict = {
    'clock_rate':1.8e9,
    'reciever_losses':9,
    'ec_efficency':1.00,
    'dark_counts':500,
    'detector_error': 0.01,
    'detector_time': 400*1e-12,
    'background_qber': 0.5
}
protocol_dict = {
    'name': 'decoy_asym_inf',
    'internals' : {'signal_strength' : 0.475}
}


config = {'link_dict':link_dict,'hardware_dict':hardware_dict,'protocol_dict':protocol_dict}

variable_dictionary = config

def my_function(dictionary):
    ## do something

    res = keygen.get_dat_der_key(dictionary['link_dict'],dictionary['hardware_dict'],dictionary['protocol_dict'])
    result ={'result':res}
    return result
