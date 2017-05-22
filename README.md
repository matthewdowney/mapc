# mapc
Easily execute the same bash command within multiple subdirectories.


I wrote this to deprecate the need for multiple bash `for` loops. 
I have a directory which contains many git repositories which are also maven projects, and two of the maven projects must be built before the rest.
To do this I would execute something like
```
$ for file in $(ls); do cd $file && git pull && cd ..; done
$ for file in dependencyA dependencyB; do cd $file && mvn clean install && cd ..; done
$ for file in $(ls -I dependencyA dependencyB); do cd $file && mvn clean install && cd ..; done
```
So I thought a more agreeable syntax would incorporate some sort of [mapping function](https://en.wikipedia.org/wiki/Map_(higher-order_function)) across an ordered list of directories.
To do the same with `mapc` I would use this one liner
```
$ mapc -o dependencyA dependencyB -c "git pull && mvn clean install"
```
which _maps_ the function `git pull && mvn clean install` across each directory within the working dir, with the optional `-o` parameter to indicate that the function should first be performed within the `dependencyA` directory, then `dependencyB`, and finally the rest.

There's also a `-i` flag to exclude directories from the function.

# Usage

```
matthew@inspiron:~$ python mapc.py
Maps a command across directories within the working directory.
Usage:
    mapc.py -c <command>

Options
    -o dirs ... Directories for which the command will be executed first, in the order specified.
    -i dirs ... Directories which will be ignored.
    -O dirs ... The ONLY directories for which the command will be executed, in order. Supercedes -o but takes -i into account.
    -c command  The command to execute within each directory.

For example, if the current working directory contains many individual git
repositories and one non-git directory, to pull on each repository: 
    mapc.py -c git pull -i <non-git dir>
Including %N within a command will replace %N with the name of the current directory
Any directories listed in .mapcignore will be ignored.
```
