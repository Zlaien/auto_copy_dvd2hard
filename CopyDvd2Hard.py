import os  
import win32file  
import shutil  
import time  
import SimpleHTTPServer
import SocketServer
import threading
import inspect
import ctypes
import thread

def _async_raise(tid, exctype):
	tid=ctypes.c_long(tid)
	if not inspect.isclass(exctype):
		exctype=type(exctype)
	res=ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
	if res ==0:
		raise ValueError("invalid thread ID")
	elif res !=1:
		ctypes.pythonapi.PyThreadState_SetAsyncExc(tid,None)
		raise SystemError("PyThreadState_SetAsyncExc failed")
		
def stop_thread(thread):
	#用于强制结束线程
	_async_raise(thread.ident,SystemExit)
	

	
def copy_cd(source,dest):
	try:
		t1=threading.Thread(target=shutil.copytree,args=(source,dest))
		t1.start()
		time.sleep(3)
		while t1.is_alive():
			time.sleep(3)
			if os.system('dir ' + source):
				#如果中途退碟，则强制结束复制线程
				stop_thread(t1)
				return -2;
		return 0;
	except Exception as e:
		print e
		return -1;

def simpleServer(PORT,destDir):
	#http传送文件
	os.chdir(destDir)
	Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
	httpd = SocketServer.TCPServer(("", PORT), Handler)
	httpd.serve_forever()		
		
def copydvd2hard(dstdir='temp'): 
	#目的文件夹名为‘temp’ 
	letters = [l.upper() + ':' for l in 'abcdefghijklmnopqrstuvwxyz']
	cdrom = ''  
	harddrive = '' 
	#判断最后一个光驱为选定光驱，最后一个硬盘为目的硬盘
	for drive in letters:  
		if win32file.GetDriveType(drive) == 3:  
			harddrive = drive  
		if win32file.GetDriveType(drive) == 5:  
			cdrom = drive 
	destDir=harddrive + '/' + dstdir+ '/'
	harddrive = harddrive + '/' + dstdir+ '/' +time.strftime('%Y.%m.%d-%H.%M.%S',time.localtime(time.time()))+ '/'
	# 开启本地端口8000传送文件
	thread.start_new_thread(simpleServer,(8000,destDir))	
	while (True):       
		while os.system('dir ' + cdrom):
			print 'notcopy'
			time.sleep(5)
		copyDir=destDir + time.strftime('%Y.%m.%d-%H.%M.%S',time.localtime(time.time()))+ '/'
		copy_cd(cdrom, copyDir);
		while not os.system('dir ' + cdrom):
			print 'copy finished'
			time.sleep(5)
			
	 
if __name__ == '__main__': 
	copydvd2hard('temp')
      