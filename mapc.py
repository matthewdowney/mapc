import os
import sys
import subprocess

def getArg(flag, args):
    if flag not in args: return []

    # trim match to the first flag
    match = args
    while match[0] != flag: match = match[1:]

    # trim match to the next flag
    isFlag = lambda arg: len(arg) == 2 and arg[0] == "-"
    match = match[1:]
    final = []
    while not match == [] and not isFlag(match[0]): 
        final.append(match[0])
        match = match[1:]
    return final

def execute(dirName, cmd):
    path = os.path.abspath(dirName)
    cwd = os.getcwd()
    try:
        os.chdir(path)
        os.system(cmd)
        os.chdir(cwd)
    except OSError:
        print("Couldn't chdir %s" % path)

if len(sys.argv) == 1:
    print("Maps a command across directories within the working directory.")
    print("Usage:\n\t%s -c <command>\n" % sys.argv[0])
    print("Options\n\t-o dirs ...\tDirectories for which the command will be executed first, in the order specified.\n" +
          "\t-i dirs ...\tDirectories which will be ignored.\n" +
          "\t-c command\tThe command to execute within each directory.\n")
    print("For example, if the current working directory contains many individual git\n" +
          "repositories and one non-git directory, to pull on each repository: \n\t" +
          "%s -c git pull -i <non-git dir>" % sys.argv[0]) 

# Parse the command and directories to prioritize/ignore from the flags
get = lambda flag: getArg(flag, sys.argv)
ordered = get("-o")
ignores = get("-i")
command = " ".join(get("-c"))

# Map relative directories -> abspaths
ordered = map(os.path.abspath, ordered)
ignores = map(os.path.abspath, ignores)

# Filter out ignores & non dirs from the prioritized
ordered = filter(lambda x: x not in ignores, ordered)
if ordered != filter(os.path.isdir, ordered):
    print "Ignoring non directories %s" % filter(lambda x: not os.path.isdir(x), ordered)
ordered = filter(os.path.isdir, ordered)

# The rest of the directories are then those that aren't ordered but are in the working directory
rest = filter(os.path.isdir, os.listdir(os.getcwd()))
rest = map(os.path.abspath, rest)
rest = filter(lambda x: x not in ignores and x not in ordered, rest)

# Execute the command across the ordered directories, and then the rest
execCmd = lambda x: execute(x, command)
map(execCmd, ordered)
map(execCmd, rest)