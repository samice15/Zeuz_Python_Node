import time
import keyboard, autoit, pyautogui
import os, sys
import inspect
from colorama import Fore
from PIL import ImageGrab as ImageGrab_Mac_Win
from PIL import Image, ImageTk
import configparser

new_line = True
import clr, System
import tkinter

screen_title = "ZeuZ Windows Inspector"
os.system("title " + screen_title)
dll_path = os.getcwd().split("Apps")[0] + "Framework" + os.sep + "windows_dll_files" + os.sep
clr.AddReference(dll_path + "UIAutomationClient")
clr.AddReference(dll_path + "UIAutomationTypes")
clr.AddReference(dll_path + "UIAutomationProvider")
clr.AddReference( "System.Windows.Forms")
x, y = -1, -1
path_priority = 0
xml_str = ""
from System.Windows.Automation import *


def ExecLog(sModuleInfo, sDetails, iLogLevel):
    if iLogLevel == 1:
        status = "Passed"
        line_color = Fore.GREEN
    elif iLogLevel == 2:
        status = "Warning"
        line_color = Fore.YELLOW
    elif iLogLevel == 3:
        status = "Error"
        line_color = Fore.RED
    else:
        return
    info = f"{sModuleInfo}\t\n"
    print(line_color + f"{status.upper()} - {info}{sDetails}")

def Exception_Handler(exec_info):
    sModuleInfo_Local = inspect.currentframe().f_code.co_name + " : " + inspect.getmodulename(__file__)
    exc_type, exc_obj, exc_tb = exec_info
    Error_Type = (
        (str(exc_type).replace("type ", ""))
        .replace("<", "")
        .replace(">", "")
        .replace(";", ":")
    )
    Error_Message = str(exc_obj)
    File_Name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    Function_Name = os.path.split(exc_tb.tb_frame.f_code.co_name)[1]
    Line_Number = str(exc_tb.tb_lineno)
    Error_Detail = (
        "Error Type ~ %s: Error Message ~ %s: File Name ~ %s: Function Name ~ %s: Line ~ %s"
        % (Error_Type, Error_Message, File_Name, Function_Name, Line_Number)
    )
    sModuleInfo = Function_Name + ":" + File_Name
    ExecLog(sModuleInfo, "Following exception occurred: %s" % (Error_Detail), 3)

def _found2(Element):
    try:
        left = Element.Left
        right = Element.Right
        bottom = Element.Bottom
        top = Element.Top
        if left <= x <= right and top <= y <= bottom:
            return True
        return False
    except Exception:
        print(sys.exc_info())
        return False

def create_index2(index_trace: dict, element):
    NameE = element.Name
    ClassE = element.ClassName
    AutomationE = element.AutomationId
    LocalizedControlTypeE = element.LocalizedControlType

    s = 'automationid="%s"' % AutomationE
    if s in index_trace: index_trace[s] += 1
    else: index_trace[s] = 0

    s = 'name="%s"' % NameE
    if s in index_trace: index_trace[s] += 1
    else: index_trace[s] = 0

    s = 'name="%s",control="%s"' % (NameE, LocalizedControlTypeE)
    if s in index_trace: index_trace[s] += 1
    else: index_trace[s] = 0

    s = 'class="%s"' % ClassE
    if s in index_trace: index_trace[s] += 1
    else: index_trace[s] = 0

    s = 'name="%s",class="%s"' % (NameE, ClassE)
    if s in index_trace: index_trace[s] += 1
    else: index_trace[s] = 0

def create_path2(index_trace: dict, element):
    NameE = element.Name
    ClassE = element.ClassName
    AutomationE = element.AutomationId
    LocalizedControlTypeE = element.LocalizedControlType

    s_name = 'name="%s"' % NameE
    if NameE and s_name not in index_trace:
        return s_name + ">" + "\n" if new_line else ""
    s_name_control = 'name="%s",control="%s"' % (NameE, LocalizedControlTypeE)
    if NameE and LocalizedControlTypeE and s_name_control not in index_trace:
        return s_name_control + ">" + "\n" if new_line else ""
    s = 'automationid="%s"' % AutomationE
    if AutomationE and s not in index_trace:
        return s + ">" + "\n" if new_line else ""
    s_class = 'class="%s"' % ClassE
    if ClassE and s_class not in index_trace:
        return s_class + ">" + "\n" if new_line else ""
    s = 'name="%s",class="%s"' % (NameE, ClassE)
    if NameE and ClassE and s not in index_trace:
        return s + ">" + "\n" if new_line else ""

    if NameE and s in index_trace:
        return s_name + ">" + ',index="%s">' % (index_trace[s_name] + 1) + "\n" if new_line else ""
    if ClassE and s in index_trace:
        return s_class + ">" + ',index="%s">' % (index_trace[s_class] + 1) + "\n" if new_line else ""

    # if s_name not in index_trace:
    #     return s_name + ">" + "\n" if new_line else ""
    if s_name_control not in index_trace:
        return s_name_control + ">" + "\n" if new_line else ""
    return s_name_control + ',index="%s">' % (index_trace[s_name_control] + 1) + "\n" if new_line else ""


def _child_search2(ParentElement):
    try:
        path = ""
        child_elements = ParentElement.children
        if len(child_elements) == 0:
            return path

        index_trace = {}
        for each_child in child_elements:
            if _found(each_child):
                path += create_path(index_trace, each_child)
                # path += 'name="%s",control="%s",automationid="%s",class="%s">\n' % (NameE, LocalizedControlTypeE, AutomationE, ClassE)
                temp = _child_search(each_child)
                if temp:
                    return path + temp
            create_index(index_trace, each_child)

        return path

    except Exception:
        Exception_Handler(sys.exc_info())
        return ""

class node():
    def __init__(self, element):
        self.Name = element.Current.Name
        self.ClassName = element.Current.ClassName
        self.AutomationId = element.Current.AutomationId
        self.LocalizedControlType = element.Current.LocalizedControlType

        try:
            self.Left = element.Current.BoundingRectangle.Left
            self.Right = element.Current.BoundingRectangle.Right
            self.Bottom = element.Current.BoundingRectangle.Bottom
            self.Top = element.Current.BoundingRectangle.Top
        except:
            self.Left = -1
            self.Right = -1
            self.Bottom = -1
            self.Top = -1

        self.parent = None      # Implement it later
        self.children = []

def copy_tree2(Children, ParentElement):
    try:
        Children.append(node(ParentElement))
        Node = Children[-1]
        child_elements = ParentElement.FindAll(TreeScope.Children, Condition.TrueCondition)
        if child_elements.Count == 0:
            return
        for each_child in child_elements:
            copy_tree(Node.children, each_child)
    except:
        Exception_Handler(sys.exc_info())

global_root = None
def close(e):
    global x,y
    x = e.x
    y = e.y
    global_root.quit()
def showPIL(pilImage):
    root = tkinter.Tk()
    global global_root
    global_root = root
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    print(w,h)
    root.overrideredirect(1)
    root.geometry("%dx%d+0+0" % (w, h))
    root.focus_set()
    # root.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))
    root.bind("<Escape>", close, root)
    root.bind("<ButtonPress>", close, root)

    canvas = tkinter.Canvas(root,width=w,height=h)
    canvas.pack()
    canvas.configure(background='black')
    imgWidth, imgHeight = pilImage.size
    if imgWidth > w or imgHeight > h:
        ratio = min(w/imgWidth, h/imgHeight)
        imgWidth = int(imgWidth*ratio)
        imgHeight = int(imgHeight*ratio)
        pilImage = pilImage.resize((imgWidth,imgHeight), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(pilImage)
    imagesprite = canvas.create_image(w/2,h/2,image=image)
    root.mainloop()

def main2():
    try:
        global x, y
        print("Press enter to inspect")
        # time.sleep(5)
        start = time.time()
        Root = node(AutomationElement.RootElement)
        all_windows = AutomationElement.RootElement.FindAll(TreeScope.Children, Condition.TrueCondition)
        if all_windows.Count == 0:
            return
        print("Enter between 1-%s to select a window" % all_windows.Count)
        for i in range(len(all_windows)):
            print("%s. %s" % (i+1, all_windows[i].Current.Name))
        dur = time.time() - start
        idx = input()
        start = time.time()
        try:
            idx = int(idx.strip())
        except:
            return Exception_Handler(sys.exc_info())
        window = all_windows[idx-1]
        window_name = window.Current.Name
        Root.children.append(node(window))
        all_elements = window.FindAll(TreeScope.Children, Condition.TrueCondition)
        if all_elements.Count != 0:
            for each_child in all_elements:
                copy_tree(Root.children[0].children, each_child)
        print("time taken for copy = %s" % (time.time() - start + dur))
        autoit.win_activate(window_name)
        time.sleep(0.5)
        ImageName = "ss.png"
        image = ImageGrab_Mac_Win.grab()
        autoit.win_activate(screen_title)
        # image.save(ImageName, format="PNG")
        # image = Image.open(ImageName)
        showPIL(image)
        print("tkinter close")
        print("************ YOUR Exact Path *************")
        if x>=0 and y>=0:
            res = _child_search(Root)[:-2] + "\n"
            print(res)
    except:
        Exception_Handler(sys.exc_info())

def _found(Element):
    try:
        left = Element.Current.BoundingRectangle.Left
        right = Element.Current.BoundingRectangle.Right
        bottom = Element.Current.BoundingRectangle.Bottom
        top = Element.Current.BoundingRectangle.Top
        if left <= x <= right and top <= y <= bottom:
            return True
        return False
    except Exception:
        print(sys.exc_info())
        return False

def create_index(index_trace: dict, element):
    NameE = element.Current.Name
    ClassE = element.Current.ClassName
    AutomationE = element.Current.AutomationId
    LocalizedControlTypeE = element.Current.LocalizedControlType

    s = 'automationid="%s"' % AutomationE
    if s in index_trace: index_trace[s] += 1
    else: index_trace[s] = 0

    s = 'name="%s"' % NameE
    if s in index_trace: index_trace[s] += 1
    else: index_trace[s] = 0

    s = 'name="%s",control="%s"' % (NameE, LocalizedControlTypeE)
    if s in index_trace: index_trace[s] += 1
    else: index_trace[s] = 0

    s = 'class="%s"' % ClassE
    if s in index_trace: index_trace[s] += 1
    else: index_trace[s] = 0

    s = 'name="%s",class="%s"' % (NameE, ClassE)
    if s in index_trace: index_trace[s] += 1
    else: index_trace[s] = 0

def create_path(index_trace: dict, element):
    NameE = element.Current.Name
    ClassE = element.Current.ClassName
    AutomationE = element.Current.AutomationId
    LocalizedControlTypeE = element.Current.LocalizedControlType

    s_name = 'name="%s"' % NameE
    if NameE and s_name not in index_trace:
        return s_name + ">" + "\n" if new_line else ""
    s_name_control = 'name="%s",control="%s"' % (NameE, LocalizedControlTypeE)
    if NameE and LocalizedControlTypeE and s_name_control not in index_trace:
        return s_name_control + ">" + "\n" if new_line else ""
    s = 'automationid="%s"' % AutomationE
    if AutomationE and s not in index_trace:
        return s + ">" + "\n" if new_line else ""
    s_class = 'class="%s"' % ClassE
    if ClassE and s_class not in index_trace:
        return s_class + ">" + "\n" if new_line else ""
    s = 'name="%s",class="%s"' % (NameE, ClassE)
    if NameE and ClassE and s not in index_trace:
        return s + ">" + "\n" if new_line else ""

    global path_priority
    path_priority = 2
    if NameE and s in index_trace:
        return s_name + ">" + ',index="%s">' % (index_trace[s_name] + 1) + "\n" if new_line else ""
    if ClassE and s in index_trace:
        return s_class + ">" + ',index="%s">' % (index_trace[s_class] + 1) + "\n" if new_line else ""

    # if s_name not in index_trace:
    #     return s_name + ">" + "\n" if new_line else ""
    if s_name_control not in index_trace:
        return s_name_control + ">" + "\n" if new_line else ""
    return s_name_control + ',index="%s">' % (index_trace[s_name_control] + 1) + "\n" if new_line else ""


element_plugin = False
def _child_search(ParentElement, parenthesis=1):
    try:
        path = ""
        global xml_str, element_plugin
        child_elements = ParentElement.FindAll(TreeScope.Children, Condition.TrueCondition)
        if child_elements.Count == 0:
            return path

        index_trace = {}
        temp = ""
        found = False
        for each_child in child_elements:
            elem_name = each_child.Current.Name.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&apos;").replace(r"\Automation_Solutionz\Zeuz_Node\Public_Node\Zeuz_Python_Node\Apps\W", "xyz")
            elem_automationid = each_child.Current.AutomationId.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&apos;")
            elem_class = each_child.Current.ClassName.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&apos;")
            elem_control = each_child.Current.LocalizedControlType.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&apos;")

            xml_str += "\n" + "  "*parenthesis + '<div Name="%s" AutomationId="%s" ClassName="%s" LocalizedControlType="%s">' % \
            (elem_name, elem_automationid, elem_class, elem_control)
            if _found(each_child) and not found:
                path += create_path(index_trace, each_child)
                found = True
                if not element_plugin:
                    xml_len = len(xml_str)
            if not temp:
                temp = _child_search(each_child, parenthesis+1)
            else:
                _child_search(each_child, parenthesis+1)
            if not found:
                create_index(index_trace, each_child)
            xml_str += "\n" + "  "*parenthesis + "</div>"

        if found and not element_plugin:
            xml_str = xml_str[:xml_len-1] + ' zeuz="aiplugin"' + xml_str[xml_len-1:]
            element_plugin = True
        return path + temp

    except Exception:
        print(sys.exc_info())
        return ""

server = ""
api_key = ""
def Authenticate():
    global server, api_key
    config = configparser.ConfigParser()
    config.read("..\..\Framework\settings.conf")
    try: api_key = config.get("Authentication", "api-key")
    except: api_key = ""
    try: server = config.get("Authentication", "server_address")
    except: server = ""
    while not server or not api_key:
        server = input("Provide Server Address: ")
        api_key = input("Provide API-Key: ")

def main():
    try:
        global x, y, path_priority, element_plugin
        Authenticate()
        print("Hover over the desired element and press control")
        while True:
            keyboard.wait("ctrl")
            x, y = pyautogui.position()
            windows = AutomationElement.RootElement.FindAll(TreeScope.Children, Condition.TrueCondition)
            if windows.Count == 0:
                return
            global xml_str
            for window in windows:
                if _found(window):
                    xml_str += '<body Window="%s">' % window.Current.Name
                    path = create_path({}, window)
                    break
            else:
                ExecLog("No window found in that coordinate")
                return
            path += _child_search(window)[:-2] + "\n"
            xml_str += "\n" + "</body>"

            print("************* xml_str *************")
            print(xml_str)
            print("************* Exact Path *************")
            print(path)
            print("************* path_priority *************")
            print("Path priority =", path_priority, "\n\n")
            with open("xml.xml", "w") as f:
                f.write(xml_str.encode('ascii', 'ignore').decode())     # ignore characters which are not ascii presentable
            print("done writing xml_str")
            xml_str = ""
            path_priority = 0
            element_plugin = False
            break
    except:
        Exception_Handler(sys.exc_info())
        xml_str = ""
        path_priority = 0
        element_plugin = False

if __name__ == "__main__":
    main()
