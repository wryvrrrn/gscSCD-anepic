#(original script) Written by Tester-ом.
#https://anivisual.net/index/8-78951
#For inquiries, please (do not) contact:
#testertesterovtesterovich@yandex.ru
#(keeping this part for credit, don't actually contact them
#regarding script issues and stuff)
#(for inquiries regarding the ~an epic~ version of the script,
#idk, open a github issue or DM wryvrrrn on bsky/tumblr or something)
#(if you contact me without fully reading the documentation though
#you grant me full legal authority to burn down your home)

#A relatively simple editor for basic .gsc scripts
#used in the codeX RScript engine,
#which these companies use to develop their games:
#Liar-soft;
#raiL-soft;

#Written in Python 3.
#Requires the following libraries to be installed: struct, tkinter.
#These are standard libraries, but due to certain issues, they may not work.

#Make sure your system locale is set to Japanese!!!! Will get mojibake otherwise

import struct
from tkinter import *
from tkinter import messagebox as mb

class GscFile:
    FileName = ''
    #By default, it is open, but it can be closed and switched to write mode.
    FileParametrs = []
    #See FileParametrsSupport.
    FileParametrsSupport = ('File size',
                            'Header size',
                            'Command section size',
                            'String declaration section size',
                            'String definition section size',
                            '???',
                            '???',
                            '???',
                            '???')
    #Packaging structures:
    FileStruct = [b'', b'', b'', b'', b''] #b'' is byte string (vs human-readable character string); stores sections of the gsc as listed in FileStructSupport
    #See FileStructSupport.
    FileStructSupport = ('Header',
                         'Command Section',
                         'String Declaration Section',
                         'String Definition Section',
                         'Other')
    #Terms:
    FileStringOffsets = []
    FileStrings = []
    #Teams:
    CommandArgs = []
    #CommandArgs: A 2D list in which the inner lists represent the arguments for a specific command.
    #Commands are listed in order; i.e. CommandArgs[0] is the list containing arguments for the first command
    #CommandArgs[1] for the second, etc.
    Commands = []
    #Commands: A list of the commands found, in order.
    CommandsLibrary = ((0x03, 'i', 'JUMP_UNLESS'),
                       (0x05, 'i', 'JUMP'),
                       (0x0D, 'i', 'PAUSE'),
                       (0x0C, 'i', 'CALL_SCRIPT'), #[Script name without leading zeros, ???]; 'ii' for newer, 'i' in sapphism
                       (0x0E, 'hiiiiiiiiiiiiii', 'CHOICE'),
                       (0x14, 'ii', 'IMAGE_GET'),
                       (0x1A, '', 'IMAGE_SET'),
                       (0x1C, 'iii', 'BLEND_IMG'),
                       (0x1E, 'iiiiii', 'IMAGE_DEF'), #(confirmed for sapphism)
                       (0x51, 'iiiiiii', 'MESSAGE'), #(confirmed for sapphism)
                       (0x52, 'iiiiii', 'APPEND_MESSAGE'),
                       (0x53, 'i', 'CLEAR_MESSAGE_WINDOW'),
                       (0x79, 'ii', 'GET_DIRECTORY'),
                       (0xC8, 'iiiiiiiiiii', 'READ_SCENARIO'), #??? Adjust the number of arguments?
                       (0xFF, 'iiiii', 'SPRITE'),
                       (0x3500, 'hhh', 'AND'),
                       (0x4800, 'hhh', 'EQUALS'),
                       (0x5400, 'hhh', 'GREATER_EQUALS'),
                       (0xAA00, 'hhh', 'ADD'),
                       (0xF100, 'hh', 'ASSIGN'),
                       (0x04, 'i', ''),
                       (0x08, '', ''),
                       (0x09, 'h', ''),
                       (0x0A, '', 'WAIT_FOR_CLICK'), #h in a different type? Hmm... #WAIT_FOR_CLICK?
                       (0x0B, '', ''),
                       (0x0F, 'i', 'TOGGLE_LAYER'), #TOGGLE_LAYER?
                       #Originally, ??? #An array? Adjust the number of arguments?
                       #for newer games, 'iiiiiiiiiiii', for sapphism, 'i'
                       (0x10, 'i', ''),
                       (0x11, '', ''),
                       (0x12, 'ii', ''),
                       (0x13, 'i', ''),
                       (0x15, 'i', ''),
                       (0x16, 'iiii', ''),
                       (0x17, 'ii', ''), #"iiii" for newer games, 'ii' for sapphism (see 6100.gsc)
                       (0x18, 'ii', ''),
                       (0x19, 'ii', ''),
                       (0x1B, '', ''),
                       (0x1D, 'ii', ''),
                       (0x20, 'iiiiii', 'TITLE'), #TITLE? see 7061.gsc
                       (0x21, 'iiiii', 'MOVE_SPRITE'), #MOVE_SPRITE? see 1801.gsc
                       (0x22, 'iiiii', ''),
                       (0x23, 'ii', 'WARP_SPRITE'), #WARP_SPRITE?
                       (0x24, 'ii', 'REMOVE_SPRITE'), #REMOVE_SPRITE? see 6510.gsc
                       (0x25, 'ii', ''),
                       (0x26, 'iii', ''), #Kusarihime: iii; The Rest: iiii?
                       (0x27, 'iii', ''),
                       (0x28, 'ii', ''),
                       (0x29, 'ii', ''),
                       (0x2A, 'ii', ''),
                       (0x2B, 'ii', ''),
                       (0x2C, 'i', ''),
                       (0x2D, 'ii', ''),
                       (0x2E, 'i', ''),
                       (0x2F, 'ii', ''),
                       (0x30, 'ii', ''), #Kusarihime: ii, The Rest: iii?
                       (0x31, 'ii', ''),
                       (0x32, '', ''),
                       (0x33, '', ''),
                       (0x34, '', ''),
                       (0x35, 'i', ''),
                       (0x37, '', ''),
                       (0x38, 'iiiii', ''),
                       (0x39, '', ''),
                       (0x3A, '', ''),
                       (0x3B, 'iiii', ''),
                       (0x3C, 'ii', 'PLAY_BGM'), #PLAY_BGM? 'iii' for newer games, 'ii' for sapphism (see 6510.gsc)
                       (0x3D, 'i', 'STOP_BGM'), #STOP_BGM? 'ii' for newer games, 'i' for sapphism (see 7061.gsc)
                       (0x3E, 'i', 'PLAY_WAV'), #PLAY_WAV? 'i'? According to Dungeons&Daimeiwaku 'ii'.
                       (0x3F, 'iii', ''), #'iii'? According to D&D 'iiii'.
                       (0x40, 'i', ''), #'i'? According to D&D 'ii'.
                       (0x41, 'i', ''),
                       (0x42, 'iiii', ''),
                       (0x43, 'i', ''),
                       (0x44, '', ''),
                       (0x45, '', ''),
                       (0x46, 'iiii', ''),
                       (0x47, 'iiii', ''),
                       (0x48, 'i', ''),
                       (0x49, 'iii', ''),
                       (0x4A, 'i', ''),
                       (0x4B, 'iiiii', ''),
                       (0x4D, 'iiii', ''),
                       (0x50, 'i', ''),
                       (0x5A, 'iii', ''),
                       (0x5B, 'iiiii', ''),
                       (0x5C, 'ii', ''),
                       (0x5D, 'ii', ''),
                       (0x5E, 'i', ''),
                       (0x5F, 'ii', ''),
                       (0x60, 'ii', ''),
                       (0x61, 'ii', ''),
                       (0x62, 'ii', ''),
                       (0x63, 'iii', ''),
                       (0x64, 'iii', ''),
                       (0x65, 'ii', ''),
                       (0x66, 'i', ''),
                       (0x67, 'ii', ''),
                       (0x68, 'iiii', ''),
                       (0x69, 'i', ''), #For others, is ii?
                       (0x6A, 'iiiii', ''),#TEMP!
                       (0x6B, 'iii', ''), #TEMP!
                       (0x6C, 'iii', ''), #TEMP
                       (0x6E, 'iii', ''),
                       (0x6F, 'iii', ''),
                       (0x70, 'i', ''),
                       (0x71, 'ii', ''),
                       (0x72, 'ii', ''),
                       (0x73, 'ii', ''),
                       (0x74, 'ii', ''),
                       (0x75, 'ii', ''),
                       (0x78, 'ii', ''),
                       (0x82, 'iiii', ''),
                       (0x83, 'iiiii', ''),
                       (0x84, 'ii', ''),
                       (0x86, 'iii', ''),
                       (0x87, 'iiiii', ''),
                       (0x88, 'iii', ''),
                       (0x96, 'ii', ''),
                       (0x97, 'ii', ''),
                       (0x98, 'ii', ''),
                       (0x99, 'ii', ''),
                       (0x9A, 'ii', ''),
                       (0x9B, 'ii', ''),
                       (0x9E, 'ii', ''),
                       (0x9F, 'ii', ''),
                       (0x9C, 'iii', ''),
                       (0x9D, 'iiiii', ''),
                       (0xC9, 'iiiii', ''),
                       (0xCA, 'iii', ''),
                       (0xD2, 'ii', ''),
                       (0xD3, 'iiii', ''),
                       (0xD4, 'i', ''),
                       (0xD5, 'iii', ''),
                       (0xDC, 'iii', ''),
                       (0xDD, 'ii', ''),
                       (0xDE, '', ''),
                       (0xDF, 'ii', ''),
                       (0xE1, 'iiiii', ''),
                       (0xE6, 'i', ''),
                       (0xE7, 'i', ''),
                       (0x1800, 'hhh', 'DRAW_CG'), #DRAW_CG?
                       (0x1810, 'hhh', ''), #!!!
                       (0x1900, 'hhh', ''),
                       (0x1910, 'hhh', ''),
                       (0x2500, 'hhh', ''),
                       (0x1A01, 'hhh', ''), #!!!
                       (0x1A00, 'hhh', ''),
                       (0x4400, 'hhh', ''),
                       (0x4810, 'hhh', ''), #!!!
                       (0x4900, 'hhh', ''),
                       (0x4A00, 'hhh', ''),
                       (0x5800, 'hhh', ''),
                       (0x6800, 'hhh', ''),
                       (0x7800, 'hhh', ''),
                       (0x7A00, 'hhh', ''),
                       (0x8800, 'hhh', ''),
                       (0x8A00, 'hhh', ''),
                       (0x9800, 'hhh', ''),
                       (0x9810, 'hhh', ''), #!!!
                       (0x9A00, 'hhh', ''),
                       (0xA100, 'hhh', ''),
                       (0xA200, 'hhh', ''),
                       (0xA201, 'hhh', ''), #!!
                       (0xA400, 'hhh', ''),
                       (0xA500, 'hhh', ''),
                       (0xA600, 'hhh', ''),
                       (0xA800, 'hhh', ''),
                       (0xA810, 'hhh', ''), #!!!
                       (0xA900, 'hhh', ''),
                       (0xB400, 'hhh', ''),
                       (0xB800, 'hhh', ''),
                       (0xB900, 'hhh', ''),
                       (0xC400, 'hhh', ''),
                       (0xC800, 'hhh', ''),
                       (0xD400, 'hhh', ''),
                       (0xD800, 'hhh', ''),
                       (0xE400, 'hhh', ''),
                       (0xE800, 'hhh', ''))
    #Command Library: 2D Tuple.
    #(n)(0) - command;
    #(n)(1) - structure;
    #(n)(2) - Definition (may be empty).

    ConnectedStringsLibrary = [[0x0E, [1, 7, 8, 9, 10, 11]], #Remove 1? #CHOICE
                               #[0x0F, [1]], #doesn't seem to have a string index for sapphism, see 6510.gsc offset(dec) 1200
                               [0x20, [-1]], #tentative; see 7061.gsc (originally [0x20, [0]])
                               [0x51, [-3, -2]], #MESSAGE
                               [0x52, [-2]], #APPEND_MESSAGE
                               [0x79, [1]]] #GET_DIRECTORY
    #Library of string-related arguments.
    #(n)(0) - command;
    #(n)(1) - List of related arguments.

    #Next, hacks/workarounds for arguments related to offsets.

    ConnectedOffsetsLibrary = [[0x03, [0]], #JUMP_UNLESS
                               [0x05, [0]], #JUMP
                               [0x0E, [2, 3, 4, 5, 6]], #CHOICE
                               [0xC8, [0]]] #READ_SCENARIO
    Labels = []
    #[0] — label index, [1] — label offset.
    
    def __init__(self, FileName, Mode):
        self.FileName = FileName
        if (Mode == 0):
            self.File = open(self.FileName + ".gsc", mode="rb")
        else:
            self.File = open(self.FileName + ".txt", mode="r", encoding="cp932")
    #Technical display/mapping/rendering:
    def PrintFilePmt(self):
        for i in range(0, len(self.FileParametrs)):
            print(self.FileParametrsSupport[i] + ": " + str(self.FileParametrs[i]) + ".")
    def PrintFileStrc(self):
        Aller = '' #<not sure what this means, just a dummy name?>
        for i in range(0, len(self.FileStruct)):
            Aller = self.FileStruct[i].hex()
            AllerN = ''
            ii = 2
            while (ii < len(Aller)):
                AllerN += Aller[(ii-2):ii] + " ";
                ii += 2
            AllerN += Aller[(ii-2):ii]
            print(self.FileStructSupport[i] + ":\n" + AllerN)
    #Reading a Binary File:
    def ReadHeader(self):
        self.File.seek(0,0) #move cursor to start of file
        Kortez = struct.unpack('ii', self.File.read(8)) #reads first 8 bytes of the gsc (pair of hex digits (i.e. 00) is one byte), treats them as two signed 32-bit integers (4 bytes each) read little-endian
        for i in range(0, 2):
            self.FileParametrs.append(Kortez[i])
        #print(self.FileParametrs) #DEBUG
        #don't hard code unpacking, interpret as n 32-bit ints instead
        Kortez = struct.unpack('i'*int((self.FileParametrs[1]-8)/4), self.File.read(self.FileParametrs[1]-8))
        for i in range(0, len(Kortez)):
            self.FileParametrs.append(Kortez[i])
        self.File.seek(0,0)
        self.FileStruct[0] = self.File.read(self.FileParametrs[1]) #read header using header length, place in header of filestruct
    def ReadCommand(self):
        self.File.seek(self.FileParametrs[1], 0) #start reading past the header
        Reader = 0
        CommandNumber = 0
        while (Reader < self.FileParametrs[2]): #FileParametrs[2] is command section size
            Kerza = []
            Reader += 2
            # print("Reader advanced to " + str(Reader)) #DEBUG
            Code = self.File.read(2)
            Code = struct.unpack('H', Code)[0] #go through two bytes as a time, treat as unsigned short; [0] is because it returns tuple
            SupportCode = Code & 0xf000 #seemingly unused
            DontKnow = 0
            self.CommandArgs.append([])
            DontKnow = 1
            CommandArgsStruct = ''
            for i in range(0, len(self.CommandsLibrary)):
                if (Code == self.CommandsLibrary[i][0]): #check if current byte is a known command
                    # print("found command " + str(hex(self.CommandsLibrary[i][0])) + " (" + str(self.CommandsLibrary[i][2])+")") #DEBUG
                    DontKnow = 0
                    CommandArgsStruct = self.CommandsLibrary[i][1]
                    break;
            if (DontKnow == 1): #Let's try to infer the arguments from the mask.
                # print("found unknown command " + str(hex(Code))) #DEBUG
                if ((Code & 0xf000) == 0xf000):
                    # print("found inferred hh (4 bytes)") #DEBUG
                    CommandArgsStruct = 'hh'
                elif ((Code & 0xf000) == 0x0000):
                    # print("found inferred nothing") #DEBUG
                    CommandArgsStruct = ''
                else:
                    # print("found inferred hhh (6 bytes)") #DEBUG
                    CommandArgsStruct = 'hhh'
            # print("CommandArgsStruct = " + str(CommandArgsStruct)) #DEBUG
            for i in CommandArgsStruct:
                if ((i == 'i') or (i == 'I')):
                    ByteSize = 4
                elif ((i == 'h') or (i == 'H')):
                    ByteSize = 2
                Reader += ByteSize
                # print("Reader arg'd up to " + str(Reader)) #DEBUG
                self.CommandArgs[CommandNumber].append(struct.unpack(i, self.File.read(ByteSize))[0])
            self.Commands.append(Code)
            #CONTROL!!! TECHNICAL!!! (seems to help list unknown commands, not relevant for us)
            DontDef = 0
            #if ((DontKnow == 1) and (Code != 0x00)):
            if (DontKnow == 1):
            #if (DontKnow == 0):
            #if (Code == 0x51):
            #if (0 == 1):
                for i in range(0, len(self.CommandsLibrary)):
                    DontDef = 1
                    if ((self.Commands[CommandNumber] == self.CommandsLibrary[i][0]) and (self.CommandsLibrary[i][2] != '')):
                        DontDef = 0
                        break;
                if (DontDef == 0):
                    print(self.CommandsLibrary[i][2])
                else:
                    print(self.Commands[CommandNumber])
                print(self.CommandArgs[CommandNumber])
            #!!!
            #if Code == 0x51 or Code == 0x52 or Code == 0x0E or Code == 0x20: #DEBUG
            #    print("(Append) Message/Choice CommandArgs:")
            #    print(print(self.CommandArgs[CommandNumber]))
            # print("Reader is at " + str(Reader)) #DEBUG
            CommandNumber += 1
        # print("CONTROL: " + str(Reader) + " : " + str(self.FileParametrs[2])) #DEBUG
        self.File.seek(self.FileParametrs[1], 0)
        self.FileStruct[1] = self.File.read(self.FileParametrs[2])
    def ReadStringDec(self):
        Offset = 0
        for i in range(1, 3):
            Offset += self.FileParametrs[i]
        self.File.seek(Offset, 0)

        self.FileStringOffsets = []
        for i in range(0, self.FileParametrs[3]//4):
            self.FileStringOffsets.append(struct.unpack('i', self.File.read(4))[0])
        
        self.File.seek(Offset, 0)
        self.FileStruct[2] = self.File.read(self.FileParametrs[3])
        # print("File String Offsets:") #DEBUG
        # print(self.FileStringOffsets) #DEBUG
    def ReadStringDef(self):
        Offset = 0
        for i in range(1, 4):
            Offset += self.FileParametrs[i]
        self.File.seek(Offset, 0)

        self.FileStrings = []
        for i in range(0, len(self.FileStringOffsets)):
            Dohod = 0
            if (i == (len(self.FileStringOffsets) - 1)):
                Dohod = self.FileParametrs[4]
            else:
                Dohod = self.FileStringOffsets[i+1]
            Dohod -=  self.FileStringOffsets[i]
            self.FileStrings.append(self.File.read(Dohod-1).decode("cp932"))
            self.File.read(1)

        #print(self.FileStrings) #DEBUG
        
        self.File.seek(Offset, 0)
        self.FileStruct[3] = self.File.read(self.FileParametrs[4])
        #print(self.FileStruct[3].decode("cp932")) #DEBUG
    def ReadRemaining(self):
        Offset = 0
        for i in range(1, 5):
            Offset += self.FileParametrs[i]
        self.File.seek(Offset, 0)
        self.FileStruct[4] = b''
        for i in range(5, len(self.FileParametrs)):
            self.FileStruct[4] += self.File.read(self.FileParametrs[i])
    def ReadAll(self):
        self.ReadHeader()
        self.ReadCommand()
        self.ReadStringDec()
        self.ReadStringDef()
        self.ReadRemaining()
    #Writing to and Linking with .txt Files:
    def RewriteGscFile(self):
        for i in self.FileStruct:
            self.File.write(i)
    def RemakeGscFromGsc(self):
        self.ReadAll() #Reading All Sections.
        #self.PrintFilePmt() #Initial Control.
        self.RedoAll()
        #self.PrintFileStrc() #Outputting the Structure.
        self.CloseFile() #Closing a file.
        self.WriteFileBin() #Writing Binary Strings to .gsc.
        self.RewriteGscFile() #Overwriting a Binary File.
        self.PrintFilePmt() #Final Assessment.
        self.CloseFile() #Closing a file.
    def DecompileGscToTxt(self):
        self.ReadAll()
        self.CloseFile()
        self.WriteFile()

        StringCount = 0
        Offset = 0
        
        #We determine the specified offsets in advance.
        LabelNumber = 0
        for CommandNumber in range(0, len(self.Commands)):
            FindOffset = 0
            ConOff = 0 #originally Marbas
            doKnowOffset = -1
            while (ConOff < len(self.ConnectedOffsetsLibrary)):
                if (self.Commands[CommandNumber] == self.ConnectedOffsetsLibrary[ConOff][0]):
                    FindOffset = 1
                    break
                ConOff += 1
            if (FindOffset == 0):
                continue
            for OffsetIndex in self.ConnectedOffsetsLibrary[ConOff][1]: #OffsetIndex previously Mardab
                #First, let's see if it corresponds to any label.
                for Label in self.Labels: #Label previously Marmal
                    if (self.CommandArgs[CommandNumber][OffsetIndex] == Label[1]):
                        doKnowOffset = Label[0]
                        break
                #Now, let us reason things out.
                if (doKnowOffset == -1):
                    self.Labels.append([])
                    self.Labels[LabelNumber].append(LabelNumber)
                    self.Labels[LabelNumber].append(self.CommandArgs[CommandNumber][OffsetIndex])
                    self.CommandArgs[CommandNumber][OffsetIndex] = LabelNumber
                    LabelNumber += 1
                else:
                    self.CommandArgs[CommandNumber][OffsetIndex] = doKnowOffset
        #Output method for debugging.
        # print("File Labels:") #DEBUG
        # print(self.Labels) #DEBUG
        
        #Main Body.
        #store header length and ??? sections first (needed for recompiling back into gsc later)
        for i in range(0, len(self.FileParametrs)):
            if i not in {0, 2, 3, 4}:
                self.File.write('`' + str(self.FileParametrs[i]) + '\n')
        
        for CommandNumber in range(0, len(self.Commands)):
            #First, if necessary, a label should be defined.
            for Label in self.Labels:
                if (Offset == Label[1]):
                    self.File.write('@' + str(Label[0]) + '\n')
            #We need to define a few things first...
            DontDef = 0
            DontKnow = 0
            MessageKostil = 0
            CommandName = ''
            for i in range(0, len(self.CommandsLibrary)):
                DontDef = 1
                DontKnow = 1
                #if ((self.Commands[CommandNumber] == self.CommandsLibrary[i][0]) and (self.CommandsLibrary[i][2] != '')):
                #    DontDef = 0
                #    break;
                if (self.Commands[CommandNumber] == self.CommandsLibrary[i][0]):
                    if (self.CommandsLibrary[i][2] != ''):
                        DontDef = 0
                    DontKnow = 0
                    break;
            if (DontDef == 0):
                CommandName = self.CommandsLibrary[i][2]
            else:
                CommandName = str(self.Commands[CommandNumber])
            #Secondly, obtain the offset after this iteration..
            Offset += 2 #All commands are two bytes long.
            if (DontKnow == 0):
                for OfferI in self.CommandsLibrary[i][1]:
                    if ((OfferI == 'h') or (OfferI == 'H')):
                        Offset += 2
                    elif ((OfferI == 'i') or (OfferI == 'I')):
                        Offset += 4
            else:
                if ((self.Commands[CommandNumber] & 0xf000) == 0xf000):
                    Offset += 4
                elif ((self.Commands[CommandNumber] & 0xf000) == 0x0000):
                    Offset += 0
                else:
                    Offset += 6
            #And then, everything else.
            
            ConStr = 0
            CommIndex = 0 #(formerly kk)
            for CommIndex in range(0, len(self.ConnectedStringsLibrary)):
                if (self.Commands[CommandNumber] == self.ConnectedStringsLibrary[CommIndex][0]):
                    ConStr = 1
                    break
            if (ConStr > 0):
                kkk = 0
                StringsNew = []
                for kkk in range(len(self.ConnectedStringsLibrary[CommIndex][1])):
                    MessageArgsTrue = self.CommandArgs[CommandNumber]
                    # print("CommandNumber= " + str(CommandNumber)) #DEBUG
                    # print("MessageArgsTrue= " + str(MessageArgsTrue)) #DEBUG
                    MessageNum = MessageArgsTrue[self.ConnectedStringsLibrary[CommIndex][1][kkk]]
                    MessageArgsTrue[self.ConnectedStringsLibrary[CommIndex][1][kkk]] = -1
                    StringsNew.append(self.FileStrings[MessageNum].replace('^n', '\n'))
                    # print("StringCount: " + str(StringCount)) #DEBUG
                    # print("MessageNum: " + str(MessageNum)) #DEBUG
                    #presumably meant to list missed strings
                    #either strings linked to undefined commands or improperly interpreted commands
                    while (StringCount < MessageNum):
                        self.File.write('>' + str(StringCount) + '\n')
                        self.File.write(self.FileStrings[StringCount].replace('^n', '\n') + '\n')
                        StringCount += 1
                    if MessageNum == StringCount: #to stop StringCount from incrementing when MessageNum = 0 (no speaker name)
                        StringCount += 1
                    
                self.File.write("#" + CommandName + '\n')
                self.File.write(str(self.CommandArgs[CommandNumber]))
                for z in StringsNew:
                    self.File.write("\n>-1\n" + z)                
            else:
                self.File.write("#" + CommandName + '\n')
                self.File.write(str(self.CommandArgs[CommandNumber]))
            if (CommandNumber != (len(self.Commands) - 1)):
                self.File.write("\n")
            else:
                while (StringCount < len(self.FileStrings)):
                    self.File.write('\n>' + str(StringCount) + '\n')
                    self.File.write(self.FileStrings[StringCount].replace('^n', '\n'))
                    StringCount += 1
        self.CloseFile()
        print("Verifying commands section parsing: " + str(Offset) + " : " + str(len(self.FileStruct[1])))
    def CompileTxtToGsc(self):
        Lines = self.File.read().split('\n')
        i = 0
        
        #read and remove header sections first
        self.FileParametrs = [0, 0, 0, 0, 0]
        if Lines[i][0] == '`': #check for header length marker
            self.FileParametrs[1] = int(Lines[i][1:])
            while (i+1 < len(Lines)):
                if Lines[i+1][0] == '`':
                    i+=1
                    self.FileParametrs.append(int(Lines[i][1:]))
                else:
                    break
            for line in range(0, i+1):
                Lines.pop(0)
            i = 0
        else:
            print("Header parameters not found, defaulting to 36 byte header length and using hardcoded ??? section values")
            self.FileParametrs[1] = 36
            self.FileParametrs.append(4)
            self.FileParametrs.append(1)
            self.FileParametrs.append(4)
            self.FileParametrs.append(1)

        #Let's label all the markers..
        Offset = 0
        LenOff = 0
        while (i < len(Lines)):
            if (Lines[i] == ''):
                i += 1
                continue
            if (Lines[i][0] == '@'):
                NotAnythingNew = 0
                LabelNumber = int(Lines[i][1:])
                for Marbas in self.Labels:
                    if (LabelNumber == Marbas[0]):
                        NotAnythingNew = 1
                        break
                if (NotAnythingNew == 1):
                    i += i
                    continue
                self.Labels.append([])
                self.Labels[LenOff].append(LabelNumber)
                self.Labels[LenOff].append(Offset)
                LenOff += 1
                i += 1
            elif (Lines[i][0] == '#'):
                CommandDef = Lines[i][1:]
                DontKnow = 1
                iz = 0
                while (iz < len(self.CommandsLibrary)):
                    if (CommandDef == str(self.CommandsLibrary[iz][0])):
                        DontKnow = 0
                        break
                    elif (CommandDef == self.CommandsLibrary[iz][2]):
                        DontKnow = 0
                        CommandDef = str(self.CommandsLibrary[iz][0])
                        break
                    iz += 1
                CommandDef = int(CommandDef)
                Offset += 2
                if (DontKnow == 0):
                    for OfferI in self.CommandsLibrary[iz][1]:
                        if ((OfferI == 'h') or (OfferI == 'H')):
                            Offset += 2
                        elif ((OfferI == 'i') or (OfferI == 'I')):
                            Offset += 4
                else:
                    if ((CommandDef & 0xf000) == 0xf000):
                        Offset += 4
                    elif ((CommandDef & 0xf000) == 0x0000):
                        Offset += 0
                    else:
                        Offset += 6
                i += 1
            else:
                i += 1
                continue

        #We'll take care of everything else..
        i = 0
        while (i < len(Lines)):
            if (Lines[i] == ''):
                i += 1
                continue
            if (Lines[i][0] == '$'): #Comments.
                i += 1
                continue
            if (Lines[i][0] == '@'): #Labels (retrieved earlier).
                i += 1
                continue
            if (Lines[i][0] == '>'):
                String = ''
                i += 1
                KostilPer = 1
                while (i < len(Lines)):
                    if (len(Lines[i]) == 0):
                        if (KostilPer == 1):
                            KostilPer = 0
                        else:
                            String = String + '^n'
                        i += 1
                        continue
                    if (Lines[i][0] == '$'): #Comments.
                        i += 1
                        continue
                    if ((Lines[i][0] == '#') or (Lines[i][0] == '>') or (Lines[i][0] == '@')):
                        break
                    if (KostilPer == 1):
                        KostilPer = 0
                    else:
                        String = String + '^n'
                    String = String + Lines[i]
                    i += 1
                self.FileStrings.append(String)
            elif (Lines[i][0] == '#'):
                CommandType = 0
                CommandCTR = []
                CommandNEW = []
                for Cmed in self.CommandsLibrary:
                    if (Lines[i][1:] == Cmed[2]):
                        Lines[i] = Lines[i].replace(Cmed[2], str(Cmed[0]))
                        break
                CommandType = int(Lines[i][1:])
                self.Commands.append(CommandType)
                i += 1
                Lines[i] = Lines[i].replace('[', '').replace(', ', ' ').replace(']', '')
                CommandCTR = Lines[i].split(' ')
                if (CommandCTR == ['']):
                    CommandCTR = []
                for ii in range(0, len(CommandCTR)):
                    CommandNEW.append(int(CommandCTR[ii]))
                #Working with commands involving arguments related to offsets.
                Farba = 0
                while (Farba < len(self.ConnectedOffsetsLibrary)):
                    if (CommandType == self.ConnectedOffsetsLibrary[Farba][0]):
                        for NewZeland in self.ConnectedOffsetsLibrary[Farba][1]:  #what are these variable names even
                            Ermeg = 0
                            Ermeg = CommandNEW[NewZeland]
                            Ai = 0
                            for Ai in self.Labels:
                                if (Ermeg == Ai[0]):
                                    CommandNEW[NewZeland] = Ai[1]
                        break   
                    Farba += 1
                
                #From here on, everything is as usual.
                self.CommandArgs.append(CommandNEW)
                i += 1

                ConStr = 0
                kk = 0
                for kk in range(0, len(self.ConnectedStringsLibrary)):
                    if (CommandType == self.ConnectedStringsLibrary[kk][0]):
                        ConStr = 1
                        break
                
                if (ConStr > 0):
                    kkk = 0
                    for kkk in range(len(self.ConnectedStringsLibrary[kk][1])):
                        String = ''
                        i += 1
                        KostilPer = 1
                        while (i < len(Lines)):
                            if (len(Lines[i]) == 0):
                                if (KostilPer == 1):
                                    KostilPer = 0
                                else:
                                    String = String + '^n'
                                i += 1
                                continue
                            if (Lines[i][0] == '$'): #Comments.
                                i += 1
                                continue
                            if ((Lines[i][0] == '#') or (Lines[i][0] == '>') or (Lines[i][0] == '@')):
                                break
                            if (KostilPer == 1):
                                KostilPer = 0
                            else:
                                String = String + '^n'
                            if (i >= len(Lines)):
                                i -= 1
                            String = String + Lines[i]
                            i += 1
                        self.FileStrings.append(String)
                        self.CommandArgs[-1][self.ConnectedStringsLibrary[kk][1][kkk]] = (len(self.FileStrings) - 1)
            else:
                i += 1
                continue
        self.CloseFile()
        
        self.WriteFileBin()
        self.RedoAll()
        self.RewriteGscFile()
        self.PrintFilePmt()
        self.CloseFile()
    #Overriding:
    def RefreshHeaderPrm(self):
        # Sizer = 36
        # self.FileParametrs = [0, 36]
        Sizer = self.FileParametrs[1]
        for i in range(2, 5):
            Sizer += len(self.FileStruct[i-1])
            self.FileParametrs[i] = len(self.FileStruct[i-1])
            #self.FileParametrs.append(len(self.FileStruct[i-1]))
        # self.FileParametrs.append(4)
        # self.FileParametrs.append(1)
        # self.FileParametrs.append(4)
        # self.FileParametrs.append(1)
        Sizer += len(self.FileStruct[4])
        self.FileParametrs[0] = Sizer
    def RemakeHeaderFromPrm(self):
        self.FileStruct[0] = b''
        for i in self.FileParametrs:
            self.FileStruct[0] += struct.pack("i", i)
    def RedoHeader(self):
        self.RefreshHeaderPrm()
        self.RemakeHeaderFromPrm()
    def RemakeOffsetsFromStrings(self):
        self.FileStringOffsets = []
        Dohod = 0
        for i in range(0, len(self.FileStrings)):
            self.FileStringOffsets.append(Dohod)
            Dohod += 1 + len(self.FileStrings[i].encode("cp932"))
    def RewriteStringDec(self):
        self.FileStruct[2] = b''
        for i in self.FileStringOffsets:
            self.FileStruct[2] += struct.pack("i", i)
    def RewriteStringDef(self):
        self.FileStruct[3] = b''
        for i in self.FileStrings:
            self.FileStruct[3] += i.encode("cp932") + b'\x00'
    def RedoStrings(self):
        self.RemakeOffsetsFromStrings()
        self.RewriteStringDec()
        self.RewriteStringDef()
    def RedoCommands(self):
        self.FileStruct[1] = b''
        for NumCom in range(0, len(self.Commands)):
            Code = self.Commands[NumCom]
            DontKnow = 1
            CommandArgsStruct = ''
            for i in range(0, len(self.CommandsLibrary)):
                if (Code == self.CommandsLibrary[i][0]):
                    DontKnow = 0
                    CommandArgsStruct = self.CommandsLibrary[i][1]
                    break;
            if (DontKnow == 1): #Let's try to infer the arguments from the mask.
                if ((Code & 0xf000) == 0xf000):
                    CommandArgsStruct = 'hh'
                elif ((Code & 0xf000) == 0x0000):
                    CommandArgsStruct = ''
                else:
                    CommandArgsStruct = 'hhh'
            self.FileStruct[1] += struct.pack('H', Code)
            for NumArg in range(0, len(CommandArgsStruct)):
                CommandStruct = CommandArgsStruct[NumArg]
                self.FileStruct[1] += struct.pack(CommandStruct, self.CommandArgs[NumCom][NumArg])
    def RedoRemaining(self):
        self.FileStruct[4] = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    def RedoAll(self):
        self.RedoStrings()
        self.RedoCommands()
        self.RedoRemaining()
        self.RedoHeader()
    def ReinitAll(self):
        self.FileName = ''
        self.FileParametrs = []
        self.FileParametrsSupport = ('File size',
                                    'Header size',
                                    'Command section size',
                                    'String declaration section size',
                                    'String definition section size',
                                    '???',
                                    '???',
                                    '???',
                                    '???')
        self.FileStruct = [b'', b'', b'', b'', b'']
        self.FileStructSupport = ('Header',
                                 'Command Section',
                                 'String Declaration Section',
                                 'String Definition Section',
                                 'Other')
        self.FileStringOffsets = []
        self.FileStrings = []
        self.CommandArgs = []
        self.Commands = []
        self.Labels = []
    #Technical File Operations:
    def CloseFile(self):
        self.File.close()
    def ReadFileBin(self):
        self.File = open(self.FileName + ".gsc", mode="rb")
    def ReadFile(self):
        self.File = open(self.FileName + ".txt", mode="r", encoding="cp932")
    def WriteFileBin(self):
        self.File = open(self.FileName + ".gsc", mode="wb")   
    def WriteFile(self):
        self.File = open(self.FileName + ".txt", mode="w", encoding="cp932")

class GUI():
    root = Tk()
    Language = 'ENG' #RUS
    FileName = ''
    LeftSide = Frame(root)
    LeftTop = Frame(root)
    LeftMiddle = Frame(root)
    LeftBottom = Frame(root)
    RussianLang = Button(root)
    EnglishLang = Button(root)
    InputName = Entry(root)
    Definer = Button(root)
    Clearer = Button(root)
    Undefiner = Button(root)
    SpacerTop = LabelFrame(root)
    # Rebuild = Button(root)
    Decompile = Button(root)
    Compile = Button(root)
    SpacerBottom = LabelFrame(root)
    CommonHelper = Button(root)
    CommandHelper = Button(root)
    SyntaxHelper = Button(root)
    
    def __init__(self):
        self.root['background']='white'
        self.root.resizable(width=False, height=False)
        
        self.root.geometry("400x420+{}+{}".format((self.root.winfo_screenwidth()-400)//2, (self.root.winfo_screenheight()-420)//2))
        self.root.title("GscScriptCompAndDecompiler by Tester 2.0")
            
        self.LeftSide = Frame(self.root, width=400, heigh=600)
        self.LeftSide.pack(side='left')

        self.LeftTop = Frame(self.LeftSide, width=400, height=32, bg="grey")
        self.LeftMiddle = Frame(self.LeftSide, width=400, height=62, bg="grey")
        self.LeftBottom = Frame(self.LeftSide, width=400, height=568, bg="grey")
        self.LeftTop.pack_propagate(False)
        self.LeftTop.pack()
        self.LeftMiddle.pack_propagate(False)
        self.LeftMiddle.pack()
        self.LeftBottom.pack()
    def InitLangButtons(self):
        self.RussianLang = Button(self.LeftTop, command=self.SetLangRus, bg='white', activebackground='gray', font = 'calibri 12', text='　 　　　 　　　РУССКИЙ')
        self.EnglishLang = Button(self.LeftTop, command=self.SetLangEng, bg='white', activebackground='gray', font = 'calibri 12', text='ENGLISH　　　 　　　　 　')
        self.RussianLang.pack(side='left')
        self.EnglishLang.pack(side='right')
    def InitLeftSide(self):
        self.InputName = Entry(self.LeftMiddle, width=400, bd=4, fg="black", font='calibri 12', state=NORMAL)
        self.Definer = Button(self.LeftMiddle, command=self.Define, bg='white', activebackground='gray', font = 'calibri 12', text='                  DEFINE')
        self.Clearer = Button(self.LeftMiddle, command=self.Clear, bg='white', activebackground='gray', font = 'calibri 12', text='          CLEAR          ')
        self.Undefiner = Button(self.LeftMiddle, command=self.Undefine, bg='white', activebackground='gray', font = 'calibri 12', text='UNDEFINE               ')
        self.InputName.pack(side='top')
        self.Definer.pack(side='left')
        self.Clearer.pack(side='left')
        self.Undefiner.pack(side='left')
        self.SpacerTop = LabelFrame(self.LeftBottom, bg='white', height=126, width=400, font = 'calibri 12', text = "COMMANDS:")
        self.SpacerTop.pack_propagate(False)
        self.SpacerTop.pack(side='top')

        # self.Rebuild = Button(self.SpacerTop, command=self.RebuildGscFromGsc, bg='white', activebackground='gray', font = 'calibri 12', text='Rebuild .gsc from .gsc (.gsc -> .gsc)')
        # self.Rebuild.pack(side='top', fill="x", expand='yes')
        self.Decompile = Button(self.SpacerTop, command=self.DecompileToTxt, bg='white', activebackground='gray', font = 'calibri 12', text='Decompile .gsc to .txt (.gsc -> .txt)')
        self.Decompile.pack(side='top', fill="x", expand='yes')
        self.Compile = Button(self.SpacerTop, command=self.CompileFromTxt, bg='white', activebackground='gray', font = 'calibri 12', text='Compile .txt to .gsc (.txt -> .gsc)')
        self.Compile.pack(side='top', fill="x", expand='yes')
        
        self.SpacerBottom = LabelFrame(self.LeftBottom, bg='white', height=126, width=400, font = 'calibri 12', text = "HELP:")
        self.SpacerBottom.pack_propagate(False)
        self.SpacerBottom.pack()

        self.CommonHelper = Button(self.SpacerBottom, command=self.CommonHelp, bg='white', activebackground='gray', font = 'calibri 12', text='Common help')
        self.CommonHelper.pack(side='top', fill="x", expand='yes')
        self.CommandHelper = Button(self.SpacerBottom, command=self.CommandHelp, bg='white', activebackground='gray', font = 'calibri 12', text='Command help')
        self.CommandHelper.pack(side='top', fill="x", expand='yes')
        self.SyntaxHelper = Button(self.SpacerBottom, command=self.SyntaxHelp, bg='white', activebackground='gray', font = 'calibri 12', text='Syntax help')
        self.SyntaxHelper.pack(side='top', fill="x", expand='yes')
        
        self.Outer=Text(self.LeftBottom, width=400, height=3, font='arial 12', state=DISABLED)
        self.Outer.pack()

    #Техническое:
    def SetLangRus(self):
        self.Language = "RUS"
        self.root.title("GscScriptCompAndDecompiler от Tester-а 2.0")
        self.Definer['text'] = "           ОПРЕДЕЛИТЬ"
        self.Clearer['text'] = " ОЧИСТИТЬ "
        self.Undefiner['text'] = "РАЗОПРЕДЕЛИТЬ        "
        self.SpacerTop['text'] = 'КОМАНДЫ:'
        # self.Rebuild['text'] = 'Перестроить .gsc из .gsc (.gsc -> .gsc)'
        self.Decompile['text'] = 'Декомпилировать .gsc в .txt (.gsc -> .txt)'
        self.Compile['text'] = 'Компилировать .txt в .gsc (.txt -> .gsc)'
        self.SpacerBottom['text'] = 'ПОМОЩЬ:'
        self.CommonHelper['text'] = 'Общая помощь'
        self.CommandHelper['text'] = 'Помощь по командам'
        self.SyntaxHelper['text'] = 'Помощь по синтаксису'
        self.Outer['state'] = NORMAL
        self.Outer.delete(1.0, END)
        self.Outer.insert(1.0, "Язык успешно сменён.")
        self.Outer['state'] = DISABLED
    def SetLangEng(self):
        self.Language = "ENG"
        self.root.title("GscScriptCompAndDecompiler by Tester 2.0")
        self.Definer['text'] = "                  DEFINE"
        self.Clearer['text'] = "          CLEAR          "
        self.Undefiner['text'] = "UNDEFINE               "
        self.SpacerTop['text'] = 'COMMANDS:'
        # self.Rebuild['text'] = 'Rebuild .gsc from .gsc (.gsc -> .gsc)'
        self.Decompile['text'] = 'Decompile .gsc to .txt (.gsc -> .txt)'
        self.Compile['text'] = 'Compile .txt to .gsc (.txt -> .gsc)'
        self.SpacerBottom['text'] = 'HELP:'
        self.CommonHelper['text'] = 'Common help'
        self.CommandHelper['text'] = 'Command help'
        self.SyntaxHelper['text'] = 'Syntax help'
        self.Outer['state'] = NORMAL
        self.Outer.delete(1.0, END)
        self.Outer.insert(1.0, "The language was succesfully changed.")
        self.Outer['state'] = DISABLED
    def Clear(self):
        if (self.InputName['state'] == NORMAL):
            self.InputName.delete(0, END)
            self.Outer['state'] = NORMAL
            self.Outer.delete(1.0, END)
            if (self.Language == 'RUS'):
                self.Outer.insert(1.0, "Поле ввода имени успешно очищено.")
            else:
                self.Outer.insert(1.0, "The name entry was succesfully cleared.")
            self.Outer['state'] = DISABLED
        else:
            self.Outer['state'] = NORMAL
            self.Outer.delete(1.0, END)
            if (self.Language == 'RUS'):
                self.Outer.insert(1.0, "Очистка не удалась, ибо имя определено.")
            else:
                self.Outer.insert(1.0, "Can't clear, for the name is defined.")
            self.Outer['state'] = DISABLED
    def Define(self):
        self.FileName = self.InputName.get()
        try:
            if ((self.FileName[-4:] == ".gsc") or (self.FileName[-4:] == '.txt')):
                self.FileName = self.FileName[:-4]
                self.InputName.delete(0, END)
                self.InputName.insert(0, self.FileName)
        except:
            pass
        self.InputName['state'] = DISABLED
        self.Outer['state'] = NORMAL
        self.Outer.delete(1.0, END)
        if (self.Language == 'RUS'):
            self.Outer.insert(1.0, "Поле ввода имени успешно определено.")
        else:
            self.Outer.insert(1.0, "The name entry was succesfully defined.")   
        self.Outer['state'] = DISABLED  
    def Undefine(self):
        self.FileName = ''
        self.InputName['state'] = NORMAL
        self.Outer['state'] = NORMAL
        self.Outer.delete(1.0, END)
        if (self.Language == 'RUS'):
            self.Outer.insert(1.0, "Поле ввода имени успешно разопределено.")
        else:
            self.Outer.insert(1.0, "The name entry was succesfully undefined.")    
        self.Outer['state'] = DISABLED      
    def CommonHelp(self):
        if (self.Language == "RUS"):
            mb.showwarning("Общая помощь", """Данная программа разработана для корректной работы с файлами .gsc движка codeX RScript, известным также как Liar-soft Engine и raiL-soft Engine. Движок относительно простой, как и относительно просты его форматы, в частности .gsc, с которым, впрочем, есть проблематичные моменты, что купируются своеобразной схемой декомпиляции и компиляции. Из-за которой, впрочем, в некоторых случаях возможны проблемы.\n\nДанная программа позволяет:\n1. Декомпиляция .gsc в .txt, позволяющая сколь угодно (в рамках синтаксиса, команд и прочего) редактировать скрипты. Например, с помощью средства добавить новое сообщение проще простого.\n2. Компиляция .txt в .gsc. Она в свою очередь позволяет пересобирать .gsc на основе импровизированного разобранного кода. Для данной команды старый .gsc-скрипт не требуется.\n\nДля использования:\n1. Перетащите либо скрипт .gsc, либо файл .txt с декомпилированными данными в директорию средства.\n2. Напишите его имя в поле ввода и нажмите "ОПРЕДЕЛИТЬ".\n3. Используйте комманды снизу.""")
        else:
            mb.showwarning("Common help", """This program was developed for correctly working with .gsc files of the engine codeX Rscript, which also called as Liar-soft Engine and raiL-soft Engine. The engine is rather simple much like it's formats, for example .gsc, with which through may be some problematic moments. Still the moments are ceasing by the specific decompile and compile. But the scheme can also cause problems it some situations.\n\nThis program allow you to:\n1. .gsc to .txt decomple. It allow you to edit scripts as you like (with limitations of syntax, of course). For example, with this tool you can easily add new message.\n2. .txt to .gsc compile. This allow you to rebuild .gsc from decompiled and may be edited ealier code. It doesn't need an ealier .gsc to present for run.\n\nFor usage:\n1. Drag the .gsc script or .txt with decompiled data to the tool directory.\n2. Write the file name in the tool entry and push the "DEFINE".\n3. Use the commands below.""")
    def CommandHelp(self):
        if (self.Language == "RUS"):
            mb.showwarning("Помощь по командам", """Увы, команд известно мало (но не их структур), а их аргументов ещё меньше. Что, впрочем, может измениться в будущем. Всякая известная команда в файле обозначена некоторой строкой.\n\nИтак, приведём базовые известные команды с аргументами:\n\n3 (0x03): JUMP_UNLESS.\nАргументы: [метка].\n5 (0x05): JUMP.\nАргументы: [метка].\n12 (0x0C): CALL_SCRIPT.\nАргументы: [номер скрипта, ???]\n13 (0x0D): PAUSE.\nАргументы: [время в секундах].\n14 (0x0E): CHOICE.\nАргументы: [???, ???, ???, ???, ???, ???, ???, -1, -1, -1, -1, -1, ???, ???, ???].\n20 (0x14): IMAGE_GET.\nАргументы: [индекс картинки (из имени), ???].\n26 (0x1A): IMAGE_SET.\nАргументы: [].\n28 (0x1C): BLEND_IMG.\nАргументы: [???, тип1, тип2].\n30 (0x1E): IMAGE_DEF.\nАргументы: [???, ???, ???, ???, ???, ???].\n81 (0x51): MESSAGE.\nАргументы: [???, индекс гласа (из имени), ???, -1, -1, ???].\n82 (0x52): APPEND_MESSAGE.\nАргументы: [???, ???, ???, ???, -1, ???].\n83 (0x53): CLEAR_MESSAGE_WINDOW.\nАргументы: [???].\n121 (0x79): GET_DIRECTORY.\nАргументы: [???, -1].\n200 (0xC8): READ_SCENARIO.\nАргументы: [label, ???, ???, ???, ???, ???, ???, ???, ???, ???, ???].\n255 (0xFF): SPRITE.\nАргументы: [режим, позиция, индекс картинки, ???, ???].\n13568 (0x3500): AND.\nАргументы: [???, ???, ???].\n18432 (0x4800): EQUALS.\nАргументы: [???, ???, ???].\n21504 (0x5400): GREATER_EQUALS.\nАргументы: [???, ???, ???].\n43520 (0xAA00): ADD.\nАргументы: [???, ???, ???].\n61696 (0xF100): ASSIGN.\nАргументы: [???, ???].""")
        else:
            mb.showwarning("Command help", """Unfortunately, the number of known commands aren't big (but not of the structures). It may change it the future. All known commands are defined in decomilated file as a string.\n\nWell, let's show you a basic known commands with the arguments:\n\n3 (0x03): JUMP_UNLESS.\nArguments: [label]\n5 (0x05): JUMP.\nArguments: [label].\n12 (0x0C): CALL_SCRIPT.\nArguments: [script number, ???]0\n13 (0x0D): PAUSE.\nArguments: [time in seconds].\n14 (0x0E): CHOICE.\nArguments: [???, ???, ???, ???, ???, ???, ???, -1, -1, -1, -1, -1, ???, ???, ???].\n20 (0x14): IMAGE_GET.\nArguments: [image index (from the name), ???].\n26 (0x1A): IMAGE_SET.\nArguments: [].\n28 (0x1C): BLEND_IMG.\nArguments: [???, type1, type2].\n30 (0x1E): IMAGE_DEF.\nArguments: [???, ???, ???, ???, ???, ???].\n81 (0x51): MESSAGE.\nArguments: [???, voice index (from the name), ???, -1, -1, ???].\n82 (0x52): APPEND_MESSAGE.\nArguments: [???, ???, ???, ???, -1, ???].\n\n83 (0x53): CLEAR_MESSAGE_WINDOW.\nArguments: [???].121 (0x79): GET_DIRECTORY.\nArguments: [???, -1].\n200 (0xC8): READ_SCENARIO.\nArguments: [метка, ???, ???, ???, ???, ???, ???, ???, ???, ???, ???].\n255 (0xFF): SPRITE.\nArguments: [mode, position, image index, ???, ???].\n13568 (0x3500): AND.\nArguments: [???, ???, ???].\n18432 (0x4800): EQUALS.\nArguments: [???, ???, ???].\n21504 (0x5400): GREATER_EQUALS.\nArguments: [???, ???, ???].\n43520 (0xAA00): ADD.\nArguments: [???, ???, ???].\n61696 (0xF100): ASSIGN.\nArguments: [???, ???].""")
    def SyntaxHelp(self):
        if (self.Language == "RUS"):
            mb.showwarning("Помощь по синтаксису", """Для тех, кто скрипты именно редактировать жаждет, сие крайне важно знать. Синтаксис в целом прост, но имеет ряд особенностей.\n\n|"$" в начале строки обозначает однострочный комментарий.\n"#" в начале строки есть определение команды.\n\n"[..., ..., ...]" есть форма описания аргументов функции (разделяются запятой) и следует сразу после определения команды.\n\n"@" есть метка, на кою ссылаются некоторые команды.\n\nАргумент "-1" значит, что он связан с индексом следующей строки.\n\n">" обозначает строк начало.\nПосле сего идёт либо показатель изначального индекса строки, либо -1. -1 значит, что строка связанная. Связанные строки всегда следуют после задачи связанных аргументов.\nВАЖНО: ИНДЕКСЫ ПОСЛЕ ">" ОТОБРАЖАЮТ ЛИШЬ ИЗНАЧАЛЬНЫЕ ИНДЕКСЫ! ПРИ КОМПИЛЯЦИИ ИНДЕКС СТРОКИ БЕРЁТСЯ ЛИШЬ ИЗ НОМЕРА ">" В СКРИПТЕ!\nВАЖНО: НЕ ВСЕ СВЯЗНАННЫЕ ИНДЕКСЫ БЫЛИ НАЙДЕНЫ!""")
        else:
            mb.showwarning("Syntax help", """For those who desire for scripts to edit it's very important. The syntax is rather simple, but it have some specific moments.\n\n"$" is the string's beginning is for one-string comment.\n\n"#" in the string's beginning is for defination of command.\n\n"[..., ..., ...]" is for function argument's splitted with "," form. It goes strictly on the next line after the command defination.\n\n"@" is a label, to which some arguments are connecting.\n\nA "-1" argument means it connected with next string index.\n\n">" is for string beginning.\nAfter its goes mark of primar index of string or -1. If it's -1, the string is connected. Connected strings always goes after the defination of connected arguments.\nDO NOTE: INDEXES AFTER ">" SHOWS ONLY PRIMAR INDEXES! THEN COMPILE PROGRAM TAKE A STRING INDEX ONLY FROM THE NUMBER OF ">" IN SCRIPT!\nDO NOTE: NOT AN ALL OF CONNECTED INDEXES WAS FOUND!""")
    #Connection to .gsc:
    def RebuildGscFromGsc(self):
        try:
            NewScript = GscFile(self.FileName, 0)
            NewScript.ReinitAll()
            NewScript.FileName = self.FileName
            NewScript.RemakeGscFromGsc()
            self.Outer['state'] = NORMAL
            self.Outer.delete(1.0, END)
            if (self.Language == 'RUS'):
                self.Outer.insert(1.0, ".gsc успешно перестроен.")
            else:
                self.Outer.insert(2.0, ".gsc was succesfully rebuilt.")
            self.Outer['state'] = DISABLED
        except:
            self.Outer['state'] = NORMAL
            self.Outer.delete(1.0, END)
            if (self.Language == 'RUS'):
                self.Outer.insert(1.0, "Что-то пошло не так...\nНе удалось перестроить сей .gsc...")
            else:
                self.Outer.insert(1.0, "Something went wrong...\nCouldn't rebuilt this .gsc...")
            self.Outer['state'] = DISABLED
    def DecompileToTxt(self):
        NewScript = GscFile(self.FileName, 0)
        NewScript.ReinitAll()
        NewScript.FileName = self.FileName
        NewScript.DecompileGscToTxt()
        try:
            #NewScript = GscFile(self.FileName, 0)
            #NewScript.ReinitAll()
            #NewScript.FileName = self.FileName
            #NewScript.DecompileGscToTxt()
            self.Outer['state'] = NORMAL
            self.Outer.delete(1.0, END)
            if (self.Language == 'RUS'):
                self.Outer.insert(1.0, ".gsc успешно декомпилирован.")
            else:
                self.Outer.insert(2.0, ".gsc was succesfully decompiled.")
            self.Outer['state'] = DISABLED
        except:
            self.Outer['state'] = NORMAL
            self.Outer.delete(1.0, END)
            if (self.Language == 'RUS'):
                self.Outer.insert(1.0, "Что-то пошло не так...\nНе удалось декомпилировать сей .gsc...")
            else:
                self.Outer.insert(1.0, "Something went wrong...\nCouldn't decompile this .gsc...")
            self.Outer['state'] = DISABLED
    def CompileFromTxt(self):
        NewScript = GscFile(self.FileName, 1)
        NewScript.ReinitAll()
        NewScript.FileName = self.FileName
        NewScript.CompileTxtToGsc()
        try:
            #NewScript = GscFile(self.FileName, 1)
            #NewScript.ReinitAll()
            #NewScript.FileName = self.FileName
            #NewScript.CompileTxtToGsc()
            self.Outer['state'] = NORMAL
            self.Outer.delete(1.0, END)
            if (self.Language == 'RUS'):
                self.Outer.insert(1.0, ".gsc успешно компилирован.")
            else:
                self.Outer.insert(2.0, ".gsc was succesfully compiled.")
            self.Outer['state'] = DISABLED
        except:
            self.Outer['state'] = NORMAL
            self.Outer.delete(1.0, END)
            if (self.Language == 'RUS'):
                self.Outer.insert(1.0, "Что-то пошло не так...\nНе удалось компилировать сей .txt...")
            else:
                self.Outer.insert(1.0, "Something went wrong...\nCouldn't compile this .txt...")
            self.Outer['state'] = DISABLED
CurrentSession = GUI()
CurrentSession.InitLangButtons()
CurrentSession.InitLeftSide()
CurrentSession.root.mainloop()
