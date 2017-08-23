from config.property_reader import PropertyReader


class Properties:

    p = PropertyReader("config.properties")

    depth = p.depth
    mode = p.mode
    device = p.device
    folder = p.folder
    image_check = p.image_check
    spell_check = p.spell_check
    threads = p.threads
    home_page = p.home_page
