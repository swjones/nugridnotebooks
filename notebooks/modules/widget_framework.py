from IPython.html import widgets
from IPython.display import display

class framework():
    def __init__(self):
        self._state = ""
        
        self._default_io_style = {}
        self._default_layout_style = {}
        self._object_list = {}

        #state specific properties
        #_propertie[state][object][propertie]=value
        self._attributes = {}
        self._links = {}
        self._callbacks = {}
        self._children = {}
        
        #registration lists
        self._state_list = []
        self._primary_display_list = []
        self._display_list = []
        self._io_list = []

        self.add_state("default")
        
    def add_state(self, state_name):
        if state_name in self._state_list:
            raise ValueError("the state: "+state_name+" is already defined!")
        else:
            self._state_list.append(state_name)
    
    def switch_state(self, state):
        if state in self._state_list:
            self._state = state
            pass #reset all functionality
        else:
            raise ValueError("no state: "+state+" defined!")

    def set_state_callbacks(self, obj_name, callback, attribute=None, state="default", type="on_trait_change"):
        """ 
        Set callback for the object obj_name when the state is state.
        type must be one of "on_trait_change", "on_click", "on_submit"
        """
        if obj_name in self._object_list:
            if state in self._state_list:
                if type in ["on_trait_change", "on_click", "on_submit"]:
                    if not (state in self._callbacks):
                        self._callbacks[state]={}
                    if not (obj_name in self._callbacks[state]):
                        self._callbacks[state][obj_name]={}
                    if (type == "on_trait_change") and (attribute==None):
                        raise ValueError("if type == 'on_trait_change' then attribute must be defined")
                    self._callbacks[state][obj_name][type] = [callback, attribute]
                else:
                    raise ValueError("no callback: "+type+" defined!")
            else:
                raise ValueError("no state: "+state+" defined!")
        else:
            raise ValueError("no object: "+obj_name+" defined!")
            
    def set_state_links(self, link_name, links, state="default", directional=False):
        """ 
        Set links for the state. links should be of the form [("obj_name", "atribute"), ("obj_name", "attribute")]
        """
        if state in self._state_list:
            if not (state in self._links):
                self._links[state]={}
            if not (link_name in self._links[state]):
                self._links[state][link_name]=[]
            self._links[state][link_name] = [directional, links]
        else:
            raise ValueError("no state: "+state+" defined!")
            
    def set_state_attribute(self, obj_name, state="default", **kwargs):
        """ 
        Set attributes of the object: obj_name when the current state is state
        """
        if obj_name in self._object_list:
            if state in self._state_list:
                if not (state in self._attributes):
                    self._attributes[state]={}
                if not (obj_name in self._attributes[state]):
                    self._attributes[state][obj_name]={}
                for key in kwargs:
                    self._attributes[state][obj_name][key] = kwargs[key]
            else:
                raise ValueError("no state: "+state+" defined!")
        else:
            raise ValueError("no object: "+obj_name+" defined!")
            
    def set_children(self, obj_name, children, state="default"):
        if state in self._state_list:
            if obj_name in self._display_list:
                if not (state in self._children):
                    self._children[state]={}
                if not (obj_name in self._children[state]):
                    self._children[state][obj_name] = []
                for child_name in children:
                    if child_name in self._object_list:
                        if not (child_name in self._children[state][obj_name]):
                            self._children[state][obj_name].append(child_name)
                    else:
                        raise ValueError("no object: "+child_name+" defined!")
            else:
                if obj_name in self._object_list:
                    raise ValueError("object: "+obj_name+" must be a display object to be a parent object")
                else:
                    raise ValueError("no object: "+obj_name+" defined!")
        else:
            raise ValueError("no state: "+state+" defined!")
            
    def switch_primary_display(self, obj_name):
        """ 
        Switch between primary display layout widgets. When widgets
        are switched the active widget becomes visible and all inactive
        widgets are set to invisible.
        """
        not_found = True
        for key in self._primary_display_list:
            if key == obj_name:
                self._object_list[key].visible = True
                not_found = False
            else:
                self._object_list[key].visible = False
        if not_found:
            raise ValueError("the object "+obj_name+" was not found!")

    def add_primary_display_object(self, obj_name):
        """ 
        Add primary display widgets, these widgets should contain all
        other widgets.
        """
        if obj_name in self._primary_display_list:
            raise ValueError("The object: " + obj_name+" is already defined!")
        else:
            self._primary_display_list.append(obj_name)
            self.add_display_object(obj_name)
        
    def add_display_object(self, obj_name):
        """ 
        add display widget, these widgets should all be container type
        widgets.
        """
        if (obj_name in self._display_list) or (obj_name in self._object_list):
            raise ValueError("The object: " + obj_name+" is already defined!")
        else:
            self._display_list.append(obj_name)
            self._object_list[obj_name] = None

    def add_io_object(self, obj_name):
        """ 
        add io widget.
        """
        if (obj_name in self._io_list) or (obj_name in self._object_list):
            raise ValueError("The object: " + obj_name+" is already defined!")
        else:
            self._io_list.append(obj_name)
            self._object_list[obj_name] = None
            
    def set_object(self, obj_name, object):
        if obj_name in self._object_list:
            self._object_list[obj_name] = object
        else:
            raise ValueError("The object: "+obj_name+" is not defined!")
        
    def set_default_io_style(self, **kwargs):
        self._default_io_style = kwargs
        
    def set_default_layout_style(self, **kwargs):
        self._default_layout_style = kwargs
        
    def _apply_attributes(self, obj_name, **kwargs):
        if obj_name in self._object_list:
            obj = self._object_list[obj_name]
            for attr in kwargs:
                if hasattr(obj,attr):
                    setattr(obj, attr, kwargs[attr])
                else:
                    raise AttributeError(obj_name+" does not have attribute "+attr)
        else:
            raise ValueError("The object: "+obj_name+" is not defined!")
            
