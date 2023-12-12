import fnmatch
import os
import sys
import time


def parse_arguments(args):
    path = args[1]
    options = []
    arguments = []
    output_location = None

    for arg in args[2:]:
        if arg.startswith("-"):
            options.append(arg)
        elif arg == ">":
            output_location = args[-1] + "!"
            break
        elif arg == ">>":
            output_location = args[-1]
            break
        else:
            arguments.append(arg)

    return path, options, arguments, output_location


def findDirectories(root):
    directories = []
    for dir_path, dir_names, filenames in os.walk(root):
        for dir in dir_names:
            directories.append(os.path.join(dir_path, dir))
    return directories


def findByName(path, file_name_pattern):
    if fnmatch.fnmatch(path, file_name_pattern):
        return path
    else:
        return None


def findBySize(path, file_size):
    if file_size.startswith("+"):
        if os.path.getsize(path) > int(file_size[1:]):
            return path
    elif file_size.startswith("-"):
        if os.path.getsize(path) < int(file_size[1:]):
            return path
    elif file_size.startswith("="):
        if os.path.getsize(path) == int(file_size[1:]):
            return path
    else:
        print("Error: Invalid file size")
        sys.exit(1)


def findByTimeCreated(path, file_time):
    createdTime = os.path.getctime(path)
    currentTime = time.time()

    timeDifference = currentTime - createdTime

    if timeDifference <= int(file_time):
        return path
    else:
        return None


def findByTimeModified(path, file_time):
    moddedTime = os.path.getmtime(path)
    currentTime = time.time()

    timeDifference = currentTime - moddedTime

    if timeDifference <= int(file_time):
        return path
    else:
        return None


def findByTimeAccessed(path, file_time):
    accessedTime = os.path.getatime(path)
    currentTime = time.time()

    timeDifference = currentTime - accessedTime

    if timeDifference <= int(file_time):
        return path
    else:
        return None


def find(input):
    path, options, arguments, outputLocation = parse_arguments(input)

    output = []
    try:
        for dir_path, dir_names, filenames in os.walk(path):
            for option in options:
                if option == "-type":
                    file_type = arguments[options.index(option)]
                    if file_type == 'f':
                        for file in filenames:
                            file_path = os.path.join(dir_path, file)
                            output.append(file_path)
                    elif file_type == 'd':
                        for dir in dir_names:
                            output.append(os.path.join(dir_path, dir))

                elif option == "-name":
                    file_name_pattern = arguments[options.index(option)]
                    for file in filenames:
                        file_path = os.path.join(dir_path, file)
                        if findByName(file_path, file_name_pattern) is not None:
                            output.append(file_path)

                elif option == "-size":
                    file_size = arguments[options.index(option)]
                    for file in filenames:
                        file_path = os.path.join(dir_path, file)
                        if findBySize(file_path, file_size) is not None:
                            output.append(file_path)

                elif option == "-ctime":
                    file_time = arguments[options.index(option)]
                    for file in filenames:
                        file_path = os.path.join(dir_path, file)
                        if findByTimeCreated(file_path, file_time) is not None:
                            output.append(file_path)

                elif option == "-mtime":
                    file_time = arguments[options.index(option)]
                    for file in filenames:
                        file_path = os.path.join(dir_path, file)
                        if findByTimeModified(file_path, file_time) is not None:
                            output.append(file_path)

                elif option == "-atime":
                    file_time = arguments[options.index(option)]
                    for file in filenames:
                        file_path = os.path.join(dir_path, file)
                        if findByTimeAccessed(file_path, file_time) is not None:
                            output.append(file_path)
                else:
                    raise Exception("Invalid option")

        appearances = {}
        for path in output:
            if path in appearances:
                appearances[path] += 1
            else:
                appearances[path] = 1

        output = []
        for path in appearances:
            if appearances[path] == len(options):
                output.append(path)

        if outputLocation is not None:
            if outputLocation.endswith("!"):
                with open(outputLocation[:-1], "w") as f:
                    f.write("\n".join(output))
            else:
                with open(outputLocation, "a") as f:
                    f.write("\n".join(output))
        else:
            print("\n".join(output))

    except FileNotFoundError:
        print(f"Error: Directory not found - {path}")
    except PermissionError:
        print(f"Error: Permission issue accessing files in directory - {path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


find(sys.argv)
