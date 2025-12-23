from .config import read_config
from .paths import find_repo_root, pecko_dir, config_path, get_root


config_path = config_path(get_root())
config = read_config(config_path)
print(config)