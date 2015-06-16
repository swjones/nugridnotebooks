import threading
import widget_framework as framework
from widget_utils import int_text, token_text
from IPython.html import widgets
from IPython.display import display, clear_output
from matplotlib import pyplot
import nugridse as mp
import mesa as ms

def start_explorer(global_namespace):
    frame = framework.framework()
    frame.set_default_display_style(padding="0.25em",background_color="white", border_color="LightGrey", border_radius="0.5em")
    frame.set_default_io_style(padding="0.25em", margin="0.25em", border_color="LightGrey", border_radius="0.5em")

    group_style = {"border_style":"none", "border_radius":"0em", "width":"100%"}
    text_box_style = {"width":"10em"}
    button_style = {"font_size":"1.25em", "font_weight":"bold"}
    first_tab_style = {"border_radius":"0em 0.5em 0.5em 0.5em"}

    states_movie = ["movie", "movie_iso_abund", "movie_abu_chart"]
    states_nugrid = ["nugrid", "nugrid_w_data", "nugrid_get_data", "iso_abund", "abu_chart", "nugrid_plot"]+states_movie
    states_mesa = ["mesa", "mesa_w_data", "get_data", "hrd", "plot", "kip_cont", "kippenhahn", "tcrhoc"]
    states_plotting = states_nugrid[3:]+states_mesa[3:]

    frame.set_state_data("model_data", (None, None, None))
    frame.set_state_data("variable_name_timer", None)

    frame.add_state(states_nugrid)
    frame.add_state(states_mesa)

    frame.add_display_object("window")
    frame.add_io_object("Title")
    frame.add_display_object("widget")

    ###Data page###
    frame.add_display_object("page_data")
    frame.add_io_object("mass")
    frame.add_io_object("Z")
    frame.add_io_object("select_nugrid_mesa")

    frame.add_display_object("contain_module_load")
    frame.add_io_object("select_module")
    frame.add_display_object("contain_model_select")
    frame.add_io_object("model_select")
    frame.add_io_object("load_data")

    frame.set_state_children("window", ["Title", "widget"])
    frame.set_state_children("widget", ["page_data"], titles=["Data"])
    frame.set_state_children("page_data", ["mass", "Z", "select_nugrid_mesa",
                                           "contain_module_load"])
    frame.set_state_children("contain_module_load", ["select_module", "contain_model_select", "load_data"])
    frame.set_state_children("contain_model_select", ["model_select"])

    ###Plotting page###
    frame.add_display_object("page_plotting")

    frame.add_io_object("select_plot")

    frame.add_io_object("warning_msg")

    frame.add_io_object("plot_name")
    frame.add_io_object("cycle")
    frame.add_io_object("cycle_range")
    frame.add_io_object("movie_type")

    frame.add_display_object("xax")
    frame.add_io_object("xaxis")
    frame.add_io_object("logx")
    frame.add_display_object("yax")
    frame.add_io_object("yaxis")
    frame.add_io_object("logy")

    frame.add_display_object("mass_settings")
    frame.add_io_object("set_amass")
    frame.add_io_object("amass_range")
    frame.add_io_object("set_mass")
    frame.add_io_object("mass_range")
    frame.add_io_object("lbound")

    frame.add_display_object("kipp_settings")
    frame.add_io_object("plot_star_mass")
    frame.add_io_object("plot_c12border")
    frame.add_io_object("plot_engminus")
    frame.add_io_object("plot_engplus")

    frame.add_io_object("ixaxis")
    frame.add_display_object("lim_settings")
    frame.add_io_object("set_lims")
    frame.add_io_object("ylim")
    frame.add_io_object("xlim")
    frame.add_io_object("yres")
    frame.add_io_object("xres")

    frame.add_io_object("stable")

    frame.add_display_object("abu_settings")
    frame.add_io_object("ilabel")
    frame.add_io_object("imlabel")
    frame.add_io_object("imagic")

    frame.add_io_object("variable_name")

    frame.add_io_object("generate_plot")

    frame.set_state_children("widget", ["page_plotting"], titles=["Plotting"])
    frame.set_state_children("page_plotting", ["select_plot", "warning_msg", "plot_name", "movie_type", "variable_name", "cycle", "cycle_range",
                                               "xax", "yax", "stable", "mass_settings", "kipp_settings", 
                                               "lim_settings", "abu_settings", "stable", "generate_plot"])
    frame.set_state_children("xax", ["xaxis", "logx"])
    frame.set_state_children("yax", ["yaxis", "logy"])
    frame.set_state_children("mass_settings", ["set_amass", "amass_range", "set_mass", "mass_range",
                                               "lbound"])
    frame.set_state_children("lim_settings", ["ixaxis", "set_lims", "xlim", "ylim", "xres", "yres"])
    frame.set_state_children("abu_settings", ["ilabel", "imlabel", "imagic"])
    frame.set_state_children("kipp_settings", ["plot_star_mass", "plot_c12border", "plot_engminus", "plot_engplus"])


    ###DEFAULT###

    frame.set_state_data("class_instance", None)

    frame.set_state_attribute('window', visible=True, **group_style)
    frame.set_state_attribute('Title', visible=True, value = "<center><h1>NuGrid Set explorer</h1></center><p><center>This explorer allows you to investigate NuGrid stellar evolution and yields data sets.</center></p>")
    frame.set_state_attribute('widget', visible=True, **group_style)

    frame.set_state_attribute("page_data", visible=True, **first_tab_style)
    frame.set_state_attribute('mass', visible=True, description="Mass: ", options=["1.0", "1.65", "2.0", "3.0", "4.0", "5.0", "6.0", "7.0", "12.0", "15.0", "20.0", "25.0", "32.0", "60.0"], selected_label="2.0")
    frame.set_state_attribute('Z', visible=True, description="Z: ", options=["1E-4", "1E-3", "6E-3", "1E-2", "2E-2"])
    frame.set_state_attribute("select_nugrid_mesa", visible=True, description="Select NuGrid or Mesa: ", options=["", "NuGrid", "Mesa"])
    frame.set_state_attribute("contain_module_load", visible=True, **group_style)
    frame.set_state_attribute("select_module", visible=True, description="Select data type: ", disabled=True)

    frame.set_state_attribute("contain_model_select", border_style="none", padding="0px", margin="0px", width="18em")
    frame.set_state_attribute("model_select", visible=True, description="Select model: ", placeholder="1", **text_box_style)

    frame.set_state_attribute("load_data", visible=True, description="Load Data", disabled=True, **button_style)

    ###NUGRID###
    frame.set_state_attribute("select_module", states_nugrid, options=["", "H5 out"], disabled=False)
    frame.set_state_attribute("load_data", states_nugrid, disabled=False)

    ###MESA###
    frame.set_state_attribute("select_module", states_mesa, options=["", "History", "Profile"], disabled=False)
    frame.set_state_attribute("load_data", states_mesa, disabled=False)

    ###CALLBACKS###
    def model_select_handler(name, value):
        frame.set_attributes("model_select", value=int_text(value))

    def mass_Z_handler(name, value):
        if frame.get_attribute("contain_model_select", "visible"):
            mass = float(frame.get_attribute("mass", "value"))
            Z = float(frame.get_attribute("Z", "value"))
            mmass, mZ, mmodel = frame.get_state_data("model_data")
            if (mmass != mass) or (mZ != Z) or (mmodel == None):
                clear_output()
                pre_data = ms.mesa_profile(mass=mass, Z=Z)
                frame.set_state_data("model_data", (mass, Z, pre_data.model))

    def sel_nugrid_mesa(name, value):
        if value=="NuGrid":
            frame.set_state("nugrid")
        elif value=="Mesa":
            frame.set_state("mesa")
        elif value=="":
            frame.set_state("default")

    def load(widget):
        clear_output()
        data = None
        mass = float(frame.get_attribute("mass", "value"))
        Z = float(frame.get_attribute("Z", "value"))
        if frame.get_attribute("model_select", "value") != "":
            model = int(frame.get_attribute("model_select", "value"))
        else:
            model = 1
        module = frame.get_attribute("select_module", "value")
        if module == "H5 out":
            data = mp.se(mass=mass, Z=Z)
            frame.set_state("nugrid_w_data")
            properties = ["mass", "radius", "rho", "temperature"]
            frame.set_attributes("xaxis", options=properties+data.se.isotopes)
            frame.set_attributes("yaxis", options=properties+data.se.isotopes)
        elif module == "History":
            data = ms.history_data(mass=mass, Z=Z)
            frame.set_state("mesa_w_data")
            frame.set_attributes("xaxis", options=sorted(data.cols.keys()))
            frame.set_attributes("yaxis", options=sorted(data.cols.keys()))
        elif module == "Profile":
            data = ms.mesa_profile(mass=mass, Z=Z, num=model)
            frame.set_state("mesa_w_data")
            frame.set_attributes("xaxis", options=sorted(data.cols.keys()))
            frame.set_attributes("yaxis", options=sorted(data.cols.keys()))
        else:
            nugrid_or_mesa = frame.get_attribute("select_nugrid_mesa", 'value')
            if nugrid_or_mesa == "NuGrid":
                frame.set_state("nugrid")
            elif nugrid_or_mesa == "Mesa":
                frame.set_state("mesa")
        
        frame.set_state_data("class_instance", data)
        frame.set_attributes("select_plot", selected_label="")
    
        
    def change_module(widget, value):
        if value == "History":
            frame.set_state_attribute("select_plot", states_mesa[1:], options={"":"mesa_w_data", "HR-Diagram":"hrd", "Plot":"plot", "Kippenhahn":"kippenhahn", "Kippenhahan contour":"kip_cont", "TCRhoC plot":"tcrhoc", "Get data":"get_data"})
            frame.set_state_attribute("contain_model_select", states_mesa, visible=False)
            frame.set_attributes("contain_model_select", visible=False)
        elif value == "Profile":
            frame.set_attributes("load_data", disabled=True)
            frame.set_state_attribute("select_plot", states_mesa[1:], options={"":"mesa_w_data", "Plot":"plot", "Get data":"get_data"})

            mass = float(frame.get_attribute("mass", "value"))
            Z = float(frame.get_attribute("Z", "value"))
            mmass, mZ, mmodel = frame.get_state_data("model_data")
            if (mmass != mass) or (mZ != Z) or (mmodel == None):
                clear_output()
                pre_data = ms.mesa_profile(mass=mass, Z=Z)
                mmodel = pre_data.model
                frame.set_state_data("model_data", (mass, Z, mmodel))

            frame.set_state_attribute("contain_model_select", states_mesa, visible=True)
            frame.set_attributes("contain_model_select", visible=True)
            frame.set_attributes("model_select", value=str(mmodel[-1]))
            frame.set_attributes("load_data", disabled=False)
        else:
            frame.set_state_attribute("contain_model_select", states_mesa, visible=False)
            frame.set_attributes("contain_model_select", visible=False)

    frame.set_state_callbacks("model_select", model_select_handler)
    frame.set_state_callbacks("mass", mass_Z_handler)
    frame.set_state_callbacks("Z", mass_Z_handler)
    frame.set_state_callbacks("select_nugrid_mesa", sel_nugrid_mesa)
    frame.set_state_callbacks("select_module", change_module)
    frame.set_state_callbacks("load_data", load, attribute=None, type="on_click")

    frame.set_object("window", widgets.Box())
    frame.set_object("Title", widgets.HTML())
    frame.set_object("widget", widgets.Tab())

    frame.set_object("page_data", widgets.VBox())
    frame.set_object("mass", widgets.Dropdown())
    frame.set_object("Z", widgets.ToggleButtons())

    frame.set_object("select_nugrid_mesa", widgets.Dropdown())
    frame.set_object("contain_module_load", widgets.HBox())
    frame.set_object("select_module", widgets.Dropdown())
    frame.set_object("contain_model_select", widgets.HBox())
    frame.set_object("model_select", widgets.Text())
    frame.set_object("load_data", widgets.Button())


    ###Plotting page###
    frame.set_state_attribute('page_plotting', visible=True)

    frame.set_state_attribute("select_plot", visible=True, description="Select plot type: ", disabled=True)
    frame.set_state_attribute("select_plot", states_nugrid[1:], options={"":"nugrid_w_data", "Isotope abundance":"iso_abund", "Abundance chart":"abu_chart", "Movie":"movie", "Plot":"nugrid_plot", "Get data":"nugrid_get_data"}, disabled=False)
    frame.set_state_attribute("select_plot", states_mesa[1:], options={"":"mesa_w_data", "HR-Diagram":"hrd", "Plot":"plot", "Kippenhahn":"kippenhahn", "Kippenhahan contour":"kip_cont", "TCRhoC":"tcrhoc", "Get data":"nugrid_get_data"}, disabled=False)

    frame.set_state_attribute('warning_msg', visible=True, value="<h3>Error: No data loaded!</h3>", **group_style)
    frame.set_state_attribute("warning_msg", ["nugrid_w_data", "mesa_w_data"], value="<h2>Select plot.</h2>")
    frame.set_state_attribute("warning_msg", states_plotting + ["get_data", "nugrid_get_data"], visible=False)

    frame.set_state_attribute("plot_name", **group_style)
    frame.set_state_attribute('plot_name', "iso_abund", visible=True, value="<h2>Isotope abundance</h2>")
    frame.set_state_attribute('plot_name', "abu_chart", visible=True, value="<h2>Abundance chart</h2>")
    frame.set_state_attribute('plot_name', states_movie, visible=True, value="<h2>Movie</h2>")
    frame.set_state_attribute('plot_name', "hrd", visible=True, value="<h2>HR-Diagram</h2>")
    frame.set_state_attribute('plot_name', ["plot", "nugrid_plot"], visible=True, value="<h2>Plot</h2>")
    frame.set_state_attribute('plot_name', "kippenhahn", visible=True, value="<h2>Kippenhahn</h2>")
    frame.set_state_attribute('plot_name', "kip_cont", visible=True, value="<h2>Kippenhahn contour</h2>")
    frame.set_state_attribute('plot_name', "tcrhoc", visible=True, value="<h2>Central temperature vs central density</h2>")
    frame.set_state_attribute('plot_name', ["get_data", "nugrid_get_data"], visible=True, value="<h2>Get data</h2>")

    frame.set_state_attribute("variable_name", ["get_data", "nugrid_get_data"], visible=True, description="Variable name: ", placeholder="Enter name.", **text_box_style)

    frame.set_state_attribute('movie_type', states_movie, visible=True, description="Movie Type: ", options={"":"movie", "Isotope abundance":"movie_iso_abund", "Abundance chart":"movie_abu_chart"})
    frame.set_state_attribute('cycle', ["iso_abund", "abu_chart", "nugrid_plot", "nugrid_get_data"], visible=True, description="cycle: ")
    frame.set_state_attribute('cycle_range', states_movie[1:], visible=True)

    frame.set_state_attribute('xax', ["plot", "nugrid_plot", "get_data", "nugrid_get_data"], visible=True, **group_style)
    frame.set_state_attribute('xaxis', visible=True, description="select X-axis: ")
    frame.set_state_attribute('xaxis', ["get_data", "nugrid_get_data"], description="select data: ")
    frame.set_state_attribute('logx', visible=True, description="log X-axis: ")
    frame.set_state_attribute('logx', ["get_data", "nugrid_get_data"], visible=False)
    frame.set_state_attribute('yax', ["plot", "nugrid_plot"], visible=True, **group_style)
    frame.set_state_attribute('yaxis', visible=True, description="select Y-axis: ")
    frame.set_state_attribute('logy', visible=True, description="log Y-axis: ")

    frame.set_state_attribute("mass_settings", ["iso_abund", "abu_chart"]+states_movie[1:], visible=True, **group_style)
    frame.set_state_attribute("set_amass", ["iso_abund", "movie_iso_abund"], visible=True, description="Set atomic mass: ")
    frame.set_state_attribute("amass_range", ["iso_abund", "movie_iso_abund"], description="Atomi mass range: ", min=0, max=211, value=(0, 211))
    frame.set_state_attribute("set_mass", ["iso_abund", "abu_chart"]+states_movie[1:], visible=True, description="Set mass: ")
    frame.set_state_attribute("mass_range", ["iso_abund", "abu_chart"]+states_movie[1:], description="Mass range: ")
    frame.set_state_attribute("lbound", "abu_chart", visible=True, description="lbound", min=-12, max=0, step=0.05, value=(-12, 0))

    frame.set_state_links("amass_link", [("set_amass", "value"), ("amass_range", "visible")], ["iso_abund", "movie_iso_abund"], True)
    frame.set_state_links("mass_link", [("set_mass", "value"), ("mass_range", "visible")], ["iso_abund", "abu_chart"]+states_movie[1:], True)

    frame.set_state_attribute("lim_settings" , ["iso_abund", "abu_chart", "kip_cont", "tcrhoc"]+states_movie[1:], visible=True, **group_style)
    frame.set_state_attribute("set_lims", ["iso_abund", "abu_chart", "kip_cont", "tcrhoc"]+states_movie[1:], visible=True, description="Set axis limits: ")
    frame.set_state_attribute("xlim", ["abu_chart", "movie_abu_chart", "kip_cont"], description="x-axis limits: ", min=0, max=130, value=(0, 130), step=0.5)
    frame.set_state_attribute("xlim", "tcrhoc", description="x-axis limits: ", min=3.0, max=10.0, value=(3.0, 10.0), step=0.5)
    frame.set_state_attribute("ylim", ["iso_abund", "abu_chart", "kip_cont", "tcrhoc"]+states_movie[1:], description="y-axis limits: ")
    frame.set_state_attribute("ylim", ["iso_abund", "movie_iso_abund"], min=-13, max=0, step=0.05, value=(-13, 0))
    frame.set_state_attribute("ylim", ["abu_chart", "movie_abu_chart"], min=0, max=130, value=(0, 130), step=0.5)
    frame.set_state_attribute("ylim", "kip_cont", min=0, max=1, value=(0, 1), step=0.005)#mass
    frame.set_state_attribute("ylim", "tcrhoc", min=8.0, max=10.0, value=(8.0, 10.0), step=0.5)
    frame.set_state_attribute("ixaxis", "kip_cont", visible=True, description="X axis format: ", options={"Log time":"log_time_left", "Age":"age", "Model number":"model_number"}, value="model_number")

    frame.set_state_links("xlims_link", [("set_lims", "value"), ("xlim", "visible")], ["abu_chart", "movie_abu_chart", "kip_cont", "tcrhoc"], True)
    frame.set_state_links("ylims_link", [("set_lims", "value"), ("ylim", "visible")], ["iso_abund", "abu_chart", "kip_cont", "tcrhoc"]+states_movie[1:], True)

    frame.set_state_attribute("xres", "kip_cont", visible=True, description="x resolution: ", placeholder="1000", **text_box_style)
    frame.set_state_attribute("yres", "kip_cont", visible=True, description="y resolution: ", placeholder="1000", **text_box_style)

    frame.set_state_links("xres_link", [("set_lims", "value"), ("xres", "visible")], "kip_cont", True)
    frame.set_state_links("yres_link", [("set_lims", "value"), ("yres", "visible")], "kip_cont", True) 

    frame.set_state_attribute("abu_settings", ["abu_chart", "movie_abu_chart"], visible=True, **group_style)
    frame.set_state_attribute("ilabel", ["abu_chart", "movie_abu_chart"], visible=True, description="Element label")
    frame.set_state_attribute("imlabel", ["abu_chart", "movie_abu_chart"], visible=True, description="Isotope label")
    frame.set_state_attribute("imagic", ["abu_chart", "movie_abu_chart"], visible=True, description="Magic numbers")

    frame.set_state_attribute("kipp_settings", ["kippenhahn", "kip_cont"], visible=True, **group_style)
    frame.set_state_attribute("plot_star_mass", "kippenhahn", visible=True, description="Plot star mass: ")
    frame.set_state_attribute("plot_c12border", ["kippenhahn", "kip_cont"], visible=True, description="Show C-12 Border: ")
    frame.set_state_attribute("plot_engminus", "kip_cont", visible=True, description="Energy generation contours (eps_nuc>0): ")
    frame.set_state_attribute("plot_engplus", "kip_cont", visible=True, description="Energy generation contours (eos_nuc<0): ")

    frame.set_state_attribute("stable", "iso_abund", visible=True, description="stable: ")

    frame.set_state_attribute('generate_plot', states_plotting, visible=True, description="Generate Plot", **button_style)
    frame.set_state_attribute('generate_plot', ["get_data", "nugrid_get_data"], visible=True, description="Get Data", **button_style)

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
            timer = threading.Timer(1.0, variable_name_full_validation, kwargs={"value":value})
            timer.start()
        else:
            timer.cancel()
            timer = None
        frame.set_state_data("variable_name_timer", timer)

    def yres_handler(name, value):
        frame.set_attributes("yres", value=int_text(value))

    def xres_handler(name, value):
        frame.set_attributes("xres", value=int_text(value))
        
    def sel_plot(widget, value):
        data = frame.get_state_data("class_instance")
    
        if value in ["iso_abund", "abu_chart"]:
            cycle_list = data.se.cycles
            step = int(cycle_list[1])-int(cycle_list[0])
            min = int(cycle_list[0])
            max = int(cycle_list[-1])
        
            mass_list = data.se.get(min, "mass")
            mass_min, mass_max = mass_list[0], mass_list[-1]
            mass_step = (mass_max - mass_min)/200.0
            frame.set_state_attribute("mass_range", ["iso_abund", "abu_chart"], min=mass_min, max=mass_max, value=(mass_min, mass_max), step=mass_step)
        
            frame.set_state_attribute('cycle', ["iso_abund", "abu_chart"], min=min, max=max, step=step)
    
        if value == "kip_cont":
            min = 0
            max = len(data.data)
            mass = data.header_attr["initial_mass"]
        
            frame.set_state_attribute("xlim", "kip_cont", min=min, max=max, step=1, value=(min, max))    
            frame.set_state_attribute("ylim", "kip_cont", min=0.0, max=mass, step=mass/200.0, value=(0.0, mass))

        if value in ["nugrid_plot", "nugrid_get_data"]:
            cycle_list = data.se.cycles
            step = int(cycle_list[1])-int(cycle_list[0])
            min = int(cycle_list[0])
            max = int(cycle_list[-1])
        
            frame.set_state_attribute('cycle', ["nugrid_plot", "nugrid_get_data"], min=min, max=max, step=step)
        
        frame.set_state(value)
        
    def sel_movie_plot(widget, value):
        data = frame.get_state_data("class_instance")
    
        if value in ["movie_iso_abund", "movie_abu_chart"]:
            cycle_list = data.se.cycles
            step = int(cycle_list[1])-int(cycle_list[0])
            min = int(cycle_list[0])
            max = int(cycle_list[-1])
        
            mass_list = data.se.get(min, "mass")
            mass_min, mass_max = mass_list[0], mass_list[-1]
            mass_step = (mass_max - mass_min)/200.0
            frame.set_state_attribute("mass_range", ["movie_iso_abund", "movie_abu_chart"], min=mass_min, max=mass_max, value=(mass_min, mass_max), step=mass_step)
        
            frame.set_state_attribute('cycle_range', ["movie_iso_abund", "movie_abu_chart"], min=min, max=max, step=step, value=(min, max))
        
        frame.set_state(value)

    def make_plot(widget):
        clear_output()
        pyplot.close("all")
        state = frame.get_state()
    
        data = frame.get_state_data("class_instance")
        variable_name = frame.get_attribute("variable_name", "value")
        cycle = frame.get_attribute("cycle", "value")
        cycle_range = frame.get_attribute("cycle_range", "value")
        xax = frame.get_attribute("xaxis", "value")
        logx = frame.get_attribute("logx", "value")
        yax = frame.get_attribute("yaxis", "value")
        logy = frame.get_attribute("logy", "value")
        if frame.get_attribute("set_amass", "value"):
            amass = frame.get_attribute("amass_range", "value")
            amass = [amass[0], amass[1]]
        else:
            amass = None
        
        if frame.get_attribute("set_mass", "value"):
            mass = frame.get_attribute("mass_range", "value")
            mass = [mass[0], mass[1]]
        else:
            mass = None
        
        lbound = frame.get_attribute("lbound", "value")
        
        if frame.get_attribute("set_lims", "value"):
            xlim = frame.get_attribute("xlim", "value")
            ylim = frame.get_attribute("ylim", "value")
        else:
            xlim = [0, 0]
            ylim = [0, 0]
            
        xres = frame.get_attribute("xres", "value")
        if xres == "":
            xres = "1000"
        yres = frame.get_attribute("yres", "value")
        if yres == "":
            yres = "1000"
        
        xres = int(xres)
        yres = int(yres)
        
        ixaxis = frame.get_attribute("ixaxis", "value") 
        
        stable = frame.get_attribute("stable", "value")
        ilabel = frame.get_attribute("ilabel", "value")
        imlabel = frame.get_attribute("imlabel", "value")
        imagic = frame.get_attribute("imagic", "value")

        plot_star_mass = frame.get_attribute("plot_star_mass", "value")
        plot_c12border = frame.get_attribute("plot_c12border", "value")
        plot_engminus = frame.get_attribute("plot_engminus", "value")
        plot_engplus = frame.get_attribute("plot_engplus", "value")
        
        if state=="iso_abund":
            data.iso_abund(cycle, stable, amass, mass, ylim)
        elif state=="abu_chart":
            plotaxis = [xlim[0], xlim[1], ylim[0], ylim[1]]
            data.abu_chart(cycle, mass, ilabel, imlabel, imagic=imagic, lbound=lbound, plotaxis=plotaxis, ifig=1)
        elif state=="plot":
            if isinstance(yax, basestring):
                yax = [yax]
            for yaxis in yax:
                data.plot(xax, yaxis, logx=logx, logy=logy, shape="-")
        elif state=="nugrid_plot":
            if isinstance(yax, basestring):
                yax = [yax]
            for yaxis in yax:
                data.plot(xax, yaxis, logx=logx, logy=logy, shape="-", fname=cycle, numtype="time")
        elif state=="hrd":
            data.hrd_new()
        elif state=="kippenhahn":
            data.kippenhahn(0, "model", plot_star_mass=plot_star_mass, c12_bm=plot_c12border)
        elif state=="kip_cont":
            xlims=[xlim[0], xlim[1]]
            ylims=[ylim[0], ylim[1]]
            if (xlims == [0,0]) and (ylims == [0,0]):
                xlim = frame.get_attribute("xlim", "value")
                ylim = frame.get_attribute("ylim", "value")
                xlims=[xlim[0], xlim[1]]
                ylims=[ylim[0], ylim[1]]
            data.kip_cont(modstart=xlims[0], modstop=xlims[1], ylims=ylims, xres=xres, yres=yres, engenPlus=plot_engplus, engenMinus=plot_engminus, c12_boundary=plot_c12border, ixaxis = ixaxis)
        elif state=="tcrhoc":
            lims=[xlim[0], xlim[1], ylim[0], ylim[1]]
            if lims == [0, 0, 0, 0]:
                lims = [3.0, 10.0, 8.0, 10.0]
            data.tcrhoc(lims=lims)
        elif state=="movie_iso_abund":
            cycles = data.se.cycles
            cyc_min = cycles.index("%010d" % (cycle_range[0], ))
            cyc_max = cycles.index("%010d" % (cycle_range[1], ))
            cycles = cycles[cyc_min:cyc_max]
            display(data.movie(cycles, "iso_abund", amass_range=amass, mass_range=mass, ylim=ylim))
        elif state=="movie_abu_chart":
            cycles = data.se.cycles
            cyc_min = cycles.index("%010d" % (cycle_range[0], ))
            cyc_max = cycles.index("%010d" % (cycle_range[1], ))
            cycles = cycles[cyc_min:cyc_max]
            plotaxis = [xlim[0], xlim[1], ylim[0], ylim[1]]
            display(data.movie(cycles, "abu_chart", mass_range=mass, ilabel=ilabel, imlabel=imlabel, imagic=imagic, plotaxis=plotaxis))
        elif state=="get_data":
            global_namespace[variable_name] = data.get(xax)
            print("\nThe data " + str(xax) + " is loaded into the global namespace under the variable name \"" + str(variable_name) + "\".")
        elif state=="nugrid_get_data":
            global_namespace[variable_name] = data.se.get(cycle, xax)
            print("\nThe data " + str(xax) + " is loaded into the global namespace under the variable name \"" + str(variable_name) + "\".")

    def test(widget):
        print("submit!")

    frame.set_state_callbacks("variable_name", variable_name_handler)
    frame.set_state_callbacks("variable_name", test, attribute=None, type="on_click")
    frame.set_state_callbacks("yres", yres_handler)
    frame.set_state_callbacks("xres", xres_handler)
    frame.set_state_callbacks("select_plot", sel_plot)
    frame.set_state_callbacks("movie_type", sel_movie_plot)
    frame.set_state_callbacks("generate_plot", make_plot, attribute=None, type="on_click")

    frame.set_object("page_plotting", widgets.VBox())
    frame.set_object("select_plot", widgets.Dropdown())
    frame.set_object("warning_msg", widgets.HTML())
    frame.set_object("plot_name", widgets.HTML())
    frame.set_object("movie_type", widgets.Dropdown())
    frame.set_object("variable_name", widgets.Text())
    frame.set_object("cycle", widgets.IntSlider())
    frame.set_object("cycle_range", widgets.IntRangeSlider())
    frame.set_object("xax", widgets.HBox())
    frame.set_object("xaxis", widgets.Select())
    frame.set_object("logx", widgets.Checkbox())
    frame.set_object("yax", widgets.HBox())
    frame.set_object("yaxis", widgets.SelectMultiple())
    frame.set_object("logy", widgets.Checkbox())

    frame.set_object("mass_settings", widgets.VBox())
    frame.set_object("set_amass", widgets.Checkbox())
    frame.set_object("amass_range", widgets.IntRangeSlider())
    frame.set_object("set_mass", widgets.Checkbox())
    frame.set_object("mass_range", widgets.FloatRangeSlider())
    frame.set_object("lbound", widgets.FloatRangeSlider())

    frame.set_object("lim_settings", widgets.VBox())
    frame.set_object("set_lims", widgets.Checkbox())
    frame.set_object("ixaxis", widgets.Dropdown())
    frame.set_object("ylim", widgets.FloatRangeSlider())
    frame.set_object("xlim", widgets.FloatRangeSlider())
    frame.set_object("yres", widgets.Text())
    frame.set_object("xres", widgets.Text())

    frame.set_object("stable", widgets.Checkbox())

    frame.set_object("abu_settings", widgets.HBox())
    frame.set_object("ilabel", widgets.Checkbox())
    frame.set_object("imlabel", widgets.Checkbox())
    frame.set_object("imagic", widgets.Checkbox())

    frame.set_object("kipp_settings", widgets.HBox())
    frame.set_object("plot_star_mass", widgets.Checkbox())
    frame.set_object("plot_c12border", widgets.Checkbox())
    frame.set_object("plot_engminus", widgets.Checkbox())
    frame.set_object("plot_engplus", widgets.Checkbox())

    frame.set_object("generate_plot", widgets.Button())

    frame.display_object("window")
