#  Copyright (c) 2020. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

class Merger(object):
    def __init__(self, ssi_integration, ssi_bsk1) -> None:
        self.ssi_integration_item = ssi_integration
        self.ssi_bsk = ssi_bsk1
        # self.delta = self.ssi_integration_item["dF"] if type(self.ssi_integration_item["dF"]) == int else 0
        self.config_id = self.ssi_integration_item["id"]
        self.lvl = self.ssi_integration_item["level"]
        self.bsk1_id = self.ssi_integration_item["id_bsk1"]
        self.power_in = self.ssi_integration_item["Pin"]
        self.bw = self.ssi_integration_item["BW"]
        self.bsk2_id = self.ssi_integration_item["id_bsk2"]
        self.bsk3_id = self.ssi_integration_item["id_bsk3"]

    def merge(self) -> dict:
        bsk1_in = None
        bsk1_out = None
        bsk_full_level = None
        bsk_full = None
        finded_out = False
        finded_in = False
        finded_full_level = False
        finded_full = False

        finded_string = str(self.bsk1_id) + "_in_" + self.lvl
        for ssi in self.ssi_bsk:
            if ssi["id"] == finded_string:
                bsk1_in = ssi
                finded_in = True
                break

        finded_string = str(self.bsk1_id) + "_in"
        for ssi in self.ssi_bsk:
            if ssi["id"] == finded_string:
                bsk1_in = ssi
                finded_in = True
                break

        finded_string = str(self.bsk1_id) + "_out"
        for ssi in self.ssi_bsk:
            if ssi["id"] == finded_string:
                bsk1_out = ssi
                finded_out = True
                break

        finded_string = str(self.bsk1_id) + '_' + self.lvl
        for ssi in self.ssi_bsk:
            if ssi['id'] == finded_string:
                bsk_full = ssi
                finded_full_level = True
                break

        for ssi in self.ssi_bsk:
            if ssi['id'] == int(self.bsk1_id):
                bsk_full = ssi
                finded_full_level = True
                break
        if finded_in and finded_out:
            merged_ssi = self.merge_ssi_in_and_out(bsk1_in, bsk1_out)
        elif finded_full_level or finded_full:
            merged_ssi = self.merge_ssi_full(bsk_full)
        else:
            raise Exception("Can't find needed SSI_CONFIG for:" + str(self.ssi_integration_item["id"]))
        return merged_ssi

    def merge_ssi_in_and_out(self, bsk1_in, bsk1_out):
        print(self.config_id)
        z = {'id': self.config_id,
             'power_in': self.power_in,
             'power_level': self.lvl,
             'bw': self.bw,
             'frequency_start': bsk1_in['frequency_start'],
             'frequency_out': bsk1_out['frequency_out'],
             'KPA_FIN': self.ssi_integration_item['Fc_in'],
             'KPA_FOUT': self.ssi_integration_item['Fc_out'],
             'bsk2': self.bsk2_id,
             'bsk3': self.bsk3_id,
             'query_route': bsk1_in['query_route'] + bsk1_out['query_route'],
             'route': bsk1_in['route'] + bsk1_out['route'],
             'route_long_name': bsk1_in['route_long_name'] + ' ' + bsk1_out['route_long_name'] + ' BSK2_' + str(
                 self.bsk2_id) + ' BSK3_' + str(self.bsk3_id),
             'route_short_name': bsk1_in['route_short_name'] + '_' + bsk1_out['route_short_name'] + ' BSK2_' + str(
                 self.bsk2_id) + ' BSK3_' + str(self.bsk3_id),
             'config_name': bsk1_in['config_name'],
             'cnv_cif': bsk1_in['cnv_cif'],
             'cnv_ska': bsk1_in['cnv_ska'],
             'cnv_kka': bsk1_in['cnv_kka'],
             'mlo': bsk1_in['mlo'],
             'dtp': bsk1_in['dtp'],
             'twta_tas': bsk1_out['twta_tas'],
             'twta_mda': bsk1_out['twta_mda'],
             'cnv_ifs': bsk1_in['cnv_ifs'],
             'cnv_kuc': bsk1_in['cnv_kuc'],
             'cnv_lc': bsk1_in['cnv_lc'],
             'query_route_ports': bsk1_in['query_route_ports'] + bsk1_out['query_route_ports'],
             'global_lo': bsk1_in['global_lo']
             }
        return z

    def merge_ssi_full(self, bsk_full):
        z = bsk_full
        z["id"] = self.config_id
        z["power_level"] = self.lvl[0]
        z["power_in"] = self.power_in
        # 'frequency_out': self.ssi_integration_item['Fc_out'] - self.bw / 2,
        # 'frequency_start': self.ssi_integration_item['Fc_in'] - self.bw / 2,
        z['frequency_start'] = bsk_full['frequency_start']
        z['frequency_out'] = bsk_full['frequency_out']
        z['KPA_FIN'] = self.ssi_integration_item['Fc_in']
        z['KPA_FOUT'] = self.ssi_integration_item['Fc_out']
        z['bw'] = self.bw
        z['bsk2'] = self.bsk2_id
        z['bsk3'] = self.bsk3_id
        z["route_short_name"] = z["route_short_name"] + ' BSK2_' + str(self.bsk2_id) + ' BSK3_' + str(self.bsk3_id)
        z['route_long_name'] = z['route_long_name'] + ' BSK2_' + str(self.bsk2_id) + ' BSK3_' + str(self.bsk3_id)
        return z
