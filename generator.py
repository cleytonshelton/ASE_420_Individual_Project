from dataclasses import dataclass
from typing import List


@dataclass
class Context:
    conveyor_name: str
    num_conveyors: int
    has_makeup_unit: bool


class Section:
    def render(self, ctx: Context) -> str:
        raise NotImplementedError


class PeJamSection(Section):
    def render(self, ctx: Context) -> str:
        lines: List[str] = ["**** PE JAM FAULTS **** \n"]
        for i in range(1, ctx.num_conveyors + 1):
            idx = i - 1
            lines.append(
                f"[XIO(I_{ctx.conveyor_name}_{i:02}_PE_HEAD_END)"
                f"[XIC({ctx.conveyor_name}_{i:02}_VFD:I.Data[0].4),XIC(E3D_READ[0].{idx})]"
                f"[TON(PE_JAM_TMR[{idx}],?,?),XIC(PE_JAM_TMR[{idx}].DN)OTL(F_{ctx.conveyor_name}_{i:02}_PE_JAM)],"
                f"XIC(I_{ctx.conveyor_name}_{i:02}_PE_HEAD_END)XIC(F_{ctx.conveyor_name}_{i:02}_PE_JAM)"
                f"XIC(F_CS_{ctx.conveyor_name}_{i:02}_EPB)XIO(I_CS_{ctx.conveyor_name}_{i:02}_EPB)"
                f"XIC(I_CS_{ctx.conveyor_name}_{i:02}_SPB)OTU(F_{ctx.conveyor_name}_{i:02}_PE_JAM)];"
            )
        return "".join(lines)


class MotorFaultSection(Section):
    def render(self, ctx: Context) -> str:
        lines: List[str] = ["\n**** MOTOR FAULTS **** \n"]
        misc_index = 30
        for i in range(1, ctx.num_conveyors + 1):
            lines.append(
                f"[[XIC({ctx.conveyor_name}_{i:02}_VFD:O.Data[0].7)XIO({ctx.conveyor_name}_{i:02}_VFD:I.Data[0].4),"
                f"XIO({ctx.conveyor_name}_{i:02}_VFD:O.Data[0].7)XIC({ctx.conveyor_name}_{i:02}_VFD:I.Data[0].4)]"
                f"TON({ctx.conveyor_name}_{i:02}_VFD_FAULTED_FAULT_TMR,?,?),"
                f"XIC(I_MCP_DC01_EZONE1_ESCR)"
                f"[XIC({ctx.conveyor_name}_{i:02}_VFD_FAULTED_FAULT_TMR.DN),"
                f"XIO(F_{ctx.conveyor_name}_{i:02}_VFD_COMM_FLT)XIC({ctx.conveyor_name}_{i:02}_VFD:I.Data[0].8)"
                f"ONS(MISC_REGS[{misc_index}].0)]OTL(F_{ctx.conveyor_name}_{i:02}_VFD_FLT)];"
            )
            misc_index += 1

        if ctx.has_makeup_unit:
            for i in range(1, 3):
                lines.append(
                    f"[[XIC({ctx.conveyor_name}_M{i}_VFD:O.Data[0].7)XIO({ctx.conveyor_name}_M{i}_VFD:I.Data[0].4),"
                    f"XIO({ctx.conveyor_name}_M{i}_VFD:O.Data[0].7)XIC({ctx.conveyor_name}_M{i}_VFD:I.Data[0].4)]"
                    f"TON({ctx.conveyor_name}_M{i}_VFD_FAULTED_FAULT_TMR,?,?),"
                    f"XIC(I_MCP_{ctx.conveyor_name}_EZONE3_ESCR)"
                    f"[XIC({ctx.conveyor_name}_M{i}_VFD_FAULTED_FAULT_TMR.DN),"
                    f"XIO(F_{ctx.conveyor_name}_M{i}_VFD_COMM_FLT)XIC({ctx.conveyor_name}_M{i}_VFD:I.Data[0].8)"
                    f"ONS(MISC_REGS[{misc_index}].0)]OTL(F_{ctx.conveyor_name}_M{i}_VFD_FLT)];"
                )
                misc_index += 1
        return "".join(lines)


class CommFaultSection(Section):
    def render(self, ctx: Context) -> str:
        lines: List[str] = ["\n**** COMM FAULTS **** \n"]
        for i in range(1, ctx.num_conveyors + 1):
            lines.append(
                f"XIC({ctx.conveyor_name}_{i:02}_VFD:I.ConnectionFaulted)OTE(F_{ctx.conveyor_name}_{i:02}_VFD_COMM_FLT);"
            )
        if ctx.has_makeup_unit:
            for i in range(1, 3):
                lines.append(
                    f"XIC({ctx.conveyor_name}_M{i}_VFD:I.ConnectionFaulted)OTE(F_{ctx.conveyor_name}_M{i}_VFD_COMM_FLT);"
                )
        return "".join(lines)


class DiscFaultSection(Section):
    def render(self, ctx: Context) -> str:
        lines: List[str] = ["\n**** DISC FAULTS **** \n"]
        for i in range(1, ctx.num_conveyors + 1):
            lines.append(
                f"XIO(I_{ctx.conveyor_name}_{i:02}_MSD)OTE(F_{ctx.conveyor_name}_{i:02}_MSD);"
            )
        if ctx.has_makeup_unit:
            for i in range(1, 3):
                lines.append(
                    f"XIO(I_{ctx.conveyor_name}_M{i}_MSD)OTE(F_{ctx.conveyor_name}_M{i}_MSD);"
                )
        return "".join(lines)


class EStopFaultSection(Section):
    def render(self, ctx: Context) -> str:
        lines: List[str] = ["\n**** ESTOP FAULTS **** \n"]
        for i in range(1, ctx.num_conveyors + 1):
            lines.append(
                f"[XIC(I_CS_{ctx.conveyor_name}_{i:02}_EPB)OTL(F_CS_{ctx.conveyor_name}_{i:02}_EPB),"
                f"XIO(I_CS_{ctx.conveyor_name}_{i:02}_EPB)XIC(I_CS_{ctx.conveyor_name}_{i:02}_SPB)OTU(F_CS_{ctx.conveyor_name}_{i:02}_EPB)];"
            )
        for letter in "ABCDEFG":
            lines.append(
                f"[XIC(I_CS_{ctx.conveyor_name}{letter}_EPB)OTL(F_CS_{ctx.conveyor_name}{letter}_EPB),"
                f"XIO(I_CS_{ctx.conveyor_name}{letter}_EPB)XIC(I_CS_{ctx.conveyor_name}{letter}_KSW)OTU(F_CS_{ctx.conveyor_name}{letter}_EPB)];"
            )
        return "".join(lines)


class Conveyor:
    def __init__(self, name: str, count: int, has_makeup_unit: bool) -> None:
        self.ctx = Context(name, count, has_makeup_unit)
        self.sections: List[Section] = [
            PeJamSection(),
            MotorFaultSection(),
            CommFaultSection(),
            DiscFaultSection(),
            EStopFaultSection(),
        ]

    def generate(self) -> str:
        return "".join(section.render(self.ctx) for section in self.sections)


def generate_plc_code(conveyor_name: str, num_conveyors: int, has_makeup_unit: bool) -> str:
    conveyor = Conveyor(conveyor_name, num_conveyors, has_makeup_unit)
    return conveyor.generate()


