class ConfigurationEntity:
    def __init__(self, dogs_source: str, cats_source: str,root_path:str, env: str) -> None:
        self.dogs_source = dogs_source
        self.cats_source = cats_source
        self.root_path = root_path
        self.env = env
