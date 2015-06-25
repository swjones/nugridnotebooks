import widget_framework as framework
#from widget_utils import int_text, token_text
from IPython.html import widgets
from IPython.display import display, clear_output
from matplotlib import pyplot
import ppm

def start_PPM(global_namespace):
    frame = framework.framework()
    frame.set_default_display_style(padding="0.25em",background_color="white", border_color="LightGrey", border_radius="0.5em")
    frame.set_default_io_style(padding="0.25em", margin="0.25em", border_color="LightGrey", border_radius="0.5em")

    group_style = {"border_style":"none", "border_radius":"0em", "width":"100%"}
    text_box_style = {"width":"10em"}
    button_style = {"font_size":"1.25em", "font_weight":"bold"}
    first_tab_style = {"border_radius":"0em 0.5em 0.5em 0.5em"}

    states_plotting = []
    states = ["data_loaded"] + states_plotting

    frame.add_state(states)
    
    frame.set_state_data("data_sets", [])
    frame.set_state_data("data_set_count", 0)
    
    def add_data_set(data, name):
        data_set_count = frame.get_state_data("data_set_count")
        data_sets = frame.get_state_data("data_sets")
        widget_name = "data_set_widget_#"+str(data_set_count)
        
        frame.add_io_object(widget_name)
        frame.set_state_attribute(widget_name, visible=True, description=name)
        frame.set_object(widget_name, widgets.Checkbox())
        
        runs_data.append((data, name, widget_name))
        frame.set_state_children("data_sets", [widget_name])
        frame.set_state_data("data_sets", data_sets)
        data_set_count += 1
        frame.set_state_data("data_set_count", data_set_count)

    def remove_data_set():
        data_sets = frame.get_state_data("data_sets")
        children = ["data_sets_title"]
        tmp_data_sets = []
        for i in xrange(len(data_sets)):
            widget_name = data_sets[i][3]
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

    frame.add_display_object("window")
    frame.add_io_object("Title")
    
    frame.add_display_object("widget_data_set_group")
    frame.add_display_object("widget")
    
    frame.add_display_object("data_sets")
    frame.add_io_object("data_sets_title")
    
    ##data page
    frame.add_display_object("data_page")
    frame.add_display_object("file_system_group")
    frame.add_io_object("adress_bar")
    frame.add_io_object("directory_list")
    
    frame.add_display_object("name_load_remove_group")
    frame.add_io_object("data_set_name")
    frame.add_io_object("data_set_load")
    frame.add_io_object("data_set_remove")
    
    ##plotting page
    frame.add_display_object("plotting_page")
    frame.add_io_object("select_plot")
    frame.add_io_object("warning_msg")
    
    frame.add_io_object("plot")

    frame.set_state_children("window", ["Title", "widget_data_set_group"])
    frame.set_state_children("widget_data_set_group", ["widget", "data_sets"])
    
    frame.set_state_children("data_sets", ["data_sets_title"])
    frame.set_state_children("widget", ["data_page", "plotting_page"], titles=["Data", "Plotting"])
    frame.set_state_children("data_page", ["file_system_group", "name_load_remove_group"])
    frame.set_state_children("file_system_group", ["adress_bar", "directory_list"])
    frame.set_state_children("name_load_remove_group", ["data_set_name", "data_set_load", "data_set_remove"])
    
    frame.set_state_children("plotting_page", ["select_plot", "warning_msg", "plot"])

    ###CALLBACKS###
    def model_select_handler(name, value):
        frame.set_attributes("model_select", value=int_text(value))

    frame.set_state_callbacks("model_select", model_select_handler)

    frame.set_object("window", widgets.Box())
    frame.set_object("Title", widgets.HTML())
    frame.set_object("widget", widgets.Tab())

    frame.display_object("window")
