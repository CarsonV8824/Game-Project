def map_colors() -> dict:
    return {
        "objective":  (0, 80, 250),
        "air": (135, 206, 235),
        "leaves": (34, 139, 34),
        "log": (139, 69, 19),
        "green_land": (0, 255, 0),
        "cactus": (0, 100, 0),
        "sand": (194, 178, 128),
        "ice_block": (173, 216, 230),
        "snow": (255, 250, 250),
        "water": (0, 191, 255),
        "enemy_spawn": (255, 0, 0),
    }

def collision_tiles() -> set:
    return {"log", "cactus", "ice_block", "objective"}