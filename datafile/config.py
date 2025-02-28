class DataEconomy:
    START_UPDATERS = {
        'click_mob': 0,
        'x': 0,
        'custom_x': 0,
        'key': 0,
        'level_upgrade': 0,
        'max_money': 0,
        'discount_shop': 0,
        'money': 100,
        'profit': 1
    }


    CLICK_MOB = {
        0: {'price': 500, 'effect': 1},
        1: {'price': 1500, 'effect': 2},
        2: {'price': 4000, 'effect': 4},
        3: {'price': 8000, 'effect': 7},
        4: {'price': 9000, 'effect': 10},
        5: {'price': 15000, 'effect': 13},
        6: {'price': 20000, 'effect': 17},
        7: {'price': 25000, 'effect': 20},
        8: {'price': 32000, 'effect': 25},
        9: {'price': 50000, 'effect': 30}
    }

    X = {
        0: {'price': 400, 'effect': 1.1},
        1: {'price': 1000, 'effect': 1.2},
        2: {'price': 1800, 'effect': 1.4},
        3: {'price': 3200, 'effect': 1.7},
        4: {'price': 5000, 'effect': 2.1},
        5: {'price': 7500, 'effect': 2.6},
        6: {'price': 11000, 'effect': 3.2},
        7: {'price': 16000, 'effect': 4.0},
        8: {'price': 23000, 'effect': 5.0},
        9: {'price': 32000, 'effect': 6.2}
    }

    CUSTOM_X = {
        0: {'price': 600, 'effect': 1},
        1: {'price': 1400, 'effect': 1.3},
        2: {'price': 2500, 'effect': 1.7},
        3: {'price': 4000, 'effect': 2.2},
        4: {'price': 6500, 'effect': 2.8},
        5: {'price': 9500, 'effect': 3.5},
        6: {'price': 14000, 'effect': 4.3},
        7: {'price': 20000, 'effect': 5.2},
        8: {'price': 28000, 'effect': 6.2},
        9: {'price': 38000, 'effect': 7.5}
    }

    KEY = {
        0: {'price': 1000, 'effect': 1},
        1: {'price': 2500, 'effect': 2},
        2: {'price': 5000, 'effect': 3},
        3: {'price': 8500, 'effect': 4},
        4: {'price': 13000, 'effect': 5},
        5: {'price': 19000, 'effect': 6},
        6: {'price': 27000, 'effect': 7},
        7: {'price': 37000, 'effect': 8},
        8: {'price': 50000, 'effect': 9},
        9: {'price': 65000, 'effect': 10}
    }


    LEVEL_UPGRADE = {
        0: {'price': 2000, 'effect': 0},
        1: {'price': 5000, 'effect': 1},
        2: {'price': 9000, 'effect': 2},
        3: {'price': 15000, 'effect': 3},
        4: {'price': 22000, 'effect': 4},
        5: {'price': 31000, 'effect': 5},
        6: {'price': 42000, 'effect': 6},
        7: {'price': 55000, 'effect': 7},
        8: {'price': 70000, 'effect': 8}
    }

    MAX_MONEY = {
        0: {'price': 1000, 'effect': 5000},
        1: {'price': 3000, 'effect': 12000},
        2: {'price': 7000, 'effect': 25000},
        3: {'price': 14000, 'effect': 50000},
        4: {'price': 23000, 'effect': 100000},
        5: {'price': 35000, 'effect': 250000},
        6: {'price': 50000, 'effect': 500000},
        7: {'price': 70000, 'effect': 1000000},
        8: {'price': 95000, 'effect': 2500000},
        9: {'price': 125000, 'effect': 5000000}
    }

    DISCOUNT_SHOP = {
        0: {'price': 3000, 'effect': 0.98},
        1: {'price': 7500, 'effect': 0.96},
        2: {'price': 14000, 'effect': 0.93},
        3: {'price': 23000, 'effect': 0.90},
        4: {'price': 35000, 'effect': 0.87},
        5: {'price': 50000, 'effect': 0.83},
        6: {'price': 68000, 'effect': 0.78},
        7: {'price': 89000, 'effect': 0.72},
        8: {'price': 114000, 'effect': 0.65},
        9: {'price': 143000, 'effect': 0.58}
    }

