import win32serviceutil  
import win32service  
import win32event  
import CopyDvd2Hard  

# copyleft zhou_laien@126.com 
# auto_copy_cd vision 2.0
# 需要安装python2.7和pywin32-221.win_py27   
# 安装命令：
# python main.py install
# 启动命令：
# python main.py start
# 停止服务命令：
# python main.py stop 
# 删除服务命令：
# python main.py remove

      
class auto_copy_service(win32serviceutil.ServiceFramework): 
     
    _svc_name_ = "auto_copy"
    _svc_display_name_ = "auto_copy_Service"
    def __init__(self, args):  
        win32serviceutil.ServiceFramework.__init__(self, args)  
        # Create an event which we will use to wait on.  
        # The "service stop" request will set this event.  
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)  
      
    def SvcStop(self):  
        # Before we do anything, tell the SCM we are starting the stop process.  
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)  
        # And set my event.  
        win32event.SetEvent(self.hWaitStop)  
      
    def SvcDoRun(self):   
        CopyDvd2Hard.copydvd2hard()  
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)  
      
if __name__=='__main__':  
    win32serviceutil.HandleCommandLine(auto_copy_service)
