import os.path
import traceback
from os import path

from configuration import Configuration

from clear import clear_symlinks
from common import print_cute_message
from common import BACKUP_SUFFIX


def create_symlinks(config: Configuration):
    print_cute_message("# [CREATE] STARTING #")

    total = 0
    for drive in config.final_scanned_disks:
        print(f"\tCHECK {drive}:")
        roms_path = f"{drive}:{config.external_roms_path}"
        if path.exists(roms_path):
            print(f"\t\tFOUND [{roms_path}]")
            for console in next(os.walk(roms_path))[1]:
                internal_console_path = f"{config.internal_roms_path + console}"
                external_console_path = roms_path + console
                if path.exists(internal_console_path) and not path.islink(internal_console_path):
                    print(f"\t\tBACKUP [{internal_console_path}] -> [{internal_console_path + BACKUP_SUFFIX}]")
                    os.rename(internal_console_path, internal_console_path + BACKUP_SUFFIX)
                elif path.islink(internal_console_path):
                    print(
                        f"\t\tSKIPPING_LINK [{internal_console_path}] POINTS_TO [{os.readlink(internal_console_path)}]")
                    continue

                print(f"\t\tCREATING_LINK [{external_console_path}] -> [{internal_console_path}]")
                total += 1
                os.symlink(external_console_path, internal_console_path)
        else:
            print(f"\t\tSKIPPING {drive}:")

    final_message = f"# [CREATE] FINISHED - [{str(total)}] SYMLINKS CREATED #"
    print_cute_message(final_message)


if __name__ == '__main__':
    config = Configuration()
    try:
        clear_symlinks(config)
        print()
        create_symlinks(config)
    except Exception as e:
        traceback.print_exc()
        print()
        print(f"An error occurred: {str(e)}")
    finally:
        input("Press [ENTER] to continue...")
