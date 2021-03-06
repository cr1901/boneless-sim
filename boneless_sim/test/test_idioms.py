from boneless_sim.test.common import *

# Test common assembly-language idioms in this file.
class Test32bMath(BonelessTestCase):
    def test_32b_sub(self):
        self.init_regs[R0] = 0x7FFF
        self.init_regs[R1] = 0xFFFF
        self.init_regs[R3] = 0xC000
        self.init_regs[R4] = 0xFFFE

        self.payload = [
            SUB(R5, R0, R3),
            JC("skip_sub1"),
            SUB(R6, R1, R4),
            SUBI(R6, 1),
            J("end"),
            L("skip_sub1"),
            SUB(R6, R1, R4),
            L("end")
        ]

        self.cpu.load_program(self.flatten())
        self.run_cpu(1)
        self.assertEqual(self.cpu.regs()[5], 0xBFFF)
        self.assertEqual(self.cpu.flags, { "Z" : 0, "S" : 1, "C" : 0, "V" : 1})
        self.run_cpu(1)
        self.assertEqual(self.cpu.pc, 18)
        self.run_cpu(1)
        self.assertEqual(self.cpu.flags, { "Z" : 0, "S" : 0, "C" : 1, "V" : 0})
        self.run_cpu(1)
        self.assertEqual(self.cpu.regs()[6], 0)
        self.assertEqual(self.cpu.flags, { "Z" : 1, "S" : 0, "C" : 1, "V" : 0})


class TestLoop(BonelessTestCase):
    def test_loop(self):
        self.init_regs[R0] = 0x10

        self.payload = [
            L("loop"),
            SUBI(R0, 1),
            JC("loop"),
            L("end"),
            NOP()
        ]

        self.cpu.load_program(self.flatten())
        self.run_cpu_until_pc(0x12, fail_count=34)
