"""Check if a host is in the Google Chrome HSTS Preload list"""

import functools
import os
import typing

__version__ = "2020.7.7"
__checksum__ = "fc45e7705b4e32e069173fcca812eda1a1f548eb524f713683e0c4135dcfec45"
__all__ = ["in_hsts_preload"]

# fmt: off
_GTLD_INCLUDE_SUBDOMAINS = {b'android', b'app', b'bank', b'chrome', b'dev', b'foo', b'gle', b'gmail', b'google', b'hangout', b'insurance', b'meet', b'new', b'page', b'play', b'search', b'youtube'}  # noqa: E501
_JUMPTABLE = [[(0, 11), (11, 5), None, (16, 57), (73, 26), (99, 12), None, (111, 19), (130, 11), (141, 7), (148, 20), (168, 18), None, (186, 22), (208, 45), (253, 7), (260, 9), (269, 36), (305, 10), (315, 10), (325, 21), None, (346, 50), (396, 8), (404, 9), (413, 19), (432, 13), (445, 14), (459, 14), None, None, (473, 29), (502, 16), (518, 35), (553, 14), (567, 24), (591, 9), None, (600, 25), (625, 20), (645, 8), (653, 13), (666, 10), None, (676, 11), (687, 6), (693, 26), (719, 5), (724, 5), (729, 10), (739, 10), (749, 11), (760, 12), (772, 27), None, (799, 11), (810, 11), (821, 7), (828, 29), (857, 18), (875, 27), (902, 46), (948, 25), (973, 16), (989, 8), (997, 5), (1002, 22), (1024, 18), None, (1042, 36), (1078, 15), (1093, 8), (1101, 5), None, (1106, 5), (1111, 16), (1127, 14), (1141, 18), None, (1159, 14), (1173, 18), (1191, 48), (1239, 19), (1258, 5), (1263, 46), (1309, 14), (1323, 14), (1337, 20), None, (1357, 10), (1367, 13), (1380, 10), (1390, 19), None, (1409, 13), (1422, 19), (1441, 5), (1446, 4), (1450, 22), (1472, 10), (1482, 7), (1489, 14), (1503, 21), (1524, 11), (1535, 10), (1545, 12), (1557, 32), None, (1589, 10), (1599, 14), (1613, 12), (1625, 45), (1670, 15), None, (1685, 11), (1696, 23), (1719, 21), (1740, 26), (1766, 6), (1772, 6), (1778, 7), (1785, 5), (1790, 20), (1810, 23), (1833, 24), (1857, 13), (1870, 15), (1885, 19), (1904, 6), (1910, 61), (1971, 44), (2015, 12), (2027, 23), (2050, 16), (2066, 38), (2104, 6), (2110, 12), (2122, 44), (2166, 6), (2172, 41), (2213, 13), (2226, 23), (2249, 30), (2279, 16), (2295, 8), (2303, 6), (2309, 12), (2321, 19), (2340, 21), (2361, 15), None, (2376, 35), (2411, 21), (2432, 17), (2449, 19), (2468, 26), (2494, 5), (2499, 37), (2536, 30), (2566, 16), (2582, 10), (2592, 17), (2609, 23), (2632, 14), (2646, 17), (2663, 8), (2671, 4), (2675, 7), (2682, 29), (2711, 6), (2717, 18), (2735, 27), (2762, 20), (2782, 17), (2799, 19), (2818, 12), (2830, 40), (2870, 40), (2910, 12), (2922, 48), (2970, 25), (2995, 12), None, (3007, 8), (3015, 20), (3035, 19), (3054, 6), (3060, 23), None, (3083, 23), (3106, 33), (3139, 14), (3153, 12), (3165, 27), None, (3192, 26), (3218, 31), (3249, 50), (3299, 15), (3314, 20), (3334, 15), (3349, 21), (3370, 32), (3402, 24), (3426, 20), (3446, 13), (3459, 60), (3519, 19), (3538, 9), (3547, 12), (3559, 12), (3571, 11), (3582, 10), (3592, 48), (3640, 32), None, (3672, 25), (3697, 12), None, (3709, 8), (3717, 8), (3725, 7), None, (3732, 25), (3757, 17), None, (3774, 21), (3795, 35), (3830, 12), (3842, 10), (3852, 36), (3888, 20), (3908, 22), (3930, 23), (3953, 19), (3972, 12), (3984, 5), (3989, 30), (4019, 24), (4043, 14), (4057, 14), (4071, 47), (4118, 46), None, None, (4164, 51), (4215, 42), None, (4257, 14), None, (4271, 15), (4286, 8), (4294, 21), (4315, 6), (4321, 16), (4337, 17)], [(4354, 6035), (10389, 6501), (16890, 6896), (23786, 5698), (29484, 6144), (35628, 5771), (41399, 6738), (48137, 5956), (54093, 6577), (60670, 5921), (66591, 6903), (73494, 6166), (79660, 6567), (86227, 6923), (93150, 6427), (99577, 6324), (105901, 6902), (112803, 5854), (118657, 6104), (124761, 6437), (131198, 6731), (137929, 6423), (144352, 6680), (151032, 5936), (156968, 6058), (163026, 6495), (169521, 6431), (175952, 6717), (182669, 6171), (188840, 6336), (195176, 6628), (201804, 6354), (208158, 6254), (214412, 6868), (221280, 5961), (227241, 6721), (233962, 6097), (240059, 6819), (246878, 6569), (253447, 6846), (260293, 7237), (267530, 6201), (273731, 6178), (279909, 5990), (285899, 6161), (292060, 5853), (297913, 6108), (304021, 6791), (310812, 6189), (317001, 5614), (322615, 6316), (328931, 6444), (335375, 6397), (341772, 6565), (348337, 6630), (354967, 6626), (361593, 6640), (368233, 5690), (373923, 6636), (380559, 5638), (386197, 6413), (392610, 6249), (398859, 6198), (405057, 6627), (411684, 6474), (418158, 6428), (424586, 5885), (430471, 6770), (437241, 6539), (443780, 6662), (450442, 6239), (456681, 6293), (462974, 5548), (468522, 6854), (475376, 6843), (482219, 6712), (488931, 5977), (494908, 7043), (501951, 6914), (508865, 5941), (514806, 6520), (521326, 5609), (526935, 6172), (533107, 6387), (539494, 6317), (545811, 6320), (552131, 6459), (558590, 6480), (565070, 6533), (571603, 6248), (577851, 7064), (584915, 5907), (590822, 6046), (596868, 6410), (603278, 6365), (609643, 6860), (616503, 6687), (623190, 6241), (629431, 6146), (635577, 6013), (641590, 6100), (647690, 6637), (654327, 6103), (660430, 6319), (666749, 5971), (672720, 6653), (679373, 6359), (685732, 6754), (692486, 7838), (700324, 6911), (707235, 6738), (713973, 6257), (720230, 6092), (726322, 6520), (732842, 6785), (739627, 6338), (745965, 6072), (752037, 6293), (758330, 6262), (764592, 6733), (771325, 6638), (777963, 6561), (784524, 6989), (791513, 6634), (798147, 7688), (805835, 6265), (812100, 5622), (817722, 6765), (824487, 6515), (831002, 7798), (838800, 6746), (845546, 6041), (851587, 6567), (858154, 6695), (864849, 6188), (871037, 6589), (877626, 5820), (883446, 6616), (890062, 6251), (896313, 6366), (902679, 6310), (908989, 7022), (916011, 6091), (922102, 6142), (928244, 6418), (934662, 6318), (940980, 6270), (947250, 6717), (953967, 5987), (959954, 6860), (966814, 6444), (973258, 6558), (979816, 6586), (986402, 6358), (992760, 6334), (999094, 6281), (1005375, 6254), (1011629, 6212), (1017841, 6016), (1023857, 5607), (1029464, 5926), (1035390, 6422), (1041812, 7081), (1048893, 5974), (1054867, 6376), (1061243, 6810), (1068053, 6200), (1074253, 5979), (1080232, 6617), (1086849, 6326), (1093175, 5750), (1098925, 6367), (1105292, 7425), (1112717, 5867), (1118584, 6056), (1124640, 6508), (1131148, 6100), (1137248, 6531), (1143779, 6176), (1149955, 5875), (1155830, 7132), (1162962, 6570), (1169532, 6260), (1175792, 6674), (1182466, 7052), (1189518, 7162), (1196680, 6060), (1202740, 6839), (1209579, 6119), (1215698, 6469), (1222167, 6585), (1228752, 5993), (1234745, 6663), (1241408, 6742), (1248150, 6410), (1254560, 6306), (1260866, 6163), (1267029, 6255), (1273284, 6619), (1279903, 5977), (1285880, 6451), (1292331, 5759), (1298090, 6913), (1305003, 6791), (1311794, 6507), (1318301, 6720), (1325021, 5583), (1330604, 6538), (1337142, 6341), (1343483, 6469), (1349952, 6631), (1356583, 6890), (1363473, 6342), (1369815, 6505), (1376320, 6593), (1382913, 6307), (1389220, 6269), (1395489, 6371), (1401860, 6434), (1408294, 6111), (1414405, 6300), (1420705, 5864), (1426569, 7240), (1433809, 6486), (1440295, 6160), (1446455, 6599), (1453054, 6480), (1459534, 5656), (1465190, 6437), (1471627, 6369), (1477996, 7452), (1485448, 6281), (1491729, 5703), (1497432, 6866), (1504298, 6245), (1510543, 6812), (1517355, 5974), (1523329, 6069), (1529398, 5760), (1535158, 6559), (1541717, 6268), (1547985, 6720), (1554705, 6069), (1560774, 6446), (1567220, 6244), (1573464, 6883), (1580347, 6267), (1586614, 5645), (1592259, 6404), (1598663, 6087), (1604750, 6453), (1611203, 6645), (1617848, 7032), (1624880, 6131), (1631011, 6135), (1637146, 6548)], [(1643694, 703), (1644397, 605), (1645002, 628), (1645630, 663), (1646293, 523), (1646816, 611), (1647427, 665), (1648092, 808), (1648900, 652), (1649552, 627), (1650179, 509), (1650688, 532), (1651220, 758), (1651978, 909), (1652887, 936), (1653823, 714), (1654537, 1188), (1655725, 589), (1656314, 829), (1657143, 640), (1657783, 733), (1658516, 688), (1659204, 802), (1660006, 709), (1660715, 684), (1661399, 631), (1662030, 940), (1662970, 1033), (1664003, 794), (1664797, 657), (1665454, 915), (1666369, 758), (1667127, 557), (1667684, 671), (1668355, 712), (1669067, 761), (1669828, 619), (1670447, 677), (1671124, 692), (1671816, 929), (1672745, 683), (1673428, 823), (1674251, 660), (1674911, 671), (1675582, 710), (1676292, 362), (1676654, 763), (1677417, 857), (1678274, 673), (1678947, 525), (1679472, 789), (1680261, 633), (1680894, 763), (1681657, 935), (1682592, 918), (1683510, 464), (1683974, 661), (1684635, 486), (1685121, 578), (1685699, 662), (1686361, 716), (1687077, 753), (1687830, 1008), (1688838, 813), (1689651, 602), (1690253, 692), (1690945, 753), (1691698, 444), (1692142, 540), (1692682, 487), (1693169, 692), (1693861, 789), (1694650, 521), (1695171, 725), (1695896, 634), (1696530, 671), (1697201, 552), (1697753, 680), (1698433, 752), (1699185, 428), (1699613, 672), (1700285, 607), (1700892, 828), (1701720, 623), (1702343, 588), (1702931, 282), (1703213, 597), (1703810, 703), (1704513, 756), (1705269, 647), (1705916, 816), (1706732, 1119), (1707851, 788), (1708639, 744), (1709383, 674), (1710057, 436), (1710493, 911), (1711404, 858), (1712262, 564), (1712826, 580), (1713406, 666), (1714072, 843), (1714915, 839), (1715754, 541), (1716295, 632), (1716927, 653), (1717580, 363), (1717943, 467), (1718410, 924), (1719334, 839), (1720173, 792), (1720965, 737), (1721702, 584), (1722286, 749), (1723035, 643), (1723678, 683), (1724361, 689), (1725050, 448), (1725498, 639), (1726137, 588), (1726725, 914), (1727639, 668), (1728307, 789), (1729096, 404), (1729500, 703), (1730203, 656), (1730859, 835), (1731694, 883), (1732577, 761), (1733338, 904), (1734242, 747), (1734989, 502), (1735491, 757), (1736248, 583), (1736831, 737), (1737568, 715), (1738283, 624), (1738907, 682), (1739589, 589), (1740178, 613), (1740791, 594), (1741385, 691), (1742076, 671), (1742747, 657), (1743404, 417), (1743821, 549), (1744370, 641), (1745011, 556), (1745567, 683), (1746250, 594), (1746844, 761), (1747605, 520), (1748125, 490), (1748615, 656), (1749271, 551), (1749822, 607), (1750429, 639), (1751068, 796), (1751864, 594), (1752458, 609), (1753067, 841), (1753908, 826), (1754734, 522), (1755256, 695), (1755951, 796), (1756747, 607), (1757354, 659), (1758013, 480), (1758493, 580), (1759073, 621), (1759694, 714), (1760408, 578), (1760986, 898), (1761884, 676), (1762560, 811), (1763371, 683), (1764054, 636), (1764690, 518), (1765208, 629), (1765837, 699), (1766536, 1277), (1767813, 514), (1768327, 641), (1768968, 608), (1769576, 944), (1770520, 730), (1771250, 729), (1771979, 546), (1772525, 565), (1773090, 808), (1773898, 553), (1774451, 569), (1775020, 826), (1775846, 650), (1776496, 856), (1777352, 772), (1778124, 668), (1778792, 671), (1779463, 783), (1780246, 620), (1780866, 889), (1781755, 631), (1782386, 722), (1783108, 558), (1783666, 689), (1784355, 449), (1784804, 753), (1785557, 761), (1786318, 648), (1786966, 901), (1787867, 775), (1788642, 759), (1789401, 903), (1790304, 1055), (1791359, 815), (1792174, 586), (1792760, 839), (1793599, 662), (1794261, 483), (1794744, 443), (1795187, 692), (1795879, 774), (1796653, 406), (1797059, 974), (1798033, 462), (1798495, 741), (1799236, 844), (1800080, 712), (1800792, 769), (1801561, 626), (1802187, 743), (1802930, 665), (1803595, 705), (1804300, 546), (1804846, 566), (1805412, 425), (1805837, 586), (1806423, 437), (1806860, 740), (1807600, 815), (1808415, 740), (1809155, 715), (1809870, 621), (1810491, 568), (1811059, 808), (1811867, 406), (1812273, 518), (1812791, 752), (1813543, 513), (1814056, 839), (1814895, 2071), (1816966, 507), (1817473, 602), (1818075, 875), (1818950, 817), (1819767, 510)], [(1820277, 48), None, (1820325, 35), (1820360, 42), None, None, None, None, None, None, None, None, None, None, None, None, None, (1820402, 42), None, (1820444, 25), (1820469, 16), None, None, None, None, None, None, (1820485, 26), None, None, None, None, (1820511, 21), (1820532, 25), None, None, (1820557, 26), None, None, None, None, (1820583, 44), (1820627, 21), (1820648, 23), None, None, None, None, (1820671, 48), None, None, None, None, None, (1820719, 31), None, None, None, None, (1820750, 42), None, (1820792, 22), None, (1820814, 21), None, (1820835, 26), (1820861, 42), None, None, (1820903, 77), None, None, None, None, None, (1820980, 21), (1821001, 21), None, None, (1821022, 34), (1821056, 42), None, None, None, (1821098, 25), None, None, (1821123, 21), None, None, None, None, None, (1821144, 24), (1821168, 21), None, None, (1821189, 26), None, (1821215, 18), None, (1821233, 54), None, None, None, None, None, None, (1821287, 26), None, (1821313, 19), None, (1821332, 20), None, None, (1821352, 42), (1821394, 42), (1821436, 17), None, (1821453, 26), None, (1821479, 26), None, None, None, (1821505, 26), (1821531, 20), (1821551, 26), None, (1821577, 42), (1821619, 63), None, None, None, (1821682, 40), (1821722, 48), None, None, None, (1821770, 47), None, None, None, None, None, None, None, (1821817, 42), None, (1821859, 55), None, (1821914, 9), None, (1821923, 21), (1821944, 42), None, None, (1821986, 42), (1822028, 82), None, None, (1822110, 42), None, None, None, None, None, None, None, None, None, (1822152, 42), (1822194, 21), (1822215, 21), None, (1822236, 42), (1822278, 25), None, None, (1822303, 21), (1822324, 42), None, None, (1822366, 21), (1822387, 19), (1822406, 26), None, None, None, (1822432, 21), None, None, (1822453, 38), None, (1822491, 22), (1822513, 21), (1822534, 21), None, None, (1822555, 63), None, (1822618, 21), (1822639, 42), None, (1822681, 17), None, None, None, None, (1822698, 21), (1822719, 21), None, None, (1822740, 21), None, None, (1822761, 21), None, (1822782, 26), None, (1822808, 50), None, None, None, (1822858, 50), (1822908, 26), (1822934, 21), (1822955, 21), (1822976, 19), None, (1822995, 35), (1823030, 26), (1823056, 23), (1823079, 21), (1823100, 42), None, None, None, None, None, None, (1823142, 21), None, None, None, (1823163, 21), None, None, (1823184, 90), None, (1823274, 239), (1823513, 38), None, None, None, None]]  # noqa: E501
_CRC8_TABLE = [
    0x00, 0x07, 0x0e, 0x09, 0x1c, 0x1b, 0x12, 0x15,
    0x38, 0x3f, 0x36, 0x31, 0x24, 0x23, 0x2a, 0x2d,
    0x70, 0x77, 0x7e, 0x79, 0x6c, 0x6b, 0x62, 0x65,
    0x48, 0x4f, 0x46, 0x41, 0x54, 0x53, 0x5a, 0x5d,
    0xe0, 0xe7, 0xee, 0xe9, 0xfc, 0xfb, 0xf2, 0xf5,
    0xd8, 0xdf, 0xd6, 0xd1, 0xc4, 0xc3, 0xca, 0xcd,
    0x90, 0x97, 0x9e, 0x99, 0x8c, 0x8b, 0x82, 0x85,
    0xa8, 0xaf, 0xa6, 0xa1, 0xb4, 0xb3, 0xba, 0xbd,
    0xc7, 0xc0, 0xc9, 0xce, 0xdb, 0xdc, 0xd5, 0xd2,
    0xff, 0xf8, 0xf1, 0xf6, 0xe3, 0xe4, 0xed, 0xea,
    0xb7, 0xb0, 0xb9, 0xbe, 0xab, 0xac, 0xa5, 0xa2,
    0x8f, 0x88, 0x81, 0x86, 0x93, 0x94, 0x9d, 0x9a,
    0x27, 0x20, 0x29, 0x2e, 0x3b, 0x3c, 0x35, 0x32,
    0x1f, 0x18, 0x11, 0x16, 0x03, 0x04, 0x0d, 0x0a,
    0x57, 0x50, 0x59, 0x5e, 0x4b, 0x4c, 0x45, 0x42,
    0x6f, 0x68, 0x61, 0x66, 0x73, 0x74, 0x7d, 0x7a,
    0x89, 0x8e, 0x87, 0x80, 0x95, 0x92, 0x9b, 0x9c,
    0xb1, 0xb6, 0xbf, 0xb8, 0xad, 0xaa, 0xa3, 0xa4,
    0xf9, 0xfe, 0xf7, 0xf0, 0xe5, 0xe2, 0xeb, 0xec,
    0xc1, 0xc6, 0xcf, 0xc8, 0xdd, 0xda, 0xd3, 0xd4,
    0x69, 0x6e, 0x67, 0x60, 0x75, 0x72, 0x7b, 0x7c,
    0x51, 0x56, 0x5f, 0x58, 0x4d, 0x4a, 0x43, 0x44,
    0x19, 0x1e, 0x17, 0x10, 0x05, 0x02, 0x0b, 0x0c,
    0x21, 0x26, 0x2f, 0x28, 0x3d, 0x3a, 0x33, 0x34,
    0x4e, 0x49, 0x40, 0x47, 0x52, 0x55, 0x5c, 0x5b,
    0x76, 0x71, 0x78, 0x7f, 0x6a, 0x6d, 0x64, 0x63,
    0x3e, 0x39, 0x30, 0x37, 0x22, 0x25, 0x2c, 0x2b,
    0x06, 0x01, 0x08, 0x0f, 0x1a, 0x1d, 0x14, 0x13,
    0xae, 0xa9, 0xa0, 0xa7, 0xb2, 0xb5, 0xbc, 0xbb,
    0x96, 0x91, 0x98, 0x9f, 0x8a, 0x8d, 0x84, 0x83,
    0xde, 0xd9, 0xd0, 0xd7, 0xc2, 0xc5, 0xcc, 0xcb,
    0xe6, 0xe1, 0xe8, 0xef, 0xfa, 0xfd, 0xf4, 0xf3
]
# fmt: on

_IS_LEAF = 0x80
_INCLUDE_SUBDOMAINS = 0x40


try:
    from importlib.resources import open_binary

    def open_pkg_binary(path: str) -> typing.BinaryIO:
        return open_binary("hstspreload", path)


except ImportError:

    def open_pkg_binary(path: str) -> typing.BinaryIO:
        return open(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), path), "rb",
        )


@functools.lru_cache(maxsize=1024)
def in_hsts_preload(host: typing.AnyStr) -> bool:
    """Determines if an IDNA-encoded host is on the HSTS preload list"""

    if isinstance(host, str):
        host = host.encode("ascii")
    labels = host.lower().split(b".")

    # Fast-branch for gTLDs that are registered to preload all sub-domains.
    if labels[-1] in _GTLD_INCLUDE_SUBDOMAINS:
        return True

    with open_pkg_binary("hstspreload.bin") as f:
        for layer, label in enumerate(labels[::-1]):
            # None of our layers are greater than 4 deep.
            if layer > 3:
                return False

            # Read the jump table for the layer and label
            jump_info = _JUMPTABLE[layer][_crc8(label)]
            if jump_info is None:
                # No entry: host is not preloaded
                return False

            # Read the set of entries for that layer and label
            f.seek(jump_info[0])
            data = bytearray(jump_info[1])
            f.readinto(data)

            for is_leaf, include_subdomains, ent_label in _iter_entries(data):
                # We found a potential leaf
                if is_leaf:
                    if ent_label == host:
                        return True
                    if include_subdomains and host.endswith(b"." + ent_label):
                        return True

                # Continue traversing as we're not at a leaf.
                elif label == ent_label:
                    break
            else:
                return False
    return False


def _iter_entries(data: bytes) -> typing.Iterable[typing.Tuple[int, int, bytes]]:
    while data:
        flags = data[0]
        size = data[1]
        label = bytes(data[2 : 2 + size])
        yield (flags & _IS_LEAF, flags & _INCLUDE_SUBDOMAINS, label)
        data = data[2 + size :]


def _crc8(value: bytes) -> int:
    # CRC8 reference implementation: https://github.com/niccokunzmann/crc8
    checksum = 0x00
    for byte in value:
        checksum = _CRC8_TABLE[checksum ^ byte]
    return checksum