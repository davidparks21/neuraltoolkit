#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Script to read intan binary file

Hengen Lab
Washington University in St. Louis
Author: Kiran Bhaskaran-Nair
Email: kbn.git@gmail.com
Version:  0.1

List of functions/class in ntk_channelmap
load_intan_raw_gain_chanmap(
    rawfile, number_of_channels, hstype, nprobes=1):
'''


import numpy as np


def load_intan_raw_gain_chanmap(
        rawfile, number_of_channels, hstype, nprobes=1):

    '''
    load intan data and multiply gain and apply channel mapping
    load_intan_raw_gain_chanmap(name, number_of_channels, hstype)
    hstype : 'hs64', 'intan32', 'Si_64_KS_chmap', 'Si_64_KT_T1_K2_chmap'
              and 'linear'
    nprobes : Number of probes (default 1)
    returns first timestamp and data
    '''

    from neuraltoolkit import ntk_channelmap as ntkc
    from .load_intan_rhd_format_hlab import read_data

    # Read intan file
    a = read_data(rawfile)

    # Time and data
    tr = np.array(a['t_amplifier'][0])
    dg = np.array(a['amplifier_data'])

    # Apply channel mapping
    dgc = ntkc.channel_map_data(dg, number_of_channels, hstype, nprobes)

    return tr, dgc
