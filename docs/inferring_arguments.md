# Basic Command Argument Reverse-Engineering Guide
Very fast and loose guide, make sure you understand the .gsc format first (see [Gsc Info](docs/gsc_info.md))

If you're decompiling your .gsc files and getting orphaned messages or a bunch of nonsense commands (i.e. #0 #0 #0 #0), this generally means your arguments for some commands are incorrect, which is interfering with how the script is interpreting the .gsc file

## Requirements:
- the game
- a decent hex editor (I recommend HxD because of the decimal offset setting (click the dropdown at the top that says "hex" and switch it to "dec"), int conversion in the right pane, etc.; wxMEdit is also good to have if you need to view the file strings (because of Shift-JIS support))
- Process Monitor (aka ProcMon) (for finding what .gsc file is being referenced by the game)
- garBRO/RaiLTools to obtain the .scr files themselves
- the CommandLibrary in gscSCD.py for reference(and possibly the ConnectedStringsLibrary if applicable)
- the decompiled .txt file

## Finding a scene:
- Open ProcMon and open the Filter window (ctrl+L or the blue funnel-looking icon)
- Add two entries:
    - "Process Name is \<game executable>.exe"
    - "Path ends with .gsc"
- Launch your game; when opening the scene in question, ProcMon should print the .gsc files being accessed
    - if there's multiple .gsc files printed in the log, open each of them with a hex editor (wxMEdit with View -> Encoding -> Shift-JIS), and check which .gsc file contains the scene dialog
    - (extract the .gsc files from scr.xfl via garBRO/RaiLTools first)

## Finding problematic commands:
- This is generally done by first locating known good commands, then searching forward/backward from the command to find a command you know is being interpreted incorrectly (e.g. a correctly read MESSAGE followed by other non-MESSAGE commands, and then later a MESSAGE that isn't read a MESSAGE by the script, so has an orphaned string); (at least) one of the commands in between is probably causing the issue
    - the less commands in-between, the easier it is to pinpoint what command is causing the issue
- Example steps of what might happen when resolving the prior MESSAGE example:
    - first, find the offset for the command for the last known correct MESSAGE (51 00) in a hex editor, and count the argument offset after it (i.e. "iiiiiii" means you shift the offset forward by 4x7=28 bytes)
	- then, you use the hex editor's hex string search feature to find the neighboring orphaned message (51 00)
    - you find there's 6 bytes between the offset marking the end of the first message's args and the offset marking the start of the command for the orphaned message, which would line up with 2 bytes for the command and 4 bytes for an "i" argument
	- current CommandLibrary lists the arguments for the command in-between the two MESSAGEs to be "ii", and after correcting it to "i", that section now decompiles properly
- A good indicator is also a command followed by a bunch of nonsense commands (e.g. 0x0) that aren't defined in CommandLibrary
    - it could be that the command directly preceding the nonsense is eating a following command's opcode as an argument, and the nonsense commands are arguments for the following command (original command's arguments are too long)
    - or that the nonsense commands are arguments for the command that are being interpreted as commands (original command's arguments are too short)
- General rules of thumb for arguments are:
    - if starting with arguments known working in an older engine version, they'll grow longer (i.e. "ii" becomes "iii")
    - if starting with arguments known working in a newer engine version, they'll shrink (i.e. "iiii" becomes "ii")
    - arguments are always fixed length, "i" and "h" are generally not mixed (you'll see "hh" or "iiii" but "iiih" is rare)
- Commands can generally be confirmed to have the correct arguments if:
    - they occur back to back (MESSAGE MESSAGE MESSAGE MESSAGE MESSAGE), or between two instances of already known good commands with no other commands between them (MESSAGE IMAGE_DEF MESSAGE)
    - you know what they do (not that all the arguments are defined, but that you know the command is being properly executed in-game, like MESSAGE), so you're certain it's not a misinterpreted argument
- If you're unsure as to whether a command is actually a command or an argument for a previous command being interpreted as one (e.g. you're seeing 0x3 (JUMP) when there are no branching paths in the scene), editing the decompiled script can help
    - i.e. if the mystery JUMP is pointing to the @4 label, move the label to somewhere else in the file and recompile; if the game jumps to that location, it's a proper JUMP command

## Locating command offsets:
- gscSCD ~an epic~ has a lot of commented out debug print commands, including ones that print out the offset for each command parsed
    - uncomment lines flagged with #DEBUG, then run `python3 gscSCD.py > <file name>_log.txt` (to save the terminal output to a file), decompile \<file name> in question, and close the window to save the output
    - debug lines that reference "Reader" refer to a variable in gscSCD used to store the offset of the command being parsed
        - Reader's position is the decimal offset from the start of the Command section
        - when you see "Reader is at \<position>" before "found Command", that means the two bytes for the command are located at the decimal offset \<position> + \<header length> - 2
        - (header length is listed on the first line of the decompiled txt file)
    - the debug lines don't print the command arguments (except for MESSAGE, APPEND_MESSAGE, and CHOICE), but you can generally determine which instance of a command is being referred to based on what the surrounding commands are