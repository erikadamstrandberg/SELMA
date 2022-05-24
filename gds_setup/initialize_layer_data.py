#%%

import pandas as pd

def add_to_layer_data(layer_data, key, layer_number, data_parity, a_mark_position, label):
    layer_data[key] = {'layer_number': layer_number,
                       'datatype': 1,
                       'data_parity': data_parity,
                       'a_mark_position': a_mark_position,
                       'label': label}
    return layer_data


def create_layer_data(layer_definition_sheet, mask_folder):
    KAW_data_path = str(mask_folder) + '\\' + layer_definition_sheet
    df = pd.read_excel(KAW_data_path)
    
    keys             = df['keys'].tolist()
    layer_numbers    = df['layer_numbers'].to_numpy()
    data_parity      = df['data_parity'].tolist()
    a_mark_pos       = df['alignment_mark_position'].to_numpy()
    labels           = df['labels'].tolist()
    
    layer_data = {}
    
    for i in range(len(keys)):
        add_to_layer_data(layer_data,
                          keys[i],
                          int(layer_numbers[i]),
                          data_parity[i],
                          a_mark_pos[i],
                          labels[i])
    
    
    return layer_data