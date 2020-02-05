from pandas.io.json._normalize import nested_to_record
import copy
import pandas as pd
class Looper:
    def __init__(self,function,args_dictionary,sep=':'):
        """
        given an input function and a dictionary of arguments, generates a flattened dictionary
        and uses this to generate an output dictionary of results.
        """
        self.function = function
        self.args_dictionary = copy.deepcopy(args_dictionary)
        self.sep = sep
        self.flattened_dict = nested_to_record(self.args_dictionary,sep=self.sep)

    def update_dictionary(self,flattened_key,value):
        """
        update the real dictionary with a flattened key.
        """
        _update_looper(self.args_dictionary,flattened_key,value,self.sep)
        self.flattened_dict = nested_to_record(self.args_dictionary,sep=self.sep)

    def get_value(self,flatten = False):
        res = self.function(self.args_dictionary)
        if flatten ==True:
            res = nested_to_record(res,sep=self.sep)
        return res

    def get_inputs(self):
        return self.flattened_dict

    def get_variables(self):
        return self.flattened_dict.keys()

    def run(self,panda_deps):
        """
        given a dataframe with columns which correspond to the dictionary variables will populate a results dataframe.
        """
        results_overall=[]
        for index,row in panda_deps.iterrows():
            for key in panda_deps:
                if key in self.flattened_dict:
                    self.update_dictionary(key,row[key])   #updates the variables dictionary if match found
            result_dict = self.function(self.args_dictionary)

            if type(result_dict) != dict:
                flatten_results = {'results':result_dict}
            else:
                flatten_results = nested_to_record(result_dict,sep=self.sep)

            save_dict  = self.flattened_dict.copy()   #copy the flattened dict as a row in the results dataframe
            save_dict.update(flatten_results)
            results_overall.append(save_dict)

        plot_data = pd.DataFrame(results_overall)
        return plot_data
def _update_looper(dictionary,flattened_key,value,sep):
    """
    updates the dictionary.
    """
    split = flattened_key.split(sep)
    depth = len(split)
    entry = dictionary
    for d in range(depth-1):
        entry = entry[split[d]]
    entry[split[-1]] = value
