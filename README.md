# gscScriptCompAndDecompiler \~an epic\~
A tool for decompiling and recompiling .gsc script files for the codeX Rscript engine (used by Liar-soft and Rail-soft).

This is a modified version of the [original gscSCD by TesterTesterov](https://github.com/TesterTesterov/gscScriptCompAndDecompiler/tree/master), made to work with Sapphism no Gensou ~an epic~ (also known as Porthole of Sapphism). However, it should still be perfectly compatible with other games as long as the script's arguments are adjusted to the appropriate values (see gscSCD.py's CommandsLibrary and ConnectedStringsLibrary).

This version supports variable header lengths (not just 36 bytes) and fixes some bugs (cp932 instead of shift-JIS for character support, incorrectly parsed dialog should now be written to the file). The script's command arguments have been adjusted to work with Sapphism, but newer games should still be compatible if those arguments are changed back to their old values (see gscSCD.py's CommandsLibrary and ConnectedStringsLibrary). However, the rebuilding feature (.gsc -> .gsc) has been removed.

The primary change, though, is more documentation regarding both the .gsc format and what some commands do.

Tested on:
- [Sapphism no Gensou \~an epic\~](https://vndb.org/r1040)

Original script was tested on:
- [Kusarihime \~Euthanasia\~](https://vndb.org/v37) <for the most part>
- [Sekien no Inganock -What a Beautiful People-](https://vndb.org/v417) <for the most part>
- [Hiragumo-chan -Sengoku Gekokujou Monogatari-](https://vndb.org/v10182) <for the some part>
- [Dungeons & Daimeiwaku -Great Edges in the Abyss-](https://vndb.org/v19579) <for the some part>
- [Alpha-Nighthawk](https://vndb.org/v24470) <for the some part>
- [Albatross Log](https://vndb.org/v3883) <for the most part>
- [Beta-Sixdouze Trial](https://vndb.org/r73649) <for the some part>

For editing of the engine's archive (.xfl), canvas (.lwg), and image (.wcg) files, use either [RailTools](https://github.com/EusthEnoptEron/RaiLTools) or [GARbro](https://github.com/morkt/GARbro) (the latter isn't suitable for canvases editing).

Repacking of .gsc files isn't needed to test edits, just create a `scr` folder in the game directory and place the recompiled .gsc files in there. Script files can generally be reloaded to see new edits without restarting the game by just reloading from a save, but sometimes you need to exit to the title first before loading or else things won't load properly. 

# Info and Usage

This program is designed to work with .gsc files from the codeX RScript engine (also known as the Liar-soft Engine and raiL-soft Engine). The engine is relatively simple, as are its file formats—specifically .gsc—though the latter presents certain issues that are mitigated by a unique decompilation and compilation scheme. However, this scheme can still lead to problems in some cases.

This program allows you to:
1. Decompile .gsc files into .txt format, enabling you to edit scripts freely (within the limits of syntax, commands, etc.). For instance, adding a new message is incredibly easy with this tool.
2. Compile .txt files into .gsc. This allows you to rebuild a .gsc file from the decompiled code. The original .gsc script is not required for this operation.

## Usage:
**Note: make sure you have your system locale set to Japanese before use!**
1. Drag either the .gsc script or the decompiled .txt file into the tool's directory.
2. Run `gscSCD.py`
3. Enter the file name (without `.gsc` or `.txt`) in the input field and click "DEFINE". 
4. Use the commands below.
5. To (de)compile a different file, click "UNDEFINE" and enter the new file name ("CLEAR" clears the textbox after hitting "UNDEFINE").

# .txt File Syntax

Each line of the .txt file performs one of the following functions, indicated by the first character in the line.

- `$COMMENT`: Single line comment. Not present unless added manually.
- `` `HEADER_INFO ``: Makes up the first few lines of the file. Stores the header length and the ??? sections from the header from the original .gsc file. If missing, recompilation defaults to a 36-byte header (not compatible with all games).
- `@LABEL`: Marks an offset position referred to by a command in the .gsc file.
    - Some commands, like JUMP, reference positions in the script file they're in, but those positions will end up shifting if more commands are added, making those references incorrect. Labels are placed in the decompiled .txt by gscSCD to mark those positions in order to update those references when recompiling. For example, if a command refers to offset 86, a label would mark where offset 86 would be relative to the other commands in the file. 
    - Commands known to refer to an offset will instead refer to a LabelNumber in the .txt file (i.e. a JUMP command that refers to offset 86 marked by `@0` will have [0] instead of [86] as its argument).
- `#COMMAND`: Lists a command found in the .gsc file, either as "#COMMAND_NAME" or "#`<opcode as decimal>`". Followed by arguments, in [].
- `[arg1, arg2, etc.]`: A list of arguments for the command written in the previous line, separated by ` ,`. In the case the command has any connected strings (i.e. MESSAGE, CHOICE, etc.), the argument referencing said string (see ConnectedStringsLibrary) will instead be written as -1, and the command will be followed by ">-1" and the string(s) it references.
- `>#`: Is either ">`<string index>`" or "\>-1", and is followed by a string on the following line.
    - ">`<string index>`" is written when the script finds a string that is connected to an unknown command (orphaned strings), while ">-1" is written when the string is connected to the command preceding it (connected strings) (i.e. MESSAGE, CHOICE, etc.)
		- Note: ">`<string index>`" DOESN'T mean the string is referenced the command directly preceding it, just that it's referenced by some command located before ">`<string index>`", but after the previous command with a connected string.
        - i.e. with:

                #AA
                [args]
                #BB
                [args]
                #MESSAGE
                >-1
                <string>
                #XX
                [args]
                #YY
                [args]
                #ZZ
                [args]
                >12 (the string in question)
                <string>
            
            The string in question may belong to #XX, #YY, or #ZZ, but not #AA or #BB.
		- Do note that adding/removing new strings (i.e. adding additional MESSAGEs or APPEND_MESSAGEs) will likely cause commands referencing orphaned strings to point to the wrong string, so make sure CommandsLibrary and ConnectedStringsLibrary are set properly.
    - **IMPORTANT: the index numbers shown after `>` (in the case of `<string index>`) are only the *original* indexes \[from decompilation\] referenced in the command and are for reference only\! When compiling, all string indexes are recalculated based on the order of their lines in the script, NOT by whatever number is written there\!**
    - (In other words, if orphaned strings are present, adding/removing new strings before them (i.e. adding additional MESSAGEs or APPEND_MESSAGEs) will likely cause the commands that reference them to point to the wrong string, as the original command cannot be properly updated)
    - **IMPORTANT: not all connected indexes have been found/identified\!**

# Commands

Unfortunately, little is known about the commands (though their structures are known), and even less about their arguments—though this may change in the future. Each known command in the file is represented by a specific string.

Here are the basic known commands and their arguments (confirmed for Sapphism only, see the original gscSCD for info on newer engine versions):

(`-1` arguments mean the command has a known connected string; see ConnectedStringsLibrary)

- 3 (0x03): JUMP_UNLESS
    - Arguments: [label]. (In the original script, this is an offset relative to the start of the command section).

- 5 (0x05): JUMP.
    - Arguments: [label]. (In the original script, this is an offset relative to the start of the command section).

- 12 (0x0C): CALL_SCRIPT.
    - Arguments: [script number].

- 13 (0x0D): PAUSE.
    - Arguments: [time in seconds].

- 14 (0x0E): CHOICE:
    - Arguments: [number of options, -1, label1, label2, label3, label4, label5, -1, -1, -1, -1, -1, ???, ???, ???].
    - In the original script, the "-1" values ​​are replaced by choice strings, sometimes starting with <*>.

- 20 (0x14): IMAGE_GET.
    - Arguments: [image index (from filename), ???].
    - In Sapphism, seems to be used for drawing BGs, but only for ganbare nicolle and maybe the other extra scenes? (main game uses 6144 (0x1800, DRAW_CG))
        - Image index references grpe.xfl

- 26 (0x1A): IMAGE_SET.
    - Arguments: [].

- 28 (0x1C): BLEND_IMG.
    - Arguments: [???, type1, type2].

- 30 (0x1E): IMAGE_DEF.
    - Arguments: [layer, file name, index_x, index_y(guess), effect, ???]
    - For Sapphism, used for displaying sprites (i.e. character portraits/objects, not BG/CG)
    - index_x (and likely y) seem to refer to an index in a position lookup table
        - 65688 for left side of screen, 65689 is for screen center, 65690 for right side of screen (see 7061)
        - also 65686 for screen center (6510.gsc)
    - for sprite layer, 7 is default for character portraits (first portrait drawn on screen)
        - when more than one portrait is on screen at a time, the new portrait has a different value (second portrait 6, third 5)
    - effects (same/opposite as for 0x24, barring the doubled fade in entry shifting the effect index):
        - 0: none (appear immediately)
        - 1: zoom in
        - 2: none (appear immediately)
        - 3: fade in
        - 4: fade in
        - 5: fade in (dot effect)
        - 6: fade in white
        - 7: fade in black
        - 8: enter left
        - 9: enter right
        - 10: enter top
        - 11: enter bottom
        - 12: enter top left
        - 13: enter top right
        - 14: enter bottom left
        - 15: enter bottom right
        - 16: crt on effect (fade from white, expand vertically then horizontally)
        - 17: zoom out/fade
        - 18: wipe in from small squares
        - 19: wipe in from vertical bars
        - 20: slow fade in
        - 21: fade in enter top
        - 22: fade in enter bottom
        - 23: fade in enter left
        - 24: fade in enter right
        - 25: fade in enter top/bottom
        - 26: fade in enter left/right
        - 27: fade in enter top/bottom/middle
        - 28: fade in enter left/right/middle
        - 29: spin+zoom in
    - not sure where the .xfl file referenced is defined, maybe based on layer?
        - instances of [1, ...] and [9, ...] are present in ganbare nicolle and reference grpo_ob instead of grpo_bu

- 81 (0x51): MESSAGE.
    - Arguments: [???, voice index (from filename), ???, -1 (speaker), -1 (dialog), ???].
        - In the actual .gsc file, the "-1" values ​​are replaced by line numbers!
    - If message has no speaker (i.e. monologue, narration), speaker arg is 0
    - For Sapphism, speaker is always 0, names are drawn via ^g### in the dialog text instead
    - Dialog tags:
        - `^n`: new line (replaced with line breaks in the decompiled file)
        - `^g###`: draw graphic; in Sapphism, ### references `gf###.wcg` in grps.xfl
        - `^c#`: color text; # references the color, single character long
            - 1: white
            - 2: gray
            - 3: dark red
            - 4: dark green
            - 5: light orange
            - 6: light green
            - 7: dull orange/brown
            - 8: bright red
            - 9: black
            - y: yellow
            - p: pink
            - (more to be found)
        - (more to be found)

- 82 (0x52): APPEND_MESSAGE.
    - Arguments: [???, ???, ???, ???, -1, ???].
        - In the .gsc file itself, line numbers appear instead of "-1"!

- 83 (0x53): CLEAR_MESSAGE_WINDOW.
    - Arguments: [???].

- 121 (0x79): GET_DIRECTORY.
    - Arguments: [???, -1].
        - In the .gsc file itself, line numbers appear instead of "-1"!

- 200 (0xC8): READ_SCENARIO.
    - Arguments: [label, ???, ???, ???, ???, ???, ???, ???, ???, ???, ???].

- 255 (0xFF): SPRITE.
    - Arguments: [mode, position, image index, ???, ???].

- 13568 (0x3500): AND.
    - Arguments: [???, ???, ???].

- 18432 (0x4800): EQUALS.
    - Arguments: [???, ???, ???].

- 21504 (0x5400): GREATER_EQUALS.
    - Arguments: [???, ???, ???].

- 43520 (0xAA00): ADD.
    - Arguments: [???, ???, ???].

- 61696 (0xF100): ASSIGN.
    - Arguments: [???, ???].

- 0x0A (10): WAIT_FOR_CLICK
    - Arguments: []

- 0x3c (60): play music (PLAY_BGM)
    - Arguments: [file name (no .wav suffix) in bgm.xfl, 0]

- 0x3d (61): stop music (STOP_BGM)
    - Arguments: [#]
    - 1 is to fade out, any other value stops bgm immediately

- 0x3e (62): play sound effect (PLAY_WAV)
    - Arguments: [file name (no .wav suffix) in wav.xfl]

- 0x21 (33): move existing sprite to new position (MOVE_SPRITE) (see 1801.gsc)
    - Arguments: [layer, index_x, index_y(guess), effect, ?] (similar to IMAGE_DEF, just without the file name)
        - 1: linear slide
        - 2: eased slide (slow -> fast)
        - 3: eased slide (fast -> slow)
        - 4: wiggle up/down
        - 5: arc up
        - 6: arc down
        - 7: shake up/down in place
        - 8: small shake up/down in place
        - 9: shake left/right in place
        - 10: small shake left/right in place
        - 11: small hop upwards in place
        - 12: hop upwards in place
        - 13: large hop upwards in place

- 0x2B (43): draw effect? (see 7061.gsc)
    - Arguments: [file name in grps.xfl, 0]
    - [0, 0] = erase effect
    - seems to be exclusively used for the lens flare effect?

- 0x23 (35): WARP_SPRITE (see 7061.gsc)
    - Arguments: [layer, effect]
        - 1: spin counterclockwise
        - 2: fast spin counterclockwise
        - 3: spin clockwise
        - 4: fast spin clockwise
        - 5: vertical squish
        - 6: fast vertical squish
        - 7: fall left
        - 8: fast fall left
        - 9: very fast fall left
        - 10: fall right
        - 11: fast fall right
        - 12: very fast fall right

- 0x20 (32): title text (text drawn on screen but not in a text box) (TITLE)
    - Arguments: [???, ???, ???, ???, ???, -1]
        - In the .gsc file itself, line numbers appear instead of "-1"!
    - used for the credits and stuff too, but not girls in a bottle (that's just MESSAGE + APPEND_MESSAGE)

- 0x1800 (6144): draw CG/BG? (DRAW_CG), always followed by ASSIGN (see 2811.gsc)
    - Arguments: [???, ###, file name?]
        - \### = 201: CG/BG (file name references .wcg file in grpe.xfl)
        - \### = 202: CG transition effect? follows 201 instances' ASSIGN (file name references .msk file in grps.xfl, as well as other things I'm not sure of)
        - \### = 205: ???

- 0x0F (15): TOGGLE_LAYER, see 6510.gsc
    - Arguments: [layer?]
    - executing the same command toggles it back on, it seems (i.e. 0x0F [201] first makes the BG black then brings it back when executed again)
    - related to 0x1800 (DRAW_CG)?
    - 203: hide textbox (doesn't need 0x0F [203] to turn it back on, appears on next MESSAGE)
    - 201: show/hide BG/CG (begins hidden, needs to be shown)

- 0x24 (36): REMOVE_SPRITE, see 6510.gsc
    - Arguments: [layer, effect]
    - effects:
        - 0: no effect (instant removal)
        - 1: shrink
        - 2: no effect (instant removal)
        - 3: fade
        - 4: fade (dot effect)
        - 5: fade to white, disappear instantly
        - 6: fade to black, fade away
        - 7: exit left
        - 8: exit right
        - 9: exit up
        - 10: exit down
        - 11: exit top left
        - 12: exit top right
        - 13: exit bottom left
        - 14: exit bottom right
        - 15: crt off effect (shrink horizontally then vertically, fade to white)
        - 16: zoom in fade
        - 17: wipe away as small boxes
        - 18: wipe away as vertical beams
        - 19: slow fade
        - 20: exit down and fade
        - 21: exit up and fade
        - 22: exit right and fade
        - 23: exit left and fade
        - 24: exit up+down and fade
        - 25: exit left+right and fade
        - 26: exit up+down and fade
        - 27: exit left+right and fade (middle image)
        - 28: spin+shrink (clockwise)
        - 29: no effect (instant removal)
        - 30: diagonal slice
        - 31: vertical slice (up/down)
        - 32: horizontal slice (drop to left)
        - 33: punted away
        - 34: punted away + spun
        - 35: horizontal slice (left+right)

# Further Info
See [Gsc Info](docs/gsc_info.md) for help with understanding the .gsc format, and how gscSCD handles things.

See [Inferring Arguments](docs/inferring_arguments.md) for help with adjusting command args for your game