import time
from pywinauto.application import Application
from pywinauto.keyboard import send_keys
import configparser
import os
import subprocess


def getsettings (section, value):
	return config.get(section, value)


def isFrontolStarted():
	try:
		time.sleep(3)  # debug only
		app = Application(backend='uia').connect(path=getsettings('namespace', 'FrontolPath'))
		return app
	except:
		return 0


config = configparser.ConfigParser()
config.read(os.path.dirname(os.path.realpath(__file__)) + "\inifrexit.ini")
ExitKey = getsettings('namespace', 'ExitKey')
ApplicationTitle = getsettings('namespace', 'ApplicationTitle')
app = isFrontolStarted()


def sendkey_app (keysend):
	send_keys(keysend)


def pressbutton(dlg, button):
	dlg = app.top_window()
	app.dlg.control
	dlg.child_window(title=button, control_type="Button").click()


def getCurrentWindow():
	sendkey_app(ExitKey)
	if app.window(found_index=1, title_re=ApplicationTitle).exists():
		sendkey_app(ExitKey)
		time.sleep(2)
		return "MainWindow"
	elif app.window(title_re=ApplicationTitle).exists():
		return "MainWindow"
	elif app.window(title='Супервизор').exists():
		return "Supervisor"
	elif app.window(title='Авторизация доступа').exists():
		return 'Autorization'


def exitFromMainWindow():
	if app.window(title_re=ApplicationTitle).exists():
		send_keys(getsettings('namespace', 'LogOutKey'))
		dlg = app
		dlg = app.top_window()
		app.dlg.control
		dlg.child_window(title="Да", control_type="Button").click()


def exitFromAutorization():
	dlg = app.window(title_re='Авторизация доступа').wait('visible', timeout=30, retry_interval=1)
	dlg = app.top_window()
	dlg.child_window(control_type="ComboBox").expand()
	dlg.child_window(control_type="ComboBox").click_input()
	dlg.child_window(control_type="ComboBox").select(getsettings('namespace', 'ExitUser'))
	dlg.child_window(control_type="Edit").click_input()
	dlg.child_window(control_type="Edit").set_edit_text(getsettings('namespace', 'ExitUserPassword'))
	pressbutton(dlg, 'ОК')
	time.sleep(2)
	sendkey_app(getsettings('namespace', 'KeyExitOS'))
	pressbutton(dlg, 'Да')


def exitFromSupervisor():
	dlg = app.window(title='Супервизор')
	dlg = app.top_window()
	sendkey_app(getsettings('namespace', 'LogOutKey'))
	time.sleep(2)
	pressbutton(dlg, 'Да')
	time.sleep(2)


def main():

	if app != 0:
		currentWindow = getCurrentWindow()
	if currentWindow == 'Autorization':
		exitFromAutorization()
	elif currentWindow == 'Supervisor':
		exitFromSupervisor()
		exitFromAutorization()
	elif currentWindow == 'MainWindow':
		exitFromMainWindow()
		exitFromAutorization()

	if getsettings('namespace', 'RunExternalScript') == '1':
		if isFrontolStarted() == 0:
			subprocess.Popen(getsettings('namespace', 'ExternalScriptPath'), stdout=subprocess.PIPE).communicate()


if __name__ == '__main__':
	main()
