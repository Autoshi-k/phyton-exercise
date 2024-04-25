def parsefile(filename):
    f = open(filename, "r")
    lines = f.readlines()
    f.close()

    for index, line in enumerate(lines):
        if line.endswith("\n"):
            lines[index] = line[:-1]

    # report = shit(lines, 0, False, {}, {}, "")
    print("-------------------")
    # print(report)

    print("-------------------")
    print(send_help(lines, 0, {}, {}))


def shit(lines, index, isArray, parent, obj, break_key) -> {} or []:
    if len(lines) == index or break_key and lines[index].endswith(break_key):
        return obj

    print(" - ", obj, type(obj), break_key)

    if type(parent) == list and lines[index].startswith("::::"):
        parent.append(shit(lines, index + 1, [], {}, break_key))
        return parent
    if lines[index].startswith(":") and not lines[index].startswith("::"):
        obj[lines[index].strip(":")] = shit(lines, index + 1, False, {}, {}, "::")
        return obj
    elif lines[index].startswith("[") and not lines[index].startswith("[["):
        print("elif array", lines[index])
        obj[lines[index].strip("[]")] = shit(lines, index + 1, True, [], {}, "]]")
        return obj
    else:
        print("else", lines[index], break_key)
        key_value_line = lines[index].split("::")
        obj[key_value_line[0]] = key_value_line[1]
        if not isArray:
            return shit(lines, index + 1, False, {}, obj, break_key)
        else:
            parent.append(shit(lines, index, True, parent, {}, break_key))
            return parent
            # {key_value_line[0]: key_value_line[1]}


def transform_input(lines):
    result = {}
    current_obj = result
    current_key = None
    stack = []

    for line in lines:
        if line.startswith(':'):
            current_key = line.strip(':')
            current_obj[current_key] = {}
            stack.append((current_obj, current_key))
            current_obj = current_obj[current_key]
        elif line.startswith('['):
            current_key = 'array'
            current_obj[current_key] = []
            stack.append((current_obj, current_key))
            current_obj = current_obj[current_key]
        elif line.startswith(']'):
            current_obj, current_key = stack.pop()
        elif line.startswith('::'):
            current_obj, current_key = stack.pop()
            current_obj, current_key = stack.pop()
        else:
            key, value = line.split('::')
            current_obj[key] = value

    return result


def send_help(lines, index, parent, child) -> {} or []:
    if len(lines) == index:
        return child

    elif lines[index].startswith("::::"):
        parent.append(child)
        return send_help(lines, index + 1, parent, {})

    elif lines[index].startswith("[["):
        parent.append(child)
        return parent

    elif lines[index].startswith('['):
        if type(parent) == list:
            parent.append(child)
            parent.append(send_help(lines, index + 1, [], {}))
        else:
            parent = child
            parent[lines[index].strip("[]")] = send_help(lines, index + 1, [], {})

        return parent

    elif lines[index].startswith("::"):
        parent = child
        return parent

    elif lines[index].startswith(":"):
        parent = child
        parent[lines[index].strip(":")] = send_help(lines, index + 1, {}, {})
        return parent

    else:
        key_value_line = lines[index].split("::")
        child[key_value_line[0]] = key_value_line[1]

        return send_help(lines, index + 1, parent, child)
