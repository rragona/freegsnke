import numpy as np
import pickle
from freegs.gradshafranov import Greens


eta_copper = 1.55e-8 #resistivity in Ohm*m, for active coils 
eta_steel = 5.5e-7 #in Ohm*m, for passive structures
eta_plasma = 1e-6

d1_upper_r = [
    0.35275,
    0.36745015,
    0.38215014,
    0.39685005,
    0.35275,
    0.35275,
    0.35275,
    0.35275,
    0.35275039,
    0.36745039,
    0.36745039,
    0.36745039,
    0.36745039,
    0.36745,
    0.38215002,
    0.38215002,
    0.38215002,
    0.38215002,
    0.39685014,
    0.39685014,
    0.39685014,
    0.39685014,
    0.39685008,
    0.41155013,
    0.41155013,
    0.41155013,
    0.41155013,
    0.4115501,
    0.42625037,
    0.42625007,
    0.42625007,
    0.42625007,
    0.42625007,
    0.41155002,
    0.4262501,
]

d1_upper_z = [
    1.60924995,
    1.60924995,
    1.60924995,
    1.60924995,
    1.59455001,
    1.57984996,
    1.5651499,
    1.55044997,
    1.53574991,
    1.53574991,
    1.55044997,
    1.5651499,
    1.57984996,
    1.59455001,
    1.57984996,
    1.5651499,
    1.55044997,
    1.53574991,
    1.53574991,
    1.55044997,
    1.5651499,
    1.57984996,
    1.59455001,
    1.59455001,
    1.57984996,
    1.5651499,
    1.55044997,
    1.53574991,
    1.53574991,
    1.55044997,
    1.5651499,
    1.57984996,
    1.59455001,
    1.60924995,
    1.60924995,
]

d1_lower_z = [x * -1 for x in d1_upper_z]

d2_upper_r = [
    0.60125011,
    0.58655024,
    0.60125017,
    0.60125017,
    0.60125023,
    0.58655,
    0.58655,
    0.57185012,
    0.57185036,
    0.57185042,
    0.55715007,
    0.55715007,
    0.55715001,
    0.54245019,
    0.54245019,
    0.54245001,
    0.52775019,
    0.52775025,
    0.52775025,
    0.57185012,
    0.55715013,
    0.54245007,
    0.52774996,
]

d2_upper_z = [
    1.75705004,
    1.75705004,
    1.74234998,
    1.72765005,
    1.71294999,
    1.71294999,
    1.72765005,
    1.74234998,
    1.72765005,
    1.71294999,
    1.71294999,
    1.72765005,
    1.74234998,
    1.74234998,
    1.72765005,
    1.71294999,
    1.71294999,
    1.72765005,
    1.74234998,
    1.75705004,
    1.75705004,
    1.75705004,
    1.75705004,
]

d2_lower_z = [x * -1 for x in d2_upper_z]

d3_upper_r = [
    0.82854998,
    0.8432501,
    0.84325004,
    0.84325004,
    0.82855022,
    0.82855004,
    0.8285504,
    0.81384999,
    0.81385022,
    0.81385005,
    0.79915011,
    0.79915005,
    0.79915005,
    0.78445005,
    0.78444934,
    0.78445005,
    0.76975012,
    0.76975018,
    0.76975018,
    0.76975006,
    0.78445035,
    0.79915041,
    0.81384987,
]

d3_upper_z = [
    2.00405002,
    2.00405002,
    1.98935008,
    1.97465003,
    1.95995009,
    1.97465003,
    1.98935008,
    1.98935008,
    1.97465003,
    1.95995009,
    1.95995009,
    1.97465003,
    1.98935008,
    1.98935008,
    1.97465003,
    1.95995009,
    1.95995009,
    1.97465003,
    1.98935008,
    2.00405002,
    2.00405002,
    2.00405002,
    2.00405002,
]

d3_lower_z = [x * -1 for x in d3_upper_z]

d5_upper_r = [
    1.90735006,
    1.92205048,
    1.92205,
    1.92205,
    1.92205,
    1.92205,
    1.92205,
    1.90735018,
    1.9073503,
    1.9073503,
    1.9073503,
    1.9073503,
    1.90735006,
    1.89265001,
    1.89265013,
    1.89265013,
    1.89265013,
    1.89265013,
    1.89265001,
    1.87794995,
    1.87795019,
    1.87795019,
    1.87795019,
    1.87795019,
    1.87795019,
    1.87795019,
    1.89265037,
]

d5_upper_z = [
    1.99409997,
    1.99409997,
    1.97940004,
    1.96469998,
    1.95000005,
    1.93529999,
    1.92060006,
    1.9059,
    1.92060006,
    1.93529999,
    1.95000005,
    1.96469998,
    1.97940004,
    1.97940004,
    1.96469998,
    1.95000005,
    1.93529999,
    1.92060006,
    1.9059,
    1.9059,
    1.92060006,
    1.93529999,
    1.95000005,
    1.96469998,
    1.97940004,
    1.99409997,
    1.99409997,
]

d5_lower_z = [x * -1 for x in d5_upper_z]

d6_upper_r = [
    1.30704987,
    1.32175004,
    1.32175004,
    1.32174993,
    1.30705011,
    1.32174993,
    1.30704999,
    1.29235005,
    1.30704999,
    1.29235005,
    1.27765,
    1.27765,
    1.26295006,
    1.27765,
    1.26294994,
    1.24825013,
    1.26294994,
    1.24825001,
    1.24825001,
    1.24825013,
    1.26294994,
    1.27765,
    1.29234993,
]

d6_upper_z = [
    1.44564998,
    1.44564998,
    1.46034992,
    1.47504997,
    1.48974991,
    1.48975003,
    1.47504997,
    1.46034992,
    1.46035004,
    1.47504997,
    1.48975003,
    1.47504997,
    1.46034992,
    1.46034992,
    1.47504997,
    1.48974991,
    1.48975003,
    1.47504997,
    1.46034992,
    1.44564998,
    1.44564998,
    1.44564998,
    1.44564998,
]

d6_lower_z = [x * -1 for x in d6_upper_z]

d7_upper_r = [
    1.54205,
    1.55675006,
    1.55675006,
    1.55675006,
    1.54205012,
    1.55674994,
    1.54205,
    1.52735007,
    1.54204988,
    1.52735007,
    1.51265013,
    1.52734995,
    1.51265001,
    1.49794996,
    1.51265001,
    1.49794996,
    1.48325002,
    1.48325002,
    1.48325002,
    1.48325002,
    1.49795008,
    1.51265001,
    1.52734995,
]

d7_upper_z = [
    1.44564998,
    1.44564998,
    1.46034992,
    1.47504997,
    1.48974991,
    1.48974991,
    1.47504997,
    1.46034992,
    1.46034992,
    1.47504997,
    1.48974991,
    1.48974991,
    1.47504997,
    1.46035004,
    1.46034992,
    1.47504997,
    1.48974991,
    1.47504997,
    1.46035004,
    1.44564998,
    1.44564998,
    1.44564998,
    1.44564998,
]

d7_lower_z = [x * -1 for x in d7_upper_z]

dp_upper_r = [
    0.93285,
    0.94755,
    0.93285,
    0.94755,
    0.96224999,
    0.96224999,
    0.88875002,
    0.90345001,
    0.91815001,
    0.91815001,
    0.90345001,
    0.88875002,
    0.96224999,
    0.94755,
    0.93285,
    0.96224999,
    0.94755,
    0.93285,
    0.91815001,
    0.90345001,
    0.88875002,
    0.88874996,
    0.90345001,
    0.91815001,
]

dp_upper_z = [
    1.48634994,
    1.48634994,
    1.47165,
    1.47165,
    1.48634994,
    1.47165,
    1.47165,
    1.47165,
    1.47165,
    1.48634994,
    1.48634994,
    1.48634994,
    1.51574993,
    1.51574993,
    1.51574993,
    1.50105,
    1.50105,
    1.50105,
    1.51574993,
    1.51574993,
    1.51574993,
    1.50105,
    1.50105,
    1.50105,
]

dp_lower_z = [x * -1 for x in dp_upper_z]

p4_upper_r = [
    1.43500018,
    1.53500021,
    1.51000023,
    1.48500025,
    1.46000016,
    1.43500006,
    1.43500006,
    1.46100008,
    1.43500018,
    1.46100008,
    1.48700011,
    1.4610002,
    1.48700011,
    1.51300013,
    1.48700011,
    1.51300013,
    1.53900015,
    1.51300013,
    1.53900003,
    1.56500018,
    1.53900015,
    1.56500006,
    1.56500006,
]

p4_upper_z = [
    1.04014993,
    1.03714991,
    1.03714991,
    1.03714991,
    1.03714991,
    1.07814991,
    1.1161499,
    1.15414989,
    1.15414989,
    1.1161499,
    1.07814991,
    1.07814991,
    1.1161499,
    1.15414989,
    1.15414989,
    1.1161499,
    1.07814991,
    1.07814991,
    1.1161499,
    1.15414989,
    1.15414989,
    1.1161499,
    1.07814991,
]

p4_lower_z = [x * -1 for x in p4_upper_z]

p5_upper_r = [
    1.58500004,
    1.61000001,
    1.63499999,
    1.65999997,
    1.68499994,
    1.58500004,
    1.58500004,
    1.58500004,
    1.63499999,
    1.63499999,
    1.63499999,
    1.65999997,
    1.65999997,
    1.65999997,
    1.68499994,
    1.68500006,
    1.68500006,
    1.71500003,
    1.71500003,
    1.71500003,
    1.71500003,
    1.6099776,
    1.60997999,
]

p5_upper_z = [
    0.41065004,
    0.41065004,
    0.41065004,
    0.41065004,
    0.41065004,
    0.37165004,
    0.33265004,
    0.29365003,
    0.37165004,
    0.33265004,
    0.29365003,
    0.29365003,
    0.33262005,
    0.37165004,
    0.37165004,
    0.33265004,
    0.29365003,
    0.29365006,
    0.33265004,
    0.37165004,
    0.41065004,
    0.31147972,
    0.35528255,
]

p5_lower_z = [x * -1 for x in p5_upper_z]

p6_upper_r = [
    1.2887001,
    1.2887001,
    1.30900013,
    1.2887001,
    1.30900013,
    1.33414996,
    1.33414996,
    1.35444999,
    1.33414996,
    1.35444999,
]

p6_upper_z = [
    0.99616498,
    0.97586501,
    0.95556498,
    0.95556498,
    0.97586501,
    0.931265,
    0.91096503,
    0.89066499,
    0.89066499,
    0.91096503,
]

p6_lower_z = [x * -1 for x in p6_upper_z]

px_upper_r = [
    0.24849965,
    0.24849975,
    0.24849974,
    0.2344998,
    0.24849974,
    0.24849974,
    0.24849972,
    0.24849972,
    0.24849972,
    0.24849971,
    0.24849971,
    0.24849971,
    0.24849969,
    0.24849969,
    0.24849969,
    0.24849968,
    0.24849968,
    0.24849968,
    0.24849966,
    0.24849966,
    0.24849966,
    0.24849965,
    0.23449969,
    0.23449969,
    0.23449971,
    0.23449971,
    0.23449971,
    0.23449971,
    0.23449972,
    0.23449972,
    0.23449974,
    0.23449974,
    0.23449974,
    0.23449975,
    0.23449975,
    0.23449977,
    0.23449977,
    0.23449977,
    0.23449978,
    0.23449978,
    0.2344998,
    0.2344998,
]

px_upper_z = [
    1.41640627,
    1.03640544,
    1.0554055,
    1.03164983,
    1.07440555,
    1.0934056,
    1.11240554,
    1.13140559,
    1.15040565,
    1.1694057,
    1.18840575,
    1.20740581,
    1.22640586,
    1.24540591,
    1.26440585,
    1.2834059,
    1.30240595,
    1.32140601,
    1.34040606,
    1.35940611,
    1.37840617,
    1.39740622,
    1.41164911,
    1.39264905,
    1.37364912,
    1.35464919,
    1.33564925,
    1.31664932,
    1.29764926,
    1.27864933,
    1.2596494,
    1.24064946,
    1.22164953,
    1.20264947,
    1.18364954,
    1.16464961,
    1.14564967,
    1.12664974,
    1.10764968,
    1.08864975,
    1.06964982,
    1.05064988,
]

px_lower_z = [x * -1 for x in px_upper_z]

pc_r = [
    0.05950115,
    0.05950115,
    0.05950116,
    0.05950116,
    0.05950116,
    0.05950121,
    0.05950117,
    0.05950117,
    0.05950118,
    0.05950122,
    0.05950119,
    0.05950119,
    0.05950119,
    0.05950119,
    0.05950123,
    0.0595012,
    0.0595012,
    0.0595012,
    0.0595012,
    0.0595012,
    0.0595012,
    0.0595012,
    0.0595012,
    0.0595012,
    0.0595012,
    0.0595012,
    0.0595012,
    0.0595012,
    0.05950124,
    0.05950119,
    0.05950119,
    0.05950119,
    0.05950119,
    0.05950119,
    0.05950122,
    0.05950122,
    0.05950118,
    0.05950117,
    0.05950117,
    0.05950117,
    0.05950116,
    0.05950116,
    0.05950115,
    0.05950115,
    0.05950114,
    0.05950114,
    0.05950113,
    0.05950113,
    0.05950112,
    0.05950112,
    0.05950111,
    0.0595011,
    0.05950113,
    0.05950109,
    0.05950108,
    0.05950111,
    0.0595011,
    0.05950109,
    0.05950109,
    0.05950107,
    0.0595009,
    0.05950106,
    0.05950104,
    0.05950104,
    0.05950103,
    0.05950105,
    0.05950146,
    0.05950177,
    0.05950198,
    0.05950211,
    0.05950096,
    0.07150049,
    0.0715005,
    0.07150051,
    0.07150052,
    0.07150053,
    0.07150054,
    0.07150055,
    0.07150055,
    0.07150057,
    0.07150058,
    0.07150058,
    0.07150059,
    0.0715006,
    0.07150061,
    0.07150061,
    0.07150062,
    0.07150063,
    0.07150064,
    0.07150064,
    0.07150065,
    0.07150066,
    0.07150067,
    0.07150067,
    0.07150067,
    0.07150068,
    0.07150069,
    0.0715007,
    0.0715007,
    0.0715007,
    0.07150071,
    0.07150071,
    0.07150072,
    0.07150066,
    0.07150073,
    0.07150073,
    0.07150073,
    0.07150073,
    0.07150074,
    0.07150074,
    0.07150085,
    0.07150132,
    0.07150154,
    0.07150155,
    0.07150079,
    0.07150076,
    0.07150076,
    0.07150076,
    0.07150076,
    0.07150076,
    0.07150076,
    0.07150076,
    0.07150073,
    0.07150077,
    0.07150077,
    0.07150077,
    0.07150077,
    0.07150077,
    0.07150077,
    0.07150076,
    0.07150076,
    0.07150076,
    0.07150076,
    0.07150076,
    0.07150076,
    0.07150076,
    0.07150076,
    0.07150076,
    0.07150076,
    0.07150075,
    0.07150075,
    0.07150074,
    0.0715007,
    0.07150044,
    0.07150045,
    0.07150047,
    0.07150047,
    0.07150049,
    0.07150128,
    0.07150129,
    0.07150111,
    0.07150067,
    0.07150006,
    0.07150054,
    0.07150055,
    0.07150055,
    0.07150056,
    0.07150057,
    0.07150058,
    0.07150058,
    0.0715006,
    0.07150061,
    0.07150061,
    0.07150062,
    0.07150062,
    0.07150063,
    0.07150064,
    0.07150064,
    0.07150065,
    0.07150065,
    0.07150066,
    0.07150067,
    0.07150067,
    0.07150067,
    0.07150068,
    0.07150068,
    0.07150069,
    0.07150069,
    0.0715007,
    0.0715007,
    0.0715007,
    0.0715007,
    0.0715007,
    0.07150071,
    0.07150071,
    0.07150071,
    0.07150072,
    0.07150072,
    0.07150072,
    0.07150072,
    0.07150072,
    0.07150072,
    0.07150073,
    0.07150073,
    0.07150073,
    0.07150073,
    0.07150073,
    0.07150073,
    0.07150073,
    0.07150073,
    0.07150073,
    0.07150076,
    0.07150076,
    0.07150076,
    0.07150076,
    0.07150076,
    0.07150076,
    0.07150076,
    0.07150076,
    0.07150075,
    0.07150075,
    0.07150075,
    0.07150074,
    0.059501,
    0.05950099,
    0.059501,
    0.05950118,
    0.05950101,
    0.05950101,
    0.05950101,
    0.05950102,
    0.05950102,
    0.05950102,
    0.05950103,
    0.05950122,
    0.05950122,
    0.05950122,
    0.05950104,
    0.05950104,
    0.05950104,
    0.05950104,
    0.05950104,
    0.05950104,
    0.05950104,
    0.05950104,
    0.05950104,
    0.0595013,
    0.05950121,
    0.05950123,
    0.05950116,
    0.05950124,
    0.05950121,
    0.05950119,
    0.05950121,
    0.05950122,
    0.05950122,
    0.05950121,
    0.0595012,
    0.05950121,
    0.05950121,
    0.0595012,
    0.05950101,
    0.05950119,
    0.05950119,
    0.05950118,
    0.05950118,
    0.05950117,
    0.05950117,
    0.05950116,
    0.05950116,
    0.05950119,
    0.05950115,
    0.05950114,
    0.05950114,
    0.05950113,
    0.05950112,
    0.05950112,
    0.05950111,
    0.0595011,
    0.05950109,
    0.05950108,
    0.05950107,
    0.05950107,
    0.05950106,
    0.05950105,
    0.05950104,
    0.05950103,
    0.05950102,
    0.05950101,
    0.059501,
    0.05950099,
    0.05950078,
    0.05950077,
    0.05950096,
]

pc_z = [
    -7.81521082e-01,
    -7.59520829e-01,
    -7.37520635e-01,
    -7.15520382e-01,
    -6.93520188e-01,
    -6.71519935e-01,
    -6.49519742e-01,
    -6.27519488e-01,
    -6.05519295e-01,
    -5.83519042e-01,
    -5.61518848e-01,
    -5.39518654e-01,
    -5.17518401e-01,
    -4.95518208e-01,
    -4.73517984e-01,
    -4.51517761e-01,
    -4.29517567e-01,
    -4.07517344e-01,
    -3.85517120e-01,
    -3.63516897e-01,
    -3.41516674e-01,
    -3.19516450e-01,
    -2.97516227e-01,
    -2.75516003e-01,
    -2.53515780e-01,
    -2.31515557e-01,
    -2.09515333e-01,
    -1.87515110e-01,
    -1.65514901e-01,
    -1.43514678e-01,
    -1.21514454e-01,
    -9.95142311e-02,
    -7.75140151e-02,
    -5.55137955e-02,
    -3.35135758e-02,
    -1.15133552e-02,
    1.04868645e-02,
    3.24870832e-02,
    5.44873066e-02,
    7.64875263e-02,
    9.84877497e-02,
    1.20487973e-01,
    1.42488196e-01,
    1.64488405e-01,
    1.86488628e-01,
    2.08488852e-01,
    2.30489075e-01,
    2.52489269e-01,
    2.74489492e-01,
    2.96489716e-01,
    3.18489939e-01,
    3.40490162e-01,
    3.62490386e-01,
    3.84490609e-01,
    4.06490862e-01,
    4.28490698e-01,
    4.50491309e-01,
    4.72491503e-01,
    4.94491905e-01,
    5.16492069e-01,
    5.38492322e-01,
    5.60492516e-01,
    5.82492828e-01,
    6.04492962e-01,
    6.26493216e-01,
    6.48493409e-01,
    6.70493662e-01,
    6.92494035e-01,
    7.14494169e-01,
    7.36494422e-01,
    7.58494616e-01,
    7.58488476e-01,
    7.36488640e-01,
    7.14488804e-01,
    6.92489028e-01,
    6.70489192e-01,
    6.48489356e-01,
    6.26489520e-01,
    6.04489744e-01,
    5.82489908e-01,
    5.60490072e-01,
    5.38490295e-01,
    5.16490459e-01,
    4.94490594e-01,
    4.72490788e-01,
    4.50490981e-01,
    4.28491175e-01,
    4.06491339e-01,
    3.84491533e-01,
    3.62491727e-01,
    3.40491891e-01,
    3.18492085e-01,
    2.96492279e-01,
    2.74492443e-01,
    2.52492636e-01,
    2.30492830e-01,
    2.08493009e-01,
    1.86493203e-01,
    1.64493382e-01,
    1.42493561e-01,
    1.20493740e-01,
    9.84939337e-02,
    7.64944404e-02,
    5.44943213e-02,
    3.24945636e-02,
    1.04946950e-02,
    -1.15051102e-02,
    -3.35049182e-02,
    -5.55047244e-02,
    -7.75045305e-02,
    -9.95043367e-02,
    -1.21504150e-01,
    -1.43503949e-01,
    -1.65503755e-01,
    -1.87503561e-01,
    -2.09503368e-01,
    -2.31503174e-01,
    -2.53502995e-01,
    -2.75502801e-01,
    -2.97502607e-01,
    -3.19502413e-01,
    -3.41502219e-01,
    -3.63502026e-01,
    -3.85501832e-01,
    -4.07501638e-01,
    3.95501614e-01,
    -4.29501444e-01,
    -4.51501250e-01,
    -4.73501056e-01,
    -4.95500863e-01,
    -5.17500639e-01,
    -5.39500475e-01,
    -5.61500251e-01,
    -5.83500087e-01,
    -6.05499864e-01,
    -6.27499700e-01,
    -6.49499476e-01,
    -6.71499312e-01,
    -6.93499088e-01,
    -7.15498924e-01,
    -7.37498701e-01,
    -7.59498537e-01,
    -7.81498313e-01,
    7.69502759e-01,
    7.47502983e-01,
    7.25503147e-01,
    7.03503370e-01,
    6.81503534e-01,
    6.59503758e-01,
    6.37503922e-01,
    6.15504146e-01,
    5.93504310e-01,
    5.71504533e-01,
    5.49504697e-01,
    5.27504921e-01,
    5.05505085e-01,
    4.83505279e-01,
    4.61505353e-01,
    4.39505666e-01,
    4.17505413e-01,
    3.73506218e-01,
    3.51506412e-01,
    3.29506606e-01,
    3.07506770e-01,
    2.85506964e-01,
    2.63507158e-01,
    2.41507336e-01,
    2.19507530e-01,
    1.97507709e-01,
    1.75507888e-01,
    1.53508082e-01,
    1.31508261e-01,
    1.09508440e-01,
    8.75086263e-02,
    6.55088127e-02,
    4.35089879e-02,
    2.15091743e-02,
    -4.90644481e-04,
    -2.24904604e-02,
    -4.44902778e-02,
    -6.64900914e-02,
    -8.84899125e-02,
    -1.10489726e-01,
    -1.32489547e-01,
    -1.54489353e-01,
    -1.76489174e-01,
    -1.98488995e-01,
    -2.20488816e-01,
    -2.42488623e-01,
    -2.64488459e-01,
    -2.86488265e-01,
    -3.08488101e-01,
    -3.30487907e-01,
    -3.52487713e-01,
    -3.74487549e-01,
    -3.96487355e-01,
    -4.18487161e-01,
    -4.40486997e-01,
    -4.62486804e-01,
    -4.84486639e-01,
    -5.06486416e-01,
    -5.28486252e-01,
    -5.50486028e-01,
    -5.72485864e-01,
    -5.94485700e-01,
    -6.16485476e-01,
    -6.38485312e-01,
    -6.60485148e-01,
    -6.82484925e-01,
    -7.04484761e-01,
    -7.26484597e-01,
    -7.48484373e-01,
    -7.70484209e-01,
    -7.26499677e-01,
    -7.48499930e-01,
    -7.04499483e-01,
    -7.70499945e-01,
    -6.82499230e-01,
    -6.60498977e-01,
    -6.38498724e-01,
    -6.16498530e-01,
    -5.94498277e-01,
    -5.72498024e-01,
    -5.50497830e-01,
    -5.28497398e-01,
    -5.06497145e-01,
    -4.84496951e-01,
    -4.62496907e-01,
    -4.40496653e-01,
    -4.18496430e-01,
    -3.96496207e-01,
    -3.74495953e-01,
    -3.52495730e-01,
    -3.30495477e-01,
    -3.08495253e-01,
    -2.86495030e-01,
    -2.63993531e-01,
    -2.42494494e-01,
    -2.20494315e-01,
    -1.98494136e-01,
    -1.76493689e-01,
    -1.54493496e-01,
    -1.32493302e-01,
    -1.10493094e-01,
    -8.84926915e-02,
    -6.64924607e-02,
    -4.44922261e-02,
    -2.24919878e-02,
    -4.91753221e-04,
    2.15084739e-02,
    4.35086973e-02,
    6.55087605e-02,
    1.09509401e-01,
    1.31509617e-01,
    1.53509840e-01,
    1.75510064e-01,
    1.97510287e-01,
    2.19510511e-01,
    2.41510719e-01,
    2.63510942e-01,
    8.75091851e-02,
    2.85511166e-01,
    3.07511151e-01,
    3.29511374e-01,
    3.51511598e-01,
    3.73512030e-01,
    3.95512253e-01,
    4.17512476e-01,
    4.39512491e-01,
    4.61512923e-01,
    4.83513147e-01,
    5.05513191e-01,
    5.27513623e-01,
    5.49513638e-01,
    5.71513832e-01,
    5.93514264e-01,
    6.15514517e-01,
    6.37514710e-01,
    6.59514725e-01,
    6.81514919e-01,
    7.03515172e-01,
    7.25515604e-01,
    7.47515619e-01,
    7.69516051e-01,
]

import os
this_dir , this_filename = os.path.split(__file__)
passive_path=os.path.join(this_dir,'pass_coils_n.pk')
with open(passive_path,'rb') as handle:
    pass_coil_dict = pickle.load(handle)

import populate_cancoils
coilcans_dict=populate_cancoils.pop_coilcans()
# dict with key:value entries like  'can_P5lower_7': {'R': 1.7435, 'Z': -0.31025, 'dR': 0.003, 'dZ': 0.0935}
# is using coilcans, these are all filaments, so use eta_material*2*pi*tc['R']/(tc['dR']*tc['dZ']) for the filament resistance
multicoilcans_dict=populate_cancoils.pop_multicoilcans()
# dict with key:values like 'can_P5lower': {'R':[list_of_Rs],'Z':[list_of_Zs],'series':sum(2*pi*R/(dR*dZ))}
# if using multicoilcans, multiply 'series' by eta_material to get the resistance

multican=True

#section of active coil loops
dRc = 0.0127
dZc = 0.0127
# these dRc and dZc are not really used below, each piece of metal has its own geometry data, but still

coils_dict = {}

coils_dict['Solenoid'] = {}
coils_dict['Solenoid']['coords'] = np.array([[0.19475]*324,np.linspace(-1.581,1.581,324)])
coils_dict['Solenoid']['polarity'] = np.array([1]*len(coils_dict['Solenoid']['coords'][0]))
coils_dict['Solenoid']['dR']=0.012
coils_dict['Solenoid']['dZ']=0.018


# coils_dict['Pc'] = {}
# coils_dict['Pc']['coords'] = np.array([pc_r, pc_z])
# coils_dict['Pc']['polarity'] = np.array([1]*len(coils_dict['Pc']['coords'][0]))

coils_dict['Px'] = {}
coils_dict['Px']['coords'] = np.array([px_upper_r+px_upper_r, px_upper_z+px_lower_z])
coils_dict['Px']['polarity'] = np.array([1]*len(coils_dict['Px']['coords'][0]))
coils_dict['Px']['dR']=0.011
coils_dict['Px']['dZ']=0.018

coils_dict['D1'] = {}
coils_dict['D1']['coords'] = np.array([d1_upper_r+d1_upper_r, d1_upper_z+d1_lower_z])
coils_dict['D1']['polarity'] = np.array([1]*len(coils_dict['D1']['coords'][0]))
coils_dict['D1']['dR']=0.0127
coils_dict['D1']['dZ']=0.0127

coils_dict['D2'] = {}
coils_dict['D2']['coords'] = np.array([d2_upper_r+d2_upper_r, d2_upper_z+d2_lower_z])
coils_dict['D2']['polarity'] = np.array([1]*len(coils_dict['D2']['coords'][0]))
coils_dict['D2']['dR']=0.0127
coils_dict['D2']['dZ']=0.0127

coils_dict['D3'] = {}
coils_dict['D3']['coords'] = np.array([d3_upper_r+d3_upper_r, d3_upper_z+d3_lower_z])
coils_dict['D3']['polarity'] = np.array([1]*len(coils_dict['D3']['coords'][0]))
coils_dict['D3']['dR']=0.0127
coils_dict['D3']['dZ']=0.0127

coils_dict['Dp'] = {}
coils_dict['Dp']['coords'] = np.array([dp_upper_r+dp_upper_r, dp_upper_z+dp_lower_z])
coils_dict['Dp']['polarity'] = np.array([1]*len(coils_dict['Dp']['coords'][0]))
coils_dict['Dp']['dR']=0.0127
coils_dict['Dp']['dZ']=0.0127

coils_dict['D5'] = {}
coils_dict['D5']['coords'] = np.array([d5_upper_r+d5_upper_r, d5_upper_z+d5_lower_z])
coils_dict['D5']['polarity'] = np.array([1]*len(coils_dict['D5']['coords'][0]))
coils_dict['D5']['dR']=0.0127
coils_dict['D5']['dZ']=0.0127

coils_dict['D6'] = {}
coils_dict['D6']['coords'] = np.array([d6_upper_r+d6_upper_r, d6_upper_z+d6_lower_z])
coils_dict['D6']['polarity'] = np.array([1]*len(coils_dict['D6']['coords'][0]))
coils_dict['D6']['dR']=0.0127
coils_dict['D6']['dZ']=0.0127

coils_dict['D7'] = {}
coils_dict['D7']['coords'] = np.array([d7_upper_r+d7_upper_r, d7_upper_z+d7_lower_z])
coils_dict['D7']['polarity'] = np.array([1]*len(coils_dict['D7']['coords'][0]))
coils_dict['D7']['dR']=0.0127
coils_dict['D7']['dZ']=0.0127

coils_dict['P4'] = {}
coils_dict['P4']['coords'] = np.array([p4_upper_r+p4_upper_r, p4_upper_z+p4_lower_z])
coils_dict['P4']['polarity'] = np.array([1]*len(coils_dict['P4']['coords'][0]))
coils_dict['P4']['dR']=0.024
coils_dict['P4']['dZ']=0.037

coils_dict['P5'] = {}
coils_dict['P5']['coords'] = np.array([p5_upper_r+p5_upper_r, p5_upper_z+p5_lower_z])
coils_dict['P5']['polarity'] = np.array([1]*len(coils_dict['P5']['coords'][0]))
coils_dict['P5']['dR']=0.024
coils_dict['P5']['dZ']=0.037

coils_dict['P6'] = {}
coils_dict['P6']['coords'] = np.array([p6_upper_r+p6_upper_r, p6_upper_z+p6_lower_z])
coils_dict['P6']['polarity'] = np.array([1]*len(p6_upper_r)+[-1]*len(p6_upper_r))
coils_dict['P6']['dR']=0.02836
coils_dict['P6']['dZ']=0.02836

#get number of active coils
N_active=len(coils_dict.keys())
#insert resistance-related info:
for key in coils_dict.keys():
    coils_dict[key]['resistivity'] = eta_copper/(coils_dict[key]['dR']*coils_dict[key]['dZ']) #(dRc*dZc)

#  these must be replaced with the actual vessel filaments
# for tkey in pass_coil_dict.keys():
#     tentry = pass_coil_dict[tkey]
#     coils_dict[tkey] = {}
#     coils_dict[tkey]['coords'] = np.array([ [tentry['R']], [tentry['Z']] ])
#     coils_dict[tkey]['polarity'] = np.array([1])
#     coils_dict[tkey]['resistivity'] = eta_steel/(tentry['dr']*tentry['dz'])

if multican:
    for tkey in multicoilcans_dict.keys():
        tentry=coilcans_dict[tkey]
        coils_dict[tkey] = {}
        coils_dict[tkey]['coords'] = np.array([ tentry['Rs'] , tentry['Zs'] ])
        coils_dict[tkey]['polarity'] = np.array([1]*len(coils_dict[tkey]['coords'][0]))
        coils_dict[tkey]['resistivity'] = eta_steel*coils_dict[tkey]['series']/np.mean(coils_dict[tkey]['coords'][0])
        # the last division is there because we are already multiplying by <R> in coil_resist below 
else:
    for tkey in coilcans_dict.keys():
        coils_dict[tkey] = {}
        coils_dict[tkey]['coords'] = np.array([ [tentry['R']], [tentry['Z']] ])
        coils_dict[tkey]['polarity'] = np.array([1])
        coils_dict[tkey]['resistivity'] = eta_steel/(tentry['dR']*tentry['dZ'])

#calculate coil-coil inductances and coil resistances
nloops_per_coil = np.zeros(len(coils_dict.keys()))
coil_resist = np.zeros(len(coils_dict.keys()))
coil_self_ind = np.zeros((len(coils_dict.keys()), len(coils_dict.keys())))
for i,labeli in enumerate(coils_dict.keys()):
    nloops_per_coil[i] = len(coils_dict[labeli]['coords'][0])    
    #for coil-coil flux
    for j,labelj in enumerate(coils_dict.keys()):
        greenm = Greens(coils_dict[labeli]['coords'][0][np.newaxis,:],
                        coils_dict[labeli]['coords'][1][np.newaxis,:],
                        coils_dict[labelj]['coords'][0][:,np.newaxis],
                        coils_dict[labelj]['coords'][1][:,np.newaxis])
        
        greenm *= coils_dict[labelj]['polarity'][:,np.newaxis]
        greenm *= coils_dict[labeli]['polarity'][np.newaxis,:]
        coil_self_ind[i,j] = np.sum(greenm)
    #resistance = resistivity/area * number of loops * mean_radius * 2pi
    coil_resist[i] = coils_dict[labeli]['resistivity']*np.mean(coils_dict[labeli]['coords'][0])
coil_self_ind *= 2*np.pi

#if voltages in terms of 'per loop':
# coil_self_ind /= nloops_per_coil[:,np.newaxis]
# coil_resist *= 2*np.pi

#if voltages in terms of total applied voltage:
#check also calculation of inductances in qfe!!
coil_resist *= 2*np.pi*nloops_per_coil


from freegs.machine import Machine, Circuit, Wall, Solenoid
from freegs.coil import Coil
from freegs.multi_coil import MultiCoil
#define MASTU machine including passive structures
#note that PC has been eliminated entirely (vanilla FreeGS includes it)
def MASTU_wpass():
    """MAST-Upgrade, using MultiCoil to represent coils with different locations
    for each strand.
    """
    coils = [
        ("Solenoid", Solenoid(0.19475, -1.581, 1.581, 324, control=False)),
        #("Pc", MultiCoil(pc_r, pc_z)),
        (
            "Px",
            Circuit(
                [
                    ("PxU", MultiCoil(px_upper_r, px_upper_z), 1.0),
                    ("PxL", MultiCoil(px_upper_r, px_lower_z), 1.0),
                ]
            ),
        ),
        (
            "D1",
            Circuit(
                [
                    ("D1U", MultiCoil(d1_upper_r, d1_upper_z), 1.0),
                    ("D1L", MultiCoil(d1_upper_r, d1_lower_z), 1.0),
                ]
            ),
        ),
        (
            "D2",
            Circuit(
                [
                    ("D2U", MultiCoil(d2_upper_r, d2_upper_z), 1.0),
                    ("D2L", MultiCoil(d2_upper_r, d2_lower_z), 1.0),
                ]
            ),
        ),
        (
            "D3",
            Circuit(
                [
                    ("D3U", MultiCoil(d3_upper_r, d3_upper_z), 1.0),
                    ("D3L", MultiCoil(d3_upper_r, d3_lower_z), 1.0),
                ]
            ),
        ),
        (
            "Dp",
            Circuit(
                [
                    ("DPU", MultiCoil(dp_upper_r, dp_upper_z), 1.0),
                    ("DPL", MultiCoil(dp_upper_r, dp_lower_z), 1.0),
                ]
            ),
        ),
        (
            "D5",
            Circuit(
                [
                    ("D5U", MultiCoil(d5_upper_r, d5_upper_z), 1.0),
                    ("D5L", MultiCoil(d5_upper_r, d5_lower_z), 1.0),
                ]
            ),
        ),
        (
            "D6",
            Circuit(
                [
                    ("D6U", MultiCoil(d6_upper_r, d6_upper_z), 1.0),
                    ("D6L", MultiCoil(d6_upper_r, d6_lower_z), 1.0),
                ]
            ),
        ),
        (
            "D7",
            Circuit(
                [
                    ("D7U", MultiCoil(d7_upper_r, d7_upper_z), 1.0),
                    ("D7L", MultiCoil(d7_upper_r, d7_lower_z), 1.0),
                ]
            ),
        ),
        (
            "P4",
            Circuit(
                [
                    ("P4U", MultiCoil(p4_upper_r, p4_upper_z), 1.0),
                    ("P4L", MultiCoil(p4_upper_r, p4_lower_z), 1.0),
                ]
            ),
        ),
        (
            "P5",
            Circuit(
                [
                    ("P5U", MultiCoil(p5_upper_r, p5_upper_z), 1.0),
                    ("P5L", MultiCoil(p5_upper_r, p5_lower_z), 1.0),
                ]
            ),
        ),
        (
            "P6",
            Circuit(
                [
                    ("P6U", MultiCoil(p6_upper_r, p6_upper_z), 1.0),
                    ("P6L", MultiCoil(p6_upper_r, p6_lower_z), -1.0),
                ]
            ),
        ),
    ]
    #
    # here we must add the passive-structure coils
    # e.g. ( "pas_1", Coil(R, Z) ) 
    # for tkey in pass_coil_dict.keys():
    #     tentry=pass_coil_dict[tkey]
    #     coils.append((tkey, Coil(R=tentry['R'], Z=tentry['Z'], 
    #                              area=tentry['dr']*tentry['dz'], 
    #                              control=False)))
#
#
    rwall = [1.56442 , 1.73298 , 1.34848 , 1.0882  , 0.902253, 0.903669,
       0.533866, 0.538011, 0.332797, 0.332797, 0.334796, 0.303115,
       0.305114, 0.269136, 0.271135, 0.260841, 0.260841, 0.271135,
       0.269136, 0.305114, 0.303115, 0.334796, 0.332797, 0.332797,
       0.538598, 0.534469, 0.90563 , 0.904219, 1.0882  , 1.34848 ,
       1.73018 , 1.56442 , 1.37999 , 1.37989 , 1.19622 , 1.19632 ,
       1.05537 , 1.05528 , 0.947502, 0.905686, 0.899143, 0.883388,
       0.867681, 0.851322, 0.833482, 0.826063, 0.822678, 0.821023,
       0.820691, 0.822887, 0.827573, 0.839195, 0.855244, 0.877567,
       0.899473, 1.18568 , 1.279   , 1.296   , 1.521   , 1.521   ,
       1.8     , 1.8     , 1.521   , 1.521   , 1.296   , 1.279   ,
       1.18568 , 0.899473, 0.877567, 0.855244, 0.839195, 0.827573,
       0.822887, 0.820691, 0.821023, 0.822678, 0.826063, 0.833482,
       0.851322, 0.867681, 0.883388, 0.899143, 0.905686, 0.947502,
       1.05528 , 1.05537 , 1.19632 , 1.19622 , 1.37989 , 1.37999 ,
       1.56442 ]

    zwall = [ 1.56424 ,  1.67902 ,  2.06041 ,  2.05946 ,  1.87565 ,  1.87424 ,
        1.50286 ,  1.49874 ,  1.29709 ,  1.094   ,  1.094   ,  0.8475  ,
        0.8475  ,  0.565   ,  0.565   ,  0.495258, -0.507258, -0.577   ,
       -0.577   , -0.8595  , -0.8595  , -1.106   , -1.106   , -1.30909 ,
       -1.5099  , -1.51403 , -1.88406 , -1.88547 , -2.06614 , -2.06519 ,
       -1.68099 , -1.56884 , -1.57688 , -1.57673 , -1.58475 , -1.5849  ,
       -1.59105 , -1.59091 , -1.59561 , -1.59556 , -1.59478 , -1.59026 ,
       -1.58087 , -1.56767 , -1.54624 , -1.52875 , -1.51517 , -1.49624 ,
       -1.47724 , -1.44582 , -1.41923 , -1.38728 , -1.35284 , -1.3221  ,
       -1.30018 , -1.0138  , -0.8423  , -0.8202  , -0.8202  , -0.25    ,
       -0.25    ,  0.25    ,  0.25    ,  0.8156  ,  0.8156  ,  0.8377  ,
        1.0092  ,  1.29558 ,  1.3175  ,  1.34824 ,  1.38268 ,  1.41463 ,
        1.44122 ,  1.47264 ,  1.49164 ,  1.51057 ,  1.52415 ,  1.54164 ,
        1.56307 ,  1.57627 ,  1.58566 ,  1.59018 ,  1.59096 ,  1.59101 ,
        1.58631 ,  1.58645 ,  1.5803  ,  1.58015 ,  1.57213 ,  1.57228 ,
        1.56424 ]
    
    return Machine(coils, Wall(rwall, zwall))
