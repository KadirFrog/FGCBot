import emoji as emoji_country_flag
import pycountry
import pycountry_convert as pc

def get_country_code_from_emoji(emoji_code):
    country_code = emoji_country_flag.demojize(emoji_code).upper().replace("FLAG_", "").strip(":")
    return country_code
def get_continent_from_country_name(country_name):
    country_alpha2 = pc.country_name_to_country_alpha2(country_name, cn_name_format="default")
    continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
    continent_name = pc.convert_continent_code_to_continent_name(continent_code)
    return continent_name

def get_continent_from_emoji(emoji_code):
    country_name = get_country_code_from_emoji(emoji_code)
    if country_name:
        continent_name = get_continent_from_country_name(country_name.replace("_", " ").title().lstrip().rstrip())
        return continent_name
    return None
