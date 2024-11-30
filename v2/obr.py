
from model.config import get_config, Config
def main():
    config: Config | None = get_config()
    print(config)

if __name__ == "__main__":
    main()