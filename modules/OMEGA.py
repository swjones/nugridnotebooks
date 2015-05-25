import matplotlib
import os

#temp fix
if os.path.isdir("/home/nugrid/omega_sygma"):
    os.environ["SYGMADIR"] = "/home/nugrid/omega_sygma"

import omega

import widget_framework as framework
from IPython.html import widgets
from IPython.display import display, clear_output
from matplotlib import pyplot, colors

tablist = ["sculptor", "alpha"]
yield_table_names = ["NuGrid raw", "NuGrid 25Mo Nomoto 2006", "NuGrid 30Mo Nomoto 2006", "NuGrid 40Mo Nomoto 2006"]
yield_tables = {"NuGrid raw":'yield_tables/isotope_yield_table.txt', 
                "NuGrid 25Mo Nomoto 2006":'yield_tables/isotope_yield_table_N06_25Mo_full_IMF.txt', 
                "NuGrid 30Mo Nomoto 2006":'yield_tables/isotope_yield_table_N06_30Mo_full_IMF.txt', 
                "NuGrid 40Mo Nomoto 2006":'yield_tables/isotope_yield_table_N06_40Mo_full_IMF.txt'}
elements_sculpt = ['Mg', 'Si', 'Ca', 'Ti']
elements_alpha = ['O', 'Mg', 'Si', 'S', 'Ca']

line_styles=['-', '--', '-.', ':']
line_colors=['b', 'g', 'r', 'c', 'm', 'y', 'k']

color_convert = colors.ColorConverter()

frame = framework.framework()
frame.set_default_display_style(padding="0.25em",background_color="white", border_color="LightGrey", border_radius="0.5em")
frame.set_default_io_style(padding="0.25em", margin="0.25em", border_color="LightGrey", border_radius="0.5em")

group_style = {"border_style":"", "border_radius":"0em"}
text_box_style = {"width":"10em"}
button_style = {"font_size":"1.25em", "font_weight":"bold"}

states = ["sculpt", "alpha"]

frame.add_state(states)

frame.set_state_data("runs",[],"sculpt")
frame.set_state_data("runs",[],"alpha")

run_count = 0
widget_count = 0

def float_text(string):
    for i in xrange(len(string)):
        if float_substring(string[:len(string)-i]):
            return string[:len(string)-i]
    return ""

def float_substring(string):
    string=string.strip()
    if string == "":
        return True
    special_chars = ["+", "-", ".", "e", "E"]
    try:
        if string[-1] in special_chars:
            string = string + "0"
        float(string)
        return True
    except ValueError:
        return False

def add_run(state, data, name):
    global widget_count
    widget_count += 1
    state_data = frame.get_state_data("runs",state)
    
    widget_name = "runs_widget_#"+str(widget_count)
    line_style = line_styles[widget_count % len(line_styles)]
    line_color = line_colors[widget_count % len(line_colors)]
    
    frame.add_io_object(widget_name)    
    frame.set_state_attribute(widget_name, state, visible=True, description=name)
    frame.set_object(widget_name, widgets.Checkbox())
    
    state_data.append((data, name, line_style, line_color, widget_name))
    
    frame.set_state_children("runs", [widget_name], state=state)
    frame.set_state_data("runs", state_data, state)
    
def remove_runs(state):
    state_data = frame.get_state_data("runs",state)
    children = ["runs_title"]
    tmp_data=[]
    for i in xrange(len(state_data)):
        widget_name = state_data[i][4]
        if not frame.get_attribute(widget_name, "value"):
            children.append(widget_name)
            tmp_data.append(state_data[i])
    state_data=tmp_data
    frame.set_state_children("runs", children, state=state, append=False)
    
    frame.set_state_data("runs", state_data, state)

frame.add_display_object("window")
frame.add_io_object("title")
frame.add_display_object("widget")

frame.add_display_object("simulation")
frame.add_display_object("sculptor")
frame.add_display_object("alpha")

frame.add_display_object("baryon_table_name_group")
frame.add_io_object("f_baryon")
frame.add_io_object("select_table")
frame.add_io_object("run_name")

frame.add_io_object("loading_mass")
frame.add_io_object("sn1a_pmil")

frame.add_display_object("run_add_rm_group")
frame.add_io_object("run_sim")
frame.add_io_object("rm_sim")

frame.add_display_object("plotting_runs_group")
frame.add_display_object("plotting")
frame.add_io_object("plotting_title")
frame.add_display_object("runs")
frame.add_io_object("runs_title")

frame.add_io_object("select_elem")
frame.add_io_object("plot")
frame.add_io_object("warning_msg")

frame.set_state_children("window", ["title", "widget"])
frame.set_state_children("widget", ["simulation", "plotting_runs_group"])
frame.set_state_children("simulation", tablist, titles=["Sculptor Galaxy", "Alpha Elements"])
frame.set_state_children("sculptor", ["baryon_table_name_group", "loading_mass", "sn1a_pmil", "run_add_rm_group"])
frame.set_state_children("alpha", ["baryon_table_name_group", "run_add_rm_group"])
frame.set_state_children("baryon_table_name_group", ["f_baryon", "select_table", "run_name"])
frame.set_state_children("run_add_rm_group", ["run_sim", "rm_sim"])
frame.set_state_children("plotting_runs_group", ["plotting", "runs"])
frame.set_state_children("plotting", ["plotting_title", "select_elem", "plot", "warning_msg"])
frame.set_state_children("runs", ["runs_title"], state=states)

frame.set_state_attribute('window', visible=True, **group_style)
frame.set_state_attribute('title', visible=True, value="<h1>OMEGA</h1>")
frame.set_state_attribute('widget', visible=True, **group_style)

frame.set_state_attribute('simulation', visible=True, **group_style)
frame.set_state_attribute('sculptor', visible=True)
frame.set_state_attribute('alpha', visible=True)

frame.set_state_attribute("baryon_table_name_group", visible=True, **group_style)
frame.set_state_attribute("f_baryon", "sculpt", visible=True, description="Baryon fraction: ", value=0.005, min=0.004, max=1.0, step=0.001)
frame.set_state_attribute("select_table", "alpha", visible=True, description="Yield table: ", options=yield_table_names)
frame.set_state_attribute("run_name", visible=True, description="Run name: ", placeholder="Enter name", **text_box_style)

frame.set_state_attribute("loading_mass", "sculpt", visible=True, description="Mass loading factor: ", value="40.0", **text_box_style)
frame.set_state_attribute("sn1a_pmil", "sculpt", visible=True, description="SNe Ia per stellar mass formed: ", value="2.0e-3", **text_box_style)

frame.set_state_attribute("run_add_rm_group", visible=True, **group_style)
frame.set_state_attribute("run_sim", visible=True, description="Run simulation", **button_style)
frame.set_state_attribute("rm_sim", visible=True, description="Remove selected run", **button_style)

frame.set_state_attribute("plotting_runs_group", visible=True, **group_style)
frame.set_state_attribute("plotting", visible=True)
frame.set_state_attribute("plotting_title", visible=True, value="<h2>Plotting options</h2>", **group_style)
frame.set_state_attribute("runs", visible=True)
frame.set_state_attribute("runs_title", visible=True, value="<h2>Runs</h2>", **group_style)

frame.set_state_attribute("select_elem", visible=True, description="Select Element: ", **text_box_style)
frame.set_state_attribute("select_elem", "sculpt", options=elements_sculpt)
frame.set_state_attribute("select_elem", "alpha", options=elements_alpha)
frame.set_state_attribute("plot", visible=True, description="Generate Plot", **button_style)
frame.set_state_attribute("warning_msg", visible=False, value="<h3>Error no runs selected!</h3>", **group_style)

def loading_mass_handler(name, value):
    if (value.strip())[0] == "-":
        value = "0.0"
    frame.set_attributes("loading_mass", value=float_text(value))
    
def sn1a_pmil_handler(name, value):
    frame.set_attributes("sn1a_pmil", value=float_text(value))

def simulation_run(widget):
    global run_count
    run_count += 1
    state = frame.get_state()
    data = None
    name = frame.get_attribute("run_name", "value")
    if name == "":
        name="Run: "+"%03d" % (run_count,)
    f_baryon = frame.get_attribute("f_baryon", "value")
    loading_mass = float(frame.get_attribute("loading_mass", "value"))
    sn1a_pmil = float(frame.get_attribute("sn1a_pmil", "value"))
    
    if state=="sculpt":
        mgal = f_baryon * 1.51e9
        data = omega.omega(galaxy='sculptor', in_out_control=True, mgal=mgal, mass_loading=loading_mass, 
                           nb_1a_per_m=sn1a_pmil, table='yield_tables/isotope_yield_table_N06_30Mo_full_IMF.txt')
    if state=="alpha":
        select_table = yield_tables[frame.get_attribute("select_table", "value")]
        data = omega.omega(galaxy='milky_way', table=select_table)
    
    add_run(state, data, name)
    frame.update()
    frame.set_attributes("run_name", value="")
    
def remove_simulation(widget):
    state = frame.get_state()
    
    remove_runs(state)
    frame.update()

def sel_tab(name, value):
    clear_output()
    pyplot.close("all")
    open_tab = tablist[value]
    if open_tab == "sculptor":
        frame.set_state("sculpt")
    elif open_tab == "alpha":
        frame.set_state("alpha")
    frame.set_attributes("run_name", value="")
    
def generate_plot(widget):
    clear_output()
    pyplot.close("all")
    state = frame.get_state()
    data = frame.get_state_data("runs", state)
    
    plotted_data = False
    comp_data = True
    
    if len(data) != 0:
        element = frame.get_attribute("select_elem", "value")
        for i in xrange(len(data)):
            instance, name, line_style, line_color, widget_name = data[i]
            yaxis = '['+element+'/Fe]'
            label = name+", "+yaxis
            selected = frame.get_attribute(widget_name, "value")
            if selected:
                plotted_data=True
                instance.plot_spectro(xaxis="[Fe/H]", yaxis=yaxis, show_data=comp_data, color=color_convert.to_rgba("w", 0.8),
                                      shape="-", marker=" ", linewidth=4, fsize=[10, 4.5], show_legend=False)
                if comp_data:
                    comp_data=False

        for i in xrange(len(data)):
            instance, name, line_style, line_color, widget_name = data[i]
            yaxis = '['+element+'/Fe]'
            label = name+", "+yaxis
            selected = frame.get_attribute(widget_name, "value")
            if selected:
                plotted_data=True
                instance.plot_spectro(xaxis="[Fe/H]", yaxis=yaxis, label=label, show_data=comp_data, color=line_color,
                                      shape=line_style, marker=" ", linewidth=2, fsize=[10, 4.5])
                if comp_data:
                    comp_data=False
        
        if plotted_data:
            frame.set_attributes("warning_msg", visible=False)
            if state=="sculpt":
                pyplot.ylim(-1.0,1.4)
                pyplot.xlim(-4.0, -0.5)
            elif state=="alpha":
                pyplot.ylim(-0.5,1.4)
        
            matplotlib.rcParams.update({'font.size': 14})
            pyplot.subplots_adjust(right=0.6)
            pyplot.subplots_adjust(bottom=0.15)
            pyplot.legend(loc='center left', bbox_to_anchor=(1.01, 0.5), prop={'size':12})
            pyplot.show()
        else:
            frame.set_attributes("warning_msg", visible=True, value="<h3>Error no runs selected!</h3>")
            
    else:
        frame.set_attributes("warning_msg", visible=True, value="<h3>Error no run data!</h3>")
    
frame.set_state_callbacks("loading_mass", loading_mass_handler)
frame.set_state_callbacks("sn1a_pmil", sn1a_pmil_handler)
frame.set_state_callbacks("run_sim", simulation_run, attribute=None, type="on_click")
frame.set_state_callbacks("rm_sim", remove_simulation, attribute=None, type="on_click")
frame.set_state_callbacks("simulation", sel_tab, "selected_index")
frame.set_state_callbacks("plot", generate_plot, attribute=None, type="on_click")

frame.set_object("window", widgets.Box())
frame.set_object("title", widgets.HTML())
frame.set_object("widget", widgets.VBox())
frame.set_object("simulation", widgets.Tab())
frame.set_object("sculptor", widgets.Box())
frame.set_object("alpha", widgets.Box())

frame.set_object("baryon_table_name_group", widgets.HBox())
frame.set_object("f_baryon", widgets.FloatSlider())
frame.set_object("select_table", widgets.Dropdown())
frame.set_object("run_name", widgets.Text())

frame.set_object("loading_mass", widgets.Text())
frame.set_object("sn1a_pmil", widgets.Text())

frame.set_object("run_add_rm_group", widgets.HBox())
frame.set_object("run_sim", widgets.Button())
frame.set_object("rm_sim", widgets.Button())

frame.set_object("plotting_runs_group", widgets.HBox())
frame.set_object("plotting", widgets.VBox())
frame.set_object("plotting_title", widgets.HTML())
frame.set_object("runs", widgets.VBox())
frame.set_object("runs_title", widgets.HTML())

frame.set_object("select_elem", widgets.Dropdown())
frame.set_object("plot", widgets.Button())
frame.set_object("warning_msg", widgets.HTML())

def start_OMEGA():
    frame.display_object("window")
    tab_index = frame.get_attribute("simulation", "selected_index")
    sel_tab("selected_index", tab_index)
