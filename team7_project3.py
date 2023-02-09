# Project 3
# Team 7:  Laura Rice - lmr102
#          Rowan Stone - kms240
import sys

instructionList = []  # list of raw instructions
instructionType = []  # list of instruction types ADD, SUB, MUL, etc
instrSpaced = []  # <type 'list'>: ['0 01000 00000 00001 00000 00000 001010', '1 01000 00000 00001 00000 00000 001010',...]
arg1Str = []  # <type 'list'>: ['', '\tR1', '\tR1', '', '\tR1', '\tR1', '\tR10', '\tR3', '\tR4', .....]
arg2Str = []  # <type 'list'>: [0, 1, 1, 0, 1, 0, 10, 3, 4, 5, 0, 5, 0, 5, 6, 1, 1, 0, 0]
arg3Str = []  # <type 'list'>: [0, 10, 264, 0, 264, 48, 2, 172, 216, 260, 8, 6, 0, 6, 172, -1, 264, 0, 0]
addrs = []  # <type 'list'>: [96, 100, 104, 108, ...]
opcodes = []
twosCompList = []  # list that holds 2's comp of bits 0-15 each instruction after break
registerValue = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
dataMemory = []
formattedInstruction = []
mem = []
arg1 = []
arg2 = []
arg3 = []
postMemBuf = []
postALUBuff = []
dest = []
src1 = []
src2 = []
validList = []
funcs = []
numInst = 0

global jumpAddr
global jumpFlag
global branchFlag
global branchAddr
global cycle
global instructionCount
cycle = 1


# function to determine bit 31
def FindBit31(instruction):
    valid = instruction >> 31
    validList.append(valid)
    return valid


# function to determine bits 0-5 aka func in R format
def FindBits0_5(instruction):
    instruction = instruction & 0x0000003f
    return instruction


# function to determine bits 6-10
def FindBits6_10(instruction):
    instruction = instruction & 0x000007c0
    return instruction >> 6


# function to determine bits 11-15
def FindBits11_15(instruction):
    instruction = instruction & 0x0000f800
    return instruction >> 11


# function to determine bits 16-20
def FindBits16_20(instruction):
    instruction = instruction & 0x001f0000
    return instruction >> 16


# function to determine bits 21-25
def FindBits21_25(instruction):
    instruction = instruction & 0x03e00000
    return instruction >> 21


# function to determine bits 26-30 aka opcode
def FindBits26_30(instruction):
    instruction = instruction & 0x7c000000
    return instruction >> 26


# function to determine bits 0-15
def FindBits0_15(instruction):
    instruction = instruction & 0x0000ffff
    return instruction


# function to determine bits 0-25
def FindBits0_25(instruction):
    instruction = instruction & 0x03ffffff
    return instruction


# Finds Twos Comp of a 16 bit offset (Does not work for Branch offset)
def FindTwosComp(offset):
    if offset >> 15 == 1:
        offset = offset - 2 ** 16
    return offset


# FindRegister will determine the register based on the bits passed to the function
def FindRegister(registerBits):
    if registerBits == 0:
        return "R0"
    elif registerBits == 1:
        return "R1"
    elif registerBits == 2:
        return "R2"
    elif registerBits == 3:
        return "R3"
    elif registerBits == 4:
        return "R4"
    elif registerBits == 5:
        return "R5"
    elif registerBits == 6:
        return "R6"
    elif registerBits == 7:
        return "R7"
    elif registerBits == 8:
        return "R8"
    elif registerBits == 9:
        return "R9"
    elif registerBits == 10:
        return "R10"
    elif registerBits == 11:
        return "R11"
    elif registerBits == 12:
        return "R12"
    elif registerBits == 13:
        return "R13"
    elif registerBits == 14:
        return "R14"
    elif registerBits == 15:
        return "R15"
    elif registerBits == 16:
        return "R16"
    elif registerBits == 17:
        return "R17"
    elif registerBits == 18:
        return "R18"
    elif registerBits == 19:
        return "R19"
    elif registerBits == 20:
        return "R20"
    elif registerBits == 21:
        return "R21"
    elif registerBits == 22:
        return "R22"
    elif registerBits == 23:
        return "R23"
    elif registerBits == 24:
        return "R24"
    elif registerBits == 25:
        return "R25"
    elif registerBits == 26:
        return "R26"
    elif registerBits == 27:
        return "R27"
    elif registerBits == 28:
        return "R28"
    elif registerBits == 29:
        return "R29"
    elif registerBits == 30:
        return "R30"
    elif registerBits == 31:
        return "R31"
    else:
        return " Unknown Register "


def disassemble(instruction, pc):
    global validBit
    validBit = FindBit31(instruction)
    vBitString = bin(validBit)[2:].zfill(1)

    # Memory address begins at 96
    addrs.append(pc)
    instructionCount = 0

    # determine opcode to determine instruction format
    global opcode
    opcode = int(FindBits26_30(instruction))
    opCodeString = bin(opcode)[2:].zfill(5)
    opcodes.append(opcode)

    global bits0_5
    bits0_5 = int(FindBits0_5(instruction))
    bits0_5st = bin(bits0_5)[2:].zfill(6)

    global bits6_10
    bits6_10 = int(FindBits6_10(instruction))
    bits6_10st = bin(bits6_10)[2:].zfill(5)

    global bits11_15
    bits11_15 = int(FindBits11_15(instruction))
    bits11_15st = bin(bits11_15)[2:].zfill(5)

    global bits16_20
    bits16_20 = int(FindBits16_20(instruction))
    bits16_20st = bin(bits16_20)[2:].zfill(5)

    global bits21_25
    bits21_25 = int(FindBits21_25(instruction))
    bits21_25st = bin(bits21_25)[2:].zfill(5)

    global bits0_15
    bits0_15 = int(FindBits0_15(instruction))
    bits0_25 = FindBits0_25(instruction)

    offset = int(FindBits0_15(instruction))
    offset = int(FindTwosComp(offset))

    instrSpaced.append(
        '%s %s %s %s %s %s %s' % (validBit, opCodeString, bits21_25st, bits16_20st, bits11_15st, bits6_10st, bits0_5st))


    if validBit == 1:
        global numInst
        numInst = numInst + 1
        # Since instruction is valid, determine opcode
        # using opcode, determine which format: R,I,J

        if opcode == 0:  # R format

            # determine func
            func = int(FindBits0_5(instruction))
            funcs.append(func)

            if func == 8:
                instructionType.append("JR\t")
                rs = FindRegister(bits21_25)
                src1.append(bits21_25)
                arg1Str.append(rs)
                arg1.append(bits21_25)

                arg2Str.append(" ")
                arg2.append(0)
                src2.append(-3)

                arg3Str.append(" ")
                arg3.append(0)
                dest.append(-3)

                formattedInstruction.append('\t[' + 'JR\tR' + str(bits21_25) + ']')

            elif func == 0:  # nop or sll
                # both SLL and NOP have func 0
                # distinguish between two by looking at bits 6 -10
                if FindBits6_10(instruction) == 0:
                    instructionType.append("NOP\t")
                    arg1Str.append(" ")
                    arg1.append(0)
                    src1.append(-3)

                    arg2Str.append(" ")
                    arg2.append(0)
                    src2.append(-4)

                    arg3Str.append(" ")
                    arg3.append(0)
                    dest.append(-4)

                    formattedInstruction.append('\t[' + 'NOP\t' + ']')

                else:
                    instructionType.append("SLL\t")

                    # determine rd for arg1
                    rd = FindRegister(bits11_15)
                    arg1Str.append(rd + ', ')
                    arg1.append(bits11_15)
                    dest.append(bits11_15)

                    # determine rt for arg2
                    rt = FindRegister(bits16_20)
                    arg2Str.append(rt + ', ')
                    arg2.append(bits16_20)
                    src1.append(bits16_20)

                    # determine shift amount for sll
                    shamt = FindBits6_10(instruction)
                    arg3Str.append('#' + str(shamt))
                    arg3.append(shamt)
                    src2.append(-3)

                    formattedInstruction.append('\t[SLL' + '\tR' + str(bits11_15) + ', R' + str(bits16_20) + ', #' + str(shamt) + ']')
            elif func == 2:  # srl
                instructionType.append("SRL\t")

                # determine rd for arg1
                rd = FindRegister(bits11_15)
                arg1Str.append(rd + ', ')
                arg1.append(bits11_15)
                dest.append(bits11_15)

                # determine rt for arg2
                rt = FindRegister(bits16_20)
                arg2Str.append(rt + ', ')
                arg2.append(bits16_20)
                src1.append(bits16_20)

                # determine shift amount for srl
                shamt = FindBits6_10(instruction)
                arg3Str.append('#' + str(shamt))
                arg3.append(shamt)
                src2.append(-5)

                formattedInstruction.append('\t[SRL' + '\tR' + str(bits11_15) + ', R' + str(bits16_20) + ', #' + str(shamt) + ']')

            elif func == 13:  # BREAK
                instructionType.append("BREAK")
                arg1Str.append("")
                arg2Str.append("")
                arg3Str.append("")
                arg1.append(0)
                arg2.append(0)
                arg3.append(0)
                src1.append(-3)
                src2.append(-3)
                dest.append(-3)
                funcs.append(-1)

            else:
                if func == 0x20:
                    instructionType.append("ADD\t")
                elif func == 0x22:
                    instructionType.append("SUB\t")
                elif func == 0x24:
                    instructionType.append("AND\t")
                elif func == 0x25:
                    instructionType.append("OR\t")
                elif func == 0x26:
                    instructionType.append("XOR\t")
                elif func == 0x0a:
                    instructionType.append("MOVZ\t")
                else:
                    instructionType.append("Unknown Instruction\t")
                    funcs.append(-1)

                # determine destination register or argument 1
                rd = FindRegister(bits11_15)
                arg1Str.append(rd + ', ')
                arg1.append(bits11_15)
                dest.append(bits11_15)

                # determine source register for argument 2
                rs = FindRegister(bits21_25)
                arg2Str.append(rs + ', ')
                arg2.append(bits21_25)
                src1.append(bits21_25)

                # determine tempregister for argument 3
                rt = FindRegister(bits16_20)
                arg3Str.append(rt)
                arg3.append(bits16_20)
                src2.append(bits16_20)

                #determine formatted instruction
                if func == 0x20:
                    formattedInstruction.append('\t[ADD' + '\tR' + str(bits16_20) + ', R' + str(bits11_15) + ', R' + str(bits21_25) + ']')
                elif func == 0x22:
                    formattedInstruction.append('\t[SUB' + '\tR' + str(bits16_20) + ', R' + str(bits11_15) + ', R' + str(bits21_25) + ']')
                elif func == 0x24:
                    formattedInstruction.append('\t[AND' + '\tR' + str(bits16_20) + ', R' + str(bits11_15) + ', R' + str(bits21_25) + ']')
                elif func == 0x25:
                    formattedInstruction.append('\t[OR' + '\tR' + str(bits16_20) + ', R' + str(bits11_15) + ', R' + str(bits21_25) + ']')
                elif func == 0x26:
                    formattedInstruction.append('\t[XOR' + '\tR' + str(bits16_20) + ', R' + str(bits11_15) + ', R' + str(bits21_25) + ']')
                elif func == 0x0a:
                    formattedInstruction.append('\t[MOVZ' + '\tR' + str(bits16_20) + ', R' + str(bits11_15) + ', R' + str(bits21_25) + ']')
                else:
                    formattedInstruction.append('\t[INVALID INSTRUCTION' + ']')


        elif opcode == 2:  # J Format

            # find jump address by recovering bits
            addressJump = FindBits0_25(instruction) << 2

            instructionType.append("J\t")
            arg1Str.append('#' + str(addressJump))
            arg1.append(addressJump)
            arg2Str.append(" ")
            arg2.append(0)
            arg3Str.append(" ")
            arg3.append(0)
            src1.append(-3)
            src2.append(-3)
            dest.append(-3)

            formattedInstruction.append('\t[' + 'J\t#' + str(addressJump) + ']')

        else:  # I Format

            # if branch instructions
            if opcode == 5 or opcode == 6:
                # determine offset for branch
                BOffset = bits0_15 << 2
                # Calculate 2's complement for Branch offset which is 18 bits
                # determine if most significant bit is negative
                if (BOffset >> 17 == 1):
                    BOffset = BOffset - 2 ** 18

                # determine source register
                rs = FindRegister(bits21_25)

                if opcode == 5:
                    instructionType.append("BNE\t")
                    rt = FindRegister(bits16_20)
                    arg1Str.append(rs + ', ')
                    arg1.append(bits21_25)
                    src1.append(bits21_25)

                    arg2Str.append(rt + ', ')
                    arg2.append(bits16_20)
                    src2.append(bits16_20)

                    arg3Str.append("#" + str(BOffset))
                    arg3.append(BOffset)
                    dest.append(-3)

                    formattedInstruction.append('\t[BNE' + '\tR' + str(bits21_25) + ', R' + str(bits16_20) + ', #' + str(BOffset) + ']')
                else:
                    instructionType.append("BLEZ\t")
                    arg1Str.append(rs + ', ')
                    arg1.append(rs)
                    src1.append(bits21_25)

                    arg2Str.append("#")
                    arg2.append(0)
                    src2.append(-3)

                    arg3Str.append(str(BOffset) + "")
                    arg3.append(BOffset)
                    dest.append(-3)

                    formattedInstruction.append('\t[BLEZ' + '\tR' + str(bits21_25) + ', #' + str(BOffset) + ']')
            elif opcode == 8:

                instructionType.append("ADDI\t")

                rt = FindRegister(bits16_20)
                arg1Str.append(rt + ', ')
                arg1.append(bits16_20)
                dest.append(bits16_20)

                rs = FindRegister(bits21_25)
                arg2Str.append(rs + ', ')
                arg2.append(bits21_25)
                src1.append(bits21_25)

                imm = int(FindBits0_15(instruction))
                imm = FindTwosComp(imm)
                arg3Str.append('#' + str(imm))
                arg3.append(imm)
                src2.append(-1)
                funcs.append(-1)

                formattedInstruction.append('\t[ADDI' + '\tR' + str(bits16_20) + ', R' + str(bits21_25) + ', #' + str(imm) + ']')
            elif opcode == 3:  # LW
                instructionType.append("LW\t")

                rs = FindRegister(bits21_25)
                arg3Str.append('(' + rs + ')')
                arg3.append(bits21_25)
                src1.append(bits21_25)

                rt = FindRegister(bits16_20)
                arg1Str.append(rt + ', ')
                arg1.append(bits16_20)
                src2.append(bits16_20)

                # find offset
                offset = bits0_15
                offset = FindTwosComp(offset)
                arg2Str.append(str(offset))
                arg2.append(offset)
                dest.append(-4)

                formattedInstruction.append('\t[LW' + '\tR' + str(bits16_20) + ', ' + str(offset) + '(R' + str(bits21_25) + ')' + ']')

            elif opcode == 0xb:  # SW
                instructionType.append("SW\t")

                rs = FindRegister(bits21_25)
                arg3Str.append('(' + rs + ')')
                arg3.append(bits21_25)
                src1.append(bits21_25)

                rt = FindRegister(bits16_20)
                arg1Str.append(rt + ', ')
                arg1.append(bits16_20)
                src2.append(bits16_20)

                # find offset
                offset = bits0_15
                offset = FindTwosComp(offset)
                arg2Str.append(str(offset))
                arg2.append(offset)
                dest.append(bits0_15)

                formattedInstruction.append('\t[SW' + '\tR' + str(bits16_20) + ', ' + str(offset) + '(R' + str(bits21_25) + ')' + ']')

            elif opcode == 0x1c:  # MUL
                instructionType.append("MUL\t")
                # determine destination register or argument 1
                rs = FindRegister(bits21_25)
                arg1Str.append(rs + ', ')
                arg1.append(bits21_25)


                # determine source register for argument 2
                rt = FindRegister(bits16_20)
                arg2Str.append(rt + ', ')
                arg2.append(bits16_20)

                # determine temp register for argument 3
                rd = FindRegister(bits11_15)
                arg3Str.append(rd)
                arg3.append(bits11_15)

                dest.append(bits11_15)
                src1.append(bits21_25)
                src2.append(bits16_20)

                formattedInstruction.append('\t[MUL' + '\tR' + str(bits11_15) + ', R' + str(bits21_25) + ' ,R' + str(bits16_20) + ']')
            else:
                instructionType.append("BREAK\n")
                arg1Str.append("")
                arg1.append(0)
                arg2Str.append("")
                arg2.append(0)
                arg3Str.append("")
                arg3.append(0)

                src2.append(-3)
                src1.append(-3)
                dest.append(-4)


                formattedInstruction.append('\t[BREAK]')
    else:
        # print address
        instructionType.append("Invalid Instruction")
        arg1Str.append("")
        arg1.append(0)
        arg2Str.append("")
        arg2.append(0)
        arg3Str.append("")
        arg3.append(0)

        src1.append(-3)
        src2.append(-3)
        dest.append(-3)
        funcs.append(-1)

        formattedInstruction.append('\t[Invalid Instruction' + ']')

class WB:

    def __init__(self):
        pass

    def run(self):
        #print("Post ALU Buff:" + str(simulator.postALUBuff))
        #print ("Post Mem Buff: "+str(simulator.postMemBuf))
        if simulator.postALUBuff[1] != -1:
            simulator.registerValue[simulator.destReg[simulator.postALUBuff[1]]] = simulator.postALUBuff[0]
            #print("simulator.destReg[simulator.postALUBuff[1]]: "+str(simulator.destReg[simulator.postALUBuff[1]]))
            #simulator.registerValue[simulator.postALUBuff[1]] = simulator.postALUBuff[0]
            simulator.postALUBuff[0] = -1
            simulator.postALUBuff[1] = -1

        if simulator.postMemBuf[1] != -1:
            simulator.registerValue[simulator.destReg[simulator.postMemBuf[1]]] = simulator.postMemBuf[0]
            #simulator.registerValue[simulator.postMemBuf[1]] = simulator.postMemBuf[0]
            simulator.postMemBuf[0] = -1
            simulator.postMemBuf[1] = -1

class ALU:

    def __init__(self):
        pass

    def run(self):
        #expects valid preBuff
        #print ("Pre ALU Buffer: "+str(simulator.preALUBuff))
        if simulator.preALUBuff[0] != -1:
            i = simulator.preALUBuff[0]
            simulator.postALUBuff[1] = i

            if simulator.opcodeList[i] == 0 and simulator.funcBits[i] == 0x20:  # ADD
                simulator.postALUBuff = [simulator.registerValue[simulator.arg1[i]] + simulator.registerValue[simulator.arg2[i]], i]
            elif simulator.opcodeList[i] == 8: #ADDI
                simulator.postALUBuff = [simulator.registerValue[simulator.arg1[i]] + simulator.arg3[i], i]
            elif simulator.opcodeList[i] == 0 and simulator.funcBits[i] == 0x22:  # SUB
                simulator.postALUBuff = [simulator.registerValue[simulator.arg1[i]] - simulator.registerValue[simulator.arg2[i]], i]
            elif simulator.opcodeList[i] == 0 and simulator.funcBits[i] == 0x24:  # AND
                simulator.postALUBuff = [simulator.registerValue[simulator.arg1[i]] & simulator.registerValue[simulator.arg2[i]], i]
            elif simulator.opcodeList[i] == 0 and simulator.funcBits[i] == 0x25:  # OR
                simulator.postALUBuff = [simulator.registerValue[simulator.arg1[i]] | simulator.registerValue[simulator.arg2[i]], i]
            elif simulator.opcodeList[i] == 0 and simulator.funcBits[i] == 0x24:  # XOR
                simulator.postALUBuff = [simulator.registerValue[simulator.arg1[i]] ^ simulator.registerValue[simulator.arg2[i]], i]
            elif simulator.opcodeList[i] == 0x1c and simulator.funcBits[i] == 2:  # MUL
                simulator.postALUBuff = [simulator.registerValue[simulator.arg1[i]] * simulator.registerValue[simulator.arg2[i]], i]
            elif simulator.opcodeList[i] == 0x1c and simulator.funcBits[i] == 2:  # SRL
                simulator.postALUBuff = simulator.registerValue[simulator.arg1[i]] >> simulator.arg3[i]
            elif simulator.opcodeList[i] == 0 and simulator.funcBits[i] == 0 and simulator.arg3 != 0:  # SLL
                simulator.postALUBuff = simulator.registerValue[simulator.arg1[i]] << simulator.arg3[i]
            elif simulator.opcodeList[i] == 0 and simulator.funcBits[i] == 0xa and simulator.arg3 != 0:  # MOVZ
                if simulator.src2Reg[i] == 0:
                    simulator.postALUBuff[0] = simulator.src1Reg[i]

            simulator.preALUBuff[0] = simulator.preALUBuff[1]
            simulator.preALUBuff[1] = -1

        else:
            pass

class cacheClass:   #holds both data and instructions
    #4 sets of 2 blocks, 2 words per block, each block has valid bit, dirty bit, tag, data1 and data2
    # in that order(5 elements per block)

    setMask = int('0011111', 2) #4 sets in cache ~> 2 bits needed for Set Index with Word alignment
    tagMask = int('00000000000000000000000001111111', 2)#Most significant bits after set + word alignment

    def __init__(self):
        self.cacheSets=[[[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]]
        self.lruBit = [0, 0, 0, 0]  # Least Recently Used bit, one for each set.
        self.dataWordBlock = 0
        self.memLocAddr = 0
        self.address0 = 0
        self.address1 = 0
        self.data1 = 0
        self.data2 = 0
        self.tag = 0
        self.setNum = 0
        self.missCount = 0
        self.fetchedData = 0
        self.wbAddr = 0


    def accessMem(self, memIndex, instrIndex, isWriteToMem,dataToWrite):
        cacheHit = False
        assocblock = 0

        #calculate memLocAddr based on whether instruction or data
        if instrIndex != -1:
            self.memLocAddr = 96 + (instrIndex*4)
            #print("mem Loc address: " + str(self.memLocAddr))
        #Based on address, align address to two word alignment and create addresses for the 2 words in the block
            if self.memLocAddr % 8 == 0:
                self.dataWordBlock = 0
                self.address0 = self.memLocAddr
                self.address1 = self.memLocAddr + 4

            elif self.memLocAddr % 8 != 0:
                self.dataWordBlock = 1
                self.address0 = self.memLocAddr - 4
                self.address1 = self.memLocAddr
            valIndex1 = (self.address0 - 96)/4
            valIndex2 = (self.address1 - 96)/4
            self.data1 = int(simulator.instructionList[valIndex1])
            self.data2 = int(simulator.instructionList[valIndex2])

        else:
            self.memLocAddr = 96 + (memIndex*4)
            if self.memLocAddr % 8 == 0:
                self.dataWordBlock = 0
                self.address0 = self.memLocAddr
                self.address1 = self.memLocAddr + 4

            elif self.memLocAddr % 8 != 0:
                self.dataWordBlock = 1
                self.address0 = self.memLocAddr - 4
                self.address1 = self.memLocAddr
            valIndex1 = (self.address0 - 96)/4
            valIndex2 = (self.address1 - 96)/4
            self.data1 = int(simulator.instructionList[valIndex1], 2)
            self.data2 = int(simulator.instructionList[valIndex2], 2)

        #Decode the cache address from the address for word0 (tag, set)
        print("Address: "+ str(self.address0))
        self.tag = (self.address0 ^ self.tagMask)
        print("Tag: "+str(self.tag))
        self.setNum = (self.tag & self.setMask) >> 5
        print("Set Number: " +str(self.setNum))

        # IF WRITING TO MEM(reference slides)
        if (memIndex != -1 and isWriteToMem):
            if (self.dataWordBlock == 0 and isWriteToMem):
                # Overwrite either data1 or data2 with the passed in dataToWrite based on dataword value
                self.data1 = int(dataToWrite)
            elif (self.dataWordBlock == 1 and isWriteToMem):
                self.data2 = int(dataToWrite)

        #Look in cache and see if the address we are looking for is either one of the blocks. If hit, set assocblock to the block num.
        if self.cacheSets[self.setNum][0][2] == self.tag:
            cacheHit = True
            assocblock = 0
        elif self.cacheSets[self.setNum][1][2] == self.tag:
            cacheHit = True
            assocblock = 1
        else:
            cacheHit = False

        # IF HIT and WRITING TO MEM
        if cacheHit == True and isWriteToMem:
            if simulator.cycle > 1:
                #Update cache blocks dirty bit, update set LRU bit, write the data to cache
                self.cacheSets[self.setNum][assocblock][1] = 1
                self.lruBit[self.setNum] = 1
                self.cacheSets[self.setNum][assocblock][3] = self.data1
                self.cacheSets[self.setNum][assocblock][4] = self.data2
            else:
                pass
            return(cacheHit, self.cacheSets[self.setNum][assocblock][self.dataWordBlock+3])

        # IF HIT and NOT WRITING TO MEM
        if cacheHit == True and isWriteToMem == False:
            self.lruBit[self.setNum] = 1
            return(cacheHit, self.cacheSets[self.setNum][assocblock][self.dataWordBlock+3])

        # IF MISS, CHECK IF INITIAL MISS OR SECOND MISS.
        if cacheHit == False:

            if self.missCount < 2:   # Initial Miss
                return (cacheHit, 0)

            elif self.missCount == 2:    #2nd Miss
                if instrIndex != -1:
                    self.fetchedData = int(simulator.instructionList[instrIndex])
                else:
                    self.fetchedData = int(simulator.instructionList[memIndex])

            if self.cacheSets[self.setNum][self.lruBit[self.setNum]][1] == 1:
            #write back the memory address asociated with the block
                self.wbAddr =  self.cacheSets[self.setNum][ self.lruBit[self.setNum] ][2] # #tag
                #modify tag to get back to the original address, remember all addresses are inherently word aligned
                #lower 2 bits are zero !!!!
                self.wbAddr = (self.wbAddr << 5) +(self.setNum << 3)
                if( self.wbAddr >= (simulator.numInstructions  *4) + 96 ):
                    simulator.mem[simulator.getIndexOfMemAddress(self.wbAddr)] = self.cacheSets[self.setNum][ self.lruBit[self.setNum]][3]
                if( self.wbAddr+4 >= (simulator.numInstructions  *4) + 96 ):
                    simulator.mem[simulator.getIndexOfMemAddress(self.wbAddr+4)] = self.cacheSets[self.setNum][ self.lruBit[self.setNum]][4]
                # now update the cache flag bits
                self.cacheSets[self.setNum][ self.lruBit[self.setNum] ][0] = 1 #valid  we are writing a block
                self.cacheSets[self.setNum][ self.lruBit[self.setNum] ][1] = 0 #reset the dirty bit
                if( isWriteToMem ):
                    self.cacheSets[self.setNum][ self.lruBit[self.setNum] ][1] = 1 #dirty if is data mem is dirty again, intruction mem never dirty
                # update both words in the actual cache block in set
                self.cacheSets[self.setNum][ self.lruBit[self.setNum] ][2] = self.tag #tag
                self.cacheSets[self.setNum][ self.lruBit[self.setNum] ][3] = self.data1 #data
                self.cacheSets[self.setNum][ self.lruBit[self.setNum] ][4] = self.data2 #nextData
                self.lruBit[self.setNum] = (self.lruBit[self.setNum] + 1) % 2# set lru to show block is recently used
                return (True, self.cacheSets[self.setNum][(self.lruBit[self.setNum] + 1)%2][self.dataWordBlock + 3])

            elif self.cacheSets[self.setNum][self.lruBit[self.setNum]][1] == 0:
                self.cacheSets[self.setNum][self.lruBit[self.setNum]][self.dataWordBlock + 3] = self.fetchedData
                self.cacheSets[self.setNum][self.lruBit[self.setNum]][1] = 1

            return(cacheHit, self.cacheSets[self.setNum][self.dataWordBlock][self.dataWordBlock+3])





        return (cacheHit, self.cacheSets[self.setNum][(self.lruBit[self.setNum] +1 ) % 2][self.dataWordBlock+3])


    def flush(self):
        pass #placeholder


class MEM:

    def __init__(self):
        self.isLoadStore = False
        self.cacheHit = False
        self.isStore = False
        #self.preMemBuffer = []
        self.instrOp = 0
        self.dataOrInstr = 0

    def decodeInstr(self):

        if simulator.preMemBuf[0] >= -1:
            if simulator.opcodeList[simulator.preMemBuf[0]] == 3 or simulator.opcodeList[simulator.preMemBuf[0]] == 0xb:
                self.isLoadStore = True
                if simulator.opcodeList[simulator.preMemBuf[0]] == 0xb:
                    self.isStore = True
                return simulator.opcodeList[simulator.preMemBuf[0]]
            else:
                pass
                # For testing purposes only.
                #self.isLoadStore = True
                #self.isStore = True
            return simulator.opcodeList[simulator.preMemBuf[0]]

    def checkCache(self, addrIndex, instIndex, isStore, registerValueindex):
        #   return with hit value (boolean)
        return simulator.cache.accessMem(addrIndex, instIndex, isStore, registerValueindex) #simulator.registerValue[simulator.arg2[self.preMemBuffer[0]]])

    def run(self):

        #print("Pre Mem Buffer(simulator): "+str(simulator.preMemBuf))

        self.instrOp = self.decodeInstr()

        if self.isLoadStore == True:
            if self.isStore == False:
                memAddress = simulator.arg3[simulator.preMemBuf[0]] + simulator.registerValue[simulator.src1Reg[simulator.preMemBuf[0]]]
                self.cacheHit, self.dataOrInstr = self.checkCache(memAddress, simulator.preMemBuf[0], self.isStore, simulator.registerValue[simulator.arg2[simulator.preMemBuf[0]]])

            elif self.isStore == True:
                memAddress = simulator.arg3[simulator.preMemBuf[0]] + simulator.registerValue[simulator.src2Reg[simulator.preMemBuf[0]]]
                self.cacheHit, self.dataOrInstr = self.checkCache(memAddress, simulator.preMemBuf[0], self.isStore, simulator.registerValue[simulator.arg2[simulator.preMemBuf[0]]])

            if self.cacheHit == True:
                if self.isStore == False:
                    print("Data or Instr: "+str(self.dataOrInstr))
                    simulator.postMemBuf[0] = self.dataOrInstr
                    simulator.postMemBuf[1] = simulator.preMemBuf[1]

            simulator.preMemBuf[0] = simulator.preMemBuf[1]
            simulator.preMemBuf[1] = -1

            #print("Post Mem Buffer(simulator): "+str(simulator.postMemBuf))

        else:
            pass

class Issue:

     def __init__(self):
         pass

     def run(self):
         issueMe = True
         numIssued = 0
         numInPreIssueBuff = 0
         curr = 0

         #for n in range(0, len(simulator.preIssueBuff)):
             #if(simulator.preIssueBuff[n] != -1):
                 #numInPreIssueBuff += 1


         while(numIssued < 2 and numInPreIssueBuff > 0 and curr < 4): #curr is current pre issue element
             #print("Pre Issue Buffer(simulator): "+str(simulator.preIssueBuff))
             curr = simulator.preIssueBuff[0]

             if simulator.isMemoryOp(simulator.preIssueBuff[curr]) is True and not -1 in simulator.preMemBuf:
                 issueMe = False
                 break
             elif simulator.isMemoryOp(simulator.preIssueBuff[curr]) is True and not -1 in simulator.preALUBuff:
                 issueMe = False
                 break

             if curr > 0:
                 for i in range(0, curr):
                     if simulator.destReg[simulator.preIssueBuff[curr]] == simulator.src1Reg[i] or simulator.destReg[simulator.preIssueBuff[curr]] == simulator.src2Reg[i]:
                        # found WAR hazard
                         issueMe = False
                         break
                     elif simulator.src1Reg[simulator.preIssueBuff[curr]] == simulator.destReg[i] or simulator.src2Reg[simulator.preIssueBuff[curr]] == simulator.destReg[i]:
                         #found RAW hazard
                         issueMe = False

             if simulator.isMemoryOp(simulator.preIssueBuff[curr]):
                 for i in range(0, len(simulator.preMemBuf)):
                     if simulator.preMemBuf[i] != -1:
                         if(simulator.destReg[simulator.preIssueBuff[curr]] == simulator.src1Reg[i] or simulator.destReg[simulator.preIssueBuff[curr]] == simulator.src2Reg[i]):
                             # found WAR hazard in pre issue buffer
                             issueMe = False
                             break
             if simulator.isMemoryOp(simulator.preIssueBuff[curr]):
                 for i in range(0, len(simulator.preALUBuff)):
                     if simulator.preALUBuff[i] != -1:
                         if (simulator.destReg[simulator.preIssueBuff[curr]] == simulator.src1Reg[simulator.preALUBuff[i]] or simulator.destReg[simulator.preIssueBuff[curr]] == simulator.src2Reg[simulator.preALUBuff[i]]):                                 # found WAR hazard in pre issue buffer
                             issueMe = False
                             break

             #Do RAW checks same as above and check post buffers too
             for i in range(0, len(simulator.preMemBuf)):
                if simulator.preMemBuf[i] != -1:
                    if (simulator.src1Reg[simulator.preIssueBuff[curr]] == simulator.destReg[simulator.preMemBuf[i]] or simulator.src2Reg[simulator.preIssueBuff[curr]] == simulator.destReg[simulator.preMemBuf[i]]):
                        issueMe = False
                        break

             for i in range(0, len(simulator.preALUBuff)):
                if simulator.preMemBuf[i] != -1:
                    if (simulator.src1Reg[simulator.preIssueBuff[curr]] == simulator.destReg[simulator.preALUBuff[i]] or simulator.src2Reg[simulator.preIssueBuff[curr]] == simulator.destReg[simulator.preALUBuff[i]]):
                        issueMe = False
                        break

             if simulator.postALUBuff[1] != -1:
                 if (simulator.src1Reg[simulator.preIssueBuff[curr]] == simulator.destReg[simulator.postALUBuff[1]] or simulator.src2Reg[simulator.preIssueBuff[curr]] == simulator.destReg[simulator.postALUBuff[1]]):
                     # RAW hazard found in Post ALU Buffer
                     issueMe = False

             if simulator.postMemBuf[1] != -1:
                 if (simulator.src1Reg[simulator.preIssueBuff[curr]] == simulator.destReg[simulator.postMemBuf[1]] or simulator.src2Reg[simulator.preIssueBuff[curr]] == simulator.destReg[simulator.postMemBuf[1]]):
                     # RAW hazard found in Post Mem Buffer
                     issueMe = False

             #Do WAW Hazard Check
             for i in range(0, curr):
                 if (simulator.destReg[simulator.preIssueBuff[curr]] == simulator.destReg[simulator.preIssueBuff[i]]):
                     issueMe = False

             for i in range(0, len(simulator.preMemBuf)):
                 if simulator.preMemBuf != -1:
                     if (simulator.destReg[simulator.preIssueBuff[curr]] == simulator.destReg[simulator.preMemBuf[i]]):
                         issueMe = False

             for i in range(0, len(simulator.preALUBuff)):
                 if simulator.preMemBuf != -1:
                     if (simulator.destReg[simulator.preIssueBuff[curr]] == simulator.destReg[simulator.preALUBuff[i]]):
                         issueMe = False

             for i in range(0, len(simulator.postMemBuf)):
                 if simulator.preMemBuf != -1:
                     if (simulator.destReg[simulator.preIssueBuff[curr]] == simulator.destReg[simulator.postMemBuf[i]]):
                         issueMe = False

             for i in range(0, len(simulator.postALUBuff)):
                 if simulator.preMemBuf != -1:
                     if (simulator.destReg[simulator.preIssueBuff[curr]] == simulator.destReg[simulator.postALUBuff[i]]):
                         issueMe = False

            ### Enforce Ordering of LW and Store Words, such that all word stores are done before word loads ###

            ###

         if issueMe:
             numIssued += 1
             if simulator.isMemoryOp(simulator.preIssueBuff[curr]):
                 simulator.preMemBuf[simulator.preMemBuf.index(-1)] = simulator.preIssueBuff[curr]
             else:
                 simulator.preALUBuff[simulator.preALUBuff.index(-1)] = simulator.preIssueBuff[curr]
             simulator.preIssueBuff[0:curr] = simulator.preIssueBuff[0:curr]
             simulator.preIssueBuff[curr:3] = simulator.preIssueBuff[curr+1:]
             simulator.preIssueBuff[3] = -1
             numInPreIssueBuff -= 1
         else:
             curr += 1


class Fetch:
    def __init__(self):
        pass

    def run(self):
        preIssueNum = 0
        index = (simulator.pc - 96)/4
        numInstrIssued = 0

        #Fetch up to two empty slots for preissue buffer
        for n in range(len(simulator.preIssueBuff)):
            if simulator.preIssueBuff[n] != -1:
                preIssueNum += 1

        #check if instruction is in cache but cache isn't working properly
        if preIssueNum < 4:
            #print("Fetch index: "+str(index))
            cacheHit, value = simulator.cache.accessMem(-1, index, False, 0)
            if cacheHit and preIssueNum:
                instruction = simulator.instructionList[index +1]
                simulator.preIssueBuff[preIssueNum] = index
                simulator.pc += 4
                preIssueNum += 1


        #if cache hit, determine if branch or jump
        if simulator.instructionName[index] == 'BNE' or simulator.instructionName[index] == 'BLEZ':
            #check for hazards
            pass
        elif simulator.instructionName[index] == 'J':
            simulator.pc = simulator.arg1[index]
        elif simulator.instructionName[index] == 'JR':
            simulator.pc = simulator.registerValue[simulator.src1Reg[index]]
        elif simulator.instructionName == 'Invalid Instruction':
            simulator.pc = simulator.pc + 4
        elif simulator.instructionName[index] == 'BREAK':
            #perform cleanup to make sure all instruction finish
            pass

        else:
            simulator.preIssueBuff[preIssueNum] = index
            simulator.pc += 4
            preIssueNum += 1

        if (index + 1 == (simulator.pc - 96)/4) and preIssueNum < 4:
            index += 1
            #print("preIssueNum: "+str(preIssueNum))
            simulator.preIssueBuff[preIssueNum] = index
            simulator.pc += 4
            preIssueNum += 1



        #print("Pre Issue Buffer(simulator, in Fetch): "+str(simulator.preIssueBuff))

        if(simulator.cycle > 12): ## To prevent infinite loop during testing
            return False
        else:
            return True

class sim:
    instructionList = []  # list of raw instructions
    address = []  # <type 'list'>: [96, 100, 104, 108, ...]
    twosCompList = []  # list that holds 2's comp of bits 0-15 each instruction after break
    registerValue = []#[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    dataAddress = []
    opcodeList = []
    validInstr = []
    numInstructions = 0
    mem = []
    arg1 = []
    arg2 = []
    arg3 = []
    funcBits = []
    destReg = []
    src1Reg = []
    src2Reg = []
    instructionName = []

    writeBack = WB()
    execute = ALU()
    cache = cacheClass()
    loadstore = MEM()
    issue = Issue()
    instrFetch = Fetch()

    def __init__(self, instrs, opcodes, data, valids, addrs, arg1, arg2, arg3, numInstrs, dest, src1, src2, funcs, dataMemory,instructionType):
        self.instructionList = instrs
        self.registerValue = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.opcodeList = opcodes
        self.mem = data
        self.pc = 96
        self.validInstr = valids
        self.address = addrs
        self.numInstructions = numInstrs
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.destReg = dest
        self.src1Reg = src1
        self.src2Reg = src2
        self.funcBits = funcs
        self.dataAddress = dataMemory
        self.instructionName = instructionType
        self.cycle = 1
        self.preIssueBuff = [-1, -1, -1, -1]
        self.postALUBuff = [-1, -1]    #1st number is value, 2nd number is instr index
        self.preALUBuff = [-1, -1]   #1st number is index, second is index
        self.postMemBuf = [-1, -1]   #1st number is value, 2nd number is instr index
        self.preMemBuf = [-1, -1]


    def run(self):
        go = True
        while go:
            self.writeBack.run()
            self.execute.run()
            self.loadstore.run()
            self.issue.run()
            go = self.instrFetch.run()
            self.printState()
            self.cycle += 1
            if go == False:
                self.printState()
                self.cycle += 1

    def isMemoryOp(self, i):
        if self.instructionName[i] == 'LW' or self.instructionName[i] == 'SW':
            return True
        else:
            return False

    def getIndexOfMemAddress(self,wbAddress):
        return((wbAddress - (self.numInstructions*4)+96))



    def printState(self):
        global pip_out
        global fileOb
        pip_out = p_out
        fullInstruc = ['', '', '', '', '', '', '', '', '', '', '']
        entry = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

        entry[0] = simulator.preIssueBuff[0]
        entry[1] = simulator.preIssueBuff[1]
        entry[2] = simulator.preIssueBuff[2]
        entry[3] = simulator.preIssueBuff[3]
        entry[4] = simulator.preALUBuff[0]
        entry[5] = simulator.preALUBuff[1]
        entry[6] = simulator.postALUBuff[1]
        entry[7] = simulator.preMemBuf[0]
        entry[8] = simulator.preMemBuf[1]
        entry[9] = simulator.postMemBuf[1]

        #Fill entries for one cycle
        for i in range(0, 10):

            #determine if instruction is valid
            if entry[i] != -1:
                #R Instruction
                if simulator.instructionName[entry[i]] == 'ADD\t' or simulator.instructionName[entry[i]] == 'AND\t' or simulator.instructionName[entry[i]] == 'MUL\t' or simulator.instructionName[entry[i]] == 'OR\t' or simulator.instructionName[entry[i]] == 'SUB\t':
                    fullInstruc[i] = '\t[' + simulator.instructionName[entry[i]] + 'R' + str(simulator.arg3[entry[i]]) + ', R' + str(simulator.arg1[entry[i]]) + ', R' + str(simulator.arg2[entry[i]]) + ']'
                elif simulator.instructionName[entry[i]] == 'JR\t':
                    fullInstruc[i] = '\t[JR\tR' + str(simulator.arg1[entry[i]]) + ']'
                elif simulator.instructionName[entry[i]] == 'NOP':
                    fullInstruc[i] = '\t[NOP]'
                elif simulator.instructionName[entry[i]] == 'SLL\t' or simulator.instructionName[entry[i]] == 'SRL\t':
                    fullInstruc[i] = '\t[' + simulator.instructionName[entry[i]] + '\tR' + str(simulator.arg1[entry[i]]) + ', R' + str(simulator.arg2[entry[i]]) + ', #' + str(simulator.arg3[entry[i]]) + ']'
                #I Instruction
                elif simulator.instructionName[entry[i]] == 'ADDI\t':
                    fullInstruc[i] = '\t[ADDI\tR' + str(simulator.arg2[entry[i]]) + ', R' + str(simulator.arg1[entry[i]]) + ', #' + str(simulator.arg3[entry[i]]) + ']'
                elif simulator.instructionName[entry[i]] == 'BLEZ\t':
                    fullInstruc[i] = '\t[BLEZ\tR' + str(simulator.arg1[entry[i]]) + ', #' + str(simulator.arg3[entry[i]]) + ']'
                elif simulator.instructionName[entry[i]] == 'BNE\t':
                    fullInstruc[i] = '\t[BNE\tR' + str(simulator.arg2[entry[i]]) + ', R' + str(simulator.arg1[entry[i]]) + ', #' + str(simulator.arg3[entry[i]]) + ']'
                elif simulator.instructionName[entry[i]] == 'LW\t' or simulator.instructionName[entry[i]] == 'SW\t':
                    fullInstruc[i] = '\t[' + simulator.instructionName[entry[i]] + '\tR' + str(simulator.arg2[entry[i]]) + ', ' + str(simulator.arg3[entry[i]]) + '(R' + str(simulator.arg1[entry[i]]) + ')]'
                #J Instruction
                elif simulator.instructionName[entry[i]] == 'J\t':
                    fullInstruc[i] = '\t[J\t#' + str(simulator.arg1[entry[i]]) + ']'
                else:
                    pass

            else:
                #if invalid instruction or break, make fullInstruc empty
                fullInstruc[i] = ''
        # print("opcodeList: " + str(simulator.opcodeList))
        # print("destReg: " + str(simulator.destReg))
        # print("src1Reg: " + str(simulator.src1Reg))
        # print("scr2Reg: " + str(simulator.src2Reg))
        # print("arg1: " + str(simulator.arg1))
        # print("arg2: " + str(simulator.arg2))
        # print("arg3: " + str(simulator.arg3))

        if simulator.opcodeList == 0 and simulator.funcBits == 0x20:  # ADD
            simulator.registerValue[simulator.destReg] = simulator.registerValue[simulator.src1Reg] + simulator.registerValue[simulator.src2Reg]
        elif simulator.opcodeList == 0 and simulator.funcBits == 0x22:  # SUB
            simulator.registerValue[simulator.destReg] = simulator.registerValue[simulator.src1Reg] - simulator.registerValue[simulator.src2Reg]
        elif simulator.opcodeList == 0 and simulator.funcBits == 0x24:  # AND
            simulator.registerValue[simulator.destReg] = simulator.registerValue[simulator.src1Reg] & simulator.registerValue[simulator.src2Reg]
        elif simulator.opcodeList == 0 and simulator.funcBits == 0x25:  # OR
            simulator.registerValue[simulator.destReg] = simulator.registerValue[simulator.src1Reg] | simulator.registerValue[simulator.src2Reg]
        elif simulator.opcodeList == 0 and simulator.funcBits == 0x26:  # XOR
            simulator.registerValue[simulator.destReg] = simulator.registerValue[simulator.src1Reg] ^ simulator.registerValue[simulator.src2Reg]
        elif simulator.opcodeList == 0x1c and simulator.funcBits== 2:  # MUL
            simulator.registerValue[simulator.destReg] = simulator.registerValue[simulator.src1Reg] * registerValue[simulator.src2Reg]
        elif simulator.opcodeList == 0 and simulator.funcBits == 2:  # SRL
            simulator.registerValue[simulator.destReg] = simulator.registerValue[simulator.src1Reg] >> simulator.arg3
        elif simulator.opcodeList == 0 and simulator.funcBits == 0 and simulator.src2Reg != 0:  # SLL
            simulator.registerValue[simulator.destReg] = simulator.registerValue[simulator.src1Reg] << simulator.arg3
        elif simulator.opcodeList == 0 and simulator.funcBits == 0xa:  # MOVZ
            if simulator.registerValue[simulator.src2Reg] == 0:
                simulator.registerValue[simulator.destReg] = simulator.registerValue[simulator.src1Reg]
        elif simulator.opcodeList == 0 and simulator.funcBits == 8:  # JR
           # global jumpAddr
            #jumpAddr = registerValue[rs]
            #global jumpFlag
            #jumpFlag = 1
            pass
        elif simulator.opcodeList == 0 and simulator.funcBits == 0 and simulator.src1Reg < 0:  # NOP
            # no operations
            pass
            #######################I TYPE INSTRUCTIONS####################################################

        elif simulator.opcodeList == 8:  # ADDI
            simulator.registerValue[simulator.destReg] = simulator.registerValue[simulator.src1Reg] + simulator.arg3
        elif simulator.opcodeList == 5:  # BNE
            #global branchFlag
            #global branchAddr
            #offset = offset << 2

            #if simulator.registerValue[] != registerValue[rt]:
             #   branchAddr = offset + 4 + progCounter
             #   branchFlag = 1
            pass
        elif simulator.opcodeList == 6:  # BLEZ
           # breakFlag = 0
            #offset = offset << 2

            #if registerValue[rs] <= 0:
             #   branchAddr = offset + 4 + progCounter
             #   branchFlag = 1
            pass
        elif simulator.opcodeList == 0xb:  # SW
            pass
           # breakFlag = 0
           # loc = 0
            #swAddress = registerValue[rs] + offset

            #k = 0
            #if len(data) != 0:
             #   while k < len(dataMemory):
              #      if swAddress == dataMemory[k]:
               #         loc = k
                #    k = k + 1

                #data[loc] = registerValue[rt]
        elif simulator.opcodeList == 3:  # LW
            pass
            #breakFlag = 0
            #loc = 0
            #lwAddress = registerValue[rs] + offset

            #k = 0
            #if len(data) != 0:
                #while k < len(dataMemory):
                    #if lwAddress == dataMemory[k]:
                     #   loc = k
                    #k = k + 1

                #registerValue[rt] = data[loc]

            ####################################J TYPE INSTRUCTIONS###########################################
        elif simulator.opcodeList == 2:  # J
            #jumpFlag = 1
            #jumpAddr = FindBits0_25(instruction) << 2
            pass

        pip_out.write("--------------------\n")
        pip_out.write("Cycle:" + str(simulator.cycle) + "\n")
        pip_out.write("Pre-Issue Buffer:\n")
        # need to alter str(instructionList)
        pip_out.write("\tEntry 0:\t" + fullInstruc[0] + "\n")
        pip_out.write("\tEntry 1:\t" + fullInstruc[1] + "\n")
        pip_out.write("\tEntry 2:\t" + fullInstruc[2] + "\n")
        pip_out.write("\tEntry 3:\t" + fullInstruc[3] + "\n")
        pip_out.write("Pre_ALU Queue:\n")
        pip_out.write("\tEntry 0:\t" + fullInstruc[4] + "\n")
        pip_out.write("\tEntry 1:\t" + fullInstruc[5] + "\n")
        pip_out.write("Post_ALU Queue:\n")
        pip_out.write("\tEntry 0:\t" + fullInstruc[6] + "\n")
        pip_out.write("Pre_MEM Queue:\n")
        pip_out.write("\tEntry 0:\t" + fullInstruc[7] + "\n")
        pip_out.write("\tEntry 1:\t" + fullInstruc[8] + "\n")
        pip_out.write("Post_MEM Queue:\n")
        pip_out.write("\tEntry 0:\t" + fullInstruc[9] + "\n")

        pip_out.write("Registers:\n")
        pip_out.write('r00:\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (
            simulator.registerValue[0], simulator.registerValue[1], simulator.registerValue[2], simulator.registerValue[3], simulator.registerValue[4],
            simulator.registerValue[5], simulator.registerValue[6], simulator.registerValue[7]))
        pip_out.write('r08:\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (
            simulator.registerValue[8], simulator.registerValue[9], simulator.registerValue[10], simulator.registerValue[11], simulator.registerValue[12],
            simulator.registerValue[13], simulator.registerValue[14], simulator.registerValue[15]))
        pip_out.write('r016:\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (
            simulator.registerValue[16], simulator.registerValue[17], simulator.registerValue[18], simulator.registerValue[19], simulator.registerValue[20],
            simulator.registerValue[21], simulator.registerValue[22], simulator.registerValue[23]))
        pip_out.write('r024:\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n\n' % (
            simulator.registerValue[24], simulator.registerValue[25], simulator.registerValue[26], simulator.registerValue[27], simulator.registerValue[28],
            simulator.registerValue[29], simulator.registerValue[30], simulator.registerValue[31]))
        pip_out.write("Cache:\n")
        pip_out.write("Set 0: LRU = " + str(simulator.cache.lruBit[0]) + "\n")
        pip_out.write('\tEntry 1: [(%s,%s,%s)<%s,%s>]\n' % (str(simulator.cache.cacheSets[0][0][0]),str(simulator.cache.cacheSets[0][0][1]),str(simulator.cache.cacheSets[0][0][2]),str(simulator.cache.cacheSets[0][0][3]),str(simulator.cache.cacheSets[0][0][4])))
        pip_out.write('\tEntry 2: [(%s,%s,%s)<%s,%s>]\n' % (str(simulator.cache.cacheSets[0][1][0]),str(simulator.cache.cacheSets[0][1][1]),str(simulator.cache.cacheSets[0][1][2]),str(simulator.cache.cacheSets[0][1][3]),str(simulator.cache.cacheSets[0][1][4])))
        pip_out.write("Set 1: LRU = " + str(simulator.cache.lruBit[1]) + "\n")
        pip_out.write('\tEntry 1: [(%s,%s,%s)<%s,%s>]\n' % (str(simulator.cache.cacheSets[1][0][0]),str(simulator.cache.cacheSets[1][0][1]),str(simulator.cache.cacheSets[1][0][2]),str(simulator.cache.cacheSets[1][0][3]),str(simulator.cache.cacheSets[1][0][4])))
        pip_out.write('\tEntry 2: [(%s,%s,%s)<%s,%s>]\n' % (str(simulator.cache.cacheSets[1][1][0]),str(simulator.cache.cacheSets[1][1][1]),str(simulator.cache.cacheSets[1][1][2]),str(simulator.cache.cacheSets[1][1][3]),str(simulator.cache.cacheSets[1][1][4])))
        pip_out.write("Set 2: LRU = " + str(simulator.cache.lruBit[2]) + "\n")
        pip_out.write('\tEntry 1: [(%s,%s,%s)<%s,%s>]\n' % (str(simulator.cache.cacheSets[2][0][0]),str(simulator.cache.cacheSets[2][0][1]),str(simulator.cache.cacheSets[2][0][2]),str(simulator.cache.cacheSets[2][0][3]),str(simulator.cache.cacheSets[2][0][4])))
        pip_out.write('\tEntry 2: [(%s,%s,%s)<%s,%s>]\n' % (str(simulator.cache.cacheSets[2][1][0]),str(simulator.cache.cacheSets[2][1][1]),str(simulator.cache.cacheSets[2][1][2]),str(simulator.cache.cacheSets[2][1][3]),str(simulator.cache.cacheSets[2][1][4])))
        pip_out.write("Set 3: LRU = " + str(simulator.cache.lruBit[3]) + "\n")
        pip_out.write('\tEntry 1: [(%s,%s,%s)<%s,%s>]\n' % (str(simulator.cache.cacheSets[3][0][0]),str(simulator.cache.cacheSets[3][0][1]),str(simulator.cache.cacheSets[3][0][2]),str(simulator.cache.cacheSets[3][0][3]),str(simulator.cache.cacheSets[3][0][4])))
        pip_out.write('\tEntry 2: [(%s,%s,%s)<%s,%s>]\n' % (str(simulator.cache.cacheSets[3][1][0]),str(simulator.cache.cacheSets[3][1][1]),str(simulator.cache.cacheSets[3][1][2]),str(simulator.cache.cacheSets[3][1][3]),str(simulator.cache.cacheSets[3][1][4])))
        pip_out.write("Data:\n")


        #if len(mem) != 0:
        i = 0
        d = 0  # data list counter
        lines = (len(self.mem)) / 8
        # if list is less than 8 element, then by integer division, lines = 0
        # so change listLen to 1 so that it prints just the one line of data
        if lines == 0:
            lines = 1
        while i < lines:
            pip_out.write(str(self.dataAddress[i]) + ':\t')

            i = i + 1
            k = 0
            while k < 8:
                if k == (len(self.mem) - 1):
                    k = 8

                pip_out.write(str(self.mem[d]))
                pip_out.write('\t')
                d = d + 1
                k = k + 1

            pip_out.write('\n')
        pip_out.write('\n')


def main():
    global pc
    global progCounter
    global file_object
    global out
    global p_out
    global jumpFlag
    global branchFlag
    global breakFlag
    jumpFlag = 0
    branchFlag = 0
    breakFlag = 0
    out = ""
    p_out = ""

    file_object = ""
    pc = 96
    progCounter = 96
    i = 0
    j = 0
    noBreak = True

    # CODE FROM SLIDES
    for n in range(len(sys.argv)):
        if (sys.argv[n] == '-i' and n < (len(sys.argv) - 1)):
            file_object = sys.argv[n + 1]
            print file_object
        elif (sys.argv[n]) == '-o' and n < (len(sys.argv) - 1):
            out = sys.argv[n + 1]
            p_out = sys.argv[n+1]
            print out

    # open file with machine code
    with open(file_object, 'r') as file_object:
        with open(out + "_dis.txt", 'w')as out:
            # get each 16bit word from file
            while noBreak:
                for line in file_object:

                    instruction = int(line, base=2)  # Convert each line to int value to prepare for bitwise operations
                    instructionList.append(instruction)
                    disassemble(instruction, pc)
                    if instruction == 2147483661:
                        instructionList.append(instruction)
                        noBreak = False
                        out.write(instrSpaced[i] + '\t' + str(addrs[i]) + '\t' + 'BREAK\n')
                        twosCompList.append("")
                    # break
                    elif noBreak == False:

                        #instructionList.append(instruction)
                        offset = FindBits0_15(instruction)
                        c = FindTwosComp(offset)
                        twosCompList.append(c)
                        mem.append(c)
                        dataMemory.append(pc)

                        out.write(line.strip('\n\r') + '\t' + str(addrs[i]) + '\t' + str(twosCompList[i]) + '\n')

                    else:
                        # if opcode == 0 or opcode == 3 or opcode == 8 or opcode == 0xb:
                        twosCompList.append("")
                        out.write(instrSpaced[i] + '\t' + str(addrs[i]) + '\t' + instructionType[i] + arg1Str[i]
                                  + arg2Str[i] + arg3Str[i] + '\n')

                    pc = pc + 4
                    i = i + 1
        out.close()
        with open(p_out + "_pipeline.txt", 'a+') as p_out:
            global simulator
            simulator = sim(instructionList, opcodes, mem, validList, addrs, arg1, arg2, arg3, numInst, dest, src1, src2, funcs, dataMemory, instructionType)
            simulator.run()
    file_object.close()



if __name__ == "__main__":
    main()
