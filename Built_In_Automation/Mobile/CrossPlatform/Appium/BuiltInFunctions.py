
# Android environment
from appium import webdriver
import os, sys, time, inspect, json
from Utilities import CommonUtil, FileUtilities
from Built_In_Automation.Mobile.Android.adb_calls import adbOptions
from appium.webdriver.common.touch_action import TouchAction
from Built_In_Automation.Mobile.CrossPlatform.Appium import clickinteraction as ci
from Built_In_Automation.Mobile.CrossPlatform.Appium import textinteraction as ti


PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


#if local_run is True, no logging will be recorded to the web server.  Only local print will be displayed
#local_run = True
local_run = False

global APPIUM_DRIVER_LIST
APPIUM_DRIVER_LIST = {}


def getDriversList():
    return APPIUM_DRIVER_LIST


def getDriver(index):
    try:
        return APPIUM_DRIVER_LIST[index]
    except Exception, e:
        return False


def addDriver(position, driver, port):
    try:
        APPIUM_DRIVER_LIST.update({position: {'driver':driver, 'port': port}})
        return True
    except Exception, e:
        return False


def start_selenium_hub(file_location = os.path.join(FileUtilities.get_home_folder(), os.path.join('Desktop', 'selenium-server-standalone-2.43.1.jar'))):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.ExecLog(sModuleInfo, "Starting Selenium Hub", 1, local_run)
        console_run("java -jar %s -role hub" % file_location)
        CommonUtil.ExecLog(sModuleInfo, "Selenium Hub Command given", 1, local_run)
        return True
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" + "Error Message: " + str(
            exc_obj) + ";" + "File Name: " + fname + ";" + "Line: " + str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Unable to Start Selenium Hub: Error:%s" % (Error_Detail), 3, local_run)
        return False

def console_run(run_command):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        os.system("gnome-terminal --working-directory %s -e 'bash -c \"%s ;exec bash\"'" % (FileUtilities.get_home_folder(),run_command))
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" + "Error Message: " + str(
            exc_obj) + ";" + "File Name: " + fname + ";" + "Line: " + str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Unable to run command", 3, local_run)
        return False


def init_config_for_device(port_to_connect, device_index, hub_address='127.0.0.1', hub_port=4444, base_location = os.path.join(FileUtilities.get_home_folder(), os.path.join('Desktop', 'appiumConfig')), **kwargs):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        dictJson={
            "configuration":
                {
                    "nodeTimeout": 120,
                    "port": port_to_connect,
                    "hubPort": hub_port,
                    "proxy": "org.openqa.grid.selenium.proxy.DefaultRemoteProxy",
                    "url": "http://%s:%d/wd/hub"%(hub_address,port_to_connect),
                    "hub": "%s:%d/grid/register"%(hub_address, hub_port),
                    "hubHost": "%s"%(hub_address),
                    "nodePolling": 2000,
                    "registerCycle": 10000,
                    "register": True,
                    "cleanUpCycle": 2000,
                    "timeout": 30000,
                    "maxSession": 1
                }
        }
        dictJson.update({'capabilities':[kwargs]})
        if not os.path.exists(base_location):
            FileUtilities.CreateFolder(base_location)
        file_location = os.path.join(base_location, 'nodeConfig%d.json'%device_index)
        with open(file_location, 'w') as txtfile:
            json.dump(dictJson, txtfile)
        #start appium instance
        set_appium_specific_variable()
        start_appium_instances(port_to_connect, file_location)
        return True
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" + "Error Message: " + str(
            exc_obj) + ";" + "File Name: " + fname + ";" + "Line: " + str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Unable to initiate appium instance for device:%d"%device_index, 3, local_run)
        return False


def set_appium_specific_variable():
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        env_vars = {'PATH': '', 'LD_LIBRARY_PATH': '', 'ANDROID_HOME': '', 'HOME': ''}
        not_set = False

        for var in env_vars.keys():
            env_value = os.getenv(var)

            if env_value:
                env_vars[var] = env_value

            elif not env_value:
                not_set = True

        if not_set:
            os.environ['PATH'] = env_vars['HOME'] + "/.linuxbrew/bin:" + env_vars['PATH']
            env_vars['PATH'] = env_vars['HOME'] + "/.linuxbrew/bin:" + env_vars['PATH']

            os.environ['LD_LIBRARY_PATH'] = env_vars['HOME'] + "/.linuxbrew/lib:" + env_vars['LD_LIBRARY_PATH']
            env_vars['LD_LIBRARY_PATH'] = env_vars['HOME'] + "/.linuxbrew/lib:" + env_vars['LD_LIBRARY_PATH']

            os.environ['ANDROID_HOME'] = os.path.join(FileUtilities.get_home_folder(), "android-sdk-linux")
            env_vars['ANDROID_HOME'] = os.path.join(FileUtilities.get_home_folder(), "android-sdk-linux")

            os.environ['PATH'] = env_vars['PATH'] + ":" + env_vars['ANDROID_HOME'] + "/tools:" + \
                                 env_vars['ANDROID_HOME'] + "/platform-tools"
            env_vars['PATH'] = env_vars['PATH'] + ":" + env_vars['ANDROID_HOME'] + "/tools:" + \
                               env_vars['ANDROID_HOME'] + "/platform-tools"
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" + "Error Message: " + str(
            exc_obj) + ";" + "File Name: " + fname + ";" + "Line: " + str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Unable to set appium variable", 3, local_run)
        return False

def start_appium_instances(port_to_connect, file_location, hub_address = '127.0.0.1' ):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        run_command = "appium -a %s -p %d --nodeconfig %s" % (hub_address, port_to_connect, file_location)
        console_run(run_command)
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" + "Error Message: " + str(
            exc_obj) + ";" + "File Name: " + fname + ";" + "Line: " + str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Unable to start appium instance at port :%d"%port_to_connect, 3, local_run)
        return False


def launch(package_name,activity_name):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
        CommonUtil.ExecLog(sModuleInfo,"Trying to launch the app...",1,local_run)
        
        if 'driver' not in globals():
            # appium driver not initiated.
            outcome = launch_and_start_driver(package_name, activity_name)
            if outcome == "Passed":
                CommonUtil.ExecLog(sModuleInfo,"App is launched",1,local_run)
                return "Passed"
            elif outcome == "failed":
                CommonUtil.ExecLog(sModuleInfo, "App is not launched", 3,local_run)
                return "failed"
        else:
            #driver already initiated.
            CommonUtil.ExecLog(sModuleInfo,"App is launched already.",1,local_run)
            return "Passed"
            """outcome = open()
            if outcome == "Passed":
                CommonUtil.ExecLog(sModuleInfo,"App is launched",1,local_run)
                return outcome
            elif outcome == "failed":
                CommonUtil.ExecLog(sModuleInfo, "App is not launched", 3,local_run)
                return outcome"""
    
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Unable to start WebDriver. %s"%Error_Detail, 3,local_run)
        return "failed"


def launch_and_start_driver(package_name, activity_name):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.ExecLog(sModuleInfo,"Trying to launch the app...",1,local_run)
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        df = adbOptions.get_android_version()
        CommonUtil.ExecLog(sModuleInfo,df,1,local_run)
        #adbOptions.kill_adb_server()
        desired_caps['platformVersion'] = df
        df = adbOptions.get_device_model()
        CommonUtil.ExecLog(sModuleInfo,df,1,local_run)
        #adbOptions.kill_adb_server()

        desired_caps['deviceName'] = df
        desired_caps['appPackage'] = package_name
        desired_caps['appActivity'] = activity_name
        #desired_caps['appPackage'] = 'com.assetscience.androidprodiagnostics'
        #desired_caps['appActivity'] = 'com.assetscience.recell.device.android.prodiagnostics.MainActivity'
        driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        global driver
        CommonUtil.ExecLog(sModuleInfo,"Launched the app successfully.",1,local_run)
        wait(3)
        return "Passed"
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Unable to start WebDriver. %s"%Error_Detail, 3,local_run)
        return "failed"
        
        
def close():
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.ExecLog(sModuleInfo,"Trying to close the app",1,local_run)
        driver.close_app()
        CommonUtil.ExecLog(sModuleInfo,"Closed the app successfully",1,local_run)
        driver.quit()
        return "Passed"
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Unable to close the driver. %s"%Error_Detail, 3,local_run)
        return "failed"
    
    
def install(app_location, app_package, app_activity):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
        CommonUtil.ExecLog(sModuleInfo,"Trying to install the app...",1,local_run)
        
        if 'driver' in globals():
            #driver initiated
            """if driver.is_app_installed(app_package):
                CommonUtil.ExecLog(sModuleInfo,"App is already installed.",1,local_run)
                return "Passed"
            else:
                CommonUtil.ExecLog(sModuleInfo,"App is not installed. Now installing...",1,local_run)"""
            outcome = load(app_location)
            if outcome == "Passed":
                CommonUtil.ExecLog(sModuleInfo,"App is installed.",1,local_run)
                return "Passed"
            elif outcome == "failed":
                CommonUtil.ExecLog(sModuleInfo, "Failed to install the app.", 3,local_run)
                return "failed"
        
        else:
            #driver not initiated
            try:
                #It will try to launch the app as if its already installed
                outcome = launch_and_start_driver(app_package, app_activity)
                if outcome == "Passed":
                    CommonUtil.ExecLog(sModuleInfo,"App is installed already.",1,local_run)
                    return "Passed"
                elif outcome == "failed":
                    CommonUtil.ExecLog(sModuleInfo, "App is not installed. Now trying to install and launch again...", 3,local_run)
                    answer = install_and_start_driver(app_location)
                    if answer == "Passed":
                        CommonUtil.ExecLog(sModuleInfo,"App is installed",1,local_run)
                        return "Passed"
                    elif answer == "failed":
                        CommonUtil.ExecLog(sModuleInfo, "Failed to install the app.", 3,local_run)
                        return "failed"
                    
            except:
                answer = install_and_start_driver(app_location)
                if answer == "Passed":
                    CommonUtil.ExecLog(sModuleInfo,"App is installed.",1,local_run)
                    return "Passed"
                elif answer == "failed":
                    CommonUtil.ExecLog(sModuleInfo, "Failed to install the app.", 3,local_run)
                    return "failed"
                    

    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Unable to start WebDriver. %s"%Error_Detail, 3,local_run)
        return "failed"


def install_and_start_driver(app_location):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.ExecLog(sModuleInfo,"Trying to install and then launch the app...",1,local_run)
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        df = adbOptions.get_android_version()
        CommonUtil.ExecLog(sModuleInfo,df,1,local_run)
        #adbOptions.kill_adb_server()
        desired_caps['platformVersion'] = df
        df = adbOptions.get_device_model()
        CommonUtil.ExecLog(sModuleInfo,df,1,local_run)
        #adbOptions.kill_adb_server()
        desired_caps['deviceName'] = df
        desired_caps['app'] = PATH(app_location)
        driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        global driver
        CommonUtil.ExecLog(sModuleInfo,"Installed and launched the app successfully.",1,local_run)
        time.sleep(10)
        driver.implicitly_wait(5)
        return "Passed"
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Unable to start WebDriver. %s"%Error_Detail, 3,local_run)
        return "failed"


def open():
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.ExecLog(sModuleInfo,"Trying to open the app",1,local_run)
        driver.launch_app()
        CommonUtil.ExecLog(sModuleInfo,"Opened the app successfully",1,local_run)
        return "Passed"
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Unable to open the app. %s"%Error_Detail, 3,local_run)
        return "failed"
    
    
def load(app_location):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.ExecLog(sModuleInfo,"Trying to load the app..",1,local_run)
        #driver.install_app(app_location)
        adbOptions.install_app(app_location)
        CommonUtil.ExecLog(sModuleInfo,"Loaded the app successfully",1,local_run)
        return "Passed"
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Unable to load the app. %s"%Error_Detail, 3,local_run)
        return "failed"
    

def reset():
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.ExecLog(sModuleInfo,"Trying to reset the app...",1,local_run)
        driver.reset()
        wait(5)
        CommonUtil.ExecLog(sModuleInfo,"App is reset successfully",1,local_run)
        return "Passed"
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Unable to reset the app. %s"%Error_Detail, 3,local_run)
        return "failed"
    
    
def go_back():
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.ExecLog(sModuleInfo,"Trying to go back...",1,local_run)
        driver.back()
        CommonUtil.ExecLog(sModuleInfo,"Went back successfully",1,local_run)
        return "Passed"
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Unable to go back. %s"%Error_Detail, 3,local_run)
        return "failed"

    
def wait(_time):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.ExecLog(sModuleInfo,"Starting waiting for %s seconds.."%_time,1,local_run)
        driver.implicitly_wait(_time)
        time.sleep(_time)
        CommonUtil.ExecLog(sModuleInfo,"Waited successfully",1,local_run)
        return "Passed"
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Unable to wait. %s"%Error_Detail, 3,local_run)
        return "failed"

    
def remove(app_package):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.ExecLog(sModuleInfo,"Trying to remove app with package name %s..."%app_package,1,local_run)
        #if driver.is_app_installed(app_package):
            #CommonUtil.ExecLog(sModuleInfo,"App is installed. Now removing...",1,local_run)
        try:
            driver.remove_app(app_package)
            CommonUtil.ExecLog(sModuleInfo,"App is removed successfully.",1,local_run)
            return "Passed"
        except:
            CommonUtil.ExecLog(sModuleInfo, "Unable to remove the app", 3,local_run)
            return "failed"
        """else:   
            CommonUtil.ExecLog(sModuleInfo,"App is not found.",3,local_run)
            return "failed" """
        
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Unable to wait. %s"%Error_Detail, 3,local_run)
        return "failed"


def launch_ios_app():
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.ExecLog(sModuleInfo,"Trying to launch the app...",1,local_run)
        PATH = lambda p: os.path.abspath(
            os.path.join(os.path.dirname(__file__), p)
        )
        desired_caps = {}
        desired_caps['platformName'] = 'iOS'
        desired_caps['platformVersion'] = '7.1.2'
        desired_caps['deviceName'] = 'iPhone 4s'
        desired_caps['app'] = PATH('/Users/user/Documents/workspace/asut/pro-diagnostics-1.28.2.ipa')
        desired_caps['udid'] = '848b6a392f627ff995862ed57ec1f03530deb2b8'
        desired_caps['bundleId'] = 'com.assetscience.canada.prodiagnostics'
        driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        global driver
        CommonUtil.ExecLog(sModuleInfo,"Launched the app successfully.",1,local_run)
        wait(10)
        return "Passed"
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Unable to start WebDriver. %s"%Error_Detail, 3,local_run)
        return "failed"


#################################Generic functions###################################

def Get_Element(element_parameter, element_value, reference_parameter=False, reference_value=False,
                reference_is_parent_or_child=False, get_all_unvalidated_elements=False):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.ExecLog(sModuleInfo, "Starting locating element...", 1, local_run)
        #all_elements = Get_All_Elements(element_parameter,element_value)
        element = Get_Single_Element(element_parameter, element_value)
        #element = Element_Validation(element)
        return element
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" + "Error Message: " + str(
            exc_obj) + ";" + "File Name: " + fname + ";" + "Line: " + str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Could not find your element.  Error: %s" % (Error_Detail), 3, local_run)
        return "failed"


def Click_Element(step_data):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.ExecLog(sModuleInfo, "Trying to click on element...", 1, local_run)
        element_parameter = step_data[0][0][0]
        element_value = step_data[0][0][2]
        if element_parameter == "name":
            result = ci.click_element_by_name(driver, element_value)
        elif element_parameter == "id":
            result = ci.click_element_by_id(driver, element_value)
        elif element_parameter == "accessibility_id":
            result = ci.click_element_by_accessibility_id(driver, element_value)
        elif element_parameter == "class_name":
            result = ci.click_element_by_class_name(driver, element_value)
        elif element_parameter == "xpath":
            result = ci.click_element_by_xpath(driver, element_value)
        elif element_parameter == "android_uiautomator_text":
            result = ci.click_element_by_android_uiautomator_text(driver, element_value)
        elif element_parameter == "android_uiautomator_description":
            result = ci.click_element_by_android_uiautomator_description(driver, element_value)
        elif element_parameter == "ios_uiautomation":
            result = ci.click_element_by_ios_uiautomation(driver, element_value)
        else:
            elem = driver.find_element_by_xpath("//*[@%s='%s']" % (element_parameter, element_value))
            if elem.is_enabled():
                elem.click()
                CommonUtil.ExecLog(sModuleInfo, "Clicked on element successfully", 1, local_run)
                return "Passed"
            else:
                CommonUtil.ExecLog(sModuleInfo, "Unable to click. The element is disabled.", 3, local_run)
                return "failed"

        if result == "Passed":
            CommonUtil.ExecLog(sModuleInfo, "Clicked on element successfully", 1, local_run)
            return "Passed"
        elif result == "failed":
            CommonUtil.ExecLog(sModuleInfo, "Unable to click. The element is disabled.", 3, local_run)
            return "failed"

        """element_data = Validate_Step_Data(step_data)
        elem = Get_Element(element_data[0], element_data[1])
        if elem.is_enabled():
            elem.click()
            CommonUtil.ExecLog(sModuleInfo, "Clicked on element successfully", 1, local_run)
            return "Passed"
        else:
            CommonUtil.ExecLog(sModuleInfo, "Unable to click. The element is disabled.", 3, local_run)
            return "failed" """
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" + "Error Message: " + str(
            exc_obj) + ";" + "File Name: " + fname + ";" + "Line: " + str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Unable to click on the element. %s" % Error_Detail, 3, local_run)
        return "failed"


# Method to enter texts in a text box; step data passed on by the user
def Set_Text(step_data):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    CommonUtil.ExecLog(sModuleInfo, "Inside Enter Text In Text Box function", 1, local_run)
    try:
        CommonUtil.ExecLog(sModuleInfo, "Trying to set text in the textbox...", 1, local_run)
        element_parameter = step_data[0][0][0]
        element_value = step_data[0][0][2]
        text_value = step_data[0][1][2]
        if element_parameter == "name":
            result = ti.set_text_by_name(driver, element_value, text_value)
        elif element_parameter == "id":
            result = ti.set_text_by_id(driver, element_value, text_value)
        elif element_parameter == "accessibility_id":
            result = ti.set_text_by_accessibility_id(driver, element_value, text_value)
        elif element_parameter == "class_name":
            result = ti.set_text_by_class_name(driver, element_value, text_value)
        elif element_parameter == "xpath":
            result = ti.set_text_by_xpath(driver, element_value, text_value)
        elif element_parameter == "android_uiautomator_text":
            result = ti.set_text_by_android_uiautomator_text(driver, element_value, text_value)
        elif element_parameter == "android_uiautomator_description":
            result = ti.set_text_by_android_uiautomator_description(driver, element_value, text_value)
        elif element_parameter == "ios_uiautomation":
            result = ti.set_text_by_ios_uiautomation(driver, element_value, text_value)
        else:
            elem = driver.find_element_by_xpath("//*[@%s='%s']" % (element_parameter, element_value))
            driver.set_value(elem, text_value)
            CommonUtil.ExecLog(sModuleInfo, "Entered text on element successfully", 1, local_run)
            return "Passed"

        if result == "Passed":
            CommonUtil.ExecLog(sModuleInfo, "Clicked on element successfully", 1, local_run)
            return "Passed"
        elif result == "failed":
            CommonUtil.ExecLog(sModuleInfo, "Unable to click. The element is disabled.", 3, local_run)
            return "failed"

    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" + "Error Message: " + str(
            exc_obj) + ";" + "File Name: " + fname + ";" + "Line: " + str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Could not set text.  Error: %s" % (Error_Detail), 3,
                           local_run)
        return "failed"


# Method to enter texts in a text box; step data passed on by the user
def Enter_Text_In_Text_Box(step_data):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    CommonUtil.ExecLog(sModuleInfo, "Inside Enter Text In Text Box function", 1, local_run)
    try:
        # If there are no two separate data-sets, or if the first data-set is not between 1 to 3 items, or if the second data-set doesn't have only 1 item
        if ((len(step_data) != 1) or (1 < len(step_data[0]) >= 5)):  # or (len(step_data[1]) != 1)):
            CommonUtil.ExecLog(sModuleInfo,
                               "The information in the data-set(s) are incorrect. Please provide accurate data set(s) information.",
                               3, local_run)
            return "failed"
        else:
            element_step_data = step_data[0][0:len(step_data[0]) - 1:1]
            returned_step_data_list = Validate_Step_Data(element_step_data)
            # returned_step_data_list = Validate_Step_Data(step_data[0])
            if ((returned_step_data_list == []) or (returned_step_data_list == "failed")):
                return "failed"
            else:
                try:
                    Element = Get_Element(returned_step_data_list[0], returned_step_data_list[1],
                                          returned_step_data_list[2], returned_step_data_list[3],
                                          returned_step_data_list[4])
                    text_value = step_data[0][len(step_data[0]) - 1][2]
                    # text_value = step[1][0][2]
                    # text_value=step_data[1][0][1]
                    Element.click()
                    Element.clear()
                    Element.set_value(text_value)
                    Element.click()
                    CommonUtil.TakeScreenShot(sModuleInfo, local_run)
                    CommonUtil.ExecLog(sModuleInfo, "Successfully set the value of to text to: %s" % text_value,
                                       1, local_run)
                    return "passed"
                except Exception, e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    Error_Detail = (
                    (str(exc_type).replace("type ", "Error Type: ")) + ";" + "Error Message: " + str(
                        exc_obj) + ";" + "File Name: " + fname + ";" + "Line: " + str(exc_tb.tb_lineno))
                    CommonUtil.ExecLog(sModuleInfo,
                                       "Could not select/click your element.  Error: %s" % (Error_Detail), 3,
                                       local_run)
                    return "failed"

    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" + "Error Message: " + str(
            exc_obj) + ";" + "File Name: " + fname + ";" + "Line: " + str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Could not find your element.  Error: %s" % (Error_Detail), 3,
                           local_run)
        return "failed"



    # Method to get the elements based on type - more methods may be added in the future
    # Called by: Get_Elements
def Get_Single_Element(parameter, value, parent=False):
    # http://selenium-python.readthedocs.io/locating-elements.html
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        All_Elements = []
        if parent == False:
            if parameter == "name":
                All_Elements = driver.find_element_by_name(value)
            elif parameter == "id":
                All_Elements = driver.find_element_by_id(value)
            elif parameter == "accessibility_id":
                All_Elements = driver.find_element_by_accessibility_id(value)
            elif parameter == "class_name":
                All_Elements = driver.find_element_by_class_name(value)
            elif parameter == "xpath":
                #All_Elements = driver.find_element_by_xpath(value)
                All_Elements == driver.find_element_by_xpath("//*[@%s='%s']" % (parameter, value))
            elif parameter == "android_uiautomator_text":
                All_Elements == driver.find_element_by_android_uiautomator('new UiSelector().text(' + value + ')')
            elif parameter == "android_uiautomator_description":
                All_Elements == driver.find_element_by_android_uiautomator(
                    'new UiSelector().description(' + value + ')')
            elif parameter == "ios_uiautomation":
                All_Elements == driver.find_element_by_ios_uiautomation('.elements()[0]')
            else:
                All_Elements == driver.find_element_by_xpath("//*[@%s='%s']"%(parameter, value))

        elif parent == True:
            if parameter == "name":
                All_Elements = driver.find_element_by_xpath("//*[@text='%s']" % value)
            elif parameter == "id":
                All_Elements = driver.find_element_by_id(value)
            elif parameter == "accessibility_id":
                All_Elements = driver.find_element_by_accessibility_id(value)
            elif parameter == "class_name":
                All_Elements = driver.find_element_by_class_name(value)
            elif parameter == "xpath":
                #All_Elements = driver.find_element_by_xpath(value)
                All_Elements == driver.find_element_by_xpath("//*[@%s='%s']" % (parameter, value))
            elif parameter == "android_uiautomator_text":
                All_Elements == driver.find_element_by_android_uiautomator('new UiSelector().text(' + value + ')')
            elif parameter == "android_uiautomator_description":
                All_Elements == driver.find_element_by_android_uiautomator(
                    'new UiSelector().description(' + value + ')')
            elif parameter == "ios_uiautomation":
                All_Elements == driver.find_element_by_ios_uiautomation('.elements()[0]')
            else:
                All_Elements == driver.find_element_by_xpath("//*[@%s='%s']"%(parameter,value))

        return All_Elements
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" + "Error Message: " + str(
            exc_obj) + ";" + "File Name: " + fname + ";" + "Line: " + str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Unable to get the element.  Error: %s" % (Error_Detail), 3, local_run)
        return "failed"


# Method to get the elements based on type - more methods may be added in the future
# Called by: Get_Elements
def Get_All_Elements(parameter, value, parent=False):
    # http://selenium-python.readthedocs.io/locating-elements.html
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        All_Elements = []
        if parent == False:
            if parameter == "name":
                All_Elements = driver.find_elements_by_name(value)
            elif parameter == "id":
                All_Elements = driver.find_elements_by_id(value)
            elif parameter == "accessibility_id":
                All_Elements = driver.find_elements_by_accessibility_id(value)
            elif parameter == "class_name":
                All_Elements = driver.find_elements_by_class_name(value)
            elif parameter == "xpath":
                All_Elements = driver.find_elements_by_xpath(value)
            elif parameter == "android_uiautomator_text":
                All_Elements == driver.find_elements_by_android_uiautomator('new UiSelector().text('+value+')')
            elif parameter == "android_uiautomator_description":
                All_Elements == driver.find_elements_by_android_uiautomator('new UiSelector().description('+value+')')
        elif parent == True:
            if parameter == "name":
                All_Elements = driver.find_elements_by_name(value)
            elif parameter == "id":
                All_Elements = driver.find_elements_by_id(value)
            elif parameter == "accessibility_id":
                All_Elements = driver.find_elements_by_accessibility_id(value)
            elif parameter == "class_name":
                All_Elements = driver.find_elements_by_class_name(value)
            elif parameter == "xpath":
                All_Elements = driver.find_elements_by_xpath(value)
            elif parameter == "android_uiautomator_text":
                All_Elements == driver.find_elements_by_android_uiautomator('new UiSelector().text('+value+')')
            elif parameter == "android_uiautomator_description":
                All_Elements == driver.find_elements_by_android_uiautomator('new UiSelector().description('+value+')')

        return All_Elements
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" + "Error Message: " + str(
            exc_obj) + ";" + "File Name: " + fname + ";" + "Line: " + str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Unable to get the element.  Error: %s" % (Error_Detail), 3, local_run)
        return "failed"


#Method to click on element; step data passed on by the user
"""def Click_Element(step_data):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    CommonUtil.ExecLog(sModuleInfo, "Inside Click Element function", 1,local_run)
    try:
        if ((len(step_data) != 1) or (1 < len(step_data[0]) >= 5)):
            CommonUtil.ExecLog(sModuleInfo, "The information in the data-set(s) are incorrect. Please provide accurate data set(s) information.", 3,local_run)
            return "failed"
        else:
            element_step_data = step_data[0][0:len(step_data[0])-1:1]
            returned_step_data_list = Validate_Step_Data(element_step_data)
            if ((returned_step_data_list == []) or (returned_step_data_list == "failed")):
                return "failed"
            else:
                try:
                    Element = Get_Element(returned_step_data_list[0], returned_step_data_list[1], returned_step_data_list[2], returned_step_data_list[3], returned_step_data_list[4])
                    Element.click()
                    CommonUtil.TakeScreenShot(sModuleInfo, local_run)
                    CommonUtil.ExecLog(sModuleInfo, "Successfully clicked the element with given parameters and values", 1,local_run)
                    return "passed"
                except Exception, e:
                    element_attributes = Element.get_attribute('name')
                    CommonUtil.ExecLog(sModuleInfo, "Element Attributes: %s"%(element_attributes),3,local_run)
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
                    CommonUtil.ExecLog(sModuleInfo, "Could not select/click your element.  Error: %s"%(Error_Detail), 3,local_run)
                    return "failed"

    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Could not find/click your element.  Error: %s"%(Error_Detail), 3,local_run)
        return "failed" """


#Validation of step data passed on by the user
def Validate_Step_Data(step_data):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    CommonUtil.ExecLog(sModuleInfo, "Function: Validate_Step_Data", 1,local_run)
    try:
        if (len(step_data)==1):
            element_parameter = step_data[0][0][0]
            element_value = step_data[0][0][2]
            reference_parameter = False
            reference_value = False
            reference_is_parent_or_child = False
        elif (len(step_data)==2):
            element_parameter = step_data[0][0][0]
            element_value = step_data[0][0][2]
            reference_parameter = step_data[0][1][0]
            reference_value = step_data[0][1][2]
            reference_is_parent_or_child = False
        elif (len(step_data)==3):
            element_parameter = step_data[0][0][0]
            element_value = step_data[0][0][2]
            reference_parameter = step_data[0][1][0]
            reference_value = step_data[0][1][2]
            reference_is_parent_or_child = step_data[0][2][2]
        else:
            CommonUtil.ExecLog(sModuleInfo, "Data set incorrect. Please provide accurate data set(s) information.", 3,local_run)
            return "failed"
        validated_data = (element_parameter, element_value, reference_parameter, reference_value, reference_is_parent_or_child)
        return validated_data
    except Exception, e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
            CommonUtil.ExecLog(sModuleInfo, "Could not find the new page element requested.  Error: %s"%(Error_Detail), 3,local_run)
            return "failed"


def Element_Validation(All_Elements_Found):#, index):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        #index = int(index)
        return_element = []
        all_visible_elements = []
        all_invisible_elements = []
        if All_Elements_Found == []:
            CommonUtil.ExecLog(sModuleInfo, "Could not find your element by given parameters and values", 3,local_run)
            return "failed"
        elif len(All_Elements_Found) == 1:
            for each_elem in All_Elements_Found:
                #Case 1: Found only one invisible element - pass with warning
                if each_elem.is_displayed() == False:
                    return_element.append(each_elem)
                    CommonUtil.ExecLog(sModuleInfo, "Found one invisible element by given parameters and values", 2,local_run)
                #Case 2: Found only one visible element - pass
                elif each_elem.is_displayed() == True:
                    return_element.append(each_elem)
                    CommonUtil.ExecLog(sModuleInfo, "Found one visible element by given parameters and values", 1,local_run)
                else:
                    CommonUtil.ExecLog(sModuleInfo, "Could not find element by given parameters and values", 3,local_run)
                    return "failed"
            return return_element[0]

        elif len(All_Elements_Found) > 1:
            CommonUtil.ExecLog(sModuleInfo, "Found more than one element by given parameters and values, validating visible and invisible elements. Total number of elements found: %s"%(len(All_Elements_Found)), 2,local_run)
            for each_elem in All_Elements_Found:
                if each_elem.is_displayed() == True:
                    all_visible_elements.append(each_elem)
                else:
                    all_invisible_elements.append(each_elem)
            #sequential logic - if at least one is_displayed() elements, show that, else allow invisible elements
            if len(all_visible_elements) > 0:
                CommonUtil.ExecLog(sModuleInfo, "Found at least one visible element for given parameters and values, returning the first one or by the index specified", 2,local_run)
                return_element = all_visible_elements
            else:
                CommonUtil.ExecLog(sModuleInfo, "Did not find a visible element, however, invisible elements present", 2,local_run)
                return_element = all_invisible_elements
            return return_element[0]#[index]

        else:
            CommonUtil.ExecLog(sModuleInfo, "Could not find element by given parameters and values", 3,local_run)
            return "failed"

    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Unable to get the element.  Error: %s"%(Error_Detail), 3,local_run)
        return "failed"


# Performs a series of action or logical decisions based on user input
def Sequential_Actions(step_data):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        logic_row = []
        for each in step_data:
            # finding what to do for each dataset
            if each[0][1] == "action":
                result = Action_Handler(each[1], each[0][0])
                if result == [] or result == "failed":
                    return "failed"
            elif each[1][1] == "action":
                result = Action_Handler(each[0], each[1][0])
                if result == [] or result == "failed":
                    return "failed"
            elif each[0][1] == "logic":
                logic_decision = ""
                logic_row.append(each[1])
                if len(logic_row) == 2:
                    element_step_data = each[0:len(step_data[0]) - 2:1]
                    returned_step_data_list = Validate_Step_Data(element_step_data)
                    if(returned_step_data_list == []) or (returned_step_data_list == "failed"):
                        return "failed"
                    else:
                        try:
                            Element = Get_Element(returned_step_data_list[0], returned_step_data_list[1],
                                                  returned_step_data_list[2], returned_step_data_list[3],
                                                  returned_step_data_list[4])
                            if Element == 'failed':
                                logic_decision = "false"
                            else:
                                logic_decision = "true"
                        except Exception, errMsg:
                            errMsg = "Could not find element in the by the criteria..."
                            Exception_Info(sModuleInfo, errMsg)
                else:
                    continue

                for conditional_steps in logic_row:
                    if logic_decision in conditional_steps:
                        print conditional_steps[2]
                        list_of_steps = conditional_steps[2].split(",")
                        for each_item in list_of_steps:
                            data_set_index = int(each_item) - 1
                            Sequential_Actions([step_data[data_set_index]])
                        return "passed"

            else:
                CommonUtil.ExecLog(sModuleInfo,
                                   "The sub-field information is incorrect. Please provide accurate information on the data set(s).",
                                   3, local_run)
                return "failed"
        return "passed"

    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" + "Error Message: " + str(
            exc_obj) + ";" + "File Name: " + fname + ";" + "Line: " + str(exc_tb.tb_lineno))
        print "%s" % Error_Detail
        return "failed"


# Handles actions for the sequential logic, based on the input from the mentioned function
def Action_Handler(action_step_data, action_name):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        if action_name == "click":
            result = Click_Element(action_step_data)
            if result == "failed":
                return "failed"
        elif action_name == "wait":
            result = Wait(action_step_data)
            if result == "failed":
                return "failed"
        elif action_name == "swipe":
            result = Swipe(action_step_data)
            if result == "failed":
                return "failed"
        elif action_name == "tap":
            result = Enter_Text_In_Text_Box(action_step_data)
            if result == "failed":
                return "failed"
        elif action_name == "go_back":
            result = Go_Back(action_step_data)
            if result == "failed":
                return "failed"
        elif (action_name == "validate full text" or action_name == "validate partial text"):
            result = Validate_Text(action_step_data)
            if result == "failed":
                return "failed"
        else:
            CommonUtil.ExecLog(sModuleInfo,
                               "The action you entered is incorrect. Please provide accurate information on the data set(s).",
                               3, local_run)
            return "failed"

    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" + "Error Message: " + str(
            exc_obj) + ";" + "File Name: " + fname + ";" + "Line: " + str(exc_tb.tb_lineno))
        print "%s" % Error_Detail
        return "failed"


def Exception_Info(sModuleInfo, errMsg):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
    CommonUtil.ExecLog(sModuleInfo, errMsg + ".  Error: %s"%(Error_Detail), 3,local_run)
    return "failed"


def Go_Back(step_data):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.ExecLog(sModuleInfo, "Trying to go back...", 1, local_run)
        driver.back()
        CommonUtil.ExecLog(sModuleInfo, "Went back successfully", 1, local_run)
        return "Passed"
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" + "Error Message: " + str(
            exc_obj) + ";" + "File Name: " + fname + ";" + "Line: " + str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Unable to go back. %s" % Error_Detail, 3, local_run)
        return "failed"


def Wait(step_data):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.ExecLog(sModuleInfo, "Starting waiting for %s seconds.." % step_data[2], 1, local_run)
        #function_data = Validate_Step_Data(step_data)
        driver.implicitly_wait(step_data[2])
        time.sleep(step_data[2])
        CommonUtil.ExecLog(sModuleInfo, "Waited successfully", 1, local_run)
        return "Passed"
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" + "Error Message: " + str(
            exc_obj) + ";" + "File Name: " + fname + ";" + "Line: " + str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Unable to wait. %s" % Error_Detail, 3, local_run)
        return "failed"


def Swipe(step_data):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.ExecLog(sModuleInfo, "Starting to swipe the screen...", 1, local_run)
        driver.swipe(100, 500, 100, 100, 800)
        CommonUtil.ExecLog(sModuleInfo, "Swiped the screen successfully", 1, local_run)
        return "Passed"
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" + "Error Message: " + str(
            exc_obj) + ";" + "File Name: " + fname + ";" + "Line: " + str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Unable to swipe. %s" % Error_Detail, 3, local_run)
        return "failed"

def Tap(step_data):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.ExecLog(sModuleInfo, "Starting to tap the...", 1, local_run)
        element_data = Validate_Step_Data(step_data)
        elem = Get_Element(element_data[0], element_data[1])
        if elem.is_enabled():
            action = TouchAction(driver)
            action.tap(elem).perform()
            CommonUtil.ExecLog(sModuleInfo, "Tapped on element successfully", 1, local_run)
            return "Passed"
        else:
            CommonUtil.ExecLog(sModuleInfo, "Unable to tap. The element is disabled.", 3, local_run)
            return "failed"
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" + "Error Message: " + str(
            exc_obj) + ";" + "File Name: " + fname + ";" + "Line: " + str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Unable to tap. %s" % Error_Detail, 3, local_run)
        return "failed"


# Validating text from an element given information regarding the expected text
def Validate_Text(step_data):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    CommonUtil.ExecLog(sModuleInfo, "Function: Compare_Text_Data", 1, local_run)
    try:
        if ((len(step_data) != 1) or (1 < len(step_data[0]) >= 5)):
            CommonUtil.ExecLog(sModuleInfo,
                               "The information in the data-set(s) are incorrect. Please provide accurate data set(s) information.",
                               3, local_run)
            return "failed"
        else:
            expected_text_data = step_data[0][1][2]
            if step_data[0][0][0] == "current_page":
                try:
                    Element = Get_Element('tag', 'html')
                except Exception, e:
                    errMsg = "Could not get element from the current page."
                    Exception_Info(sModuleInfo, errMsg)
            else:
                element_step_data = step_data[0][0:len(step_data[0]) - 1:1]
                returned_step_data_list = Validate_Step_Data(element_step_data)
                if ((returned_step_data_list == []) or (returned_step_data_list == "failed")):
                    return "failed"
                else:
                    try:
                        Element = Get_Element(returned_step_data_list[0], returned_step_data_list[1],
                                              returned_step_data_list[2], returned_step_data_list[3],
                                              returned_step_data_list[4])
                    except Exception, e:
                        errMsg = "Could not get element based on the information provided."
                        Exception_Info(sModuleInfo, errMsg)

            list_of_element_text = Element.text.split('\n')
            visible_list_of_element_text = []
            for each_text_item in list_of_element_text:
                if each_text_item != "":
                    visible_list_of_element_text.append(each_text_item)
            if step_data[0][1][0] == "validate partial text":
                actual_text_data = visible_list_of_element_text
                CommonUtil.ExecLog(sModuleInfo, "Expected Text: " + expected_text_data, 1, local_run)
                CommonUtil.ExecLog(sModuleInfo, "Actual Text: " + str(actual_text_data), 1, local_run)
                if (expected_text_data in each_item for each_item in actual_text_data):
                    CommonUtil.ExecLog(sModuleInfo, "The text has been validated by a partial match.", 1, local_run)
                    return "passed"
                else:
                    CommonUtil.ExecLog(sModuleInfo, "Unable to validate using partial match.", 3, local_run)
                    return "failed"
            if step_data[0][1][0] == "validate full text":
                actual_text_data = visible_list_of_element_text
                CommonUtil.ExecLog(sModuleInfo, "Expected Text: " + expected_text_data, 1, local_run)
                CommonUtil.ExecLog(sModuleInfo, "Actual Text: " + str(actual_text_data), 1, local_run)
                if (expected_text_data in actual_text_data):
                    CommonUtil.ExecLog(sModuleInfo, "The text has been validated by using complete match.", 1,
                                       local_run)
                    return "passed"
                else:
                    CommonUtil.ExecLog(sModuleInfo, "Unable to validate using complete match.", 3, local_run)
                    return "failed"

    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" + "Error Message: " + str(
            exc_obj) + ";" + "File Name: " + fname + ";" + "Line: " + str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Could not compare text as requested.  Error: %s" % (Error_Detail), 3,
                           local_run)
        return "failed"


