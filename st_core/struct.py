from itertools import izip
from collections import OrderedDict
import copy


def DeepIterator(obj,iterable=(dict,list,tuple)):
    iter_path = [iter(obj)]
    obj_path = [obj]
    while len(iter_path)>0:
        try:
            _obj = obj_path[-1]
            _val = next(iter_path[-1])
            
            if isinstance(_obj,dict):
                _val = _obj[_val]
            
            # check val - dict, list,...
            if isinstance(_val,iterable):
                obj_path.append(_val)
                iter_path.append(iter(_val))
            else:
                yield _val
            
        except:
            iter_path.pop()
            obj_path.pop()
        
    return


def PathDeepIterator(obj,iterable=(dict,list,tuple)):
    iter_path = [iter(enumerate(obj))]
    obj_path = [obj]
    path = [None]
    while len(iter_path)>0:
        try:
            _obj = obj_path[-1]
            _ind, _val = next(iter_path[-1])
            if isinstance(_obj,dict):
                path.append(_val)
                _val = _obj[_val]
            else:
                path.append(_ind)
            
            # check val - dict, list,...
            if isinstance(_val,iterable):
                obj_path.append(_val)
                iter_path.append(iter(enumerate(_val)))
            else:
                yield (copy.deepcopy(path[1:]),_val)
                path.pop()
            
        except:
            iter_path.pop()
            obj_path.pop()
            path.pop()
        
    return


def set_path(o,path,value):
    _root = o
    
    for el in path[:-1]:
        _root = _root[el]
    
    _root[path[-1]] = value
            
    return o


def get_path(o,path):
    _root = o
    
    for el in path:
        _root = _root[el]
            
    return _root


class Structure(object):
    def __init__(self,obj,iterable=(OrderedDict,list,tuple)):
        self.object = obj
        self.iterable = iterable
        
        if dict in iterable:
            raise Exception("Structure class cannot iterate over dict, only over OrderedDict")
        
        for _el in DeepIterator(obj,iterable=iterable):
            if isinstance(_el,dict):
                raise Exception("Structure class cannot work with dict, only with OrderedDict")
                
        return
    
    def __getitem__(self,name):
        if not isinstance(name,(list,tuple)):
            name = (name,)
        return get_path(self.object,name)
    
    def __setitem__(self,name,value):
        if not isinstance(name,(list,tuple)):
            name = (name,)
        return set_path(self.object,name,value)
    
    def __iter__(self):
        return DeepIterator(self.object,iterable=self.iterable)
    
    def __str__(self):
        return str(self.object)
    
    def __repr__(self):
        return repr(self.object)
    
    def iteritems(self):
        return PathDeepIterator(self.object,iterable=self.iterable)
    
    @property
    def shape(self,iterable=(OrderedDict,list,tuple)):
        shape_obj = self.object.__class__(self.object)
        iter_path = [iter(enumerate(shape_obj))]
        obj_path = [shape_obj]
        while len(iter_path)>0:
            try:
                _obj = obj_path[-1]
                _ind, _val = next(iter_path[-1])
                
                if isinstance(_obj,dict):
                    _ind = _val
                    _val = _obj[_val]
                
                _new_val = None
                
                # check val - dict, list,...
                if isinstance(_val,iterable):
                    _new_val = _val.__class__(_val)
                    obj_path.append(_new_val)
                    iter_path.append(iter(enumerate(_new_val)))
                    
                _obj[_ind] = _new_val
                
            except:
                iter_path.pop()
                obj_path.pop()
        
        return shape_obj
    
    def to_list(self):
        res_list = []
        for _el in self:
            res_list.append(_el)
            
        return res_list
    
    def from_list(self,obj_list):
        _ind = -1
        for _ind, (_path, _el) in enumerate(self.iteritems()):
            self[_path] = obj_list[_ind]
            
        if _ind != len(obj_list)-1:
            raise Exception("Shapes are not match")
            
        return
    
    def reshape(self,new_shape):
        """
            Return new structure
        """
        
        new_struc = Structure(copy.deepcopy(new_shape),iterable=self.iterable)
        
        for (_path1,_el1),_el2 in izip(new_struc.iteritems(),self):
            new_struc[_path1] = _el2
        
        return new_struc
    
    def clone(self):
        new_str = Structure(self.shape,iterable=self.iterable)
        
        for _path,_val in self.iteritems():
            new_str[_path] = _val
            
        return new_str
