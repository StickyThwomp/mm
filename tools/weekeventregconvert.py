#!/usr/bin/env python3

import argparse
import re

weekEventReg = {
    ( 0 << 8) | 0x01: "WEEKEVENTREG_00_01",
    ( 0 << 8) | 0x02: "WEEKEVENTREG_ENTERED_TERMINA_FIELD",
    ( 0 << 8) | 0x04: "WEEKEVENTREG_ENTERED_IKANA_GRAVEYARD",
    ( 0 << 8) | 0x08: "WEEKEVENTREG_ENTERED_ROMANI_RANCH",
    ( 0 << 8) | 0x10: "WEEKEVENTREG_ENTERED_GORMAN_TRACK",
    ( 0 << 8) | 0x20: "WEEKEVENTREG_ENTERED_MOUNTAIN_VILLAGE_WINTER",
    ( 0 << 8) | 0x40: "WEEKEVENTREG_ENTERED_GORON_SHRINE",
    ( 0 << 8) | 0x80: "WEEKEVENTREG_ENTERED_SNOWHEAD",
    ( 1 << 8) | 0x01: "WEEKEVENTREG_ENTERED_SOUTHERN_SWAMP_POISONED",
    ( 1 << 8) | 0x02: "WEEKEVENTREG_ENTERED_WOODFALL",
    ( 1 << 8) | 0x04: "WEEKEVENTREG_ENTERED_DEKU_PALACE",
    ( 1 << 8) | 0x08: "WEEKEVENTREG_ENTERED_GREAT_BAY_COAST",
    ( 1 << 8) | 0x10: "WEEKEVENTREG_ENTERED_PIRATES_FORTRESS",
    ( 1 << 8) | 0x20: "WEEKEVENTREG_ENTERED_ZORA_HALL",
    ( 1 << 8) | 0x40: "WEEKEVENTREG_ENTERED_WATERFALL_RAPIDS",
    ( 1 << 8) | 0x80: "WEEKEVENTREG_ENTERED_IKANA_CANYON",
    ( 2 << 8) | 0x01: "WEEKEVENTREG_ENTERED_IKANA_CASTLE",
    ( 2 << 8) | 0x02: "WEEKEVENTREG_ENTERED_STONE_TOWER",
    ( 2 << 8) | 0x04: "WEEKEVENTREG_ENTERED_STONE_TOWER_INVERTED",
    ( 2 << 8) | 0x08: "WEEKEVENTREG_ENTERED_EAST_CLOCK_TOWN",
    ( 2 << 8) | 0x10: "WEEKEVENTREG_ENTERED_WEST_CLOCK_TOWN",
    ( 2 << 8) | 0x20: "WEEKEVENTREG_ENTERED_NORTH_CLOCK_TOWN",
    ( 2 << 8) | 0x40: "WEEKEVENTREG_ENTERED_WOODFALL_TEMPLE",
    ( 2 << 8) | 0x80: "WEEKEVENTREG_ENTERED_SNOWHEAD_TEMPLE",
    ( 3 << 8) | 0x01: "WEEKEVENTREG_ENTERED_PIRATES_FORTRESS_EXTERIOR",
    ( 3 << 8) | 0x02: "WEEKEVENTREG_ENTERED_STONE_TOWER_TEMPLE",
    ( 3 << 8) | 0x04: "WEEKEVENTREG_ENTERED_STONE_TOWER_TEMPLE_INVERTED",
    ( 3 << 8) | 0x08: "WEEKEVENTREG_ENTERED_THE_MOON",
    ( 3 << 8) | 0x10: "WEEKEVENTREG_ENTERED_MOON_DEKU_TRIAL",
    ( 3 << 8) | 0x20: "WEEKEVENTREG_ENTERED_MOON_GORON_TRIAL",
    ( 3 << 8) | 0x40: "WEEKEVENTREG_ENTERED_MOON_ZORA_TRIAL",
    ( 3 << 8) | 0x80: "WEEKEVENTREG_03_80",
    ( 4 << 8) | 0x01: "WEEKEVENTREG_04_01",
    ( 4 << 8) | 0x02: "WEEKEVENTREG_04_02",
    ( 4 << 8) | 0x04: "WEEKEVENTREG_04_04",
    ( 4 << 8) | 0x08: "WEEKEVENTREG_04_08",
    ( 4 << 8) | 0x10: "WEEKEVENTREG_04_10",
    ( 4 << 8) | 0x20: "WEEKEVENTREG_04_20",
    ( 4 << 8) | 0x40: "WEEKEVENTREG_04_40",
    ( 4 << 8) | 0x80: "WEEKEVENTREG_04_80",
    ( 5 << 8) | 0x01: "WEEKEVENTREG_05_01",
    ( 5 << 8) | 0x02: "WEEKEVENTREG_05_02",
    ( 5 << 8) | 0x04: "WEEKEVENTREG_05_04",
    ( 5 << 8) | 0x08: "WEEKEVENTREG_05_08",
    ( 5 << 8) | 0x10: "WEEKEVENTREG_05_10",
    ( 5 << 8) | 0x20: "WEEKEVENTREG_05_20",
    ( 5 << 8) | 0x40: "WEEKEVENTREG_05_40",
    ( 5 << 8) | 0x80: "WEEKEVENTREG_05_80",
    ( 6 << 8) | 0x01: "WEEKEVENTREG_06_01",
    ( 6 << 8) | 0x02: "WEEKEVENTREG_06_02",
    ( 6 << 8) | 0x04: "WEEKEVENTREG_06_04",
    ( 6 << 8) | 0x08: "WEEKEVENTREG_06_08",
    ( 6 << 8) | 0x10: "WEEKEVENTREG_06_10",
    ( 6 << 8) | 0x20: "WEEKEVENTREG_06_20",
    ( 6 << 8) | 0x40: "WEEKEVENTREG_06_40",
    ( 6 << 8) | 0x80: "WEEKEVENTREG_06_80",
    ( 7 << 8) | 0x01: "WEEKEVENTREG_07_01",
    ( 7 << 8) | 0x02: "WEEKEVENTREG_07_02",
    ( 7 << 8) | 0x04: "WEEKEVENTREG_07_04",
    ( 7 << 8) | 0x08: "WEEKEVENTREG_07_08",
    ( 7 << 8) | 0x10: "WEEKEVENTREG_07_10",
    ( 7 << 8) | 0x20: "WEEKEVENTREG_07_20",
    ( 7 << 8) | 0x40: "WEEKEVENTREG_07_40",
    ( 7 << 8) | 0x80: "WEEKEVENTREG_ENTERED_WOODFALL_TEMPLE_PRISON",
    ( 8 << 8) | 0x01: "WEEKEVENTREG_08_01",
    ( 8 << 8) | 0x02: "WEEKEVENTREG_08_02",
    ( 8 << 8) | 0x04: "WEEKEVENTREG_08_04",
    ( 8 << 8) | 0x08: "WEEKEVENTREG_08_08",
    ( 8 << 8) | 0x10: "WEEKEVENTREG_08_10",
    ( 8 << 8) | 0x20: "WEEKEVENTREG_RECEIVED_DOGGY_RACETRACK_HEART_PIECE",
    ( 8 << 8) | 0x40: "WEEKEVENTREG_08_40",
    ( 8 << 8) | 0x80: "WEEKEVENTREG_08_80",
    ( 9 << 8) | 0x01: "WEEKEVENTREG_09_01",
    ( 9 << 8) | 0x02: "WEEKEVENTREG_09_02",
    ( 9 << 8) | 0x04: "WEEKEVENTREG_09_04",
    ( 9 << 8) | 0x08: "WEEKEVENTREG_09_08",
    ( 9 << 8) | 0x10: "WEEKEVENTREG_09_10",
    ( 9 << 8) | 0x20: "WEEKEVENTREG_09_20",
    ( 9 << 8) | 0x40: "WEEKEVENTREG_09_40",
    ( 9 << 8) | 0x80: "WEEKEVENTREG_09_80",
    (10 << 8) | 0x01: "WEEKEVENTREG_10_01",
    (10 << 8) | 0x02: "WEEKEVENTREG_10_02",
    (10 << 8) | 0x04: "WEEKEVENTREG_10_04",
    (10 << 8) | 0x08: "WEEKEVENTREG_10_08",
    (10 << 8) | 0x10: "WEEKEVENTREG_10_10",
    (10 << 8) | 0x20: "WEEKEVENTREG_10_20",
    (10 << 8) | 0x40: "WEEKEVENTREG_10_40",
    (10 << 8) | 0x80: "WEEKEVENTREG_10_80",
    (11 << 8) | 0x01: "WEEKEVENTREG_11_01",
    (11 << 8) | 0x02: "WEEKEVENTREG_11_02",
    (11 << 8) | 0x04: "WEEKEVENTREG_11_04",
    (11 << 8) | 0x08: "WEEKEVENTREG_11_08",
    (11 << 8) | 0x10: "WEEKEVENTREG_11_10",
    (11 << 8) | 0x20: "WEEKEVENTREG_11_20",
    (11 << 8) | 0x40: "WEEKEVENTREG_11_40",
    (11 << 8) | 0x80: "WEEKEVENTREG_11_80",
    (12 << 8) | 0x01: "WEEKEVENTREG_12_01",
    (12 << 8) | 0x02: "WEEKEVENTREG_12_02",
    (12 << 8) | 0x04: "WEEKEVENTREG_12_04",
    (12 << 8) | 0x08: "WEEKEVENTREG_12_08",
    (12 << 8) | 0x10: "WEEKEVENTREG_12_10",
    (12 << 8) | 0x20: "WEEKEVENTREG_12_20",
    (12 << 8) | 0x40: "WEEKEVENTREG_12_40",
    (12 << 8) | 0x80: "WEEKEVENTREG_12_80",
    (13 << 8) | 0x01: "WEEKEVENTREG_13_01",
    (13 << 8) | 0x02: "WEEKEVENTREG_13_02",
    (13 << 8) | 0x04: "WEEKEVENTREG_13_04",
    (13 << 8) | 0x08: "WEEKEVENTREG_13_08",
    (13 << 8) | 0x10: "WEEKEVENTREG_13_10",
    (13 << 8) | 0x20: "WEEKEVENTREG_OCEANSIDE_SPIDER_HOUSE_BUYER_MOVED_IN",
    (13 << 8) | 0x40: "WEEKEVENTREG_RECEIVED_OCEANSIDE_WALLET_UPGRADE",
    (13 << 8) | 0x80: "WEEKEVENTREG_OCEANSIDE_SPIDER_HOUSE_COLLECTED_REWARD",
    (14 << 8) | 0x01: "WEEKEVENTREG_14_01",
    (14 << 8) | 0x02: "WEEKEVENTREG_14_02",
    (14 << 8) | 0x04: "WEEKEVENTREG_14_04",
    (14 << 8) | 0x08: "WEEKEVENTREG_DRANK_CHATEAU_ROMANI",
    (14 << 8) | 0x10: "WEEKEVENTREG_14_10",
    (14 << 8) | 0x20: "WEEKEVENTREG_14_20",
    (14 << 8) | 0x40: "WEEKEVENTREG_14_40",
    (14 << 8) | 0x80: "WEEKEVENTREG_14_80",
    (15 << 8) | 0x01: "WEEKEVENTREG_15_01",
    (15 << 8) | 0x02: "WEEKEVENTREG_15_02",
    (15 << 8) | 0x04: "WEEKEVENTREG_15_04",
    (15 << 8) | 0x08: "WEEKEVENTREG_15_08",
    (15 << 8) | 0x10: "WEEKEVENTREG_15_10",
    (15 << 8) | 0x20: "WEEKEVENTREG_15_20",
    (15 << 8) | 0x40: "WEEKEVENTREG_15_40",
    (15 << 8) | 0x80: "WEEKEVENTREG_15_80",
    (16 << 8) | 0x01: "WEEKEVENTREG_16_01",
    (16 << 8) | 0x02: "WEEKEVENTREG_16_02",
    (16 << 8) | 0x04: "WEEKEVENTREG_16_04",
    (16 << 8) | 0x08: "WEEKEVENTREG_16_08",
    (16 << 8) | 0x10: "WEEKEVENTREG_16_10",
    (16 << 8) | 0x20: "WEEKEVENTREG_16_20",
    (16 << 8) | 0x40: "WEEKEVENTREG_16_40",
    (16 << 8) | 0x80: "WEEKEVENTREG_16_80",
    (17 << 8) | 0x01: "WEEKEVENTREG_17_01",
    (17 << 8) | 0x02: "WEEKEVENTREG_17_02",
    (17 << 8) | 0x04: "WEEKEVENTREG_17_04",
    (17 << 8) | 0x08: "WEEKEVENTREG_17_08",
    (17 << 8) | 0x10: "WEEKEVENTREG_17_10",
    (17 << 8) | 0x20: "WEEKEVENTREG_17_20",
    (17 << 8) | 0x40: "WEEKEVENTREG_17_40",
    (17 << 8) | 0x80: "WEEKEVENTREG_17_80",
    (18 << 8) | 0x01: "WEEKEVENTREG_18_01",
    (18 << 8) | 0x02: "WEEKEVENTREG_18_02",
    (18 << 8) | 0x04: "WEEKEVENTREG_18_04",
    (18 << 8) | 0x08: "WEEKEVENTREG_18_08",
    (18 << 8) | 0x10: "WEEKEVENTREG_18_10",
    (18 << 8) | 0x20: "WEEKEVENTREG_18_20",
    (18 << 8) | 0x40: "WEEKEVENTREG_18_40",
    (18 << 8) | 0x80: "WEEKEVENTREG_HAS_POWERDERKEG_PRIVILEGES",
    (19 << 8) | 0x01: "WEEKEVENTREG_19_01",
    (19 << 8) | 0x02: "WEEKEVENTREG_19_02",
    (19 << 8) | 0x04: "WEEKEVENTREG_19_04",
    (19 << 8) | 0x08: "WEEKEVENTREG_19_08",
    (19 << 8) | 0x10: "WEEKEVENTREG_19_10",
    (19 << 8) | 0x20: "WEEKEVENTREG_19_20",
    (19 << 8) | 0x40: "WEEKEVENTREG_19_40",
    (19 << 8) | 0x80: "WEEKEVENTREG_19_80",
    (20 << 8) | 0x01: "WEEKEVENTREG_20_01",
    (20 << 8) | 0x02: "WEEKEVENTREG_CLEARED_WOODFALL_TEMPLE",
    (20 << 8) | 0x04: "WEEKEVENTREG_20_04",
    (20 << 8) | 0x08: "WEEKEVENTREG_20_08",
    (20 << 8) | 0x10: "WEEKEVENTREG_20_10",
    (20 << 8) | 0x20: "WEEKEVENTREG_20_20",
    (20 << 8) | 0x40: "WEEKEVENTREG_20_40",
    (20 << 8) | 0x80: "WEEKEVENTREG_20_80",
    (21 << 8) | 0x01: "WEEKEVENTREG_21_01",
    (21 << 8) | 0x02: "WEEKEVENTREG_21_02",
    (21 << 8) | 0x04: "WEEKEVENTREG_TALKED_TO_GORON_GRAVEMAKER_AS_GORON",
    (21 << 8) | 0x08: "WEEKEVENTREG_THAWED_GRAVEYARD_GORON",
    (21 << 8) | 0x10: "WEEKEVENTREG_21_10",
    (21 << 8) | 0x20: "WEEKEVENTREG_21_20",
    (21 << 8) | 0x40: "WEEKEVENTREG_21_40",
    (21 << 8) | 0x80: "WEEKEVENTREG_21_80",
    (22 << 8) | 0x01: "WEEKEVENTREG_22_01",
    (22 << 8) | 0x02: "WEEKEVENTREG_22_02",
    (22 << 8) | 0x04: "WEEKEVENTREG_CALMED_GORON_ELDER_SON",
    (22 << 8) | 0x08: "WEEKEVENTREG_22_08",
    (22 << 8) | 0x10: "WEEKEVENTREG_22_10",
    (22 << 8) | 0x20: "WEEKEVENTREG_22_20",
    (22 << 8) | 0x40: "WEEKEVENTREG_22_40",
    (22 << 8) | 0x80: "WEEKEVENTREG_22_80",
    (23 << 8) | 0x01: "WEEKEVENTREG_23_01",
    (23 << 8) | 0x02: "WEEKEVENTREG_23_02",
    (23 << 8) | 0x04: "WEEKEVENTREG_23_04",
    (23 << 8) | 0x08: "WEEKEVENTREG_23_08",
    (23 << 8) | 0x10: "WEEKEVENTREG_23_10",
    (23 << 8) | 0x20: "WEEKEVENTREG_23_20",
    (23 << 8) | 0x40: "WEEKEVENTREG_23_40",
    (23 << 8) | 0x80: "WEEKEVENTREG_23_80",
    (24 << 8) | 0x01: "WEEKEVENTREG_24_01",
    (24 << 8) | 0x02: "WEEKEVENTREG_24_02",
    (24 << 8) | 0x04: "WEEKEVENTREG_24_04",
    (24 << 8) | 0x08: "WEEKEVENTREG_24_08",
    (24 << 8) | 0x10: "WEEKEVENTREG_24_10",
    (24 << 8) | 0x20: "WEEKEVENTREG_24_20",
    (24 << 8) | 0x40: "WEEKEVENTREG_24_40",
    (24 << 8) | 0x80: "WEEKEVENTREG_24_80",
    (25 << 8) | 0x01: "WEEKEVENTREG_25_01",
    (25 << 8) | 0x02: "WEEKEVENTREG_25_02",
    (25 << 8) | 0x04: "WEEKEVENTREG_25_04",
    (25 << 8) | 0x08: "WEEKEVENTREG_25_08",
    (25 << 8) | 0x10: "WEEKEVENTREG_25_10",
    (25 << 8) | 0x20: "WEEKEVENTREG_25_20",
    (25 << 8) | 0x40: "WEEKEVENTREG_25_40",
    (25 << 8) | 0x80: "WEEKEVENTREG_25_80",
    (26 << 8) | 0x01: "WEEKEVENTREG_26_01",
    (26 << 8) | 0x02: "WEEKEVENTREG_26_02",
    (26 << 8) | 0x04: "WEEKEVENTREG_26_04",
    (26 << 8) | 0x08: "WEEKEVENTREG_26_08",
    (26 << 8) | 0x10: "WEEKEVENTREG_26_10",
    (26 << 8) | 0x20: "WEEKEVENTREG_26_20",
    (26 << 8) | 0x40: "WEEKEVENTREG_26_40",
    (26 << 8) | 0x80: "WEEKEVENTREG_26_80",
    (27 << 8) | 0x01: "WEEKEVENTREG_27_01",
    (27 << 8) | 0x02: "WEEKEVENTREG_27_02",
    (27 << 8) | 0x04: "WEEKEVENTREG_27_04",
    (27 << 8) | 0x08: "WEEKEVENTREG_27_08",
    (27 << 8) | 0x10: "WEEKEVENTREG_27_10",
    (27 << 8) | 0x20: "WEEKEVENTREG_27_20",
    (27 << 8) | 0x40: "WEEKEVENTREG_27_40",
    (27 << 8) | 0x80: "WEEKEVENTREG_27_80",
    (28 << 8) | 0x01: "WEEKEVENTREG_28_01",
    (28 << 8) | 0x02: "WEEKEVENTREG_28_02",
    (28 << 8) | 0x04: "WEEKEVENTREG_28_04",
    (28 << 8) | 0x08: "WEEKEVENTREG_28_08",
    (28 << 8) | 0x10: "WEEKEVENTREG_28_10",
    (28 << 8) | 0x20: "WEEKEVENTREG_28_20",
    (28 << 8) | 0x40: "WEEKEVENTREG_28_40",
    (28 << 8) | 0x80: "WEEKEVENTREG_28_80",
    (29 << 8) | 0x01: "WEEKEVENTREG_29_01",
    (29 << 8) | 0x02: "WEEKEVENTREG_29_02",
    (29 << 8) | 0x04: "WEEKEVENTREG_29_04",
    (29 << 8) | 0x08: "WEEKEVENTREG_29_08",
    (29 << 8) | 0x10: "WEEKEVENTREG_29_10",
    (29 << 8) | 0x20: "WEEKEVENTREG_29_20",
    (29 << 8) | 0x40: "WEEKEVENTREG_29_40",
    (29 << 8) | 0x80: "WEEKEVENTREG_29_80",
    (30 << 8) | 0x01: "WEEKEVENTREG_30_01",
    (30 << 8) | 0x02: "WEEKEVENTREG_30_02",
    (30 << 8) | 0x04: "WEEKEVENTREG_30_04",
    (30 << 8) | 0x08: "WEEKEVENTREG_30_08",
    (30 << 8) | 0x10: "WEEKEVENTREG_30_10",
    (30 << 8) | 0x20: "WEEKEVENTREG_30_20",
    (30 << 8) | 0x40: "WEEKEVENTREG_30_40",
    (30 << 8) | 0x80: "WEEKEVENTREG_30_80",
    (31 << 8) | 0x01: "WEEKEVENTREG_31_01",
    (31 << 8) | 0x02: "WEEKEVENTREG_31_02",
    (31 << 8) | 0x04: "WEEKEVENTREG_31_04",
    (31 << 8) | 0x08: "WEEKEVENTREG_31_08",
    (31 << 8) | 0x10: "WEEKEVENTREG_31_10",
    (31 << 8) | 0x20: "WEEKEVENTREG_31_20",
    (31 << 8) | 0x40: "WEEKEVENTREG_31_40",
    (31 << 8) | 0x80: "WEEKEVENTREG_31_80",
    (32 << 8) | 0x01: "WEEKEVENTREG_32_01",
    (32 << 8) | 0x02: "WEEKEVENTREG_32_02",
    (32 << 8) | 0x04: "WEEKEVENTREG_32_04",
    (32 << 8) | 0x08: "WEEKEVENTREG_32_08",
    (32 << 8) | 0x10: "WEEKEVENTREG_32_10",
    (32 << 8) | 0x20: "WEEKEVENTREG_32_20",
    (32 << 8) | 0x40: "WEEKEVENTREG_32_40",
    (32 << 8) | 0x80: "WEEKEVENTREG_32_80",
    (33 << 8) | 0x01: "WEEKEVENTREG_33_01",
    (33 << 8) | 0x02: "WEEKEVENTREG_33_02",
    (33 << 8) | 0x04: "WEEKEVENTREG_33_04",
    (33 << 8) | 0x08: "WEEKEVENTREG_33_08",
    (33 << 8) | 0x10: "WEEKEVENTREG_33_10",
    (33 << 8) | 0x20: "WEEKEVENTREG_33_20",
    (33 << 8) | 0x40: "WEEKEVENTREG_33_40",
    (33 << 8) | 0x80: "WEEKEVENTREG_CLEARED_SNOWHEAD_TEMPLE",
    (34 << 8) | 0x01: "WEEKEVENTREG_34_01",
    (34 << 8) | 0x02: "WEEKEVENTREG_34_02",
    (34 << 8) | 0x04: "WEEKEVENTREG_34_04",
    (34 << 8) | 0x08: "WEEKEVENTREG_TALKED_SWAMP_SPIDER_HOUSE_MAN",
    (34 << 8) | 0x10: "WEEKEVENTREG_34_10",
    (34 << 8) | 0x20: "WEEKEVENTREG_34_20",
    (34 << 8) | 0x40: "WEEKEVENTREG_RECEIVED_MASK_OF_TRUTH",
    (34 << 8) | 0x80: "WEEKEVENTREG_34_80",
    (35 << 8) | 0x01: "WEEKEVENTREG_35_01",
    (35 << 8) | 0x02: "WEEKEVENTREG_35_02",
    (35 << 8) | 0x04: "WEEKEVENTREG_35_04",
    (35 << 8) | 0x08: "WEEKEVENTREG_35_08",
    (35 << 8) | 0x10: "WEEKEVENTREG_35_10",
    (35 << 8) | 0x20: "WEEKEVENTREG_35_20",
    (35 << 8) | 0x40: "WEEKEVENTREG_35_40",
    (35 << 8) | 0x80: "WEEKEVENTREG_35_80",
    (36 << 8) | 0x01: "WEEKEVENTREG_36_01",
    (36 << 8) | 0x02: "WEEKEVENTREG_36_02",
    (36 << 8) | 0x04: "WEEKEVENTREG_36_04",
    (36 << 8) | 0x08: "WEEKEVENTREG_36_08",
    (36 << 8) | 0x10: "WEEKEVENTREG_36_10",
    (36 << 8) | 0x20: "WEEKEVENTREG_36_20",
    (36 << 8) | 0x40: "WEEKEVENTREG_36_40",
    (36 << 8) | 0x80: "WEEKEVENTREG_36_80",
    (37 << 8) | 0x01: "WEEKEVENTREG_37_01",
    (37 << 8) | 0x02: "WEEKEVENTREG_37_02",
    (37 << 8) | 0x04: "WEEKEVENTREG_37_04",
    (37 << 8) | 0x08: "WEEKEVENTREG_37_08",
    (37 << 8) | 0x10: "WEEKEVENTREG_37_10",
    (37 << 8) | 0x20: "WEEKEVENTREG_37_20",
    (37 << 8) | 0x40: "WEEKEVENTREG_37_40",
    (37 << 8) | 0x80: "WEEKEVENTREG_37_80",
    (38 << 8) | 0x01: "WEEKEVENTREG_38_01",
    (38 << 8) | 0x02: "WEEKEVENTREG_38_02",
    (38 << 8) | 0x04: "WEEKEVENTREG_38_04",
    (38 << 8) | 0x08: "WEEKEVENTREG_38_08",
    (38 << 8) | 0x10: "WEEKEVENTREG_38_10",
    (38 << 8) | 0x20: "WEEKEVENTREG_38_20",
    (38 << 8) | 0x40: "WEEKEVENTREG_38_40",
    (38 << 8) | 0x80: "WEEKEVENTREG_38_80",
    (39 << 8) | 0x01: "WEEKEVENTREG_39_01",
    (39 << 8) | 0x02: "WEEKEVENTREG_39_02",
    (39 << 8) | 0x04: "WEEKEVENTREG_39_04",
    (39 << 8) | 0x08: "WEEKEVENTREG_39_08",
    (39 << 8) | 0x10: "WEEKEVENTREG_39_10",
    (39 << 8) | 0x20: "WEEKEVENTREG_39_20",
    (39 << 8) | 0x40: "WEEKEVENTREG_39_40",
    (39 << 8) | 0x80: "WEEKEVENTREG_39_80",
    (40 << 8) | 0x01: "WEEKEVENTREG_40_01",
    (40 << 8) | 0x02: "WEEKEVENTREG_40_02",
    (40 << 8) | 0x04: "WEEKEVENTREG_40_04",
    (40 << 8) | 0x08: "WEEKEVENTREG_40_08",
    (40 << 8) | 0x10: "WEEKEVENTREG_40_10",
    (40 << 8) | 0x20: "WEEKEVENTREG_40_20",
    (40 << 8) | 0x40: "WEEKEVENTREG_40_40",
    (40 << 8) | 0x80: "WEEKEVENTREG_40_80",
    (41 << 8) | 0x01: "WEEKEVENTREG_41_01",
    (41 << 8) | 0x02: "WEEKEVENTREG_41_02",
    (41 << 8) | 0x04: "WEEKEVENTREG_41_04",
    (41 << 8) | 0x08: "WEEKEVENTREG_41_08",
    (41 << 8) | 0x10: "WEEKEVENTREG_41_10",
    (41 << 8) | 0x20: "WEEKEVENTREG_41_20",
    (41 << 8) | 0x40: "WEEKEVENTREG_41_40",
    (41 << 8) | 0x80: "WEEKEVENTREG_41_80",
    (42 << 8) | 0x01: "WEEKEVENTREG_42_01",
    (42 << 8) | 0x02: "WEEKEVENTREG_42_02",
    (42 << 8) | 0x04: "WEEKEVENTREG_42_04",
    (42 << 8) | 0x08: "WEEKEVENTREG_42_08",
    (42 << 8) | 0x10: "WEEKEVENTREG_42_10",
    (42 << 8) | 0x20: "WEEKEVENTREG_42_20",
    (42 << 8) | 0x40: "WEEKEVENTREG_42_40",
    (42 << 8) | 0x80: "WEEKEVENTREG_42_80",
    (43 << 8) | 0x01: "WEEKEVENTREG_43_01",
    (43 << 8) | 0x02: "WEEKEVENTREG_43_02",
    (43 << 8) | 0x04: "WEEKEVENTREG_43_04",
    (43 << 8) | 0x08: "WEEKEVENTREG_43_08",
    (43 << 8) | 0x10: "WEEKEVENTREG_43_10",
    (43 << 8) | 0x20: "WEEKEVENTREG_43_20",
    (43 << 8) | 0x40: "WEEKEVENTREG_43_40",
    (43 << 8) | 0x80: "WEEKEVENTREG_43_80",
    (44 << 8) | 0x01: "WEEKEVENTREG_44_01",
    (44 << 8) | 0x02: "WEEKEVENTREG_44_02",
    (44 << 8) | 0x04: "WEEKEVENTREG_44_04",
    (44 << 8) | 0x08: "WEEKEVENTREG_44_08",
    (44 << 8) | 0x10: "WEEKEVENTREG_44_10",
    (44 << 8) | 0x20: "WEEKEVENTREG_44_20",
    (44 << 8) | 0x40: "WEEKEVENTREG_44_40",
    (44 << 8) | 0x80: "WEEKEVENTREG_44_80",
    (45 << 8) | 0x01: "WEEKEVENTREG_45_01",
    (45 << 8) | 0x02: "WEEKEVENTREG_45_02",
    (45 << 8) | 0x04: "WEEKEVENTREG_45_04",
    (45 << 8) | 0x08: "WEEKEVENTREG_45_08",
    (45 << 8) | 0x10: "WEEKEVENTREG_45_10",
    (45 << 8) | 0x20: "WEEKEVENTREG_45_20",
    (45 << 8) | 0x40: "WEEKEVENTREG_45_40",
    (45 << 8) | 0x80: "WEEKEVENTREG_45_80",
    (46 << 8) | 0x01: "WEEKEVENTREG_46_01",
    (46 << 8) | 0x02: "WEEKEVENTREG_46_02",
    (46 << 8) | 0x04: "WEEKEVENTREG_46_04",
    (46 << 8) | 0x08: "WEEKEVENTREG_46_08",
    (46 << 8) | 0x10: "WEEKEVENTREG_46_10",
    (46 << 8) | 0x20: "WEEKEVENTREG_46_20",
    (46 << 8) | 0x40: "WEEKEVENTREG_46_40",
    (46 << 8) | 0x80: "WEEKEVENTREG_46_80",
    (47 << 8) | 0x01: "WEEKEVENTREG_47_01",
    (47 << 8) | 0x02: "WEEKEVENTREG_47_02",
    (47 << 8) | 0x04: "WEEKEVENTREG_47_04",
    (47 << 8) | 0x08: "WEEKEVENTREG_47_08",
    (47 << 8) | 0x10: "WEEKEVENTREG_47_10",
    (47 << 8) | 0x20: "WEEKEVENTREG_47_20",
    (47 << 8) | 0x40: "WEEKEVENTREG_47_40",
    (47 << 8) | 0x80: "WEEKEVENTREG_47_80",
    (48 << 8) | 0x01: "WEEKEVENTREG_48_01",
    (48 << 8) | 0x02: "WEEKEVENTREG_48_02",
    (48 << 8) | 0x04: "WEEKEVENTREG_48_04",
    (48 << 8) | 0x08: "WEEKEVENTREG_48_08",
    (48 << 8) | 0x10: "WEEKEVENTREG_48_10",
    (48 << 8) | 0x20: "WEEKEVENTREG_48_20",
    (48 << 8) | 0x40: "WEEKEVENTREG_48_40",
    (48 << 8) | 0x80: "WEEKEVENTREG_48_80",
    (49 << 8) | 0x01: "WEEKEVENTREG_49_01",
    (49 << 8) | 0x02: "WEEKEVENTREG_49_02",
    (49 << 8) | 0x04: "WEEKEVENTREG_49_04",
    (49 << 8) | 0x08: "WEEKEVENTREG_49_08",
    (49 << 8) | 0x10: "WEEKEVENTREG_49_10",
    (49 << 8) | 0x20: "WEEKEVENTREG_49_20",
    (49 << 8) | 0x40: "WEEKEVENTREG_49_40",
    (49 << 8) | 0x80: "WEEKEVENTREG_49_80",
    (50 << 8) | 0x01: "WEEKEVENTREG_50_01",
    (50 << 8) | 0x02: "WEEKEVENTREG_50_02",
    (50 << 8) | 0x04: "WEEKEVENTREG_50_04",
    (50 << 8) | 0x08: "WEEKEVENTREG_50_08",
    (50 << 8) | 0x10: "WEEKEVENTREG_50_10",
    (50 << 8) | 0x20: "WEEKEVENTREG_50_20",
    (50 << 8) | 0x40: "WEEKEVENTREG_50_40",
    (50 << 8) | 0x80: "WEEKEVENTREG_50_80",
    (51 << 8) | 0x01: "WEEKEVENTREG_51_01",
    (51 << 8) | 0x02: "WEEKEVENTREG_51_02",
    (51 << 8) | 0x04: "WEEKEVENTREG_51_04",
    (51 << 8) | 0x08: "WEEKEVENTREG_51_08",
    (51 << 8) | 0x10: "WEEKEVENTREG_51_10",
    (51 << 8) | 0x20: "WEEKEVENTREG_51_20",
    (51 << 8) | 0x40: "WEEKEVENTREG_51_40",
    (51 << 8) | 0x80: "WEEKEVENTREG_51_80",
    (52 << 8) | 0x01: "WEEKEVENTREG_52_01",
    (52 << 8) | 0x02: "WEEKEVENTREG_52_02",
    (52 << 8) | 0x04: "WEEKEVENTREG_52_04",
    (52 << 8) | 0x08: "WEEKEVENTREG_52_08",
    (52 << 8) | 0x10: "WEEKEVENTREG_52_10",
    (52 << 8) | 0x20: "WEEKEVENTREG_CLEARED_STONE_TOWER_TEMPLE",
    (52 << 8) | 0x40: "WEEKEVENTREG_52_40",
    (52 << 8) | 0x80: "WEEKEVENTREG_52_80",
    (53 << 8) | 0x01: "WEEKEVENTREG_53_01",
    (53 << 8) | 0x02: "WEEKEVENTREG_53_02",
    (53 << 8) | 0x04: "WEEKEVENTREG_53_04",
    (53 << 8) | 0x08: "WEEKEVENTREG_53_08",
    (53 << 8) | 0x10: "WEEKEVENTREG_53_10",
    (53 << 8) | 0x20: "WEEKEVENTREG_53_20",
    (53 << 8) | 0x40: "WEEKEVENTREG_53_40",
    (53 << 8) | 0x80: "WEEKEVENTREG_53_80",
    (54 << 8) | 0x01: "WEEKEVENTREG_54_01",
    (54 << 8) | 0x02: "WEEKEVENTREG_54_02",
    (54 << 8) | 0x04: "WEEKEVENTREG_54_04",
    (54 << 8) | 0x08: "WEEKEVENTREG_54_08",
    (54 << 8) | 0x10: "WEEKEVENTREG_54_10",
    (54 << 8) | 0x20: "WEEKEVENTREG_54_20",
    (54 << 8) | 0x40: "WEEKEVENTREG_54_40",
    (54 << 8) | 0x80: "WEEKEVENTREG_54_80",
    (55 << 8) | 0x01: "WEEKEVENTREG_55_01",
    (55 << 8) | 0x02: "WEEKEVENTREG_55_02",
    (55 << 8) | 0x04: "WEEKEVENTREG_55_04",
    (55 << 8) | 0x08: "WEEKEVENTREG_55_08",
    (55 << 8) | 0x10: "WEEKEVENTREG_55_10",
    (55 << 8) | 0x20: "WEEKEVENTREG_55_20",
    (55 << 8) | 0x40: "WEEKEVENTREG_55_40",
    (55 << 8) | 0x80: "WEEKEVENTREG_CLEARED_GREAT_BAY_TEMPLE",
    (56 << 8) | 0x01: "WEEKEVENTREG_56_01",
    (56 << 8) | 0x02: "WEEKEVENTREG_56_02",
    (56 << 8) | 0x04: "WEEKEVENTREG_56_04",
    (56 << 8) | 0x08: "WEEKEVENTREG_56_08",
    (56 << 8) | 0x10: "WEEKEVENTREG_56_10",
    (56 << 8) | 0x20: "WEEKEVENTREG_56_20",
    (56 << 8) | 0x40: "WEEKEVENTREG_56_40",
    (56 << 8) | 0x80: "WEEKEVENTREG_56_80",
    (57 << 8) | 0x01: "WEEKEVENTREG_57_01",
    (57 << 8) | 0x02: "WEEKEVENTREG_57_02",
    (57 << 8) | 0x04: "WEEKEVENTREG_57_04",
    (57 << 8) | 0x08: "WEEKEVENTREG_57_08",
    (57 << 8) | 0x10: "WEEKEVENTREG_57_10",
    (57 << 8) | 0x20: "WEEKEVENTREG_57_20",
    (57 << 8) | 0x40: "WEEKEVENTREG_57_40",
    (57 << 8) | 0x80: "WEEKEVENTREG_57_80",
    (58 << 8) | 0x01: "WEEKEVENTREG_58_01",
    (58 << 8) | 0x02: "WEEKEVENTREG_58_02",
    (58 << 8) | 0x04: "WEEKEVENTREG_58_04",
    (58 << 8) | 0x08: "WEEKEVENTREG_58_08",
    (58 << 8) | 0x10: "WEEKEVENTREG_58_10",
    (58 << 8) | 0x20: "WEEKEVENTREG_58_20",
    (58 << 8) | 0x40: "WEEKEVENTREG_58_40",
    (58 << 8) | 0x80: "WEEKEVENTREG_58_80",
    (59 << 8) | 0x01: "WEEKEVENTREG_59_01",
    (59 << 8) | 0x02: "WEEKEVENTREG_59_02",
    (59 << 8) | 0x08: "WEEKEVENTREG_59_08",
    (59 << 8) | 0x04: "WEEKEVENTREG_59_04",
    (59 << 8) | 0x10: "WEEKEVENTREG_59_10",
    (59 << 8) | 0x20: "WEEKEVENTREG_59_20",
    (59 << 8) | 0x40: "WEEKEVENTREG_59_40",
    (59 << 8) | 0x80: "WEEKEVENTREG_59_80",
    (60 << 8) | 0x01: "WEEKEVENTREG_60_01",
    (60 << 8) | 0x02: "WEEKEVENTREG_60_02",
    (60 << 8) | 0x04: "WEEKEVENTREG_60_04",
    (60 << 8) | 0x08: "WEEKEVENTREG_60_08",
    (60 << 8) | 0x10: "WEEKEVENTREG_60_10",
    (60 << 8) | 0x20: "WEEKEVENTREG_60_20",
    (60 << 8) | 0x40: "WEEKEVENTREG_60_40",
    (60 << 8) | 0x80: "WEEKEVENTREG_60_80",
    (61 << 8) | 0x01: "WEEKEVENTREG_61_01",
    (61 << 8) | 0x02: "WEEKEVENTREG_61_02",
    (61 << 8) | 0x04: "WEEKEVENTREG_61_04",
    (61 << 8) | 0x08: "WEEKEVENTREG_61_08",
    (61 << 8) | 0x10: "WEEKEVENTREG_61_10",
    (61 << 8) | 0x20: "WEEKEVENTREG_61_20",
    (61 << 8) | 0x40: "WEEKEVENTREG_61_40",
    (61 << 8) | 0x80: "WEEKEVENTREG_61_80",
    (62 << 8) | 0x01: "WEEKEVENTREG_62_01",
    (62 << 8) | 0x02: "WEEKEVENTREG_62_02",
    (62 << 8) | 0x04: "WEEKEVENTREG_62_04",
    (62 << 8) | 0x08: "WEEKEVENTREG_62_08",
    (62 << 8) | 0x10: "WEEKEVENTREG_62_10",
    (62 << 8) | 0x20: "WEEKEVENTREG_62_20",
    (62 << 8) | 0x40: "WEEKEVENTREG_62_40",
    (62 << 8) | 0x80: "WEEKEVENTREG_62_80",
    (63 << 8) | 0x01: "WEEKEVENTREG_KICKOUT_WAIT",
    (63 << 8) | 0x02: "WEEKEVENTREG_KICKOUT_TIME_PASSED",
    (63 << 8) | 0x04: "WEEKEVENTREG_63_04",
    (63 << 8) | 0x08: "WEEKEVENTREG_63_08",
    (63 << 8) | 0x10: "WEEKEVENTREG_63_10",
    (63 << 8) | 0x20: "WEEKEVENTREG_63_20",
    (63 << 8) | 0x40: "WEEKEVENTREG_63_40",
    (63 << 8) | 0x80: "WEEKEVENTREG_63_80",
    (64 << 8) | 0x01: "WEEKEVENTREG_64_01",
    (64 << 8) | 0x02: "WEEKEVENTREG_64_02",
    (64 << 8) | 0x04: "WEEKEVENTREG_64_04",
    (64 << 8) | 0x08: "WEEKEVENTREG_64_08",
    (64 << 8) | 0x10: "WEEKEVENTREG_64_10",
    (64 << 8) | 0x20: "WEEKEVENTREG_64_20",
    (64 << 8) | 0x40: "WEEKEVENTREG_64_40",
    (64 << 8) | 0x80: "WEEKEVENTREG_TALKED_DOGGY_RACETRACK_OWNER_DAY_1",
    (65 << 8) | 0x01: "WEEKEVENTREG_TALKED_DOGGY_RACETRACK_OWNER_NIGHT_1",
    (65 << 8) | 0x02: "WEEKEVENTREG_TALKED_DOGGY_RACETRACK_OWNER_DAY_2",
    (65 << 8) | 0x04: "WEEKEVENTREG_TALKED_DOGGY_RACETRACK_OWNER_NIGHT_2",
    (65 << 8) | 0x08: "WEEKEVENTREG_TALKED_DOGGY_RACETRACK_OWNER_DAY_3",
    (65 << 8) | 0x10: "WEEKEVENTREG_TALKED_DOGGY_RACETRACK_OWNER_NIGHT_3",
    (65 << 8) | 0x20: "WEEKEVENTREG_65_20",
    (65 << 8) | 0x40: "WEEKEVENTREG_65_40",
    (65 << 8) | 0x80: "WEEKEVENTREG_65_80",
    (66 << 8) | 0x01: "WEEKEVENTREG_66_01",
    (66 << 8) | 0x02: "WEEKEVENTREG_66_02",
    (66 << 8) | 0x04: "WEEKEVENTREG_66_04",
    (66 << 8) | 0x08: "WEEKEVENTREG_66_08",
    (66 << 8) | 0x10: "WEEKEVENTREG_66_10",
    (66 << 8) | 0x20: "WEEKEVENTREG_66_20",
    (66 << 8) | 0x40: "WEEKEVENTREG_66_40",
    (66 << 8) | 0x80: "WEEKEVENTREG_66_80",
    (67 << 8) | 0x01: "WEEKEVENTREG_67_01",
    (67 << 8) | 0x02: "WEEKEVENTREG_67_02",
    (67 << 8) | 0x04: "WEEKEVENTREG_67_04",
    (67 << 8) | 0x08: "WEEKEVENTREG_67_08",
    (67 << 8) | 0x10: "WEEKEVENTREG_67_10",
    (67 << 8) | 0x20: "WEEKEVENTREG_67_20",
    (67 << 8) | 0x40: "WEEKEVENTREG_67_40",
    (67 << 8) | 0x80: "WEEKEVENTREG_67_80",
    (68 << 8) | 0x01: "WEEKEVENTREG_68_01",
    (68 << 8) | 0x02: "WEEKEVENTREG_68_02",
    (68 << 8) | 0x04: "WEEKEVENTREG_68_04",
    (68 << 8) | 0x08: "WEEKEVENTREG_68_08",
    (68 << 8) | 0x10: "WEEKEVENTREG_68_10",
    (68 << 8) | 0x20: "WEEKEVENTREG_68_20",
    (68 << 8) | 0x40: "WEEKEVENTREG_68_40",
    (68 << 8) | 0x80: "WEEKEVENTREG_68_80",
    (69 << 8) | 0x01: "WEEKEVENTREG_69_01",
    (69 << 8) | 0x02: "WEEKEVENTREG_69_02",
    (69 << 8) | 0x04: "WEEKEVENTREG_69_04",
    (69 << 8) | 0x08: "WEEKEVENTREG_69_08",
    (69 << 8) | 0x10: "WEEKEVENTREG_69_10",
    (69 << 8) | 0x20: "WEEKEVENTREG_69_20",
    (69 << 8) | 0x40: "WEEKEVENTREG_69_40",
    (69 << 8) | 0x80: "WEEKEVENTREG_69_80",
    (70 << 8) | 0x01: "WEEKEVENTREG_70_01",
    (70 << 8) | 0x02: "WEEKEVENTREG_70_02",
    (70 << 8) | 0x04: "WEEKEVENTREG_70_04",
    (70 << 8) | 0x08: "WEEKEVENTREG_70_08",
    (70 << 8) | 0x10: "WEEKEVENTREG_70_10",
    (70 << 8) | 0x20: "WEEKEVENTREG_70_20",
    (70 << 8) | 0x40: "WEEKEVENTREG_70_40",
    (70 << 8) | 0x80: "WEEKEVENTREG_70_80",
    (71 << 8) | 0x01: "WEEKEVENTREG_71_01",
    (71 << 8) | 0x02: "WEEKEVENTREG_71_02",
    (71 << 8) | 0x04: "WEEKEVENTREG_71_04",
    (71 << 8) | 0x08: "WEEKEVENTREG_71_08",
    (71 << 8) | 0x10: "WEEKEVENTREG_71_10",
    (71 << 8) | 0x20: "WEEKEVENTREG_71_20",
    (71 << 8) | 0x40: "WEEKEVENTREG_71_40",
    (71 << 8) | 0x80: "WEEKEVENTREG_71_80",
    (72 << 8) | 0x01: "WEEKEVENTREG_72_01",
    (72 << 8) | 0x02: "WEEKEVENTREG_72_02",
    (72 << 8) | 0x04: "WEEKEVENTREG_72_04",
    (72 << 8) | 0x08: "WEEKEVENTREG_72_08",
    (72 << 8) | 0x10: "WEEKEVENTREG_72_10",
    (72 << 8) | 0x20: "WEEKEVENTREG_72_20",
    (72 << 8) | 0x40: "WEEKEVENTREG_72_40",
    (72 << 8) | 0x80: "WEEKEVENTREG_72_80",
    (73 << 8) | 0x01: "WEEKEVENTREG_73_01",
    (73 << 8) | 0x02: "WEEKEVENTREG_73_02",
    (73 << 8) | 0x04: "WEEKEVENTREG_73_04",
    (73 << 8) | 0x08: "WEEKEVENTREG_73_08",
    (73 << 8) | 0x10: "WEEKEVENTREG_73_10",
    (73 << 8) | 0x20: "WEEKEVENTREG_73_20",
    (73 << 8) | 0x40: "WEEKEVENTREG_73_40",
    (73 << 8) | 0x80: "WEEKEVENTREG_73_80",
    (74 << 8) | 0x01: "WEEKEVENTREG_74_01",
    (74 << 8) | 0x02: "WEEKEVENTREG_74_02",
    (74 << 8) | 0x04: "WEEKEVENTREG_74_04",
    (74 << 8) | 0x08: "WEEKEVENTREG_74_08",
    (74 << 8) | 0x10: "WEEKEVENTREG_74_10",
    (74 << 8) | 0x20: "WEEKEVENTREG_74_20",
    (74 << 8) | 0x40: "WEEKEVENTREG_74_40",
    (74 << 8) | 0x80: "WEEKEVENTREG_74_80",
    (75 << 8) | 0x01: "WEEKEVENTREG_75_01",
    (75 << 8) | 0x02: "WEEKEVENTREG_75_02",
    (75 << 8) | 0x04: "WEEKEVENTREG_75_04",
    (75 << 8) | 0x08: "WEEKEVENTREG_75_08",
    (75 << 8) | 0x10: "WEEKEVENTREG_75_10",
    (75 << 8) | 0x20: "WEEKEVENTREG_75_20",
    (75 << 8) | 0x40: "WEEKEVENTREG_75_40",
    (75 << 8) | 0x80: "WEEKEVENTREG_75_80",
    (76 << 8) | 0x01: "WEEKEVENTREG_76_01",
    (76 << 8) | 0x02: "WEEKEVENTREG_76_02",
    (76 << 8) | 0x04: "WEEKEVENTREG_76_04",
    (76 << 8) | 0x08: "WEEKEVENTREG_76_08",
    (76 << 8) | 0x10: "WEEKEVENTREG_76_10",
    (76 << 8) | 0x20: "WEEKEVENTREG_76_20",
    (76 << 8) | 0x40: "WEEKEVENTREG_76_40",
    (76 << 8) | 0x80: "WEEKEVENTREG_76_80",
    (77 << 8) | 0x01: "WEEKEVENTREG_77_01",
    (77 << 8) | 0x02: "WEEKEVENTREG_77_02",
    (77 << 8) | 0x04: "WEEKEVENTREG_77_04",
    (77 << 8) | 0x08: "WEEKEVENTREG_77_08",
    (77 << 8) | 0x10: "WEEKEVENTREG_77_10",
    (77 << 8) | 0x20: "WEEKEVENTREG_77_20",
    (77 << 8) | 0x40: "WEEKEVENTREG_77_40",
    (77 << 8) | 0x80: "WEEKEVENTREG_77_80",
    (78 << 8) | 0x01: "WEEKEVENTREG_78_01",
    (78 << 8) | 0x02: "WEEKEVENTREG_78_02",
    (78 << 8) | 0x04: "WEEKEVENTREG_78_04",
    (78 << 8) | 0x08: "WEEKEVENTREG_78_08",
    (78 << 8) | 0x10: "WEEKEVENTREG_78_10",
    (78 << 8) | 0x20: "WEEKEVENTREG_78_20",
    (78 << 8) | 0x40: "WEEKEVENTREG_78_40",
    (78 << 8) | 0x80: "WEEKEVENTREG_78_80",
    (79 << 8) | 0x01: "WEEKEVENTREG_79_01",
    (79 << 8) | 0x02: "WEEKEVENTREG_79_02",
    (79 << 8) | 0x04: "WEEKEVENTREG_79_04",
    (79 << 8) | 0x08: "WEEKEVENTREG_79_08",
    (79 << 8) | 0x10: "WEEKEVENTREG_79_10",
    (79 << 8) | 0x20: "WEEKEVENTREG_79_20",
    (79 << 8) | 0x40: "WEEKEVENTREG_79_40",
    (79 << 8) | 0x80: "WEEKEVENTREG_79_80",
    (80 << 8) | 0x01: "WEEKEVENTREG_80_01",
    (80 << 8) | 0x02: "WEEKEVENTREG_80_02",
    (80 << 8) | 0x04: "WEEKEVENTREG_80_04",
    (80 << 8) | 0x08: "WEEKEVENTREG_80_08",
    (80 << 8) | 0x10: "WEEKEVENTREG_80_10",
    (80 << 8) | 0x20: "WEEKEVENTREG_80_20",
    (80 << 8) | 0x40: "WEEKEVENTREG_80_40",
    (80 << 8) | 0x80: "WEEKEVENTREG_80_80",
    (81 << 8) | 0x01: "WEEKEVENTREG_81_01",
    (81 << 8) | 0x02: "WEEKEVENTREG_81_02",
    (81 << 8) | 0x04: "WEEKEVENTREG_81_04",
    (81 << 8) | 0x08: "WEEKEVENTREG_81_08",
    (81 << 8) | 0x10: "WEEKEVENTREG_81_10",
    (81 << 8) | 0x20: "WEEKEVENTREG_81_20",
    (81 << 8) | 0x40: "WEEKEVENTREG_81_40",
    (81 << 8) | 0x80: "WEEKEVENTREG_81_80",
    (82 << 8) | 0x01: "WEEKEVENTREG_82_01",
    (82 << 8) | 0x02: "WEEKEVENTREG_82_02",
    (82 << 8) | 0x04: "WEEKEVENTREG_82_04",
    (82 << 8) | 0x08: "WEEKEVENTREG_82_08",
    (82 << 8) | 0x10: "WEEKEVENTREG_82_10",
    (82 << 8) | 0x20: "WEEKEVENTREG_82_20",
    (82 << 8) | 0x40: "WEEKEVENTREG_82_40",
    (82 << 8) | 0x80: "WEEKEVENTREG_82_80",
    (83 << 8) | 0x01: "WEEKEVENTREG_83_01",
    (83 << 8) | 0x02: "WEEKEVENTREG_83_02",
    (83 << 8) | 0x04: "WEEKEVENTREG_83_04",
    (83 << 8) | 0x08: "WEEKEVENTREG_83_08",
    (83 << 8) | 0x10: "WEEKEVENTREG_83_10",
    (83 << 8) | 0x20: "WEEKEVENTREG_83_20",
    (83 << 8) | 0x40: "WEEKEVENTREG_83_40",
    (83 << 8) | 0x80: "WEEKEVENTREG_83_80",
    (84 << 8) | 0x01: "WEEKEVENTREG_84_01",
    (84 << 8) | 0x02: "WEEKEVENTREG_84_02",
    (84 << 8) | 0x04: "WEEKEVENTREG_84_04",
    (84 << 8) | 0x08: "WEEKEVENTREG_84_08",
    (84 << 8) | 0x10: "WEEKEVENTREG_84_10",
    (84 << 8) | 0x20: "WEEKEVENTREG_84_20",
    (84 << 8) | 0x40: "WEEKEVENTREG_84_40",
    (84 << 8) | 0x80: "WEEKEVENTREG_84_80",
    (85 << 8) | 0x01: "WEEKEVENTREG_85_01",
    (85 << 8) | 0x02: "WEEKEVENTREG_85_02",
    (85 << 8) | 0x04: "WEEKEVENTREG_85_04",
    (85 << 8) | 0x08: "WEEKEVENTREG_85_08",
    (85 << 8) | 0x10: "WEEKEVENTREG_85_10",
    (85 << 8) | 0x20: "WEEKEVENTREG_85_20",
    (85 << 8) | 0x40: "WEEKEVENTREG_85_40",
    (85 << 8) | 0x80: "WEEKEVENTREG_85_80",
    (86 << 8) | 0x01: "WEEKEVENTREG_86_01",
    (86 << 8) | 0x02: "WEEKEVENTREG_86_02",
    (86 << 8) | 0x04: "WEEKEVENTREG_86_04",
    (86 << 8) | 0x08: "WEEKEVENTREG_86_08",
    (86 << 8) | 0x10: "WEEKEVENTREG_86_10",
    (86 << 8) | 0x20: "WEEKEVENTREG_86_20",
    (86 << 8) | 0x40: "WEEKEVENTREG_86_40",
    (86 << 8) | 0x80: "WEEKEVENTREG_86_80",
    (87 << 8) | 0x01: "WEEKEVENTREG_87_01",
    (87 << 8) | 0x02: "WEEKEVENTREG_87_02",
    (87 << 8) | 0x04: "WEEKEVENTREG_87_04",
    (87 << 8) | 0x08: "WEEKEVENTREG_87_08",
    (87 << 8) | 0x10: "WEEKEVENTREG_87_10",
    (87 << 8) | 0x20: "WEEKEVENTREG_87_20",
    (87 << 8) | 0x40: "WEEKEVENTREG_87_40",
    (87 << 8) | 0x80: "WEEKEVENTREG_87_80",
    (88 << 8) | 0x01: "WEEKEVENTREG_88_01",
    (88 << 8) | 0x02: "WEEKEVENTREG_88_02",
    (88 << 8) | 0x04: "WEEKEVENTREG_88_04",
    (88 << 8) | 0x08: "WEEKEVENTREG_88_08",
    (88 << 8) | 0x10: "WEEKEVENTREG_88_10",
    (88 << 8) | 0x20: "WEEKEVENTREG_88_20",
    (88 << 8) | 0x40: "WEEKEVENTREG_GATEKEEPER_OPENED_GORON_SHRINE",
    (88 << 8) | 0x80: "WEEKEVENTREG_GATEKEEPER_OPENED_GORON_SHRINE_FOR_HUMAN",
    (89 << 8) | 0x01: "WEEKEVENTREG_GATEKEEPER_OPENED_GORON_SHRINE_FOR_DEKU",
    (89 << 8) | 0x02: "WEEKEVENTREG_GATEKEEPER_OPENED_GORON_SHRINE_FOR_ZORA",
    (89 << 8) | 0x04: "WEEKEVENTREG_GATEKEEPER_OPENED_GORON_SHRINE_FOR_GORON",
    (89 << 8) | 0x08: "WEEKEVENTREG_89_08",
    (89 << 8) | 0x10: "WEEKEVENTREG_89_10",
    (89 << 8) | 0x20: "WEEKEVENTREG_89_20",
    (89 << 8) | 0x40: "WEEKEVENTREG_89_40",
    (89 << 8) | 0x80: "WEEKEVENTREG_89_80",
    (90 << 8) | 0x01: "WEEKEVENTREG_90_01",
    (90 << 8) | 0x02: "WEEKEVENTREG_90_02",
    (90 << 8) | 0x04: "WEEKEVENTREG_90_04",
    (90 << 8) | 0x08: "WEEKEVENTREG_90_08",
    (90 << 8) | 0x10: "WEEKEVENTREG_90_10",
    (90 << 8) | 0x20: "WEEKEVENTREG_90_20",
    (90 << 8) | 0x40: "WEEKEVENTREG_90_40",
    (90 << 8) | 0x80: "WEEKEVENTREG_90_80",
    (91 << 8) | 0x01: "WEEKEVENTREG_91_01",
    (91 << 8) | 0x02: "WEEKEVENTREG_91_02",
    (91 << 8) | 0x04: "WEEKEVENTREG_91_04",
    (91 << 8) | 0x08: "WEEKEVENTREG_91_08",
    (91 << 8) | 0x10: "WEEKEVENTREG_91_10",
    (91 << 8) | 0x20: "WEEKEVENTREG_91_20",
    (91 << 8) | 0x40: "WEEKEVENTREG_91_40",
    (91 << 8) | 0x80: "WEEKEVENTREG_91_80",
    (92 << 8) | 0x01: "WEEKEVENTREG_92_01",
    (92 << 8) | 0x02: "WEEKEVENTREG_92_02",
    (92 << 8) | 0x04: "WEEKEVENTREG_92_04",
    (92 << 8) | 0x08: "WEEKEVENTREG_92_08",
    (92 << 8) | 0x10: "WEEKEVENTREG_92_10",
    (92 << 8) | 0x20: "WEEKEVENTREG_92_20",
    (92 << 8) | 0x40: "WEEKEVENTREG_92_40",
    (92 << 8) | 0x80: "WEEKEVENTREG_92_80",
    (93 << 8) | 0x01: "WEEKEVENTREG_93_01",
    (93 << 8) | 0x02: "WEEKEVENTREG_93_02",
    (93 << 8) | 0x04: "WEEKEVENTREG_93_04",
    (93 << 8) | 0x08: "WEEKEVENTREG_93_08",
    (93 << 8) | 0x10: "WEEKEVENTREG_93_10",
    (93 << 8) | 0x20: "WEEKEVENTREG_93_20",
    (93 << 8) | 0x40: "WEEKEVENTREG_93_40",
    (93 << 8) | 0x80: "WEEKEVENTREG_93_80",
    (94 << 8) | 0x01: "WEEKEVENTREG_94_01",
    (94 << 8) | 0x02: "WEEKEVENTREG_94_02",
    (94 << 8) | 0x04: "WEEKEVENTREG_94_04",
    (94 << 8) | 0x08: "WEEKEVENTREG_94_08",
    (94 << 8) | 0x10: "WEEKEVENTREG_94_10",
    (94 << 8) | 0x20: "WEEKEVENTREG_94_20",
    (94 << 8) | 0x40: "WEEKEVENTREG_94_40",
    (94 << 8) | 0x80: "WEEKEVENTREG_94_80",
    (95 << 8) | 0x01: "WEEKEVENTREG_95_01",
    (95 << 8) | 0x02: "WEEKEVENTREG_95_02",
    (95 << 8) | 0x04: "WEEKEVENTREG_95_04",
    (95 << 8) | 0x08: "WEEKEVENTREG_95_08",
    (95 << 8) | 0x10: "WEEKEVENTREG_95_10",
    (95 << 8) | 0x20: "WEEKEVENTREG_95_20",
    (95 << 8) | 0x40: "WEEKEVENTREG_95_40",
    (95 << 8) | 0x80: "WEEKEVENTREG_95_80",
    (96 << 8) | 0x01: "WEEKEVENTREG_96_01",
    (96 << 8) | 0x02: "WEEKEVENTREG_96_02",
    (96 << 8) | 0x04: "WEEKEVENTREG_96_04",
    (96 << 8) | 0x08: "WEEKEVENTREG_96_08",
    (96 << 8) | 0x10: "WEEKEVENTREG_96_10",
    (96 << 8) | 0x20: "WEEKEVENTREG_96_20",
    (96 << 8) | 0x40: "WEEKEVENTREG_96_40",
    (96 << 8) | 0x80: "WEEKEVENTREG_96_80",
    (97 << 8) | 0x01: "WEEKEVENTREG_97_01",
    (97 << 8) | 0x02: "WEEKEVENTREG_97_02",
    (97 << 8) | 0x04: "WEEKEVENTREG_97_04",
    (97 << 8) | 0x08: "WEEKEVENTREG_97_08",
    (97 << 8) | 0x10: "WEEKEVENTREG_97_10",
    (97 << 8) | 0x20: "WEEKEVENTREG_97_20",
    (97 << 8) | 0x40: "WEEKEVENTREG_97_40",
    (97 << 8) | 0x80: "WEEKEVENTREG_97_80",
    (98 << 8) | 0x01: "WEEKEVENTREG_98_01",
    (98 << 8) | 0x02: "WEEKEVENTREG_98_02",
    (98 << 8) | 0x04: "WEEKEVENTREG_98_04",
    (98 << 8) | 0x08: "WEEKEVENTREG_98_08",
    (98 << 8) | 0x10: "WEEKEVENTREG_98_10",
    (98 << 8) | 0x20: "WEEKEVENTREG_98_20",
    (98 << 8) | 0x40: "WEEKEVENTREG_98_40",
    (98 << 8) | 0x80: "WEEKEVENTREG_98_80",
    (99 << 8) | 0x01: "WEEKEVENTREG_99_01",
    (99 << 8) | 0x02: "WEEKEVENTREG_99_02",
    (99 << 8) | 0x04: "WEEKEVENTREG_99_04",
    (99 << 8) | 0x08: "WEEKEVENTREG_99_08",
    (99 << 8) | 0x10: "WEEKEVENTREG_99_10",
    (99 << 8) | 0x20: "WEEKEVENTREG_99_20",
    (99 << 8) | 0x40: "WEEKEVENTREG_99_40",
    (99 << 8) | 0x80: "WEEKEVENTREG_99_80",
}

def getFlagMacro(index: int, mask: int) -> str:
    flag = (index << 8) | mask
    if flag in weekEventReg:
        return weekEventReg[flag]
    return f"WEEKEVENTREG_{index:02}_{mask:02X}"

def getCheckMacro(index: int, mask: int) -> str:
    return f"CHECK_WEEKEVENTREG({getFlagMacro(index, mask)})"

def getSetMacro(index: int, mask: int) -> str:
    return f"SET_WEEKEVENTREG({getFlagMacro(index, mask)})"

def getClearMacro(index: int, mask: int) -> str:
    return f"CLEAR_WEEKEVENTREG({getFlagMacro(index, mask)})"

NUMBER_PATTERN = r"(0[xX])?[0-9a-fA-F]+"

def applyChange(fileContents: str, compiledRegex: re.Pattern, callback) -> str:
    parsedContents = ""

    match = compiledRegex.search(fileContents)
    while match:
        index = int(match.group("index"), 0)
        mask = int(match.group("mask"), 0)

        start, end = match.span()
        parsedContents += fileContents[:start]
        parsedContents += callback(index, mask)

        fileContents = fileContents[end:]
        match = compiledRegex.search(fileContents)

    parsedContents += fileContents
    return parsedContents


def updateCheck(fileContents: str) -> str:
    # gSaveContext.save.saveInfo.weekEventReg[86] & 2
    checkRegex = re.compile(rf"gSaveContext.save.saveInfo.weekEventReg\[(?P<index>{NUMBER_PATTERN})\]\s*\&\s*(?P<mask>{NUMBER_PATTERN})")

    return applyChange(fileContents, checkRegex, getCheckMacro)

def updateSet(fileContents: str) -> str:
    # gSaveContext.save.saveInfo.weekEventReg[51] |= 0x10
    setRegex = re.compile(rf"gSaveContext.save.saveInfo.weekEventReg\[(?P<index>{NUMBER_PATTERN})\]\s*\|=\s*(?P<mask>{NUMBER_PATTERN})")

    return applyChange(fileContents, setRegex, getSetMacro)

def updateClear(fileContents: str) -> str:
    # gSaveContext.save.saveInfo.weekEventReg[85] &= (u8)~0x80
    clearRegex = re.compile(rf"gSaveContext.save.saveInfo.weekEventReg\[(?P<index>{NUMBER_PATTERN})\]\s*\&=\s*(\(u8\))?~(?P<mask>{NUMBER_PATTERN})")

    return applyChange(fileContents, clearRegex, getClearMacro)


def read_file(filename):
    with open(filename) as src_file:
        return src_file.read()

def write_file(filename, contents):
    with open(filename, "w") as f:
        f.write(contents)


def main():
    parser = argparse.ArgumentParser(description="Converts a weekEventReg access to a macro")

    parser.add_argument("filename", help="Replace every occurrence of numeric weekEventReg on this file to the corresponding macro")
    args = parser.parse_args()

    fileContents = read_file(args.filename)

    parsedContents = updateCheck(fileContents)
    parsedContents = updateSet(parsedContents)
    parsedContents = updateClear(parsedContents)

    if fileContents != parsedContents:
        write_file(args.filename, parsedContents)

if __name__ == "__main__":
    main()
