#  Copyright (c) 2020. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.
import json

from utils.merger import Merger

init_path = './configs/'
config_to_merge = [
    '500+.json',
    ['5000.json', 'config_routes.json']
]

big_data = []
data_item = []
for conf in config_to_merge:
    if type(conf) is str:
        with open(init_path + conf, "r") as read_file:
            integration_data = json.load(read_file)
            data_item += integration_data
    else:
        with open(init_path + conf[0], "r") as read_file:
            integration_data = json.load(read_file)
        for i in integration_data:
            if (i['id_bsk1'] < 800):
                with open(init_path + '500+.json', "r") as read_file:
                    bsk1_data = json.load(read_file)
            else:
                with open(init_path + conf[1], "r") as read_file:
                    bsk1_data = json.load(read_file)
            merger = Merger(i, bsk1_data)
            data_item.append(merger.merge())
with open('5000_configs.json', 'w') as outfile:
    json.dump(data_item, outfile)
