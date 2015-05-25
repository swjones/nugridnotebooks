import matplotlib
import os

#temp fix
if os.path.isdir("/home/nugrid/omega_sygma"):
    os.environ["SYGMADIR"] = "/home/nugrid/omega_sygma"
#if os.path.isdir("/rpod3/lsiemens/omega_sygma"):
#    os.environ["SYGMADIR"] = "/rpod3/lsiemens/omega_sygma"

import sygma as s

import widget_framework as framework
from widget_utils import float_text
from IPython.html import widgets
from IPython.display import display, clear_output
from matplotlib import pyplot

frame = framework.framework()
frame.set_default_display_style(padding="0.25em",background_color="white", border_color="LightGrey", border_radius="0.5em")
frame.set_default_io_style(padding="0.25em", margin="0.25em", border_color="LightGrey", border_radius="0.5em")

group_style = {"border_style":"", "border_radius":"0em"}
text_box_style = {"width":"10em"}
button_style = {"font_size":"1.25em", "font_weight":"bold"}

states = ["run_sim", "plot_totmasses", "plot_mass", "plot_spectro", "plot_mass_range"]

frame.add_state(states)

isotopes_all=['H-1','H-2','He-3','He-4','Li-7','B-11','C-12','C-13','N-14','N-15','O-16','O-17','O-18','F-19','Ne-20','Ne-21','Ne-22','Na-23','Mg-24','Mg-25','Mg-26','Al-27','Si-28','Si-29','Si-30','P-31','S-32','S-33','S-34','S-36','Cl-35','Cl-37','Ar-36','Ar-38','Ar-40','K-39','K-40','K-41','Ca-40','Ca-42','Ca-43','Ca-44','Ca-46','Ca-48','Sc-45','Ti-46','Ti-47','Ti-48','Ti-49','Ti-50','V-50','V-51','Cr-50','Cr-52','Cr-53','Cr-54','Mn-55','Fe-54','Fe-56','Fe-57','Fe-58','Co-59','Ni-58','Ni-60','Ni-61','Ni-62','Ni-64']
elements_all=['H','He','Li','B','C','N','O','F','Ne','Na','Mg','Al','Si','P','S','Cl','Ar','K','Ca','Sc','Ti','V','Cr','Mn','Fe','Co','Ni']
isotopes_sn1a=['C-12','C-13','N-14','N-15','O-16','O-17','O-18','F-19','Ne-20','Ne-21','Ne-22','Na-23','Mg-24','Mg-25','Mg-26','Al-27','Si-28','Si-29','Si-30','P-31','S-32','S-33','S-34','S-36','Cl-35','Cl-37','Ar-36','Ar-38','Ar-40','K-39','K-40','K-41','Ca-40','Ca-42','Ca-43','Ca-44','Ca-46','Ca-48','Sc-45','Ti-46','Ti-47','Ti-48','Ti-49','Ti-50','V-50','V-51','Cr-50','Cr-52','Cr-53','Cr-54','Mn-55','Fe-54','Fe-56','Fe-57','Fe-58','Co-59','Ni-58','Ni-60','Ni-61','Ni-62','Ni-64']
elements_sn1a=['C','N','O','F','Ne','Na','Mg','Al','Si','P','S','Cl','Ar','K','Ca','Sc','Ti','V','Cr','Mn','Fe','Co','Ni']

frame.set_state_data("elements", elements_all)
frame.set_state_data("isotopes", isotopes_all)

frame.add_display_object("window")
frame.add_io_object("title")
frame.add_display_object("widget")

###Sim page###
frame.add_display_object("sim_page")

frame.add_display_object("mass_Z_group")
frame.add_io_object("init_Z")
frame.add_io_object("mass_gas")

frame.add_display_object("time_group")
frame.add_io_object("t_end")
frame.add_io_object("dt")

frame.add_display_object("imf_type_group")
frame.add_io_object("imf_type")
frame.add_io_object("imf_alpha")

frame.add_display_object("imf_mass_group")
frame.add_io_object("imf_mass_min")
frame.add_io_object("imf_mass_max")

frame.add_display_object("sn1a_group")
frame.add_io_object("use_sn1a")
frame.add_io_object("sn1a_rates")
frame.add_io_object("run_sim")

frame.add_io_object("plot_type")
frame.add_io_object("sim_responce")

frame.set_state_children("window", ["title", "widget"])
frame.set_state_children("widget", ["sim_page"], titles=["Simulation"])
frame.set_state_children("sim_page", ["mass_Z_group", "time_group", "imf_type_group", "imf_mass_group", "sn1a_group", "run_sim", "sim_responce"])
frame.set_state_children("mass_Z_group", ["mass_gas", "init_Z"])
frame.set_state_children("time_group", ["t_end", "dt"])
frame.set_state_children("imf_type_group", ["imf_type", "imf_alpha"])
frame.set_state_children("imf_mass_group", ["imf_mass_min", "imf_mass_max"])
frame.set_state_children("sn1a_group", ["use_sn1a", "sn1a_rates"])

###plotting page###
frame.add_display_object("plot_page")

frame.add_display_object("warning_msg")
frame.add_display_object("plot_name")
frame.add_io_object("source")

frame.add_display_object("spieces_group")
frame.add_io_object("iso_or_elem")
frame.add_io_object("spieces")

frame.add_io_object("elem_numer")
frame.add_io_object("elem_denom")
frame.add_io_object("plot")

frame.set_state_children("widget", ["plot_page"], titles=["Plotting"])
frame.set_state_children("plot_page", ["warning_msg", "plot_type", "plot_name", "source", "spieces_group", "elem_numer", "elem_denom", "plot"])
frame.set_state_children("spieces_group", ["iso_or_elem", "spieces"])


frame.set_state_data("sygma", None)

frame.set_state_attribute('window', visible=True, **group_style)
frame.set_state_attribute('title', visible=True, value="<h1>SYGMA</h1>")
frame.set_state_attribute('widget', visible=True, **group_style)

frame.set_state_attribute('sim_page', visible=True)
frame.set_state_attribute("mass_Z_group", visible=True, **group_style)
frame.set_state_attribute("mass_gas", visible=True, description="Total stellar mass [$M_{\odot}$]:", value="1.0", **text_box_style)
frame.set_state_attribute('init_Z', visible=True, description="Initial metallicity: ", options=["0.02", "0.01", "0.006", "0.001", "0.0001", "0.0"])

frame.set_state_attribute('time_group', visible=True, **group_style)
frame.set_state_attribute('t_end', visible=True, description="Final time [yrs]: ", value="1.0e10", **text_box_style)
frame.set_state_attribute('dt', visible=True, description="Time step [yrs]: ", value="1.0e7", **text_box_style)

frame.set_state_attribute('imf_type_group', visible=True, **group_style)
frame.set_state_attribute('imf_type', visible=True, description="IMF type: ", options=['salpeter', 'chabrier', 'kroupa', 'alphaimf'])
frame.set_state_attribute('imf_alpha', description="Set alpha: ", min=0, max=5)

frame.set_state_attribute("imf_mass_group", visible=True, **group_style)
frame.set_state_attribute('imf_mass_min', visible=True, description="IMF lower limit [$M_{\odot}$]: ", value="1.0", **text_box_style)
frame.set_state_attribute('imf_mass_max', visible=True, description="IMF upper limit [$M_{\odot}$]: ", value="30.0", **text_box_style)

frame.set_state_attribute('sn1a_group', visible=True, **group_style)
frame.set_state_attribute('use_sn1a', visible=True, description="Include SNe Ia: ", value=True)
frame.set_state_links("sn1a_link", [("use_sn1a", "value"), ("sn1a_rates", "visible")], directional=True)

frame.set_state_attribute('sn1a_rates', description="SNe Ia rates: ", options=['Power law', 'Exponential', 'Gaussian'])

frame.set_state_attribute('run_sim', visible=True, description="Run simulation", **button_style)

frame.set_state_attribute("sim_responce", value="<p>Simulation data loaded.</p>", **group_style)
frame.set_state_attribute("sim_responce", states, visible=True)

frame.set_state_attribute('plot_type', states, visible=True, description="Plot type: ", options=["Total mass", "Species mass", "Species spectroscopic", "Mass range contributions"])

def mass_gas_handler(name, value):
    frame.set_attributes("mass_gas", value=float_text(value))

def t_end_handler(name, value):
    frame.set_attributes("t_end", value=float_text(value))

def dt_handler(name, value):
    frame.set_attributes("dt", value=float_text(value))

def imf_mass_min_handler(name, value):
    frame.set_attributes("imf_mass_min", value=float_text(value))

def imf_mass_max_handler(name, value):
    frame.set_attributes("imf_mass_max", value=float_text(value))

def sel_imf_type(attribute, value):
    if value=="alphaimf":
        frame.set_state_attribute("imf_alpha", visible=True)
        frame.set_attributes("imf_alpha", visible=True, value=2.35)
    else:
        frame.set_state_attribute("imf_alpha", visible=False)
        frame.set_attributes("imf_alpha", visible=False)

def run_simulation(widget):
    frame.set_attributes("sim_responce", visible=False)
    clear_output()
    pyplot.close("all")
    
    sn1a_map = {"Power law":"maoz", "Exponential":"wiersmaexp", "Gaussian":"wiersmagauss"}
    
    mgal = float(frame.get_attribute("mass_gas", "value"))
    iniZ = float(frame.get_attribute("init_Z", "value"))
    imf_type = frame.get_attribute("imf_type", "value")
    alphaimf = frame.get_attribute("imf_alpha", "value")
    mass_min = float(frame.get_attribute("imf_mass_min", "value"))
    mass_max = float(frame.get_attribute("imf_mass_max", "value"))
    imf_bdys = [mass_min, mass_max]
    sn1a_on = frame.get_attribute("use_sn1a", "value")
    sn1a_rate = sn1a_map[frame.get_attribute("sn1a_rates", "value")]
    dt = float(frame.get_attribute("dt", "value"))
    tend = float(frame.get_attribute("t_end", "value"))
    if iniZ==0.0:
        data=s.sygma(mgal=mgal, iniZ=iniZ, imf_type=imf_type, alphaimf=alphaimf, imf_bdys=[10.1, 100.0], imf_bdys_pop3=imf_bdys, sn1a_on=sn1a_on,
                     sn1a_rate=sn1a_rate, dt=dt,tend=tend)
    else:
        data=s.sygma(mgal=mgal, iniZ=iniZ, imf_type=imf_type, alphaimf=alphaimf, imf_bdys=imf_bdys, sn1a_on=sn1a_on,
                     sn1a_rate=sn1a_rate, dt=dt,tend=tend)
    frame.set_state_data("sygma", data)
    frame.set_state("run_sim")
    ##force reset plottype
    frame.set_attributes("plot_type", selected_label="Species mass", value="Species mass")
    frame.set_attributes("plot_type", selected_label="Total mass", value="Total mass")
    
def sel_plot_type(attribute, value):
    if value=="Total mass":
        frame.set_state("plot_totmasses")
    elif value=="Species mass":
        frame.set_state("plot_mass")
    elif value=="Species spectroscopic":
        frame.set_state("plot_spectro")
    elif value=="Mass range contributions":
        frame.set_state("plot_mass_range")
    
    iniZ = float(frame.get_attribute("init_Z", "value"))
    if iniZ==0.0:
        frame.set_attributes("source", options=["All", "AGB", "Massive"])
    else:
        frame.set_attributes("source", options=["All", "AGB", "SNe Ia", "Massive"])


frame.set_state_callbacks("mass_gas", mass_gas_handler)        
frame.set_state_callbacks("t_end", t_end_handler)        
frame.set_state_callbacks("dt", dt_handler)        
frame.set_state_callbacks("imf_mass_min", imf_mass_min_handler)        
frame.set_state_callbacks("imf_mass_max", imf_mass_max_handler)        
frame.set_state_callbacks("imf_type", sel_imf_type)
frame.set_state_callbacks("run_sim", run_simulation, attribute=None, type="on_click")
frame.set_state_callbacks("plot_type", sel_plot_type)

frame.set_object("window", widgets.Box())
frame.set_object("title", widgets.HTML())
frame.set_object("widget", widgets.Tab())

frame.set_object("sim_page", widgets.VBox())
frame.set_object("mass_Z_group", widgets.HBox())
frame.set_object("mass_gas", widgets.Text())
frame.set_object("init_Z", widgets.Dropdown(options=["0.02"]))# option 0.02 is included since selection_label is set and will be called before options in set_state_attributes

frame.set_object("time_group", widgets.HBox())
frame.set_object("t_end", widgets.Text())
frame.set_object("dt", widgets.Text())

frame.set_object("imf_type_group", widgets.HBox())
frame.set_object("imf_type", widgets.Dropdown(options=['salpeter']))
frame.set_object("imf_alpha", widgets.FloatSlider())

frame.set_object("imf_mass_group", widgets.HBox())
frame.set_object("imf_mass_min", widgets.Text())
frame.set_object("imf_mass_max", widgets.Text())

frame.set_object("sn1a_group", widgets.HBox())
frame.set_object("use_sn1a", widgets.Checkbox())
frame.set_object("sn1a_rates", widgets.Dropdown())

frame.set_object("run_sim", widgets.Button())
frame.set_object("sim_responce", widgets.HTML())

frame.set_object("plot_type", widgets.Dropdown())


frame.set_state_attribute("plot_page", visible=True)
frame.set_state_attribute("warning_msg", visible=True, value="<h3>Error: No simulation data!</h3>", **group_style)
frame.set_state_attribute("warning_msg", states[1:], visible=False)
frame.set_state_attribute("plot_name", **group_style)
frame.set_state_attribute("plot_name", "plot_totmasses", visible=True, value="<h2>Plot: Total mass evolution</h2>")
frame.set_state_attribute("plot_name", "plot_mass", visible=True, value="<h2>Plot: Species mass evolution</h2>")
frame.set_state_attribute("plot_name", "plot_spectro", visible=True, value="<h2>Plot: Spectroscopic Mass evolution</h2>")
frame.set_state_attribute("plot_name", "plot_mass_range", visible=True, value="<h2>Plot: Mass range contributions</h2><p>Only ejecta from AGB and massive stars are considered.</p>")

frame.set_state_attribute("source", ["plot_totmasses", "plot_mass", "plot_spectro"], visible=True, description="Yield source: ", options=["All", "AGB", "SNe Ia", "Massive"], selected_label="All")
frame.set_state_attribute("spieces_group", ["plot_mass", "plot_mass_range"], visible=True, **group_style)
frame.set_state_attribute("iso_or_elem", visible=True, description="Spieces type: ", options=["Elements", "Isotopes"], selected_label="Elements")
frame.set_state_attribute("spieces", visible=True, description="Element: ", options=elements_all, **text_box_style)
frame.set_state_attribute("elem_numer", "plot_spectro", visible=True, description="Y-axis [X/Y], choose X: ", options=elements_all, **text_box_style)
frame.set_state_attribute("elem_denom", "plot_spectro", visible=True, description="Y-axis [X/Y], choose Y: ", options=elements_all, **text_box_style)
frame.set_state_attribute("plot", states[1:], visible=True, description="Generate Plot", **button_style)

def sel_source(attribute, value):
    if value=="SNe Ia":
        frame.set_state_data("elements", elements_sn1a)
        frame.set_state_data("isotopes", isotopes_sn1a)
    else:
        frame.set_state_data("elements", elements_all)
        frame.set_state_data("isotopes", isotopes_all)
        frame.set_attributes("elem_numer", options=[])
        frame.set_attributes("elem_denom", options=[])
        frame.set_attributes("spieces", options=[])

    elements = frame.get_state_data("elements")
    isotopes = frame.get_state_data("isotopes")
    frame.set_attributes("elem_numer", options=elements)
    frame.set_attributes("elem_denom", options=elements)
    
    if frame.get_attribute("iso_or_elem", "value")=="Isotopes":
        frame.set_attributes("spieces", description="Isotope: ", options=isotopes)
    elif frame.get_attribute("iso_or_elem", "value")=="Elements":
        frame.set_attributes("spieces", description="Element: ", options=elements)

def sel_iso_or_elem(attribute, value):
    elements = frame.get_state_data("elements")
    isotopes = frame.get_state_data("isotopes")
    if value=="Isotopes":
        frame.set_attributes("spieces", description="Isotope: ", options=isotopes)
    elif value=="Elements":
        frame.set_attributes("spieces", description="Element: ", options=elements)
    
def run(widget):
    clear_output()
    pyplot.close("all")
    source_map = {"All":"all", "AGB":"agb", "SNe Ia":"sn1a", "Massive":"massive"}
    state = frame.get_state()
    data = frame.get_state_data("sygma")
    source = source_map[frame.get_attribute("source", "value")]
    spieces = frame.get_attribute("spieces", "value")
    
    if state=="plot_totmasses":
        data.plot_totmasses(source=source)
    elif state=="plot_mass":
        data.plot_mass(specie=spieces, source=source)
    elif state=="plot_spectro":
        X = frame.get_attribute("elem_numer", "value")
        Y = frame.get_attribute("elem_denom", "value")
        yaxis = "["+X+"/"+Y+"]"
        data.plot_spectro(yaxis=yaxis, source=source)
    elif state=="plot_mass_range":
        data.plot_mass_range_contributions(specie=spieces)

frame.set_state_callbacks("source", sel_source, state=["plot_spectro", "plot_mass"])
frame.set_state_callbacks("iso_or_elem", sel_iso_or_elem)
frame.set_state_callbacks("plot", run, attribute=None, type="on_click")

frame.set_object("plot_page", widgets.VBox())
frame.set_object("warning_msg", widgets.HTML())
frame.set_object("plot_name", widgets.HTML())
frame.set_object("source", widgets.Dropdown(options=["All"]))
frame.set_object("spieces_group", widgets.VBox())
frame.set_object("iso_or_elem", widgets.RadioButtons(options=["Elements"]))
frame.set_object("spieces", widgets.Select())
frame.set_object("elem_numer", widgets.Select())
frame.set_object("elem_denom", widgets.Select())
frame.set_object("plot", widgets.Button())

def start_SYGMA():
    frame.display_object("window")
