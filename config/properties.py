from config.property_reader import PropertyReader


class Properties:

    p = PropertyReader("config.properties")

    depth = p.depth
    mode = p.mode
    blank_pages_file = p.blank_pages_file
    broken_images_file = p.broken_images_file
    broken_links_file = p.broken_links_file
    error_file = p.error_file
    device = p.device
    folder = p.folder
    crawled_file = p.crawled_file
    queue_file = p.queue_file
    image_check = p.image_check
    spell_check = p.spell_check
    spelling_file = p.spelling_file
    threads = p.threads
    home_page = p.home_page
