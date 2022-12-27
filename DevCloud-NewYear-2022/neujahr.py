#!/usr/bin/env python3
import json
import math
import os
import pathlib
import random
import re
import shutil
import sys

cfg_dir = os.path.join(
            os.getenv("XFG_CONFIG_HOME", os.path.expanduser("~/.config")),
            "neujahr"
        )
cfg_path = os.path.join( cfg_dir, "config.json" )
argv = sys.argv[1:]

# print an error and then exit with error code
def error(message):
    print(f"error: {message}")
    exit(1)

# create the configuration file if it does not exists
def create_cfg():
    try:
        # we first check if it does exists
        open(cfg_path, "r")
    except:
        os.system(f"mkdir -p \"{cfg_dir}\"")
        os.system(f"touch \"{cfg_path}\"")
        with open(cfg_path, "w+") as f:
            f.write("{ \"data\": [] }")

# parse the config file to a JSON-object
def parse_cfg():
    create_cfg()
    with open(cfg_path, "r") as f:
        return json.loads("\n".join(f.readlines()))

# save the config file with a new config
def save_cfg(config):
    create_cfg()
    with open(cfg_path, "w") as f:
        f.write(json.dumps(config, indent="\t"))

if len(argv) < 1:
    error("please provide a command to execute.")

cmd = argv[0]

if cmd == "intro":
    print("""
Hi!

This program allows you to save your "Neujahrs Vorsätze"
or in english "new year's resolutions".

You can add those by running
    $ neujahr.py add
then, they will be saved in a config for later usage.

Also I would recommend adding a automatic call for this
program to your shell entry file.
If you use bash, it it usually your bashrc at `~/.bashrc`.
There you can append the following snippet at the end of
the file:
    neujahr.py run

For this to work, you have to put the `neujahr.py` file
in a directory that is included in your `PATH` environ-
ment variable. I recommend putting the script to a place
like `~/.local/bin`.

If there are any questions left, feel free to write me
on Discord: Marius#0686
""")
elif cmd == "run":
    config = parse_cfg()
    data = config["data"]
    if len(data) < 1:
        print("warning: there is currently no data provided. please add some to run 'neujahr.py'.")
        print("tip: you can add data by executing 'neujahr.py add'")
        exit(0)

    chance = 0
    try:
        # we want that 0 < chance < 1
        # 0 would mean that it cannot be run
        # 1 would mean that it is runned every time
        chance = max(min(config["chance"], 1), 0)
    except:
        chance = 0.2

    if random.random() > chance:
        exit(0)

    random = data[math.floor(random.random() * len(data))]

    # FIXME:
    # the following code SHOULD center print the
    # message on an empty screen and this also
    # kind of works. but this does not work really
    # and i just don't want to fix it *shrug*

    size = shutil.get_terminal_size()
    mlen = len(random)
    padding_top = math.floor(size.lines / 2);

    os.system('cls' if os.name == 'nt' else 'clear')

    print("(press ENTER to continue)")

    for i in range(0, padding_top):
        print("")

    print(random.center(size.columns))

    for i in range(0, size.lines - padding_top - mlen):
        print("")

    input()
elif cmd == "add":
    print("info: please input now the data you want to add.")
    print("tip: you can exit the prompt with '.exit'.")
    print("tip: you can break your current session with '.break'. that won't add the befor entered elements to the data.")
    new_data = []
    while True:
        inp = input("> ").strip()
        if len(inp) < 1:
            pass
        if inp == ".exit":
            break
        if inp == ".break":
            print("BREAK!")
            print("All entered elements won't be added to the config.")
            exit(0)
        new_data.append(inp)
        print("(added 1 element)")
    config = parse_cfg()
    current_data = config["data"]
    current_data.extend(new_data)
    config["data"] = current_data
    save_cfg(config)
    print(f"info: added {len(new_data)} elements. Now having {len(current_data)} elements.")
elif cmd == "remove":
    config = parse_cfg()
    data = config["data"]

    for i in range(0, len(data)):
        print(f"[{i}] {data[i]}")

    print("\n\n")
    raw = input("please provide a comma-seperated list of the elements you want to remove (by index):\n")
    to_remove = list(map(int, re.split(r",\s?", raw)))

    idx = 0
    for el in to_remove:
        # we subtract idx because we already removed
        # elements from the base array so we need
        # to access the new index on the base array
        # with the provided index of the old array.
        del data[el - idx]
        idx += 1

    config["data"] = data
    save_cfg(config)

    print(f"info: removed {len(to_remove)} items from the list.")
elif cmd == "raw":
    print(json.dumps(parse_cfg(), indent="\t"))
elif cmd == "help":
    print(f"""
neujahr.py v1.0.0

USAGE
  neujahr.py <command>

COMMANDS
  add     add data to the program.
  help    show this help message.
  intro   shows an introduction to
          this program.
  raw     print out all data.
  remove  remove elements from the
          data.
  run     let the program print some
          data to the console with a
          possibility.

CONFIG
  {cfg_path}
""")
else:
    error(f"the command you provided ({cmd}) does not exists.")
