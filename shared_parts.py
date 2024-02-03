from functools import lru_cache

class SharedPartsManager:
    
    def __init__(
        self, 
        class_storage_dict: dict, 
        use_cache: bool=True,  
        cache_limit: int = 50,
        *init_args
    ) -> None:
        self.class_storage_dict = class_storage_dict
        self.init_args = init_args
        if use_cache:
            self.__getattr__ = lru_cache(cache_limit)(self.__getattr__)
        
    
    def __getattr__(self, name: str):
        try:
            class_tpl = self.class_storage_dict[name]
        except KeyError:
            raise AttributeError(
                'SharedPartsManager does not'
                ' have the class named %s' % name
            ) from None
        
        return class_tpl(self, *self.init_args)
        