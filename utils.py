def get_image_url(product):
    url = product.get('gallery').get("images")[0].get('template')
    fixed_url = "https:" + url.replace("{SEQUENCE}", "1").replace("{WIDTH}", "920")
    return fixed_url
