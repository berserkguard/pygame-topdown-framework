class Config():
    # Width & Height of the screen
    width = 800
    height = 600
    
    # Size of the map (in tiles)
    map_size = 100
    
    # Size of a tile (in pixels)
    tile_size = 128
    
    # Size of a scrap (in pixels)
    scrap_size = 32
    
    # Number of scraps per tile
    scrap_density = 0.02
    
    # Percentage a part can degrade by at a time
    degrade_amount = 0.3
    
    # Scrap gravitation speed (in pixels/second)
    scrap_gravitation_speed = 250
    
    # Starting position of messages
    message_x = width / 2
    message_y = height / 2 - 100
    
    # Message duration (in seconds)
    message_duration = 3
    
    # Message scroll speed (in pixels/second)
    message_scroll_speed = 80
