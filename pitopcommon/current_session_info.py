from os import listdir, environ

from pitopcommon.logger import PTLogger


def get_current_user():
    '''
    Returns the name of the user that invoked this function

            Returns:
                    user (str): String representing the user
    '''
    if environ.get('SUDO_USER'):
        return environ.get('SUDO_USER')
    elif environ.get('USER'):
        return environ.get('USER')
    else:
        return get_user_using_first_display()


def get_list_of_displays() -> int:
    def represents_int(s):
        try:
            int(s)
            return True
        except ValueError:
            return False
    displays = [f.replace('X', ':') for f in listdir(
        "/tmp/.X11-unix/") if represents_int(f.replace('X', ''))]
    PTLogger.debug("List of displays found: {}".format(displays))
    return displays


def get_first_display() -> int:
    displays = get_list_of_displays()
    first_display = displays[0] if len(displays) > 0 else None
    PTLogger.debug("First display is: {}".format(first_display))
    return first_display


def get_user_using_display(display_no):
    '''
    Returns the name of the user that is currently using the defined display

            Returns:
                    user (str): String representing the user
    '''
    from pitopcommon.command_runner import run_command
    user = None
    for line in run_command("who", timeout=1).split("\n"):
        if "(%s)" % display_no in line:
            fields = line.split(" ")
            if len(fields) > 1:
                user = fields[0]
                break
    return user


def get_user_using_first_display():
    '''
    Returns the name of the user that is currently using the first available display

    This function is useful when targeting a particular active user by something that is running
    as something different to the current user, where `get_current_user()` would be incorrect.

    For example, with a system service, `get_current_user()` would return "root" (from the USER
    environment variable), where the active user (e.g. "pi") is actually wanted.

            Returns:
                    user (str): String representing the user
    '''
    return get_user_using_display(get_first_display())
