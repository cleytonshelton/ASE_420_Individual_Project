from dataclasses import dataclass
from typing import List
from datetime import datetime

# ----- Small helper dataclass for outputs from sections -----
@dataclass
class RoutineOutput:
    name: str
    logic: str            # Ladder ASCII / routine body (already formatted with RC:, N:, etc.)
    tags: List[str]       # Tag declarations (strings like "F_MyConv_01_PE_JAM : BOOL;")

# ----- Context -----
@dataclass
class Context:
    conveyor_name: str
    num_conveyors: int
    has_makeup_unit: bool

# ----- Base Section class -----
class Section:
    def render(self, ctx: Context) -> RoutineOutput:
        raise NotImplementedError

# ----- PE Jam Section -----
class PeJamSection(Section):
    def render(self, ctx: Context) -> RoutineOutput:
        name = "PE_Jam_Faults"
        logic_lines: List[str] = []
        tags: List[str] = []

        # We will need a timer array (PE_JAM_TMR) sized to number of conveyors
        tags.append(f"PE_JAM_TMR : TIMER[{ctx.num_conveyors}];")
        # Add per-conveyor fault flags
        for i in range(1, ctx.num_conveyors + 1):
            idx = i - 1
            tags.append(f"F_{ctx.conveyor_name}_{i:02}_PE_JAM : BOOL;")
            tags.append(f"I_{ctx.conveyor_name}_{i:02}_PE_HEAD_END : BOOL;")
            # Build ladder-like ASCII line (keeps similarity with your initial code)
            logic_lines.append(
                f"RC: \"$N\" \"{ctx.conveyor_name}-{i:02} PE JAM FAULT $N\" \"$N\" \"\";\n"
                f"N: [XIO(I_{ctx.conveyor_name}_{i:02}_PE_HEAD_END) "
                f"[XIC({ctx.conveyor_name}_{i:02}_VFD:I.Data[0].4), XIC(E3D_READ[0].{idx})] "
                f"[TON(PE_JAM_TMR[{idx}], 2000, 0), XIC(PE_JAM_TMR[{idx}].DN) OTL(F_{ctx.conveyor_name}_{i:02}_PE_JAM)],"
                f" XIC(I_{ctx.conveyor_name}_{i:02}_PE_HEAD_END) XIC(F_{ctx.conveyor_name}_{i:02}_PE_JAM) "
                f"XIC(F_CS_{ctx.conveyor_name}_{i:02}_EPB) XIO(I_CS_{ctx.conveyor_name}_{i:02}_EPB) "
                f"XIC(I_CS_{ctx.conveyor_name}_{i:02}_SPB) OTU(F_{ctx.conveyor_name}_{i:02}_PE_JAM)];\n"
            )

        return RoutineOutput(name, "".join(logic_lines), tags)

# ----- Motor Fault Section -----
class MotorFaultSection(Section):
    def render(self, ctx: Context) -> RoutineOutput:
        name = "Motor_Faults"
        lines: List[str] = []
        tags: List[str] = []

        tags.append(f"MISC_REGS : DINT[128];")
        misc_index = 30

        for i in range(1, ctx.num_conveyors + 1):
            tags.append(f"F_{ctx.conveyor_name}_{i:02}_VFD_FLT : BOOL;")
            tags.append(f"F_{ctx.conveyor_name}_{i:02}_VFD_COMM_FLT : BOOL;")
            tags.append(f"{ctx.conveyor_name}_{i:02}_VFD_FAULTED_FAULT_TMR : TIMER;")

            # Comment
            lines.append(f"        RC: \"$N\" \"{ctx.conveyor_name}-{i:02} MOTOR FAULT $N\" \"$N\" \"\";\n")
            # Rung 1: detect VFD output on + input off -> start TON (example condition)
            lines.append(
                f"        N: XIC({ctx.conveyor_name}_{i:02}_VFD:O.Data[0].7) XIO({ctx.conveyor_name}_{i:02}_VFD:I.Data[0].4) "
                f"TON({ctx.conveyor_name}_{i:02}_VFD_FAULTED_FAULT_TMR, 2000, 0);\n"
            )
            # Rung 2: when timer DN and comm/state conditions -> latch VFD_FLT
            lines.append(
                f"        N: XIC(I_MCP_DC01_EZONE1_ESCR) XIC({ctx.conveyor_name}_{i:02}_VFD_FAULTED_FAULT_TMR.DN) "
                f"XIO(F_{ctx.conveyor_name}_{i:02}_VFD_COMM_FLT) XIC({ctx.conveyor_name}_{i:02}_VFD:I.Data[0].8) "
                f"ONS(MISC_REGS[{misc_index}].0) OTL(F_{ctx.conveyor_name}_{i:02}_VFD_FLT);\n"
            )
            misc_index += 1

        # Makeup units (if present)
        if ctx.has_makeup_unit:
            for i in range(1, 3):
                tags.append(f"F_{ctx.conveyor_name}_M{i}_VFD_FLT : BOOL;")
                tags.append(f"F_{ctx.conveyor_name}_M{i}_VFD_COMM_FLT : BOOL;")
                tags.append(f"{ctx.conveyor_name}_M{i}_VFD_FAULTED_FAULT_TMR : TIMER;")

                lines.append(f"        RC: \"$N\" \"{ctx.conveyor_name}-{i} MOTOR FAULT $N\" \"$N\" \"\";\n")
                lines.append(
                    f"        N: XIC({ctx.conveyor_name}_M{i}_VFD:O.Data[0].7) XIO({ctx.conveyor_name}_M{i}_VFD:I.Data[0].4) "
                    f"TON({ctx.conveyor_name}_M{i}_VFD_FAULTED_FAULT_TMR, 2000, 0);\n"
                )
                lines.append(
                    f"        N: XIC(I_MCP_{ctx.conveyor_name}_EZONE3_ESCR) XIC({ctx.conveyor_name}_M{i}_VFD_FAULTED_FAULT_TMR.DN) "
                    f"XIO(F_{ctx.conveyor_name}_M{i}_VFD_COMM_FLT) XIC({ctx.conveyor_name}_M{i}_VFD:I.Data[0].8) "
                    f"ONS(MISC_REGS[{misc_index}].0) OTL(F_{ctx.conveyor_name}_M{i}_VFD_FLT);\n"
                )
                misc_index += 1

        return RoutineOutput(name, "".join(lines), tags)

# ----- Comm Fault Section -----
# class CommFaultSection(Section):
#     def render(self, ctx: Context) -> RoutineOutput:
#         name = "Comm_Faults"
#         logic_lines: List[str] = []
#         tags: List[str] = []

#         for i in range(1, ctx.num_conveyors + 1):
#             tags.append(f"F_{ctx.conveyor_name}_{i:02}_VFD_COMM_FLT : BOOL;")
#             tags.append(f"")
#             logic_lines.append(
#                 f"RC: \"$N\" \"COMM FAULT CONV {i:02}$N\" \"$N\" \"\";\n"
#                 f"N: XIC({ctx.conveyor_name}_{i:02}_VFD:I.ConnectionFaulted) OTE(F_{ctx.conveyor_name}_{i:02}_VFD_COMM_FLT);\n"
#             )

#         if ctx.has_makeup_unit:
#             for i in range(1, 3):
#                 tags.append(f"F_{ctx.conveyor_name}_M{i}_VFD_COMM_FLT : BOOL;")
#                 logic_lines.append(
#                     f"RC: \"$N\" \"COMM FAULT MU {i}$N\" \"$N\" \"\";\n"
#                     f"N: XIC({ctx.conveyor_name}_M{i}_VFD:I.ConnectionFaulted) OTE(F_{ctx.conveyor_name}_M{i}_VFD_COMM_FLT);\n"
#                 )

#         return RoutineOutput(name, "".join(logic_lines), tags)

# ----- Disc Fault Section -----
class DiscFaultSection(Section):
    def render(self, ctx: Context) -> RoutineOutput:
        name = "Disc_Faults"
        logic_lines: List[str] = []
        tags: List[str] = []

        for i in range(1, ctx.num_conveyors + 1):
            tags.append(f"F_{ctx.conveyor_name}_{i:02}_MSD : BOOL;")
            tags.append(f"I_{ctx.conveyor_name}_{i:02}_MSD : BOOL;")
            logic_lines.append(
                f"RC: \"$N\" \"DISC FAULT CONV {i:02}$N\" \"$N\" \"\";\n"
                f"N: XIO(I_{ctx.conveyor_name}_{i:02}_MSD) OTE(F_{ctx.conveyor_name}_{i:02}_MSD);\n"
            )

        if ctx.has_makeup_unit:
            for i in range(1, 3):
                tags.append(f"F_{ctx.conveyor_name}_M{i}_MSD : BOOL;")
                tags.append(f"I_{ctx.conveyor_name}_M{i}_MSD : BOOL;")
                logic_lines.append(
                    f"RC: \"$N\" \"DISC FAULT MU {i}$N\" \"$N\" \"\";\n"
                    f"N: XIO(I_{ctx.conveyor_name}_M{i}_MSD) OTE(F_{ctx.conveyor_name}_M{i}_MSD);\n"
                )

        return RoutineOutput(name, "".join(logic_lines), tags)

# ----- E-Stop Fault Section -----
class EStopFaultSection(Section):
    def render(self, ctx: Context) -> RoutineOutput:
        name = "EStop_Faults"
        logic_lines: List[str] = []
        tags: List[str] = []
        tags.append(f"I_MCP_{ctx.conveyor_name}_EPB : BOOL;")
        tags.append(f"F_MCP_{ctx.conveyor_name}_EPB : BOOL;")
        tags.append(f"I_MCP_{ctx.conveyor_name}_SPB : BOOL;")

        # Per-conveyor EPB handling
        for i in range(1, ctx.num_conveyors + 1):
            tags.append(f"F_CS_{ctx.conveyor_name}_{i:02}_EPB : BOOL;")
            tags.append(f"I_CS_{ctx.conveyor_name}_{i:02}_EPB : BOOL;")
            tags.append(f"I_CS_{ctx.conveyor_name}_{i:02}_SPB : BOOL;")
            logic_lines.append(
                f"RC: \"$N\" \"ESTOP CS {ctx.conveyor_name} {i:02} FAULT $N\" \"$N\" \"\";\n"
                f"N: [XIC(I_CS_{ctx.conveyor_name}_{i:02}_EPB) OTL(F_CS_{ctx.conveyor_name}_{i:02}_EPB), "
                f"XIO(I_CS_{ctx.conveyor_name}_{i:02}_EPB) XIC(I_CS_{ctx.conveyor_name}_{i:02}_SPB) OTU(F_CS_{ctx.conveyor_name}_{i:02}_EPB)];\n"
            )

        # Fixed set of letters A..G as in your previous sample
        for letter in "ABCDEFG":
            tags.append(f"F_CS_{ctx.conveyor_name}{letter}_EPB : BOOL;")
            tags.append(f"I_CS_{ctx.conveyor_name}{letter}_EPB : BOOL;")
            tags.append(f"I_CS_{ctx.conveyor_name}{letter}_SPB : BOOL;")

            logic_lines.append(
                f"RC: \"$N\" \"ESTOP {ctx.conveyor_name}{letter} FAULT $N\" \"$N\" \"\";\n"
                f"N: [XIC(I_CS_{ctx.conveyor_name}{letter}_EPB) OTL(F_CS_{ctx.conveyor_name}{letter}_EPB), "
                f"XIO(I_CS_{ctx.conveyor_name}{letter}_EPB) XIC(I_CS_{ctx.conveyor_name}{letter}_KSW) OTU(F_CS_{ctx.conveyor_name}{letter}_EPB)];\n"
            )

        return RoutineOutput(name, "".join(logic_lines), tags)

# ----- Conveyor aggregator that builds routines and tags -----
class Conveyor:
    def __init__(self, name: str, count: int, has_makeup_unit: bool) -> None:
        self.ctx = Context(name, count, has_makeup_unit)
        self.sections: List[Section] = [
            PeJamSection(),
            MotorFaultSection(),
            #CommFaultSection(),
            DiscFaultSection(),
            EStopFaultSection(),
        ]

    def generate_routines_and_tags(self):
        all_tags: List[str] = []
        all_routines: List[RoutineOutput] = []

        for sec in self.sections:
            out = sec.render(self.ctx)
            # Avoid duplicate tags (simple dedupe while preserving order)
            for t in out.tags:
                if t not in all_tags:
                    all_tags.append(t)
            all_routines.append(out)

        return all_tags, all_routines
    
    @staticmethod
    def generate_program_block(tags: List[str], routines: List[RoutineOutput]) -> str:
        # Global TAG block (before the PROGRAM)
        global_tag_lines = ["\tTAG"]
        for t in tags:
            global_tag_lines.append(f"\t\t{t}")
        global_tag_lines.append("\tEND_TAG")
        global_tags_block = "\n".join(global_tag_lines)

        # Build routines
        routines_text = []
        for r in routines:
            routines_text.append(f"\tROUTINE {r.name}\n{indent_body(r.logic, 8)}\tEND_ROUTINE\n")

        # MainRoutine calling all routines
        jr_calls = [f"\t\tN: JSR({r.name},0);" for r in routines]
        main_routine = (
            "\tROUTINE MainRoutine\n"
            "\t\tRC: \"$N\" \"MAIN ROUTINE - CALL GENERATED ROUTINES$N\" \"$N\" \"\";\n"
            "\t\tN: NOP();\n"
            + "\n".join(jr_calls) + "\n"
            "\tEND_ROUTINE\n"
        )
        routines_text.append(main_routine)

        # Empty TAG block inside PROGRAM (Studio 5000 requires it)
        program_block = f"""
    \tPROGRAM MainProgram (MAIN := "MainRoutine",
    \t                     MODE := 0,
    \t                     DisableFlag := 0,
    \t                     UseAsFolder := 0)
    \t\tTAG
    \t\tEND_TAG

    {''.join(routines_text)}
    \tEND_PROGRAM
    """.strip()

        return global_tags_block + "\n\n" + program_block

    # ----- High-level generator function -----
    def generate_plc_code_full(conveyor_name: str, num_conveyors: int, has_makeup_unit: bool, controller_name: str) -> str:
        conv = Conveyor(conveyor_name, num_conveyors, has_makeup_unit)
        tags, routines = conv.generate_routines_and_tags()
        
        # Static header with modules
        static_header = f"""(*********************************************

    Import-Export
    Version   := RSLogix 5000 v32.01
    Owner     := admin, 
    Exported  := {datetime.now().strftime("%a %b %d %H:%M:%S %Y")}

    Note:  File encoded in UTF-8.  Only edit file in a program 
            which supports UTF-8 (like Notepad, not Wordpad).

    **********************************************)
    IE_VER := 2.23;

    CONTROLLER {controller_name} (ProcessorType := "1756-L81E",
                        Major := 32,
                        RedundancyEnabled := 0,
                        KeepTestEditsOnSwitchOver := 0,
                        SecurityCode := 0,
                        ChangesToDetect := 16#ffff_ffff_ffff_ffff,
                        SFCExecutionControl := "CurrentActive",
                        SFCRestartPosition := "MostRecent",
                        SFCLastScan := "DontScan",
                        SerialNumber := 16#0000_0000,
                        MatchProjectToController := No,
                        CanUseRPIFromProducer := No,
                        InhibitAutomaticFirmwareUpdate := 0,
                        PassThroughConfiguration := EnabledWithAppend,
                        DownloadProjectDocumentationAndExtendedProperties := Yes,
                        ReportMinorOverflow := 0)
        MODULE Local (Parent := "Local",
                    ParentModPortId := 1,
                    CatalogNumber := "1756-L81E",
                    Vendor := 1,
                    ProductType := 14,
                    ProductCode := 164,
                    Major := 32,
                    Minor := 11,
                    PortLabel := "RxBACKPLANE",
                    ChassisSize := 10,
                    Slot := 0,
                    Mode := 2#0000_0000_0000_0001,
                    CompatibleModule := 0,
                    KeyMask := 2#0000_0000_0000_0000)
        END_MODULE

        MODULE R01S01_EN2T (Parent := "Local",
                            ParentModPortId := 2,
                            CatalogNumber := "1756-EN2T",
                            Vendor := 1,
                            ProductType := 12,
                            ProductCode := 166,
                            Major := 12,
                            Minor := 1,
                            PortLabel := "ENet",
                            ChassisSize := 17,
                            Slot := 0,
                            NodeAddress := "192.168.1.12",
                            CommMethod := 805306369,
                            Mode := 2#0000_0000_0000_0000,
                            CompatibleModule := 1,
                            KeyMask := 2#0000_0000_0001_1111)
            ExtendedProp := [[[___<public><Vendor>Rockwell Automation/Allen-Bradley</Vendor><CatNum>1756-EN2T</CatNum><ConfigID>4456551</ConfigID></public>___]]]
            CONNECTION Output (Rate := 10000,
                            EventID := 0,
                            Unicast := Yes)
                InputData  := [0,[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]];
                OutputData  := [0,[[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0]]];
            END_CONNECTION
        END_MODULE
        """

        # Generate PROGRAM block with global tags + routines + MainRoutine
        program_block = Conveyor.generate_program_block(tags, routines)

        # Static footer (TASK + CONFIG + END_CONTROLLER)
        static_footer = """
        TASK MainTask (Type := CONTINUOUS,
                    Rate := 10,
                    Priority := 10,
                    Watchdog := 500,
                    DisableUpdateOutputs := No,
                    InhibitTask := No)
            MainProgram;
        END_TASK

        CONFIG CST(SystemTimeMasterID := 0) END_CONFIG
        CONFIG EthernetPort1(Label := "1", PortEnabled := 1) END_CONFIG
        CONFIG TimeSynchronize(Priority1 := 128, Priority2 := 128, PTPEnable := 0) END_CONFIG
        CONFIG WallClockTime(LocalTimeAdjustment := 0, TimeZone := 0) END_CONFIG
        END_CONTROLLER
        """

        # Combine everything
        return static_header + "\n" + program_block + "\n" + static_footer

# ----- small helper used in building routine blocks -----
def indent_body(body: str, spaces: int) -> str:
    indent = " " * spaces
    # ensure trailing newline for proper formatting
    if not body.endswith("\n"):
        body = body + "\n"
    return "".join(indent + line if line.strip() != "" else line for line in body.splitlines(True))

# ----- Example usage (uncomment for quick test) -----
if __name__ == "__main__":
    sample = generate_plc_code("LineA", 4, True, "Cley_Test")
    # Save to file to import in Studio 5000
    with open("Cley_Test_generated.L5K", "w", encoding="utf-8") as f:
        f.write(sample)
    print("Generated Cley_Test_generated.L5K")
