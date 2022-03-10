from python_get_resolve import GetResolve
resolve = GetResolve()


try:
    project_manager = resolve.GetProjectManager()
    current_project = project_manager.GetCurrentProject()
except:
    print("Davinci is not open yet")



class FunctionsButtonStreamdeck():
    pass

def dummy_function():
    print('test dummy_function')

def dummy_os_mkdir_func():
    import os
    dir = "new_dir"
    if not os.path.exists(dir):
        os.mkdir(dir)

def dummy_function_testing_davinci():
    pass