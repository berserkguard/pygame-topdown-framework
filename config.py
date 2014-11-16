class Config():
    # Width & Height of the screen
    width = 1024
    height = 768
    
    # Size of the map (in tiles)
    map_size = 100
    
    # Size of a tile (in pixels)
    tile_size = 128
    
    # Size of a scrap (in pixels)
    scrap_size = 32
    
    # Size of turret (in pixels)
    turret_size = 64
    
    # Number of scraps per tile
    scrap_density = 0.03
    
    turret_density = 0.01
    
    # Percentage a part can degrade by at a time
    degrade_amount = 0.3
    
    # Percentage a part can be repaired by a scrap
    repair_amount = 0.2
    
    # Scrap gravitation speed (in pixels/second)
    scrap_gravitation_speed = 250
    
    # Starting position of messages
    message_x = width / 2
    message_y = height / 2 - 100
    
    # Message duration (in seconds)
    message_duration = 3
    
    # Message scroll speed (in pixels/second)
    message_scroll_speed = 80
    
    # Turret maximum tracking distance (in pixels)
    turret_track_distance = 350
