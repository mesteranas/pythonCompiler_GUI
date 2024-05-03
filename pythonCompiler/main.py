import sys
from custome_errors import *
sys.excepthook = my_excepthook
import update
import gui
import guiTools
from settings import *
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
language.init_translation()
class TermnalBox(qt.QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.setAccessibleName(_("Terminal"))
        self.setReadOnly(True)
    def write(self,text):
        self.appendPlainText(str(text))
class Thread(qt2.QRunnable):
    def __init__(self,code,textEdit):
        super().__init__()
        self.textEdit=textEdit
        self.code=code
    def run(self):
        try:
            sys.stdout=self.textEdit
            exec(self.code)
        except Exception as error:
            self.textEdit.write("error: " + str(error))
        finally:
            sys.stdout=sys.__stdout__
class main (qt.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(app.name + _("version : ") + str(app.version))
        layout=qt.QVBoxLayout()
        self.code=qt.QPlainTextEdit()
        self.code.setAccessibleName(_("code"))
        layout.addWidget(self.code)
        self.run=qt.QPushButton(_("run code"))
        self.run.setDefault(True)
        self.run.setShortcut("f5")
        self.run.clicked.connect(self.on_run)
        layout.addWidget(self.run)
        self.terminal=TermnalBox()
        layout.addWidget(self.terminal)
        self.setting=qt.QPushButton(_("settings"))
        self.setting.setDefault(True)
        self.setting.clicked.connect(lambda: settings(self).exec())
        layout.addWidget(self.setting)
        w=qt.QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)

        mb=self.menuBar()
        openFile=qt1.QAction(_("open file"),self)
        mb.addAction(openFile)
        openFile.setShortcut("ctrl+o")
        openFile.triggered.connect(self.On_open)
        help=mb.addMenu(_("help"))
        helpFile=qt1.QAction(_("help file"),self)
        help.addAction(helpFile)
        helpFile.triggered.connect(lambda:guiTools.HelpFile())
        helpFile.setShortcut("f1")
        cus=help.addMenu(_("contact us"))
        telegram=qt1.QAction("telegram",self)
        cus.addAction(telegram)
        telegram.triggered.connect(lambda:guiTools.OpenLink(self,"https://t.me/mesteranasm"))
        telegramc=qt1.QAction(_("telegram channel"),self)
        cus.addAction(telegramc)
        telegramc.triggered.connect(lambda:guiTools.OpenLink(self,"https://t.me/tprogrammers"))
        githup=qt1.QAction(_("Github"),self)
        cus.addAction(githup)
        githup.triggered.connect(lambda: guiTools.OpenLink(self,"https://Github.com/mesteranas"))
        X=qt1.QAction(_("x"),self)
        cus.addAction(X)
        X.triggered.connect(lambda:guiTools.OpenLink(self,"https://x.com/mesteranasm"))
        email=qt1.QAction(_("email"),self)
        cus.addAction(email)
        email.triggered.connect(lambda: guiTools.sendEmail("anasformohammed@gmail.com","project_type=GUI app={} version={}".format(app.name,app.version),""))
        Github_project=qt1.QAction(_("visite project on Github"),self)
        help.addAction(Github_project)
        Github_project.triggered.connect(lambda:guiTools.OpenLink(self,"https://Github.com/mesteranas/{}".format(settings_handler.appName)))
        Checkupdate=qt1.QAction(_("check for update"),self)
        help.addAction(Checkupdate)
        Checkupdate.triggered.connect(lambda:update.check(self))
        licence=qt1.QAction(_("license"),self)
        help.addAction(licence)
        licence.triggered.connect(lambda: Licence(self))
        donate=qt1.QAction(_("donate"),self)
        help.addAction(donate)
        donate.triggered.connect(lambda:guiTools.OpenLink(self,"https://www.paypal.me/AMohammed231"))
        about=qt1.QAction(_("about"),self)
        help.addAction(about)
        about.triggered.connect(lambda:qt.QMessageBox.information(self,_("about"),_("{} version: {} description: {} developer: {}").format(app.name,str(app.version),app.description,app.creater)))
        self.setMenuBar(mb)
        if settings_handler.get("update","autoCheck")=="True":
            update.check(self,message=False)
    def closeEvent(self, event):
        if settings_handler.get("g","exitDialog")=="True":
            m=guiTools.ExitApp(self)
            m.exec()
            if m:
                event.ignore()
        else:
            self.close()
    def on_run(self):
        self.terminal.clear()
        thread=Thread(self.code.toPlainText(),self.terminal)
        qt2.QThreadPool.globalInstance().start(thread)
        self.terminal.setFocus()
    def On_open(self):
        file=qt.QFileDialog(self)
        file.setDefaultSuffix("py")
        if file.exec()==file.DialogCode.Accepted:
            with open(file.selectedFiles()[0],"r",encoding="utf-8") as data:
                self.code.setPlainText(data.read())
App=qt.QApplication([])
w=main()
w.show()
App.setStyle('fusion')
App.exec()