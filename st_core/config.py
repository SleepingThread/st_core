"""
Example of usage:
    conf_parser = ConfigurationParser()
    conf_parser.add_parameter(("a",12))
    conf_parser.add_parameter(("b",15))

    d = {'a':18,'b':19}
    f = open('test.json','w')
    f.write(json.dumps(d))
    f.close()

    conf = conf_parser.read_parameters("test.json")
"""

import copy
import json

    
class Configuration(object):
    
    def __init__(self,param_dict,allow_set_undefined = False):
        self.__dict__["param_dict"] = copy.deepcopy(param_dict)
        self.__dict__["allow_set_undefined"] = allow_set_undefined
        return
        
    def __getattr__(self,name):
        if name in self.__dict__:
            return self.__dict__[name]
        elif name in self.param_dict:
            return self.param_dict[name]
        else:
            raise Exception("No such parameter: '"+name+"' in configuration!")
            
        return

    def __setattr__(self,name,value):
        if name in self.__dict__:
            self.__dict__[name] = value
        elif name in self.param_dict:
            self.param_dict[name] = value
        else:
            if self.allow_set_undefined:
                self.__dict__[name] = value
            else:
                raise Exception("Trying to set undefined attribute! allow_set_undefined = False")
            
        return
    
    def __getitem__(self,name):
        if name in self.param_dict:
            return self.param_dict[name]
        else:
            raise Exception("No such parameter: '"+name+"' in configuration!")
            
        return

    def __setitem__(self,name,value):
        self.param_dict[name] = value
        return


class ConfigurationParser(object):
    def __init__(self,rule_replace=False):
        # dict of all available parameters in configuration
        self.param_dict = {}
        # dict of input parameters ( from <config file> )
        self.input_dict = {}
        # dict of default parameters ()
        self.default_dict = {}
        
        # list of rule functions
        self.rules = []
        self.rule_replace = rule_replace
        return
    
    def add_parameter(self,param):
        self.param_dict[param[0]] = None
        
        if len(param)>1:
            self.default_dict[param[0]] = param[1]
        return
        
    def add_parameters(self,param_list):
        for param in param_list:
            self.add_parameter(param)
        return
    
    def add_rule(self,rule_func):
        self.rules.append(rule_func)
        return
    
    def read_parameters(self,conf_filename):
        """
            Create operation to merge dict or 
                use existing
            merge(default,input) - 
                like "setdefault" but for dicts
        """
        # read params from JSON conf_filename
        self.input_dict = json.load(open(conf_filename,'r'))
        if not isinstance(self.input_dict,dict):
            raise Exception("JSON file: '"+conf_filename+"' must store dict")
       
        # check input_dict if there are unknown parameters
        _input_dict_set = set(self.input_dict.keys())
        _param_dict_set = set(self.param_dict.keys())
        _undefined_params = list(_input_dict_set-_param_dict_set)
        if len(_undefined_params)>0:
            raise Exception("There are undefined params in configuration .json file: "+str(_undefined_params))

        # merge param_dict, input_dict, default_dict 
        result_dict = {}
        for param in self.param_dict:
            if param in self.input_dict:
                result_dict[param] = self.input_dict[param]
            elif param in self.default_dict:
                result_dict[param] = self.default_dict[param]
            else:
                raise Exception("No default value for parameter '"+param+"'. Set it.")
        
        # apply rules to result_dict, create rule_dict
        rule_dict = {}
        for ind, rule in enumerate(self.rules):
            _rule_result = {}
            if not rule(result_dict,_rule_result):
                raise Exception("Rule No. "+str(ind)+" error")
                
            # apply _rule_result to rule_dict
            for param in _rule_result:
                if param in rule_dict:
                    if self.rule_replace:
                        rule_dict[param] = _rule_result[param]
                    else:
                        raise Exception("Rule No. "+str(ind)+" make replacement of parameter '"+param+"'")
                else:
                    rule_dict[param] = rule_result[param]
        
        # apply rule_dict to result_dict
        for param in result_dict:
            if param in rule_dict:
                result_dict[param] = rule_dict[param]
        
        return Configuration(result_dict)
