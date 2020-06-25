#!/usr/bin/env python3

import fileinput
import getopt
import os
import sys

affected_envs = []
ignore_dev = False
do_sync = True
reqs_file_path = "requirements/" if os.path.isdir("./requirements") else "./"


def parse_args():
    global ignore_dev
    global do_sync

    options, arguments = getopt.gnu_getopt(
        sys.argv[1:], "nse:", ["no-dev", "no-sync", "env="]
    )

    for opt, arg in options:
        if opt in ("-e", "--env"):
            push_env(arg)

        elif opt in ("-n", "--no-dev"):
            ignore_dev = True

        elif opt in ("-s", "--no-sync"):
            do_sync = False

    return arguments


def main():
    arguments = parse_args()
    if not arguments:
        print("no argument passed, nothing to do")
        return

    func_to_run = arguments[0]

    if func_to_run == "install":
        return install(arguments)
    elif func_to_run in ("remove", "uninstall"):
        return remove(arguments[1:])
    elif func_to_run == "sync":
        return sync()
    elif func_to_run == "compile":
        return compile()


def push_env(env):
    global affected_envs

    affected_envs.append(env)


def remove(arguments):
    if affected_envs:
        for env in affected_envs:
            filepath = f"{reqs_file_path}requirements-{env}.in"
            if os.path.exists(filepath):
                remove_reqs_from_file(filepath, arguments)
                os.system(f"pip-compile {filepath}")

    else:
        remove_reqs_from_file(f"{reqs_file_path}requirements.in", arguments)
        os.system(f"pip-compile {reqs_file_path}requirements.in")

    if do_sync:
        sync()


def remove_reqs_from_file(filename, reqs):
    with fileinput.FileInput(filename, inplace=True) as f:
        for line in f:
            if line.strip() not in reqs:
                print(line, end="")


def sync():
    if affected_envs:
        files_to_sync = f"{reqs_file_path}requirements.txt"
        for env in affected_envs:
            if os.path.exists(f"{reqs_file_path}requirements-{env}.txt"):
                files_to_sync += f" {reqs_file_path}requirements-{env}.txt"

        os.system(f"pip-sync {files_to_sync}")

    else:
        if ignore_dev or not os.path.exists(f"{reqs_file_path}requirements-dev.txt"):
            os.system(f"pip-sync {reqs_file_path}requirements.txt")
        else:
            os.system(
                f"pip-sync {reqs_file_path}requirements.txt {reqs_file_path}requirements-dev.txt"
            )


def compile():
    for file in os.listdir(f"{reqs_file_path}"):
        if file.endswith(".in"):
            os.system(f"pip-compile {reqs_file_path}{file}")


def install(arguments):
    if len(arguments) <= 1:
        print("no package name provided, cannot install")
        return

    if affected_envs:
        for env in affected_envs:
            filepath = f"{reqs_file_path}requirements-{env}.in"
            if not os.path.exists(filepath):
                with open(filepath, "w") as f:
                    f.write("-c requirements.txt")

            add_reqs_to_file(filepath, arguments[1:])
            os.system(f"pip-compile {filepath}")

    else:
        # no env specified, install to reqs.in
        add_reqs_to_file(f"{reqs_file_path}requirements.in", arguments[1:])
        os.system(f"pip-compile {reqs_file_path}requirements.in")

    if do_sync:
        sync()


def add_reqs_to_file(filename, reqs):
    with open(filename, "a") as f:
        for arg in reqs:
            f.write(f"{arg}\n")


if __name__ == "__main__":
    main()
