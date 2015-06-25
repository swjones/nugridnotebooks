from IPython.html import widgets
from IPython.utils import traitlets
from IPython.display import display

class framework():
    def __init__(self):
        self._state = ""
        
        ##order of operations
        self._order_of_operations = ["options", "max", "min", "max", "value", "selected_index"]
        
        #global defaults
        self._default_io_style = {}
        self._default_display_style = {}

        #object lists
        self._object_list = {}
        self._link_object = {}

        #state specific properties
        self._attributes = {}
        self._links = {}
        self._callbacks = {}
        self._children = {}
        self._data = {}
        
        #registration lists
        self._state_list = []
        self._display_list = []
        self._io_list = []

        self.add_state("default")
        
    def update(self):
        self._update(self._state)
        
    def _update(self, state="default"):
        for obj_name in self._object_list:
            ##apply attributes
            default_style = {}
            if obj_name in self._display_list:
                default_style = self._default_display_style
            elif obj_name in self._io_list:
                default_style = self._default_io_style
                
            default_attributes = {}
            if "default" in self._attributes:
                if obj_name in self._attributes["default"]:
                    default_attributes = self._attributes["default"][obj_name]
            
            state_attributes = {}
            if state in self._attributes:
                if obj_name in self._attributes[state]:
                    state_attributes = self._attributes[state][obj_name]
            
            attributes = default_style.copy()
            attributes.update(default_attributes)
            attributes.update(state_attributes)
            
            if not "visible" in attributes:
                attributes["visible"] = False

            self.set_attributes(obj_name, **attributes)

        ##apply links
        for link_name in self._link_object: #clear link objects
            self._link_object[link_name].unlink()
        self._link_objects = {}

        default_links = {}
        if "default" in self._links:
            default_links = self._links["default"]
        
        state_links = {}
        if state in self._links:
            state_links = self._links[state]
        
        links_dict = default_links.copy()
        links_dict.update(state_links)
        
        for link_name in links_dict:
            directional, links_list = links_dict[link_name]
            links = []
            for link in links_list:
                links.append((self._object_list[link[0]], link[1]))
            if directional:
                self._link_objects[link_name] = traitlets.dlink(*links)
            else:
                self._link_objects[link_name] = traitlets.link(*links)


        ##callbacks
        default_callbacks = {}
        if "default" in self._callbacks:
            default_callbacks = self._callbacks["default"]
        
        state_callbacks = {}
        if state in self._callbacks:
            state_callbacks = self._callbacks[state]
            
        callbacks = default_callbacks.copy()
        callbacks.update(state_callbacks)
        
        for obj_name in callbacks:
            for type in callbacks[obj_name]:
                if hasattr(self._object_list[obj_name], type):
                    if type == "on_trait_change":
                        self._object_list[obj_name].on_trait_change(*callbacks[obj_name][type])
                    elif type == "on_click":
                        self._object_list[obj_name].on_click(callbacks[obj_name][type][0])
                    elif type == "on_submit":
                        self._object_list[obj_name].on_submit(callbacks[obj_name][type][0])
                    else:
                        raise ValueError("the object: "+obj_name+" has no method called: "+type)
        ##children
        default_children = {}
        if "default" in self._children:
            default_children = self._children["default"]
            
        state_children = {}
        if state in self._children:
            state_children = self._children[state]
            
        children = default_children.copy()
        children.update(state_children)

        for obj_name in children:
            if children[obj_name][0]:
                for i, title in enumerate(children[obj_name][2]):
                    self._object_list[obj_name].set_title(i, title) 
            children_list = [self._object_list[child_name] for child_name in children[obj_name][1]]
            self._object_list[obj_name].children = children_list

    def display_object(self, obj_name, state="default"):
        if obj_name in self._object_list:
            if state in self._state_list:
                self.set_state(state)
                display(self._object_list[obj_name])
            else:
                raise ValueError("no state: "+state+" defined!")
        else:
            raise ValueError("no object: "+obj_name+" defined!")
        
    def add_state(self, state_name):
        if not isinstance(state_name, basestring):
            for one_state_name in state_name:
                self.add_state(one_state_name)
        else:
            if state_name in self._state_list:
                raise ValueError("the state: "+state_name+" is already defined!")
            else:
                self._state_list.append(state_name)

    def get_state(self):
        return self._state
    
    def set_state(self, state="default"):
        if state in self._state_list:
            self._state = state
            self.update()
        else:
            raise ValueError("no state: "+state+" defined!")

    def set_state_callbacks(self, obj_name, callback, attribute="value",
                            state="default", type="on_trait_change"):
        """ 
        Set callback for the object obj_name when the state is state.
        type must be one of "on_trait_change", "on_click", "on_submit"
        """
        if not isinstance(state, basestring):
            for one_state in state:
                self.set_state_callbacks(obj_name, callback, attribute, one_state, type)
        else:
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
            
    def set_state_links(self, link_name, links, state="default",
                        directional=False):
        """ 
        Set links for the state. links should be of the form [("obj_name", "atribute"), ("obj_name", "attribute")]
        """
        if not isinstance(state, basestring):
            for one_state in state:
                self.set_state_links(link_name, links, one_state, directional)
        else:
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
        if not isinstance(state, basestring):
            for one_state in state:
                self.set_state_attribute(obj_name, one_state, **kwargs)
        else:
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
            
    def set_state_children(self, obj_name, children, state="default", titles=None, append=True):
        """ 
        Set chidren of the display widgets, children should be a list of names
        """
        if not isinstance(state, basestring):
            for one_state in state:
                self.set_state_children(obj_name, children, one_state, titles, append)
        else:
            if state in self._state_list:
                if obj_name in self._display_list:
                    if not (state in self._children):
                        self._children[state]={}
                    if titles == None:
                        if not (obj_name in self._children[state]):
                            self._children[state][obj_name] = (False, [])
                        if not append:
                            self._children[state][obj_name] = (False, [])
                        for child_name in children:
                            if child_name in self._object_list:
                                if not (child_name in self._children[state][obj_name][1]):
                                    self._children[state][obj_name][1].append(child_name)
                            else:
                                raise ValueError("no object: "+child_name+" defined!")
                    else:
                        if not (obj_name in self._children[state]):
                            self._children[state][obj_name] = (True, [], [])
                        if not append:
                            self._children[state][obj_name] = (True, [], [])
                        for i, child_name in enumerate(children):
                            if child_name in self._object_list:
                                if not (child_name in self._children[state][obj_name][1]):
                                    self._children[state][obj_name][1].append(child_name)
                                    self._children[state][obj_name][2].append(titles[i])
                            else:
                                raise ValueError("no object: "+child_name+" defined!")
                else:
                    if obj_name in self._object_list:
                        raise ValueError("object: "+obj_name+" must be a display object to be a parent object")
                    else:
                        raise ValueError("no object: "+obj_name+" defined!")
            else:
                raise ValueError("no state: "+state+" defined!")
    
    def set_state_data(self, data_name, data, state="default"):
        """ 
        Set data associated with the given state.
        """
        if not isinstance(state, basestring):
            for one_state in state:
                self.set_state_data(data_name, data, one_state)
        else:
            if state in self._state_list:
                if not (state in self._data):
                    self._data[state]={}
                if not (data_name in self._data[state]):
                    self._data[state][data_name]=None
                self._data[state][data_name] = data
            else:
                raise ValueError("no state: "+state+" defined!")

    def get_state_data(self, data_name, state="default"):
        """ 
        get data associated with the given state
        """
        if state in self._state_list:
            if data_name in self._data[state]:
                return self._data[state][data_name]
            else:
                raise ValueError("no data: "+data_name+" defained for the state: "+state)
        else:
            raise ValueError("no state: "+state+" defined!")

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
            
    def remove_object(self, obj_name):
        if obj_name in self._display_list:
            index = self._display_list.index(obj_name)
            del self._display_list[index]
        elif obj_name in self._io_list:
            index = self._io_list.index(obj_name)
            del self._io_list[index]
        else:
            raise ValueError("The object: "+obj_name+" is not defined!")
        
        if obj_name in self._object_list:
            if self._object_list[obj_name] != None:
                self._object_list[obj_name].close()
            
            del self._object_list[obj_name]
        else:
            raise ValueError("The object: "+obj_name+" is not defined!")        

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
        
    def set_default_display_style(self, **kwargs):
        self._default_display_style = kwargs
        
    def set_attributes(self, obj_name, **kwargs):
        if obj_name in self._object_list:
            un_ordered_keys = kwargs.keys()
            un_ordered_keys = list(set(un_ordered_keys) - set(self._order_of_operations))

            for attr in self._order_of_operations: #apply attributes in a given order
                if attr in kwargs:
                    if hasattr(self._object_list[obj_name], attr):
                        try:
                            setattr(self._object_list[obj_name], attr, kwargs[attr])
                        except ValueError:
                            if not (attr in ["min", "max"]):
                                raise
                    else:
                        raise AttributeError(obj_name+" does not have attribute "+attr)
            
            for attr in un_ordered_keys: #apply all other attributes in an arbitrary order
                if hasattr(self._object_list[obj_name], attr):
                    setattr(self._object_list[obj_name], attr, kwargs[attr])
                else:
                    raise AttributeError(obj_name+" does not have attribute "+attr)
        else:
            raise ValueError("The object: "+obj_name+" is not defined!")

    def get_attribute(self, obj_name, attribute):
        if obj_name in self._object_list:
            obj = self._object_list[obj_name]
            if hasattr(obj,attribute):
                return getattr(obj, attribute)
            else:
                raise AttributeError(obj_name+" does not have attribute "+attribute)
        else:
            raise ValueError("The object: "+obj_name+" is not defined!")
