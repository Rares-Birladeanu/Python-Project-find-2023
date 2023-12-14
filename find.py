import fnmatch
import os
import sys
import time


def parse_arguments(args):
    if args[1] == ".":
        path = os.getcwd()
    else:
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


def find_by_name(path, file_name_pattern):

    file_name = os.path.basename(path)

    if fnmatch.fnmatch(file_name, file_name_pattern):
        return path
    else:
        return None


def find_by_size_file(path, file_size):
    size = os.path.getsize(path)
    if file_size.startswith("m"):
        if size > int(file_size[1:]):
            return path
    elif file_size.startswith("l"):
        if size < int(file_size[1:]):
            return path
    elif file_size.startswith("e"):
        if size == int(file_size[1:]):
            return path


def find_by_size_dir(path, file_size):
    size = 0
    for dir_path, dir_names, filenames in os.walk(path):
        for file in filenames:
            size += os.path.getsize(os.path.join(dir_path, file))
    if file_size.startswith("m"):
        if size > int(file_size[1:]):
            return path
    elif file_size.startswith("l"):
        if size < int(file_size[1:]):
            return path
    elif file_size.startswith("e"):
        if size == int(file_size[1:]):
            return path


def find_by_time_created(path, file_time):

    created_time = os.path.getctime(path)
    current_time = time.time()

    time_difference = current_time - created_time

    if time_difference <= int(file_time):
        return path
    else:
        return None


def find_by_time_modified(path, file_time):
    modded_time = os.path.getmtime(path)
    current_time = time.time()

    time_difference = current_time - modded_time

    if time_difference <= int(file_time):
        return path
    else:
        return None


def find_by_time_accessed(path, file_time):
    accessed_time = os.path.getatime(path)
    current_time = time.time()

    time_difference = current_time - accessed_time

    if time_difference <= int(file_time):
        return path
    else:
        return None


def find(args):
    path, options, arguments, output_location = parse_arguments(args)

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
                        if find_by_name(file_path, file_name_pattern) is not None:
                            output.append(file_path)
                    for dir in dir_names:
                        current_dir_path = os.path.join(dir_path, dir)
                        if find_by_name(current_dir_path, file_name_pattern) is not None:
                            output.append(current_dir_path)

                elif option == "-size":
                    file_size = arguments[options.index(option)]
                    for file in filenames:
                        file_path = os.path.join(dir_path, file)
                        if find_by_size_file(file_path, file_size) is not None:
                            output.append(file_path)
                    for dir in dir_names:
                        current_dir_path = os.path.join(dir_path, dir)
                        if find_by_size_dir(current_dir_path, file_size) is not None:
                            output.append(current_dir_path)

                elif option == "-ctime":
                    file_time = arguments[options.index(option)]
                    for file in filenames:
                        file_path = os.path.join(dir_path, file)
                        if find_by_time_created(file_path, file_time) is not None:
                            output.append(file_path)
                    for dir in dir_names:
                        current_dir_path = os.path.join(dir_path, dir)
                        if find_by_time_created(current_dir_path, file_time) is not None:
                            output.append(current_dir_path)

                elif option == "-mtime":
                    file_time = arguments[options.index(option)]
                    for file in filenames:
                        file_path = os.path.join(dir_path, file)
                        if find_by_time_modified(file_path, file_time) is not None:
                            output.append(file_path)
                    for dir in dir_names:
                        current_dir_path = os.path.join(dir_path, dir)
                        if find_by_time_modified(current_dir_path, file_time) is not None:
                            output.append(current_dir_path)

                elif option == "-atime":
                    file_time = arguments[options.index(option)]
                    for file in filenames:
                        file_path = os.path.join(dir_path, file)
                        if find_by_time_accessed(file_path, file_time) is not None:
                            output.append(file_path)
                    for dir in dir_names:
                        current_dir_path = os.path.join(dir_path, dir)
                        if find_by_time_accessed(current_dir_path, file_time) is not None:
                            output.append(current_dir_path)
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

        if output_location is not None:
            if output_location.endswith("!"):
                with open(output_location[:-1], "w") as f:
                    f.write("\n".join(output))
            else:
                with open(output_location, "a") as f:
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
