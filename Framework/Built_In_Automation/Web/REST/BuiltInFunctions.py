
# -*- coding: cp1252 -*-
'''
Created on April 10, 2017

@author: Built_In_Automation Solutionz Inc.
'''

import sys
import os
import requests


sys.path.append("..")

import ast
import time
import inspect
from Framework.Built_In_Automation.Shared_Resources import BuiltInFunctionSharedResources as Shared_Resources

requests.packages.urllib3.disable_warnings()

from Framework.Utilities import CommonUtil

passed_tag_list=['Pass','pass','PASS','PASSED','Passed','passed','true','TRUE','True','1','Success','success','SUCCESS']
failed_tag_list=['Fail','fail','FAIL','Failed','failed','FAILED','false','False','FALSE','0']

'============================= Sequential Action Section Begins=============================='


# Method to get the element step data from the original step_data
def Get_Element_Step_Data(step_data):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    CommonUtil.ExecLog(sModuleInfo, "Function: Get Element Step Data", 1)
    try:
        element_step_data = []
        for each in step_data[0]:
            if (each[1] == "action" or each[1] == "conditional action"):
                #CommonUtil.ExecLog(sModuleInfo, "Not a part of element step data", 2)
                continue
            else:
                element_step_data.append(each)

        return element_step_data

    except Exception:
        return CommonUtil.Exception_Handler(sys.exc_info())


# Handles actions for the sequential logic, based on the input from the mentioned function
def Action_Handler(action_step_data, action_row):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    CommonUtil.ExecLog(sModuleInfo, "Function: Action_Handler", 1)
    try:
        action_name = action_row[0]
        if action_name == "save response":
            fields_to_be_saved = action_row[2]
            result = Get_Response(action_step_data, fields_to_be_saved)
            if result == "failed":
                return "failed"
        elif action_name == "compare variable":
            result = Compare_Variables(action_step_data)
            if result == "failed":
                return "failed"
        elif action_name == "compare list":
            result = Compare_Lists(action_step_data)
            if result == "failed":
                return "failed"
        elif action_name == "sleep":
            result = Sleep(action_step_data)
            if result == "failed":
                return "failed"
        elif action_name == "initialize list":
            result = Shared_Resources.Initialize_List(action_step_data)
            if result == "failed":
                return "failed"
        elif (str(action_name).lower().strip().startswith('insert into list')):
            fields_to_be_saved = action_row[2]
            result = Insert_Into_List(action_step_data, fields_to_be_saved)
            if result == "failed":
                return "failed"
        else:
            CommonUtil.ExecLog(sModuleInfo,"The action you entered is incorrect. Please provide accurate information on the data set(s).",3)
            return "failed"

    except Exception:
        return CommonUtil.Exception_Handler(sys.exc_info())


# Method to get previous response variables

#Validating text from an element given information regarding the expected text
def Compare_Lists(step_data):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    CommonUtil.ExecLog(sModuleInfo, "Function: Compare_Lists", 1)
    try:
        element_step_data = Get_Element_Step_Data(step_data)
        if ((element_step_data == []) or (element_step_data == "failed")):
            return "failed"
        else:
            return Shared_Resources.Compare_Lists(step_data)
    except:
        return CommonUtil.Exception_Handler(sys.exc_info())


#Validating text from an element given information regarding the expected text
def Compare_Variables(step_data):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    CommonUtil.ExecLog(sModuleInfo, "Function: Compare_Variables", 1)
    try:
        element_step_data = Get_Element_Step_Data(step_data)
        if ((element_step_data == []) or (element_step_data == "failed")):
            return "failed"
        else:
            return Shared_Resources.Compare_Variables(step_data)
    except:
        return CommonUtil.Exception_Handler(sys.exc_info())


# Method to return dictonaries from string
def get_value_as_list(data):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    CommonUtil.ExecLog(sModuleInfo, "Function: get value as list", 1)
    try:
        return ast.literal_eval(data)
    except Exception:
        return CommonUtil.Exception_Handler(sys.exc_info())


# Method to save rest call parameters
def save_fields_from_rest_call(result_dict, fields_to_be_saved):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    CommonUtil.ExecLog(sModuleInfo, "Function: save fields from rest call", 1)
    try:
        fields_to_be_saved = fields_to_be_saved.split(",")
        if fields_to_be_saved[0].lower().strip() == 'all':
            for each in result_dict:
                field = each.strip()
                Shared_Resources.Set_Shared_Variables(field,result_dict[field])
            CommonUtil.ExecLog(sModuleInfo, "All response fields are saved", 1)
        elif fields_to_be_saved[0].lower().strip() == 'none':
            CommonUtil.ExecLog(sModuleInfo, "No response fields are saved", 1)
            return
        else:
            which_are_saved = []
            for each in fields_to_be_saved:
                field = each.strip()
                if field in result_dict:
                    which_are_saved.append(field)
                    Shared_Resources.Set_Shared_Variables(field, result_dict[field])

            CommonUtil.ExecLog(sModuleInfo, "%s response fields are saved"%(", ".join(str(x) for x in which_are_saved)),1)

        Shared_Resources.Show_All_Shared_Variables()
    except Exception:
        return CommonUtil.Exception_Handler(sys.exc_info())


def insert_fields_from_rest_call_into_list(result_dict, fields_to_be_saved, list_name):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    CommonUtil.ExecLog(sModuleInfo, "Function: save fields from rest call", 1)
    try:
        fields_to_be_saved = fields_to_be_saved.split(",")
        if fields_to_be_saved[0].lower().strip() == 'all':
            for each in result_dict:
                field = each.strip()
                Shared_Resources.Set_List_Shared_Variables(list_name, field,result_dict[field])
            CommonUtil.ExecLog(sModuleInfo, "All response fields are saved", 1)
        elif fields_to_be_saved[0].lower().strip() == 'none':
            CommonUtil.ExecLog(sModuleInfo, "No response fields are saved", 1)
            return
        else:
            which_are_saved = []
            for each in fields_to_be_saved:
                field = each.strip()
                if field in result_dict:
                    which_are_saved.append(field)
                    Shared_Resources.Set_List_Shared_Variables(list_name, field, result_dict[field])

            CommonUtil.ExecLog(sModuleInfo, "%s response fields are saved"%(", ".join(str(x) for x in which_are_saved)),1)

        Shared_Resources.Show_All_Shared_Variables()
    except Exception:
        return CommonUtil.Exception_Handler(sys.exc_info())


#Inserting a field into a list of shared variables
def Insert_Into_List(step_data, fields_to_be_saved):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    CommonUtil.ExecLog(sModuleInfo, "Function: Insert_Into_List", 1)
    try:
        if len(step_data[0]) == 1: #will have to test #saving direct input string data
            list_name = ''
            key = ''
            value = ''

            for each_step_data_item in step_data[0]:
                if each_step_data_item[1]=="action":
                    full_input_key_value_name = each_step_data_item[2]
                    full_input_action_name = each_step_data_item[0]

            temp_list = full_input_action_name.split(':')
            if len(temp_list) == 1:
                CommonUtil.ExecLog(sModuleInfo,
                                   "The information in the data-set(s) are incorrect. Please provide accurate data set(s) information.",
                                   3)
                return "failed"
            else:
                list_name = str(temp_list[1]).strip()

            temp_list = full_input_key_value_name.split(',')
            if len(temp_list) == 1:
                CommonUtil.ExecLog(sModuleInfo,
                                   "The information in the data-set(s) are incorrect. Please provide accurate data set(s) information.",
                                   3)
                return "failed"
            else:
                key_string = temp_list[0]
                value_string = temp_list[1]

                key = str(key_string).split(':')[1].strip()
                value = str(value_string).split(':')[1].strip()

            result = Shared_Resources.Set_List_Shared_Variables(list_name,key, value)
            if result in failed_tag_list:
                CommonUtil.ExecLog(sModuleInfo, "In list '%s' Value of Variable '%s' could not be saved!!!"%(list_name, key), 3)
                return "failed"
            else:
                Shared_Resources.Show_All_Shared_Variables()
                return "passed"



        else:
            element_step_data = Get_Element_Step_Data(step_data)

            returned_step_data_list = Validate_Step_Data(element_step_data)

            if ((returned_step_data_list == []) or (returned_step_data_list == "failed")):
                return "failed"
            else:
                try:

                    list_name = ''
                    key = ''
                    for each_step_data_item in step_data[0]:
                        if each_step_data_item[1] == "action":
                            key = each_step_data_item[2]
                            full_input_action_name = each_step_data_item[0]

                    # get list name from full input_string

                    temp_list = full_input_action_name.split(':')
                    if len(temp_list) == 1:
                        CommonUtil.ExecLog(sModuleInfo,
                                           "The information in the data-set(s) are incorrect. Please provide accurate data set(s) information.",
                                           3)
                        return "failed"
                    else:
                        list_name = str(temp_list[1]).strip()

                    return_result = handle_rest_call(returned_step_data_list, fields_to_be_saved, True, list_name)



                    return return_result
                except Exception:
                    return CommonUtil.Exception_Handler(sys.exc_info())


    except Exception:
        return CommonUtil.Exception_Handler(sys.exc_info())


# Method to handle rest calls
def handle_rest_call(data, fields_to_be_saved, save_into_list = False, list_name = ""):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    CommonUtil.ExecLog(sModuleInfo, "Function: handle rest call", 1)
    try:
        url = data[0]
        method = data[1]
        body = data[2]
        headers = data[3]
        body = get_value_as_list(body)
        headers = get_value_as_list(headers)

        CommonUtil.ExecLog(sModuleInfo,"Calling %s method"%method,1)
        CommonUtil.ExecLog(sModuleInfo, "URL: %s" % url, 1)
        CommonUtil.ExecLog(sModuleInfo, "body: %s" % body, 1)
        CommonUtil.ExecLog(sModuleInfo, "headers %s" % headers, 1)

        if method.lower().strip() == 'post':
            result = requests.post(url,json=body,headers=headers,verify=False)
        elif method.lower().strip() == 'put':
            result = requests.put(url, json=body, headers=headers, verify=False)
        elif method.lower().strip() == 'get':
            result = requests.get(url, json=body, headers=headers, verify=False)
        else:
            return "failed"
        status_code = int(result.status_code)
        Shared_Resources.Set_Shared_Variables('status_code',result.status_code)
        CommonUtil.ExecLog(sModuleInfo,'Post Call returned status code: %d'%status_code,1)
        if status_code >=400:
            CommonUtil.ExecLog(sModuleInfo,'Post Call Returned Bad Response',3)
            return "failed"
        else:
            CommonUtil.ExecLog(sModuleInfo, 'Post Call Returned Response Successfully', 1)
            CommonUtil.ExecLog(sModuleInfo,"Received Response: %s"%result.json(),1)
            if not save_into_list:
                save_fields_from_rest_call(result.json(), fields_to_be_saved)
            else:
                if list_name == "":
                    CommonUtil.ExecLog(sModuleInfo,"List name not defined!",3)
                    return "failed"
                insert_fields_from_rest_call_into_list(result.json(), fields_to_be_saved, list_name)
            return "passed"
    except Exception:
        return CommonUtil.Exception_Handler(sys.exc_info())


# Method to get responses
def Get_Response(step_data, fields_to_be_saved):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    CommonUtil.ExecLog(sModuleInfo, "Function: Get_Response", 1)
    try:
        element_step_data = Get_Element_Step_Data(step_data)

        returned_step_data_list = Validate_Step_Data(element_step_data)

        if ((returned_step_data_list == []) or (returned_step_data_list == "failed")):
            return "failed"
        else:
            try:
                return_result = handle_rest_call(returned_step_data_list, fields_to_be_saved)
                return return_result
            except Exception:
                return CommonUtil.Exception_Handler(sys.exc_info())
    except Exception:
        return CommonUtil.Exception_Handler(sys.exc_info())



# Method to sleep for a particular duration
def Sleep(step_data):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    CommonUtil.ExecLog(sModuleInfo, "Function: Sleep", 1)
    try:
            tuple = step_data[0][0]
            seconds = int(tuple[2])
            CommonUtil.ExecLog(sModuleInfo, "Sleeping for %s seconds" % seconds, 1)
            time.sleep(seconds)
            return "passed"
            # return result
    except Exception:
        return CommonUtil.Exception_Handler(sys.exc_info())


# Method to return pass or fail for the step outcome
def Step_Result(step_data):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    CommonUtil.ExecLog(sModuleInfo, "Function: Step_Result", 1)
    try:
        if ((len(step_data) != 1) or (1 < len(step_data[0]) >= 5)):
            CommonUtil.ExecLog(sModuleInfo,
                               "The information in the data-set(s) are incorrect. Please provide accurate data set(s) information.",
                               3)
            result = "failed"
        else:
            step_result = step_data[0][0][2]
            if step_result == 'pass':
                result = "passed"
            elif step_result == 'fail':
                result = "failed"

        return result
    except Exception:
        return CommonUtil.Exception_Handler(sys.exc_info())


# Performs a series of action or conditional logical action decisions based on user input
def Sequential_Actions(step_data):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    CommonUtil.ExecLog(sModuleInfo, "Function: Sequential_Actions", 1)
    try:
        for each in step_data:
            logic_row = []
            for row in each:
                # finding what to do for each dataset
                # if len(row)==5 and row[1] != "":     ##modifying the filter for changes to be made in the sub-field of the step data. May remove this part of the if statement
                if row[1] == "element parameter" or row[1] == 'compare':  ##modifying the filter for changes to be made in the sub-field of the step data. May remove this part of the if statement
                    continue

                elif row[1] == "action":
                    CommonUtil.ExecLog(sModuleInfo, "Checking the action to be performed in the action row", 1)
                    if row[0] == 'compare variable':
                        result = Action_Handler([each], row)
                    else:
                        new_data_set = Shared_Resources.Handle_Step_Data_Variables([each])
                        if new_data_set in failed_tag_list:
                            return 'failed'
                        result = Action_Handler(new_data_set, row)
                    if result in failed_tag_list:
                        return "failed"

                elif row[1] == "body" or row[1] == "header" or row[1] == "headers":
                    continue
                elif row[1] == "conditional action":
                    CommonUtil.ExecLog(sModuleInfo,
                                       "Checking the logical conditional action to be performed in the conditional action row",
                                       1)
                    logic_decision = ""
                    logic_row.append(row)
                    if len(logic_row) == 2:
                        # element_step_data = each[0:len(step_data[0])-2:1]
                        new_data_set = Shared_Resources.Handle_Step_Data_Variables([each])
                        if new_data_set in failed_tag_list:
                            return_result = 'failed'

                        return_result = Get_Response(new_data_set, 'all')
                        if return_result == 'failed':
                            logic_decision = "false"
                        else:
                            logic_decision = "true"

                    else:
                        continue

                    for conditional_steps in logic_row:
                        if logic_decision in conditional_steps:
                            print conditional_steps[2]
                            print logic_decision
                            list_of_steps = conditional_steps[2].split(",")
                            for each_item in list_of_steps:
                                data_set_index = int(each_item) - 1
                                cond_result = Sequential_Actions([step_data[data_set_index]])
                                if cond_result == "failed":
                                    return "failed"
                            return "passed"

                else:
                    CommonUtil.ExecLog(sModuleInfo,
                                       "The sub-field information is incorrect. Please provide accurate information on the data set(s).",
                                       3)
                    return "failed"




        return "passed"

    except Exception:
        return CommonUtil.Exception_Handler(sys.exc_info())


'===================== ===x=== Sequential Action Section Ends ===x=== ======================'


'============================= Validation Section Begins =============================='


# Validation of step data passed on by the user
def Validate_Step_Data(step_data):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    CommonUtil.ExecLog(sModuleInfo, "Function: Validate_Step_Data", 1)
    try:
        method = ""
        url = ""
        body = "{"
        headers = "{"
        for each in step_data:
            if each[1].lower().strip() == "element parameter":
                element_parameter = each[0]
                if element_parameter.lower().strip() == 'method':
                    method = each[2]
                elif element_parameter.lower().strip() == 'url':
                    url = each[2]
            elif each[1].lower().strip() == 'body':
                if body == "{":
                       body+="'%s' : '%s'"%(each[0], each[2])
                else:
                       body += ", '%s' : '%s'" % (each[0], each[2])
            elif each[1].lower().strip() == 'header' or each[1].lower().strip() == 'headers':
                if headers == "{":
                   headers+="'%s' : '%s'"%(each[0], each[2])
                else:
                    headers += ", '%s' : '%s'" % (each[0], each[2])

        headers += "}"
        body += "}"


        validated_data = (url, method, body, headers)
        return validated_data
    except Exception:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" + "Error Message: " + str(
            exc_obj) + ";" + "File Name: " + fname + ";" + "Line: " + str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Could not find the new page element requested.  Error: %s" % (Error_Detail), 3)
        return "failed"
