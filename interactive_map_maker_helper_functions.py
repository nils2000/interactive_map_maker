import json


def load_areas_of_interest_from_file(filename, reduction_factor):
    ret = dict()
    with open(filename) as file:
        temp = file.read()
        # remove "var rooms = " at beginning of file
        temp = temp[12:]
        print(temp)
        dict_with_keys_as_values = json.loads(temp)
        r = reduction_factor
        for key in dict_with_keys_as_values.keys():
            # print(key)
            x1, y1, x2, y2 = dict_with_keys_as_values[key]
            ret[((x1/r, y1/r), (x2/r, y2/r))] = key
    print(ret)
    return ret
