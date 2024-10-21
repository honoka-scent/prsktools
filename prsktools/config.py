import toml


def init_config():
    config = {
        "output": {
            "expert": False,
            "master": False,
            "append": False,
            "ap": False,
        },
    }
    with open("config.toml", "w") as f:
        toml.dump(config, f)


def load_config():
    with open("config.toml", "r") as f:
        config = toml.load(f)
    return config


def is_output_expert(config=None):
    if config is None:
        config = load_config()
    return config["output"]["expert"]


def is_output_master(config=None):
    if config is None:
        config = load_config()
    return config["output"]["master"]


def is_output_append(config=None):
    if config is None:
        config = load_config()
    return config["output"]["append"]


def is_output_fc(config=None):
    if config is None:
        config = load_config()
    return config["output"]["fc"]


def is_output_ap(config=None):
    if config is None:
        config = load_config()
    return config["output"]["ap"]
