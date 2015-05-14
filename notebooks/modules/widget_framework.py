from IPython.html import widgets
from IPython.display import display

class framework():
    def __init__(self):
        self._state = "default"
        
        self._default_io_style = {}
        self._default_layout_style = {}
        self._object_list = {}
        
        self._state_list = []
        self._primary_display_list = []
        self._display_list = []
        self._io_list = []
        
    def add_state(self, state_name):
        if state_name in self._state_list:
            raise ValueError("the state: "+state_name+" is currently in use.")
        else:
            self._state_list.append(state_name)
    
    def switch_state(self, state):
        if state in self._state_list:
            self._state = state
            pass #reset all functionality
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

    def add_primary_display_object(self, obj_name, obj):
        """ 
        Add primary display widgets, these widgets should contain all
        other widgets.
        """
        self._primary_display_list.append(obj_name)
        self.add_display_object(obj_name, obj)
        display(obj)
        
    def add_display_object(self, obj_name, obj):
        """ 
        add display widget, these widgets should all be container type
        widgets.
        """
        self._display_list.append(obj_name)
        self._object_list[obj_name] = obj
        obj.visible = False
        self._apply_attributes(obj_name, **self._default_layout_style)

    def add_io_object(self, obj_name, obj):
        """ 
        add io widget.
        """
        self._io_list.append(obj_name)
        self._object_list[obj_name] = obj
        obj.visible = False
        self._apply_attributes(obj_name, **self._default_io_style)
        
    def set_default_io_style(self, **kwargs):
        self._default_io_style = kwargs
        
    def set_default_layout_style(self, **kwargs):
        self._default_layout_style = kwargs
        
    def set_object
        
    def _apply_attributes(self, obj_name, **kwargs):
        if obj_name in self._object_list:
            obj = self._object_list[obj_name]
            for attr in kwargs:
                if hasattr(obj,attr):
                    setattr(obj, attr, kwargs[attr])
                else:
                    raise AttributeError(obj_name+" does not have attribute "+attr)
        else:
            raise ValueError(obj_name+" is not a valid obj_name!")
