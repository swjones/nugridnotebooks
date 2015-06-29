import widget_framework as framework
#from widget_utils import int_text, token_text
from IPython.html import widgets
from IPython.display import display, clear_output
from matplotlib import pyplot
import os
import ppm

def start_PPM(global_namespace, local_dir="./"):
    frame = framework.framework()
    frame.set_default_display_style(padding="0.25em",background_color="white", border_color="LightGrey", border_radius="0.5em")
    frame.set_default_io_style(padding="0.25em", margin="0.25em", border_color="LightGrey", border_radius="0.5em")        
    
    group_style = {"border_style":"none", "border_radius":"0em", "width":"100%"}
    text_box_style = {"width":"10em"}
    button_style = {"font_size":"1.25em", "font_weight":"bold"}
    first_tab_style = {"border_radius":"0em 0.5em 0.5em 0.5em"}

    states_plotting = ["plot_prof_time", "plot_tEkmax", "plot_vprofs", "get"]
    states_loaded = ["data_loaded"] + states_plotting
    states = states_loaded

    frame.add_state(states)
    
    frame.set_state_data("data_sets", [])
    frame.set_state_data("data_set_count", 0)
    frame.set_state_data("dir", os.path.abspath(local_dir))
    frame.set_state_data("yaxis_options", [""], "plot_prof_time")
    frame.set_state_data("yaxis_options", [""], "get")
    frame.set_state_data("cycles", [])
    
    def add_data_set(data, name):
        data_set_count = frame.get_state_data("data_set_count")
        data_sets = frame.get_state_data("data_sets")
        widget_name = "data_set_widget_#"+str(data_set_count)
        
        frame.add_io_object(widget_name)
        frame.set_state_attribute(widget_name, visible=True, description=name)
        frame.set_object(widget_name, widgets.Checkbox())
        
        data_sets.append((data, name, widget_name))
        frame.set_state_children("data_sets", [widget_name])
        frame.set_state_data("data_sets", data_sets)
        data_set_count += 1
        frame.set_state_data("data_set_count", data_set_count)

    def remove_data_set():
        data_sets = frame.get_state_data("data_sets")
        children = ["data_sets_title"]
        tmp_data_sets = []
        for i in xrange(len(data_sets)):
            widget_name = data_sets[i][2]
            if frame.get_attribute(widget_name, "value"):
                frame.remove_object(widget_name)
            else:
                children.append(widget_name)
                tmp_data_sets.append(data_sets[i])
        data_sets = tmp_data_sets
        frame.set_state_children("data_sets", children, append=False)
        frame.set_state_data("data_sets", data_sets)
        
        if data_sets == []:
            frame.set_state()
    
    def update_dir_bar_list():
        dir = frame.get_state_data("dir")
        dirs = [".", ".."] + os.listdir(dir)
        
        frame.set_state_attribute("address_bar", value=dir)
        frame.set_state_attribute("directory_list", options=dirs)

    frame.add_display_object("window")
    frame.add_io_object("Title")
    
    frame.add_display_object("widget_data_set_group")
    frame.add_display_object("widget")
    
    frame.add_display_object("data_sets")
    frame.add_io_object("data_sets_title")
    
    ##data page
    frame.add_display_object("data_page")
    frame.add_display_object("file_system_group")
    frame.add_io_object("address_bar")
    frame.add_io_object("directory_list")
    
    frame.add_display_object("name_load_remove_group")
    frame.add_io_object("data_set_name")
    frame.add_io_object("data_set_load")
    frame.add_io_object("data_set_remove")
    
    ##plotting page
    frame.add_display_object("plotting_page")
    frame.add_io_object("select_plot")
    frame.add_io_object("plot_title")
    frame.add_io_object("warning_msg")
    
    frame.add_display_object("cycle_range_group")
    frame.add_io_object("cycle")
    frame.add_io_object("cycle_range")
    frame.add_io_object("cycle_sparsity")
    
    frame.add_io_object("variable_name")
    
    frame.add_display_object("yaxis_group")
    frame.add_io_object("yaxis")
    frame.add_io_object("logy")
    
    frame.add_io_object("plot")

    frame.set_state_children("window", ["Title", "widget_data_set_group"])
    frame.set_state_children("widget_data_set_group", ["widget", "data_sets"])
    
    frame.set_state_children("data_sets", ["data_sets_title"])
    frame.set_state_children("widget", ["data_page", "plotting_page"], titles=["Data", "Plotting"])
    frame.set_state_children("data_page", ["file_system_group", "name_load_remove_group"])
    frame.set_state_children("file_system_group", ["address_bar", "directory_list"])
    frame.set_state_children("name_load_remove_group", ["data_set_load", "data_set_remove", "data_set_name"])
    
    frame.set_state_children("plotting_page", ["select_plot", "warning_msg", "plot_title", "variable_name", "cycle_range_group", "yaxis_group", "plot"])
    frame.set_state_children("cycle_range_group", ["cycle", "cycle_range", "cycle_sparsity"])
    frame.set_state_children("yaxis_group", ["yaxis", "logy"])
    
    frame.set_state_attribute("window", visible=True, **group_style)
    frame.set_state_attribute("Title", visible=True, value="<center><h1>PPM explorer</h1></center>")
    frame.set_state_attribute("widget_data_set_group", visible=True, **group_style)
    frame.set_state_attribute("data_sets", visible=True, margin="3.15em 0em 0em 0em")
    frame.set_state_attribute("data_sets_title", visible=True, value="<center><h2>Data Sets</h2></center>", **group_style)
    frame.set_state_attribute("widget", visible=True, **group_style)
    
    frame.set_state_attribute("data_page", visible=True, **first_tab_style)
    frame.set_state_attribute("file_system_group", visible=True, **group_style)
    frame.set_state_attribute("address_bar", visible=True)
    frame.set_state_attribute("directory_list", visible=True)
    frame.set_state_attribute("name_load_remove_group", visible=True, **group_style)
    frame.set_state_attribute("data_set_name", visible=True, description="Data set name:", placeholder="Enter name", **text_box_style)
    frame.set_state_attribute("data_set_load", visible=True, description="Load data set", **button_style)
    frame.set_state_attribute("data_set_remove", visible=True, description="Remove data set", **button_style)    

    def address_bar_handler(widget):
        dir = frame.get_attribute("address_bar", "value")
        if os.path.isdir(dir):
            dir = os.path.abspath(dir)
            frame.set_state_data("dir", dir)
            update_dir_bar_list()
            frame.update()
            frame.set_attributes("address_bar", value=dir)
            frame.set_attributes("directory_list", value=".", selected_label=u".")

    def directory_list_handler(name, value):
        dir = frame.get_state_data("dir")
        dir = dir + "/" + frame.get_attribute("directory_list", "value")
        if os.path.isdir(dir):
            dir = os.path.abspath(dir)
            frame.set_state_data("dir", dir)
            update_dir_bar_list()
            frame.update()
            frame.set_attributes("address_bar", value=dir)
            frame.set_attributes("directory_list", value=".", selected_label=u".")

    def data_set_load_handler(widget):
        clear_output()
        pyplot.close("all")
        
        dir = frame.get_attribute("address_bar", "value")
        data_set_count = frame.get_state_data("data_set_count")
        name = frame.get_attribute("data_set_name", "value")
        if name == "":
            name = "Data set - " + "%03d" % (data_set_count + 1, )
            
        data = ppm.yprofile(dir)
        frame.set_state("data_loaded")
        
        old_cycs = frame.get_state_data("cycles")
        cycs = data.cycles
        cycs = list(set(cycs) | set(old_cycs))
        cycs.sort()
        frame.set_state_data("cycles", cycs)
        frame.set_state_data("yaxis_options", data.dcols, "plot_prof_time")
        frame.set_state_data("yaxis_options", data.dcols + data.cattrs, "get")

        frame.set_state_attribute("cycle", min=cycs[0], max=cycs[-1], value=cycs[-1])
        frame.set_state_attribute("cycle_range", min=cycs[0], max=cycs[-1], value=(cycs[0], cycs[-1]))

        add_data_set(data, name)
        frame.update()
        
        
    def data_set_remove_handler(widget):
        remove_data_set()
        frame.update()
        
    frame.set_state_callbacks("address_bar", address_bar_handler, attribute=None, type="on_submit")
    frame.set_state_callbacks("directory_list", directory_list_handler)
    frame.set_state_callbacks("data_set_load", data_set_load_handler, attribute=None, type="on_click")
    frame.set_state_callbacks("data_set_remove", data_set_remove_handler, attribute=None, type="on_click")
    
    frame.set_object("window", widgets.Box())
    frame.set_object("Title", widgets.HTML())

    frame.set_object("widget_data_set_group", widgets.HBox())
    frame.set_object("widget", widgets.Tab())
    frame.set_object("data_sets", widgets.VBox())
    frame.set_object("data_sets_title", widgets.HTML())

    frame.set_object("data_page", widgets.VBox())

    frame.set_object("file_system_group", widgets.VBox())
    frame.set_object("address_bar", widgets.Text())
    frame.set_object("directory_list", widgets.Select())

    frame.set_object("name_load_remove_group", widgets.HBox())
    frame.set_object("data_set_name", widgets.Text())
    frame.set_object("data_set_load", widgets.Button())
    frame.set_object("data_set_remove", widgets.Button())


    frame.set_state_attribute("plotting_page", visible=True)
    frame.set_state_attribute("select_plot", states_loaded, visible=True, options={"":"data_loaded", "Profile time":"plot_prof_time", "Velocity Profile":"plot_vprofs", "tEkmax":"plot_tEkmax", "Get Data":"get"})
    frame.set_state_attribute("warning_msg", visible=True, value="<h3>No data sets loaded!</h3>", **group_style)
    frame.set_state_attribute("warning_msg", "data_loaded", value="<h3>Select plot.</h3>")
    frame.set_state_attribute("warning_msg", states_plotting, visible=False)
    frame.set_state_attribute("plot_title", visible=False, **group_style)
    frame.set_state_attribute("plot_title", "plot_prof_time", visible=True, value="<h3>Prof_time</h3>")
    frame.set_state_attribute("plot_title", "plot_vprofs", visible=True, value="<h3>Plot Velocity Profiles</h3>")
    frame.set_state_attribute("plot_title", "plot_tEkmax", visible=True, value="<h3>tEkmax</h3>")
    frame.set_state_attribute("plot_title", "get", visible=True, value="<h3>Get Data</h3>")
    
    frame.set_state_attribute("variable_name", "get", visible=True, description="Variable name:", placeholder="Enter name.", **text_box_style)
    
    frame.set_state_attribute("cycle_range_group", ["plot_prof_time", "plot_vprofs", "get"], visible=True, **group_style)
    frame.set_state_attribute("cycle", "get", visible=True, description="Cycle:")
    frame.set_state_attribute("cycle_range", ["plot_prof_time", "plot_vprofs"], visible=True, description="Cycle range:")
    frame.set_state_attribute("cycle_sparsity", ["plot_prof_time", "plot_vprofs"], visible=True, description="Cycle sparsity", value=1)
    
    frame.set_state_attribute("yaxis_group", ["plot_prof_time", "plot_vprofs", "get"], visible=True, **group_style)
    frame.set_state_attribute("yaxis", ["plot_prof_time", "get"], visible=True, description="Yaxis:", options=[""])
    frame.set_state_attribute("logy", ["plot_prof_time", "plot_vprofs"],visible=True, description="Log Y axis:")
    
    frame.set_state_attribute("plot", states_loaded, visible=True, description="Generate Plot", **button_style)
    frame.set_state_attribute("plot", "get", description="Get Data")
    
    def variable_name_full_validation(value):
        frame.set_attributes("variable_name", value=token_text(value, strict=True))
        frame.set_state_data("variable_name_timer", None)
        
    def variable_name_handler(name, value):
        value = token_text(value)
        frame.set_attributes("variable_name", value=value)
        
        timer = frame.get_state_data("variable_name_timer")
        if (value != token_text(value, strict=True)):
            if timer != None:
                timer.cancel()
            timer = threading.Timer(1.0, variable_name_full+validation, kwargs={"value":value})
            timer.start()
        else:
            if timer != None:
                timer.cancel()
            timer = None
        frame.set_state_data("variable_name_timer", timer)

    def select_plot_handler(name, value):
        if value in ["plot_prof_time", "get"]:
            frame.set_state_attribute("yaxis", value, options=frame.get_state_data("yaxis_options", value))
        frame.set_state(value)
            
    def plot_handler(widget):
        clear_output()
        pyplot.close("all")
        
        state = frame.get_state()
        data_sets = frame.get_state_data("data_sets")
                
        cycle = frame.get_attribute("cycle", "value")
        cycle_min, cycle_max = frame.get_attribute("cycle_range", "value")
        cycle_sparsity = int(frame.get_attribute("cycle_sparsity", "value"))
        if state in ["plot_prof_time", "plot_vprofs"]:
            cycles = range(cycle_min, cycle_max, cycle_sparsity)
        
        yaxis = frame.get_attribute("yaxis", "value")
        logy = frame.get_attribute("logy", "value")
        
        no_runs = True
        
        if state == "plot_prof_time":
            for data, name, widget_name in data_sets:
                if frame.get_attribute(widget_name, "value"):
                    cycs = data.cycles
                    cycs = list(set(cycs) & set(cycles))
                    cycs.sort()
                    no_runs = False
                    data.prof_time(cycs, yaxis_thing=yaxis, logy=logy)
        elif state == "plot_vprofs":
            for data, name, widget_name in data_sets:
                if frame.get_attribute(widget_name, "value"):
                    cycs = data.cycles
                    cycs = list(set(cycs) & set(cycles))
                    cycs.sort()
                    no_runs = False
                    data.vprofs(cycs, log_logic=logy)
        elif state == "plot_tEkmax":
            i = 0
            for data, name, widget_name in data_sets:
                if frame.get_attribute(widget_name, "value"):
                    no_runs = False
                    data.tEkmax(ifig=1, label=name, id=i)
                    i += 1
        elif state == "get":
            for data, name, widget_name in data_sets:
                if frame.get_attribute(widget_name, "value"):
                    no_runs = False
                    global_namespace["test"]  = data.get(attri=yaxis, fname=cycle)
        
        if no_runs:
            print "No data sets selected."
    
    frame.set_state_callbacks("select_plot", select_plot_handler)
    frame.set_state_callbacks("plot", plot_handler, attribute=None, type="on_click")
    
    frame.set_object("plotting_page", widgets.VBox())
    frame.set_object("select_plot", widgets.Dropdown())
    frame.set_object("warning_msg", widgets.HTML())
    frame.set_object("plot_title", widgets.HTML())
    frame.set_object("cycle_range_group", widgets.HBox())
    frame.set_object("cycle", widgets.IntSlider())
    frame.set_object("cycle_range", widgets.IntRangeSlider())
    frame.set_object("cycle_sparsity", widgets.IntText())
    
    frame.set_object("yaxis_group", widgets.HBox())
    frame.set_object("yaxis", widgets.Select())
    frame.set_object("logy", widgets.Checkbox())
    frame.set_object("plot", widgets.Button())

    update_dir_bar_list()
    frame.display_object("window")
