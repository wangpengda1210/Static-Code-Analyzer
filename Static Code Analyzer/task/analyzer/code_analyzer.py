# write your code here
import os
import sys
import re
import ast


def check_length(string):
    return len(string) > 79


def check_indent(string):
    indent_length = 0
    for c in string:
        if c == " ":
            indent_length += 1
        else:
            break
    return indent_length % 4 != 0


def check_semicolon(string: str):
    comment_position = string.find("#")
    sub_line = string[:comment_position].strip()
    return sub_line.endswith(";")


def check_comment_space(string: str):
    comment_position = string.find("#")
    if comment_position == -1 or comment_position == 0:
        return False

    sub_line = string[:comment_position]
    return not sub_line.endswith("  ")


def check_todo(string: str):
    comment_position = string.find("#")
    comment = string[comment_position:]
    return "TODO" in comment.upper()


def check_blank_line(string: str):
    return string.strip() == ""


def check_space(string: str):
    space_count = 0

    for s in string:
        if s == " ":
            space_count += 1
        else:
            break

    return space_count != 1


def check_camel_case(class_name):
    match = re.compile("([A-Z][a-z0-9]*)+").match(class_name)
    return match is None or match.group() != class_name


def check_snake_case(function_name):
    match = re.compile("_*[a-z0-9]+(_[a-z0-9]+)*_*").match(function_name)
    return match is None or match.group() != function_name


def check_mutable(arg):
    return isinstance(arg, ast.List)


def check_file(path):
    with open(path, 'r') as f:

        blank_line = 0
        in_function = False

        for index, line in enumerate(f.readlines()):
            if check_length(line):
                print(f'{path}: Line {index + 1}: S001 Too long')

            if check_indent(line):
                print(f'{path}: Line {index + 1}: S002 Indentation is not a multiple of four')

            if check_semicolon(line):
                print(f'{path}: Line {index + 1}: S003 Unnecessary semicolon'
                      f' after a statement')

            if check_comment_space(line):
                print(f'{path}: Line {index + 1}: S004 Less than two spaces'
                      f' before inline comments')

            if check_todo(line):
                print(f'{path}: Line {index + 1}: S005 TODO found')

            if check_blank_line(line):
                in_function = False
                blank_line += 1
            else:
                if blank_line > 2:
                    print(f'{path}: Line {index + 1}: S006 More than two blank lines '
                          f'preceding a code line')
                blank_line = 0

            line = line.strip()
            if line.startswith("class"):
                class_def = line[5:-1]

                bracket_position = class_def.strip().find("(")
                class_name = class_def.strip() if bracket_position == -1 else \
                    class_def.strip()[:class_def.find("(") - 1]

                if check_space(class_def):
                    print(f"{path}: Line {index + 1}: S007 Too many spaces after 'class'")

                if check_camel_case(class_name):
                    print(f"{path}: Line {index + 1}: S008 Class name '{class_name}'"
                          f" should use CamelCase")
            elif line.startswith("def"):
                in_function = True

                function_def = line[3:-1]
                function_name = function_def.strip()[:function_def.strip().find("(")]

                if check_space(function_def):
                    print(f"{path}: Line {index + 1}: S007 Too many spaces after 'def'")

                if check_snake_case(function_name):
                    print(f"{path}: Line {index + 1}: S009 Function name '{function_name}'"
                          f" should use snake_case")

                arguments = ast.parse(line.strip() + "pass").body[0].args
                for arg in arguments.args:
                    if check_snake_case(arg.arg):
                        print(f"{path}: Line {index + 1}: S010 Argument name '{arg.arg}'"
                              f" should use snake_case")

                for default_arg in arguments.defaults:
                    if check_mutable(default_arg):
                        print(f"{path}: Line {index + 1}: S012 The default argument value"
                              f" is mutable")
            elif in_function:
                line_parse = ast.parse(line.strip())
                line_type = line_parse.body[0]
                if isinstance(line_type, ast.Assign):
                    var = line_type.targets[0]
                    if isinstance(var, ast.Name) and check_snake_case(var.id):
                        print(f"{path}: Line {index + 1}: S011 Variable '{var.id}' "
                              f"in function should be snake_case")


def check_path(path):
    if os.path.isfile(path):
        check_file(path)
    elif os.path.isdir(path):
        for file_name in os.listdir(path):
            check_path(os.path.join(path, file_name))


check_path(sys.argv[1])
