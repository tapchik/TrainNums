import yaml

class AssetsFileNotFound(Exception):
    pass

def ReadAssetsFile(assets_file: str) -> dict[str, str]:
    try: 
        read_assets = open(assets_file)
        data_from_assets_file = yaml.safe_load(read_assets)
    except FileNotFoundError:
        raise AssetsFileNotFound("Error. Specified assets file not found. ")
    read_assets.close()
    return data_from_assets_file