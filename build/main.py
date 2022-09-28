import os
import shutil
from func.compile import *
from func.config import *
from func.constants import *
from func.setup_env import *


def main() -> None:
    setup_env()
    config_parse()
    compile()

    shutil.rmtree(os.path.join(build_dir))

if __name__ == "__main__":
    main()