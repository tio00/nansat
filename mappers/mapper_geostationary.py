# Name:         mapper_geostationary.py
# Purpose:      Generic mapper for all geostationary satellites in Eumetcast format
# Author:       Knut-Frode Dagestad
# Licence:      This file is part of NANSAT. You can redistribute it or modify
#               under the terms of GNU General Public License, v.3
#               http://www.gnu.org/licenses/gpl-3.0.html
#
# NB: This mapper works only together with a modified version of the GDAL MSG driver

from numpy import array, arange
from datetime import datetime
from vrt import *
from nansat_tools import Node

def arrays2LUTString(a, b):
    LUTString = ''
    for i, value in enumerate(a):
        if value >= 0 and value <= 256:
            LUTString = LUTString + str(value) + ':' + str(b[i]) + ','
    return LUTString[:-1]

mtsat_calibration_10_7_mum = '0:330.000, 1:329.686, 2:329.372, 3:329.057, 4:328.741, 5:328.425, 6:328.108, 7:327.790, 8:327.472, 9:327.153, 10:326.833, 11:326.513, 12:326.192, 13:325.870, 14:325.547, 15:325.224, 16:324.900, 17:324.575, 18:324.250, 19:323.924, 20:323.597, 21:323.269, 22:322.941, 23:322.612, 24:322.282, 25:321.951, 26:321.619, 27:321.287, 28:320.954, 29:320.620, 30:320.286, 31:319.950, 32:319.614, 33:319.277, 34:318.939, 35:318.600, 36:318.261, 37:317.920, 38:317.579, 39:317.237, 40:316.894, 41:316.550, 42:316.206, 43:315.860, 44:315.514, 45:315.166, 46:314.818, 47:314.469, 48:314.119, 49:313.768, 50:313.416, 51:313.063, 52:312.709, 53:312.354, 54:311.998, 55:311.642, 56:311.284, 57:310.925, 58:310.565, 59:310.205, 60:309.843, 61:309.480, 62:309.116, 63:308.751, 64:308.386, 65:308.019, 66:307.651, 67:307.281, 68:306.911, 69:306.540, 70:306.168, 71:305.794, 72:305.419, 73:305.044, 74:304.667, 75:304.288, 76:303.909, 77:303.529, 78:303.147, 79:302.764, 80:302.380, 81:301.995, 82:301.608, 83:301.220, 84:300.831, 85:300.441, 86:300.049, 87:299.656, 88:299.262, 89:298.866, 90:298.469, 91:298.071, 92:297.671, 93:297.270, 94:296.867, 95:296.463, 96:296.058, 97:295.651, 98:295.243, 99:294.833, 100:294.422, 101:294.009, 102:293.595, 103:293.179, 104:292.762, 105:292.342, 106:291.922, 107:291.500, 108:291.076, 109:290.650, 110:290.223, 111:289.794, 112:289.364, 113:288.931, 114:288.497, 115:288.061, 116:287.624, 117:287.184, 118:286.743, 119:286.299, 120:285.854, 121:285.407, 122:284.958, 123:284.507, 124:284.055, 125:283.600, 126:283.143, 127:282.684, 128:282.222, 129:281.759, 130:281.294, 131:280.826, 132:280.356, 133:279.884, 134:279.410, 135:278.933, 136:278.454, 137:277.973, 138:277.489, 139:277.003, 140:276.514, 141:276.023, 142:275.529, 143:275.033, 144:274.534, 145:274.033, 146:273.528, 147:273.021, 148:272.511, 149:271.998, 150:271.483, 151:270.964, 152:270.443, 153:269.918, 154:269.390, 155:268.860, 156:268.326, 157:267.788, 158:267.248, 159:266.704, 160:266.157, 161:265.606, 162:265.051, 163:264.494, 164:263.932, 165:263.367, 166:262.797, 167:262.224, 168:261.647, 169:261.066, 170:260.481, 171:259.891, 172:259.298, 173:258.700, 174:258.097, 175:257.490, 176:256.878, 177:256.262, 178:255.640, 179:255.014, 180:254.382, 181:253.746, 182:253.104, 183:252.456, 184:251.803, 185:251.144, 186:250.480, 187:249.809, 188:249.132, 189:248.449, 190:247.760, 191:247.064, 192:246.361, 193:245.651, 194:244.934, 195:244.209, 196:243.477, 197:242.737, 198:241.989, 199:241.232, 200:240.468, 201:239.694, 202:238.911, 203:238.119, 204:237.317, 205:236.505, 206:235.683, 207:234.850, 208:234.006, 209:233.150, 210:232.283, 211:231.403, 212:230.510, 213:229.604, 214:228.684, 215:227.749, 216:226.799, 217:225.834, 218:224.852, 219:223.852, 220:222.835, 221:221.799, 222:220.743, 223:219.665, 224:218.566, 225:217.444, 226:216.297, 227:215.124, 228:213.923, 229:212.693, 230:211.432, 231:210.138, 232:208.808, 233:207.439, 234:206.029, 235:204.575, 236:203.072, 237:201.517, 238:199.904, 239:198.228, 240:196.482, 241:194.658, 242:192.748, 243:190.740, 244:188.620, 245:186.372, 246:183.975, 247:181.403, 248:178.619, 249:175.576, 250:172.207, 251:168.411, 252:164.030, 253:158.788, 254:152.130, 255:142.597'
mtsat_calibration_3_8_mum = '0:320.000, 1:319.894, 2:319.787, 3:319.680, 4:319.573, 5:319.465, 6:319.357, 7:319.248, 8:319.140, 9:319.031, 10:318.921, 11:318.811, 12:318.701, 13:318.590, 14:318.479, 15:318.368, 16:318.256, 17:318.144, 18:318.031, 19:317.918, 20:317.805, 21:317.691, 22:317.577, 23:317.462, 24:317.347, 25:317.232, 26:317.116, 27:317.000, 28:316.883, 29:316.766, 30:316.649, 31:316.531, 32:316.412, 33:316.293, 34:316.174, 35:316.054, 36:315.934, 37:315.813, 38:315.692, 39:315.571, 40:315.449, 41:315.326, 42:315.203, 43:315.080, 44:314.956, 45:314.831, 46:314.706, 47:314.581, 48:314.455, 49:314.329, 50:314.202, 51:314.074, 52:313.946, 53:313.818, 54:313.689, 55:313.559, 56:313.429, 57:313.298, 58:313.167, 59:313.035, 60:312.903, 61:312.770, 62:312.636, 63:312.502, 64:312.368, 65:312.233, 66:312.097, 67:311.960, 68:311.823, 69:311.686, 70:311.547, 71:311.409, 72:311.269, 73:311.129, 74:310.988, 75:310.847, 76:310.705, 77:310.562, 78:310.418, 79:310.274, 80:310.130, 81:309.984, 82:309.838, 83:309.691, 84:309.543, 85:309.395, 86:309.246, 87:309.096, 88:308.946, 89:308.794, 90:308.642, 91:308.490, 92:308.336, 93:308.182, 94:308.027, 95:307.871, 96:307.714, 97:307.556, 98:307.398, 99:307.238, 100:307.078, 101:306.917, 102:306.755, 103:306.593, 104:306.429, 105:306.264, 106:306.099, 107:305.932, 108:305.765, 109:305.597, 110:305.427, 111:305.257, 112:305.086, 113:304.914, 114:304.740, 115:304.566, 116:304.391, 117:304.214, 118:304.037, 119:303.858, 120:303.679, 121:303.498, 122:303.316, 123:303.133, 124:302.949, 125:302.763, 126:302.577, 127:302.389, 128:302.200, 129:302.010, 130:301.818, 131:301.625, 132:301.431, 133:301.236, 134:301.039, 135:300.841, 136:300.641, 137:300.440, 138:300.238, 139:300.034, 140:299.829, 141:299.622, 142:299.413, 143:299.204, 144:298.992, 145:298.779, 146:298.564, 147:298.348, 148:298.130, 149:297.910, 150:297.689, 151:297.465, 152:297.240, 153:297.013, 154:296.785, 155:296.554, 156:296.321, 157:296.087, 158:295.850, 159:295.612, 160:295.371, 161:295.128, 162:294.883, 163:294.636, 164:294.386, 165:294.134, 166:293.880, 167:293.623, 168:293.364, 169:293.103, 170:292.839, 171:292.572, 172:292.302, 173:292.030, 174:291.755, 175:291.477, 176:291.197, 177:290.913, 178:290.626, 179:290.336, 180:290.043, 181:289.746, 182:289.447, 183:289.143, 184:288.836, 185:288.526, 186:288.212, 187:287.894, 188:287.571, 189:287.245, 190:286.915, 191:286.580, 192:286.241, 193:285.898, 194:285.550, 195:285.197, 196:284.839, 197:284.475, 198:284.107, 199:283.733, 200:283.353, 201:282.968, 202:282.577, 203:282.179, 204:281.775, 205:281.364, 206:280.946, 207:280.521, 208:280.088, 209:279.648, 210:279.200, 211:278.743, 212:278.277, 213:277.802, 214:277.318, 215:276.824, 216:276.319, 217:275.804, 218:275.276, 219:274.737, 220:274.185, 221:273.619, 222:273.039, 223:272.445, 224:271.835, 225:271.208, 226:270.563, 227:269.899, 228:269.216, 229:268.510, 230:267.782, 231:267.029, 232:266.250, 233:265.442, 234:264.602, 235:263.729, 236:262.819, 237:261.868, 238:260.872, 239:259.827, 240:258.726, 241:257.564, 242:256.331, 243:255.018, 244:253.612, 245:252.099, 246:250.458, 247:248.665, 248:246.683, 249:244.465, 250:241.940, 251:238.998, 252:235.455, 253:230.960, 254:224.707, 255:213.838'
mtsat_calibration_6_8_mum = '0:300.000, 1:299.835, 2:299.669, 3:299.503, 4:299.336, 5:299.168, 6:299.001, 7:298.833, 8:298.664, 9:298.495, 10:298.325, 11:298.155, 12:297.984, 13:297.813, 14:297.641, 15:297.469, 16:297.296, 17:297.123, 18:296.949, 19:296.775, 20:296.600, 21:296.425, 22:296.249, 23:296.072, 24:295.895, 25:295.718, 26:295.540, 27:295.361, 28:295.182, 29:295.002, 30:294.821, 31:294.640, 32:294.459, 33:294.277, 34:294.094, 35:293.911, 36:293.727, 37:293.542, 38:293.357, 39:293.171, 40:292.985, 41:292.798, 42:292.610, 43:292.422, 44:292.233, 45:292.043, 46:291.853, 47:291.662, 48:291.470, 49:291.278, 50:291.085, 51:290.892, 52:290.697, 53:290.502, 54:290.307, 55:290.110, 56:289.913, 57:289.715, 58:289.517, 59:289.317, 60:289.117, 61:288.916, 62:288.715, 63:288.513, 64:288.309, 65:288.106, 66:287.901, 67:287.696, 68:287.489, 69:287.282, 70:287.074, 71:286.866, 72:286.656, 73:286.446, 74:286.235, 75:286.023, 76:285.810, 77:285.596, 78:285.381, 79:285.166, 80:284.950, 81:284.732, 82:284.514, 83:284.295, 84:284.075, 85:283.854, 86:283.632, 87:283.409, 88:283.185, 89:282.960, 90:282.734, 91:282.507, 92:282.279, 93:282.050, 94:281.820, 95:281.589, 96:281.357, 97:281.124, 98:280.890, 99:280.655, 100:280.418, 101:280.180, 102:279.942, 103:279.702, 104:279.461, 105:279.219, 106:278.975, 107:278.731, 108:278.485, 109:278.238, 110:277.990, 111:277.740, 112:277.489, 113:277.237, 114:276.984, 115:276.729, 116:276.473, 117:276.215, 118:275.956, 119:275.696, 120:275.435, 121:275.171, 122:274.907, 123:274.641, 124:274.373, 125:274.104, 126:273.834, 127:273.562, 128:273.288, 129:273.013, 130:272.736, 131:272.457, 132:272.177, 133:271.895, 134:271.611, 135:271.326, 136:271.039, 137:270.750, 138:270.459, 139:270.167, 140:269.872, 141:269.576, 142:269.277, 143:268.977, 144:268.675, 145:268.371, 146:268.064, 147:267.756, 148:267.445, 149:267.132, 150:266.817, 151:266.500, 152:266.180, 153:265.859, 154:265.534, 155:265.208, 156:264.879, 157:264.547, 158:264.213, 159:263.877, 160:263.537, 161:263.195, 162:262.851, 163:262.503, 164:262.153, 165:261.800, 166:261.444, 167:261.084, 168:260.722, 169:260.357, 170:259.988, 171:259.616, 172:259.241, 173:258.863, 174:258.481, 175:258.095, 176:257.706, 177:257.313, 178:256.916, 179:256.516, 180:256.111, 181:255.702, 182:255.289, 183:254.872, 184:254.451, 185:254.025, 186:253.594, 187:253.159, 188:252.718, 189:252.273, 190:251.823, 191:251.367, 192:250.906, 193:250.440, 194:249.967, 195:249.489, 196:249.005, 197:248.514, 198:248.017, 199:247.514, 200:247.003, 201:246.486, 202:245.961, 203:245.428, 204:244.888, 205:244.340, 206:243.783, 207:243.218, 208:242.643, 209:242.059, 210:241.466, 211:240.862, 212:240.248, 213:239.623, 214:238.986, 215:238.338, 216:237.677, 217:237.002, 218:236.315, 219:235.613, 220:234.896, 221:234.163, 222:233.413, 223:232.646, 224:231.861, 225:231.055, 226:230.229, 227:229.381, 228:228.510, 229:227.614, 230:226.690, 231:225.739, 232:224.756, 233:223.740, 234:222.689, 235:221.598, 236:220.465, 237:219.286, 238:218.055, 239:216.768, 240:215.419, 241:213.999, 242:212.501, 243:210.913, 244:209.221, 245:207.410, 246:205.458, 247:203.338, 248:201.012, 249:198.429, 250:195.515, 251:192.154, 252:188.157, 253:183.166, 254:176.370, 255:165.014'

# See http://www.eumetsat.int/Home/Main/DataProducts/Calibration/MFGCalibration/
meteosat7_IR_radiances = array([0.667, 0.697, 0.727, 0.758, 0.789, 0.822, 0.856, 0.891, 0.927, 0.964, 1.002, 1.04, 1.08, 1.122, 1.164, 1.207, 1.251, 1.297, 1.344, 1.392, 1.441, 1.491, 1.542, 1.595, 1.649, 1.704, 1.761, 1.818, 1.877, 1.938, 1.999, 2.062, 2.127, 2.192, 2.259, 2.328, 2.397, 2.468, 2.541, 2.615, 2.69, 2.767, 2.846, 2.925, 3.007, 3.089, 3.174, 3.259, 3.347, 3.435, 3.526, 3.617, 3.711, 3.806, 3.902, 4, 4.1, 4.201, 4.304, 4.408, 4.514, 4.622, 4.731, 4.842, 4.955, 5.069, 5.185, 5.302, 5.422, 5.542, 5.665, 5.789, 5.915, 6.043, 6.172, 6.303, 6.436, 6.57, 6.706, 6.844, 6.983, 7.125, 7.268, 7.412, 7.559, 7.707, 7.857, 8.009, 8.162, 8.317, 8.474, 8.633, 8.793, 8.955, 9.119, 9.285, 9.453, 9.622, 9.793, 9.966, 10.141, 10.317, 10.495, 10.675, 10.857, 11.04, 11.225, 11.412, 11.601, 11.792, 11.984, 12.178, 12.374, 12.572, 12.772, 12.973, 13.176, 13.381, 13.587, 13.796, 14.006, 14.218, 14.432, 14.647, 14.864, 15.083, 15.304, 15.527, 15.751, 15.977, 16.205, 16.435, 16.666, 16.899, 17.134, 17.371, 17.609, 17.849, 18.091, 18.335, 18.58, 18.828, 19.076, 19.327, 19.579, 19.833, 20.089, 20.347, 20.606, 20.867, 21.13, 21.394, 21.66, 21.928, 22.198, 22.469, 22.742, 23.016, 23.293, 23.571, 23.85, 24.132, 24.415, 24.699, 24.986, 25.274, 25.564, 25.855, 26.148, 26.443, 26.739, 27.037, 27.337, 27.638, 27.941, 28.245, 28.552, 28.859, 29.169, 29.48, 29.792, 30.107, 30.422, 30.74, 31.059, 31.379, 31.702, 32.025, 32.351, 32.678, 33.006, 33.336, 33.668, 34.001, 34.336, 34.672, 35.01, 35.349, 35.69, 36.032])
meteosat7_VW_radiances = array([0.021,0.023,0.024,0.026,0.028,0.030,0.033,0.035,0.038,0.040,0.043,0.046,0.049,0.053,0.056,0.060,0.064,0.068,0.073,0.077,0.082,0.087,0.093,0.099,0.105,0.111,0.118,0.125,0.132,0.139,0.147,0.156,0.164,0.174,0.183,0.193,0.204,0.214,0.226,0.238,0.250,0.263,0.276,0.290,0.305,0.320,0.335,0.352,0.369,0.386,0.405,0.423,0.443,0.464,0.485,0.507,0.529,0.553,0.577,0.602,0.628,0.655,0.683,0.712,0.741,0.772,0.804,0.837,0.870,0.905,0.941,0.978,1.016,1.056,1.096,1.138,1.181,1.225,1.271,1.317,1.366,1.415,1.466,1.518,1.572,1.627,1.684,1.742,1.802,1.864,1.927,1.991,2.058,2.126,2.195,2.267,2.340,2.415,2.492,2.570,2.651,2.733,2.818,2.904,2.993,3.083,3.175,3.270,3.367,3.465,3.566,3.670,3.775,3.883,3.993,4.105,4.220,4.337,4.456,4.578,4.703,4.829,4.959,5.091,5.226,5.363,5.503,5.645,5.790,5.938,6.089,6.243,6.399,6.559,6.721,6.886,7.054,7.225,7.399,7.576,7.756,7.940,8.126,8.316,8.509,8.705,8.904,9.107,9.312,9.522,9.734,9.950,10.170,10.393,10.619,10.849,11.082,11.319,11.560,11.804,12.052,12.304,12.559,12.818,13.081,13.347,13.618,13.892,14.170,14.452,14.738,15.028,15.322,15.620,15.922,16.228,16.539,16.853,17.171,17.494,17.821,18.152,18.487,18.827,19.171,19.519,19.871,20.228,20.590,20.955,21.326,21.700,22.080,22.463,22.851,23.244,23.642,24.044,24.450,24.862])
meteosat7_temperatures = arange(170,370)
meteosat7_IR_calibration = array(0.104) # NB this calibration constant is in reality time dependent
meteosat7_VW_calibration = array(0.011) # NB this calibration constant is in reality time dependent
meteosat7_offset = array(5) # varies between 5 and 6
meteosat7_lut_IR = arrays2LUTString(meteosat7_IR_radiances/meteosat7_IR_calibration - meteosat7_offset, meteosat7_temperatures)
meteosat7_lut_VW = arrays2LUTString(meteosat7_VW_radiances/meteosat7_VW_calibration - meteosat7_offset, meteosat7_temperatures)

MSG_wavelengths = [600, 800, 1600, 3900, 6200, 7300, 8700, 9700, 10800, 12000, 13400, 700]
MSG_scale = [100, 100, 100, 1, 1, 1, 1, 1, 1, 1, 1, 100]
MSG_offset = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

satDict = [\
           {'name': 'GOES13', 'wavelengths': [700, 10700, 3900, 6600],
                'scale': [100./1023., (340.-170.)/1023., (340.-170.)/1023.,
                    (340.-170.)/1023.], 'offset': [0, 170, 170, 170]},
           {'name': 'GOES15', 'wavelengths': [700, 10700, 3900, 6600],
                'scale': [100./1023., (340.-170.)/1023., (340.-170.)/1023.,
                (340.-170.)/1023.], 'offset': [0, 170, 170, 170]},
           {'name': 'MTSAT2', 'NODATA': [255, 255, 255, 255],
                'wavelengths': [700, 3800, 6800, 10800], # 12mum ch not supported
                'LUT': ['0:0,255:100', mtsat_calibration_3_8_mum,
                    mtsat_calibration_6_8_mum, mtsat_calibration_10_7_mum]},
           {'name': 'MET7', 'wavelengths': [795, 6400, 11500],
                #'scale': [100./255., 0.103, 0.103], 'offset': [0, 5, 5]},
                'LUT': ['0:0,255:100', meteosat7_lut_VW, meteosat7_lut_IR]},
           {'name': 'MSG1', 'wavelengths': MSG_wavelengths,
                'scale': MSG_scale, 'offset': MSG_offset},
           {'name': 'MSG2', 'wavelengths': MSG_wavelengths,
                'scale': MSG_scale, 'offset': MSG_offset},
           {'name': 'MSG3', 'wavelengths': MSG_wavelengths,
                'scale': MSG_scale, 'offset': MSG_offset}
           ];


class Mapper(VRT):
    ''' VRT with mapping of WKV for Geostationary satellite data '''

    def __init__(self, fileName, gdalDataset, gdalMetadata):
        satellite = gdalDataset.GetDescription().split(",")[2]

        for sat in satDict:
            if sat['name'] == satellite:
                print 'This is ' + satellite
                wavelengths = sat['wavelengths']
                try:
                    scale = sat['scale']
                    offset = sat['offset']
                except:
                    print "No scale and offset found"
                    scale = None
                    offset = None
                try:
                    LUT = sat['LUT']
                except:
                    print "No LUT found"
                    LUT = [""]*len(wavelengths)
                try:
                    NODATA = sat['NODATA']
                except:
                    print "No NODATA values found"
                    NODATA = [""]*len(wavelengths)

        if wavelengths is None:
            raise AttributeError("No Eumetcast geostationary satellite");

        path = gdalDataset.GetDescription().split(",")[0].split("(")[1]
        datestamp = gdalDataset.GetDescription().split(",")[3]
        if satellite[0:3] == 'MSG':
            resolution = 'H'
            dataType = 'T' # Brightness temperatures and reflectances
        else:
            resolution = 'L'
            dataType = 'N' # Counts, for manual calibration

        metaDict = []
        for i, wavelength in enumerate(wavelengths):
            if wavelength > 2000:
                standard_name = 'brightness_temperature'
            else:
                standard_name = 'albedo'
            bandSource = 'MSG('+path+','+resolution+','+satellite+','+datestamp+\
                        ','+str(i+1)+',Y,' + dataType + ',1,1)'
            try:
                gdal.Open(bandSource)
            except:
                print "Warning: band missing for wavelength " + str(wavelength) + "nm"
                continue
            src = {'SourceFilename': bandSource, 'SourceBand': 1, 'LUT': LUT[i], 'NODATA': NODATA[i]}
            dst = {'wkv': standard_name, 'wavelength': str(wavelength)}
            if scale is not None:
                bandScale = scale[i]
                bandOffset = offset[i]
                src['ScaleRatio'] = str(bandScale)
                src['ScaleOffset'] = str(bandOffset)
            metaDict.append({'src': src, 'dst': dst})


        # create empty VRT dataset with geolocation only
        VRT.__init__(self, gdalDataset)

        # Create bands
        self._create_bands(metaDict)

        # For Meteosat7 ch1 has higher resolution than ch2 and ch3
        # and for MSG, channel 12 (HRV) has higher resolution than the other channels
        # If the high resolution channel is opened, the low res channels are
        # blown up to this size. If a low res channel is opened, the high res channels
        # are reduced to this size.
        if satellite == 'MET7' or satellite[0:3] == 'MSG':
            node0 = Node.create(self.read_xml())
            bands = node0.nodeList("VRTRasterBand")
            if satellite == 'MET7':
                if self.dataset.RasterXSize == 5032: # High res ch1 is opened
                    newSrcXSize = u'2532'
                    newSrcYSize = u'2500'
                    bands = bands[1:] # Ch2 and ch3 should be modified
                if self.dataset.RasterXSize == 2532: # Low res ch is opened
                    newSrcXSize = u'5032'
                    newSrcYSize = u'5000'
                    bands = [bands[0]] # Only ch1 needs to be modified
            elif satellite[0:3] == 'MSG':
                if self.dataset.RasterXSize == 11136: # High res ch1 is opened
                    newSrcXSize = u'3712'
                    newSrcYSize = u'3712'
                    bands = bands[0:10] # Channels 1-11 should be modified
                if self.dataset.RasterXSize == 3712: # Low res ch is opened
                    newSrcXSize = u'11136'
                    newSrcYSize = u'11136'
                    bands = [bands[11]] # Only ch12 needs to be modified

            for band in bands:
                band.nodeList("ComplexSource")[0].nodeList("SrcRect")[0].\
                        setAttribute("xSize", newSrcXSize)
                band.nodeList("ComplexSource")[0].nodeList("SrcRect")[0].\
                        setAttribute("ySize", newSrcYSize)
            self.write_xml(str(node0.rawxml()))

        # Set global metadata
        self.dataset.SetMetadata({'satID': satellite})

        # Set time
        self._set_time(datetime.datetime.strptime(datestamp, '%Y%m%d%H%M'))

        return
