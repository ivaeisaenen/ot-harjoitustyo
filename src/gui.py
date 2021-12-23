"""Graphical user interfase for fatigue calculation tool"""
import json
import tkinter as tk
# from tkinter.filedialog import askopenfilename, asksaveasfilename
import os

cwd = os.getcwd()
# Messy globals should be replaced buy a class definition but no time for this project
global INPUT_FILENAME, INPUT_FILENAME_SELECTED, \
       MATERIAL_FILENAME, MATERIAL_FILENAME_SELECTED, INPUT_DICT, MATERIAL_DICT, MATERIAL_NAME
global material_file_read, selected_material

INPUT_FILENAME = "./data/input_dict_gui_generated.json"
INPUT_FILENAME_SELECTED = False
MATERIAL_FILENAME_SELECTED = False
material_file_read = False

INPUT_DICT = {}
INPUT_DICT["criterion"] = None
INPUT_DICT["mean_stress_correction"] = None
INPUT_DICT["input_files"] = ["./data/stress_history1.txt", "./data/stress_history2.txt"]
INPUT_DICT["material_name"] = None
INPUT_DICT["materials"] = "./data/materials.json"

MATERIAL_DICT = {}

window = tk.Tk()
label1 = tk.Label(text="Fatigue Calculation Tool")
label1.grid(row=0, column=1)

def quit_gui():
    """Exit the program"""
    window.destroy()

exit_but = tk.Button(text="Exit", command=quit_gui)
exit_but.grid(row=0, column=5)

class ToolTip():
    """Copied from https://stackoverflow.com/a/64260119"""

    def __init__(self, widget, text):
        self.widget = widget
        self.text = text

        def enter(event):
            """enter area"""
            self.show_tool_tip()

        def leave(event):
            """leave area"""
            self.hide_tool_tip()

        widget.bind('<Enter>', enter)
        widget.bind('<Leave>', leave)

    def show_tool_tip(self):
        """Show the tool tip"""

        self.tooltipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1) # window without border and no normal means of closing
        tw.wm_geometry("+{}+{}".format(self.widget.winfo_rootx(), self.widget.winfo_rooty()))
        tk.Label(tw, text = self.text, background = "#ffffe0",
                    relief = 'solid', borderwidth = 1).pack()

    def hide_tool_tip(self):
        """Hde the tool tip"""
        toolt_tip_window = self.tooltipwindow
        toolt_tip_window.destroy()
        self.tooltipwindow = None

#############################################################################
# ANALYSIS TYPE
#############################################################################
label2 = tk.Label(text="Select analysis type:")
label2.grid(row=1, column=0)
rv = tk.StringVar(window)
rad1 = tk.Radiobutton(window, text="Safety Factor",
                    variable = rv, value = "safety_factor", state='normal')
rad2 = tk.Radiobutton(window, text="Finite Life",
                    variable = rv, value = "finite_life", state='disabled')
rad3 = tk.Radiobutton(window, text="Crack Growth",
                    variable = rv, value = "crack_growth", state='disabled')
rad1.grid(row = 2, column = 0)
rad2.grid(row = 2, column = 1)
rad3.grid(row = 2, column = 2)
rad1_tt = ToolTip(widget=rad1, text="Factor of Safety calculation")
rad2_tt = ToolTip(widget=rad2, text="Please by premium licence")
rad3_tt = ToolTip(widget=rad3, text="Please by premium licence")
rad1.select()
INPUT_DICT["analysis_type"] = rv.get()

#############################################################################
# CRITERION ie equivalent stress ie uniaxial stress criterion
#############################################################################
label2 = tk.Label(text="Select equivalent stress type:")
label2.grid(row=3, column=0)
equivalent_stress = tk.StringVar(window)
equivalent1 = tk.Radiobutton(window, text="Von Mises",
                            variable = equivalent_stress, value = "mises", state='normal')
equivalent2 = tk.Radiobutton(window, text="Tresca",
                            variable = equivalent_stress, value = "tresca", state='normal')
equivalent3 = tk.Radiobutton(window, text="MMK",
                            variable = equivalent_stress, value = "mmk", state='disabled')
equivalent1.grid(row = 4, column = 0)
equivalent2.grid(row = 4, column = 1)
equivalent3.grid(row = 4, column = 2)
equivalent1_tt = ToolTip(widget=equivalent1, text="Signed Von Mises")
equivalent2_tt = ToolTip(widget=equivalent2, text="Please by premium licence")
equivalent3_tt = ToolTip(widget=equivalent3, text="Please by premium licence")
equivalent1.select()
INPUT_DICT["criterion"] = equivalent_stress.get()


#############################################################################
# Mean stress correction for uniaxial equivalent stress
#############################################################################
label2 = tk.Label(text="Select mean stress correction type:")
label2.grid(row=5, column=0)
msc = tk.StringVar()
msc1 = tk.Radiobutton(window, text="Goodman",  variable = msc, value = "goodman", state='normal')
msc2 = tk.Radiobutton(window, text="Gerbel", variable = msc, value = "gerbel", state='normal')
msc3 = tk.Radiobutton(window, text="Soderberg",  variable = msc, value = "soderberg", state='normal')
msc4 = tk.Radiobutton(window, text="Steel", variable = msc, value = "steel", state='disabled')
msc5 = tk.Radiobutton(window, text="Cast-Iron",  variable = msc, value = "cast_iron", state='disabled')
msc6 = tk.Radiobutton(window, text="FKM",  variable = msc, value = "fkm", state='disabled')
msc1.grid(row = 6, column = 0)
msc2.grid(row = 6, column = 1)
msc3.grid(row = 6, column = 2)
msc4.grid(row = 6, column = 3)
msc5.grid(row = 6, column = 4)
msc6.grid(row = 6, column = 5)
msc1_tt = ToolTip(widget=msc1, text="Signed Von Mises")
msc2_tt = ToolTip(widget=msc2, text="Please by premium licence")
msc3_tt = ToolTip(widget=msc3, text="Please by premium licence")
msc4_tt = ToolTip(widget=msc4, text="Please by premium licence")
msc5_tt = ToolTip(widget=msc5, text="Please by premium licence")
msc6_tt = ToolTip(widget=msc6, text="Please by premium licence")
msc1.select()
INPUT_DICT["mean_stress_correction"] = msc.get()

#############################################################################
# Material selections
#############################################################################

def select_material_file_location():
    """Select material file location"""
    global MATERIAL_FILENAME, MATERIAL_FILENAME_SELECTED
    global INPUT_DICT
    MATERIAL_FILENAME = tk.filedialog.askopenfilename(initialdir='/',
                        title='Opel material data file',
                        filetypes=(('Json files', '*.json'), ('All Files', '*.*')))
    if MATERIAL_FILENAME != '':
        MATERIAL_FILENAME_SELECTED = True
        INPUT_DICT["materials"] = MATERIAL_FILENAME
        label_matfile = tk.Label(text=INPUT_DICT["materials"])
        label_matfile.grid(row=7, column=2)
        window.update()

def load_material_file():
    """Load material file"""
    global material_file_read, MATERIAL_DICT, MATERIAL_NAME
    global selected_material
    material_file_read = False
    try:
        with open(INPUT_DICT["materials"], "r", encoding='utf-8') as matfile_handle:
            material_dict = json.load(matfile_handle)
        MATERIAL_DICT = material_dict
        print("Material file read")
        material_file_read = True
    except Exception as expection_:
        print(f"material file not read because: {expection_}")
        material_file_read = False

    if material_file_read:
        print("Material file radiobutton selection")
        label_mat_read = tk.Label(text="Materials: ")
        label_mat_read.grid(row=8, column=0)
        mat_rads = []
        selected_material = tk.StringVar()
        for col, material_name in enumerate(material_dict.keys()):
            mat_rad = tk.Radiobutton(text=f"{material_name}",
                                    variable=selected_material, value=f"{material_name}")
            mat_rad.grid(row=8, column=col+1)
            mat_rads.append(mat_rad)
        window.update()
        INPUT_DICT["material_name"] = selected_material.get()
        MATERIAL_NAME = selected_material.get()


if material_file_read:
    label_mat_read = tk.Label(text="Materials: ")
    label_mat_read.grid(row=8, column=0)
    mat_rads = []
    selected_material = tk.StringVar()
    for col, material_name in enumerate(MATERIAL_DICT.keys()):
        print(f"Making of radiobuttons \"{material_name}\"")
        mat_rad = tk.Radiobutton(text=f"{material_name}",
                                variable=selected_material, value=f"{material_name}")
        mat_rad.grid(row=8, column=col+1)
        mat_rads.append(mat_rad)
    window.update()
    INPUT_DICT["material_name"] = selected_material.get()
    MATERIAL_NAME = selected_material.get()


# Select filename and directory to write input
but_loc1 = tk.Button(window, text="Select material file", command=select_material_file_location)
but_loc1.grid(row = 7, column=0)
# but_loc1_tt = ToolTip(widget=but_loc1, text="Select material file to load")

but_loc2 = tk.Button(window, text="Load material file", command=load_material_file)
but_loc2.grid(row = 7, column=1)
# but_loc2_tt = ToolTip(widget=but_loc1, text="Load material file")

label_matfile = tk.Label(text=INPUT_DICT["materials"])
label_matfile.grid(row=7, column=2)

#############################################################################
# Create INPUT_DICT
#############################################################################



#############################################################################
# Select stress history input files
#############################################################################
def select_stress_history_files():
    """Select stress history files
    """
    global INPUT_DICT
    INPUT_FILENAME = tk.filedialog.asksaveasfilename(initialdir='/',
                    title='Save File', filetypes=(('Json files', '*.json'), ('All Files', '*.*')))
    if INPUT_FILENAME != '':
        if INPUT_DICT["input_files"] == ["./data/stress_history1.txt",
                                         "./data/stress_history2.txt"]:
            INPUT_DICT["input_files"] = []
        INPUT_DICT["input_files"].append(INPUT_FILENAME)

        for i, input_file_str_ in enumerate(INPUT_DICT["input_files"]):
            label_stress_files_ = tk.Label(text=input_file_str_)
            label_stress_files_.grid(row=9, column=1+i)

for col_, input_file_str in enumerate(INPUT_DICT["input_files"]):
    label_stress_files = tk.Label(text=input_file_str)
    label_stress_files.grid(row=9, column=1+col_)

but_stress_files1 = tk.Button(window, text="Select stress history ...",
                              command=select_stress_history_files)
but_stress_files1.grid(row = 9, column=0)

#############################################################################
# Select, write and execute input file
#############################################################################
def select_file_location():
    global INPUT_FILENAME, INPUT_FILENAME_SELECTED
    INPUT_FILENAME = tk.filedialog.asksaveasfilename(initialdir='/',
                    title='Save File', filetypes=(('Json files', '*.json'), ('All Files', '*.*')))
    INPUT_FILENAME_SELECTED = True

    label_inpfile = tk.Label(text=INPUT_FILENAME)
    label_inpfile.grid(row=10, column=1)

# Select filename and directory to write input
but_loc1 = tk.Button(window, text="Write input ...", command=select_file_location)
but_loc1.grid(row = 10, column=0)
# but_loc1_tt = ToolTip(widget=but_loc1, text="Write input files only")

label_matfile = tk.Label(text=INPUT_FILENAME)
label_matfile.grid(row=10, column=1)

#############################################################################
# Write input
#############################################################################

def write_input():
    """Write input file (json)"""
    global INPUT_DICT, MATERIAL_NAME
    global selected_material
    INPUT_DICT["analysis_type"] = rv.get()
    INPUT_DICT["criterion"] = equivalent_stress.get()
    INPUT_DICT["mean_stress_correction"] = msc.get()
    INPUT_DICT["material_name"] = selected_material.get()
    print(f"selected_material = {selected_material.get()}")
    window.update()
    all_okey = True
    problems = {}
    for key, value in INPUT_DICT.items():
        if value is None:
            all_okey = False
            problems[key] = value

    if all_okey is False:
        error_str = "\n".join([f"{key} = {value}" for key,value in problems.items()])
        tk.messagebox.showerror("Inputs are not valid", error_str)
    else:
        with open(INPUT_FILENAME, "w", encoding='utf-8') as inpfile_handle:
            json.dump(INPUT_DICT, inpfile_handle, indent=4)
    return all_okey

but1 = tk.Button(window, text="Write input", command=write_input)
but1.grid(row = 11, column=3)
but1_tt = ToolTip(widget=but1, text="Write input files only")

#############################################################################
# Calculate
#############################################################################

def calculate():
    """Write input and start the calculation"""
    all_okey = write_input()
    if all_okey:
        print("running calculation")

but2 = tk.Button(window, text="Calculate", command=calculate, state="disabled")
but2.grid(row = 11, column=5)
but2_tt = ToolTip(widget=but2, text="Please by premium licence")

window.mainloop()
