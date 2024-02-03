from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Optional
from types import MappingProxyType
from abc import abstractmethod, ABCMeta
from functools import partial

if TYPE_CHECKING:
    from .attribute_dictionary import AttributeDictionary
    from .shared_parts import SharedPartsManager


def default_init(
    self, 
    shared_parts: SharedPartsManager,
    parameters: MappingProxyType,
    shared_vars: AttributeDictionary 
):
    self.parameters = parameters
    self.shared_vars = shared_vars
    self.shared_parts = shared_parts
    
def default_subclass_init(
    cls, 
    name: str, 
    shared: bool, 
    storage_class: type
):
    cls.__hook_name__ = name
    cls.__hook_shared__ = shared
    if not hasattr(storage_class, 'components'):
        storage_class.components = {}
    
    storage_class.components[name] = cls
    
    if not hasattr(storage_class, 'shared_components'):
        storage_class.shared_components = {}
            
    if shared:
        storage_class.shared_components[name] = cls
    


class HookMaker:
    
    def __init__(
        self, classname: str, 
        storage_class: type, 
        init_method: Optional[Callable] = None,
        subclass_init: Optional[Callable] = None,
        protocol: Optional[list[str]] = None
    ) -> None:
        self.classname = classname
        self.storage_class = storage_class
        if init_method is None:
            init_method = default_init
        self.init_method = init_method
        self.protocol = protocol
        
        if subclass_init is None:
            self.subclass_init = default_subclass_init
    
    def create_hook_class(self):
        
        attributes = {
            '__init__': self.init_method,
            '__init_subclass__': partial(default_subclass_init, storage_class=self.storage_class)
        }
        kwargs = {}
        if self.protocol is not None:
            kwargs['metaclass'] = ABCMeta
        
        def abstract_method(self, *args, **kwargs):
            raise NotImplementedError
        
        for method in self.protocol:
            attributes[method] = abstract_method
        
        parent_class = type(
            self.classname, 
            (object, ), 
            attributes
            **kwargs
        )
        
        for method in self.protocol:
            setattr(
                parent_class, method, 
                abstractmethod(getattr(parent_class, method))
            )
        return parent_class
            