#  Copyright (c) 2020. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.
import json

with open("/Users/alivecrim/PycharmProjects/cgcorrector2/servicedata/data/INTEGRATION/ete_complex_mes_.json",
          "r") as read_file:
    data = json.load(read_file)

for s in data:
    print(str(s["id"]) + ";" + str(s["level"]) + ";" + str(s["id_bsk1"]))
