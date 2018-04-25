from PyQt5 import QtWidgets
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QMessageBox, QDesktopWidget
from asteval import Interpreter

from calculator_window import Ui_MainWindow
from converter import *


def swap_widgets(win, ui, target):
    stack = ui.stackedWidget
    if target == 'calc':
        stack.setCurrentIndex(0)
        win.setMinimumSize(380, 286)
        win.resize(380, 286)
    else:
        stack.setCurrentIndex(1)
        win.setMinimumSize(600, 286)
        win.resize(600, 286)


def connect_calc(win: Ui_MainWindow):
    display = win.le_calc_in
    reg_ex = QRegExp('[\d+\.\d+|\d+\+,\-,\*,\/]+\d+|sqrt\(\d+\)')
    display.setValidator(QRegExpValidator(reg_ex, display))

    def update_display(symbol=None):
        content = display.text()

        if len(content) != 0 and symbol == 'sqrt(x)':
            display.setText('sqrt({0})'.format(content))
        elif len(content) != 0 and symbol == '(x+y)':
            display.setText('({0})'.format(content))
        elif symbol:
            display.setText(content + symbol)
        else:
            display.clear()

    def exec_calc():
        if len(display.text()) != 0:
            a_eval = Interpreter()
            res = str(a_eval(display.text()))

            if len(a_eval.error) > 0:
                err = a_eval.error[0].get_error()
                err_box = QMessageBox()
                err_box.setWindowTitle('Evaluation Error')
                err_box.setText('An {0} occurred. Pleas check below for details.'.format(err[0]))
                err_box.setIcon(QMessageBox.Critical)
                err_list = [str(e.get_error()[1]).strip() + '\n' for e in a_eval.error]
                err_box.setDetailedText(' '.join(err_list))
                err_box.show()
                display.setStyleSheet('background-color: rgba(200, 0, 0, .25);')
                display.setFocus()
            else:
                display.setStyleSheet('background-color: rgb(255, 255, 255);')
                display.setText(res)

    win.btn_zero.pressed.connect(lambda: update_display('0'))
    win.btn_one.pressed.connect(lambda: update_display('1'))
    win.btn_two.pressed.connect(lambda: update_display('2'))
    win.btn_three.pressed.connect(lambda: update_display('3'))
    win.btn_four.pressed.connect(lambda: update_display('4'))
    win.btn_five.pressed.connect(lambda: update_display('5'))
    win.btn_six.pressed.connect(lambda: update_display('6'))
    win.btn_seven.pressed.connect(lambda: update_display('7'))
    win.btn_eigth.pressed.connect(lambda: update_display('8'))
    win.btn_nine.pressed.connect(lambda: update_display('9'))

    win.btn_comma.pressed.connect(lambda: update_display('.'))
    win.btn_div.pressed.connect(lambda: update_display('/'))
    win.btn_mult.pressed.connect(lambda: update_display('*'))
    win.btn_sub.pressed.connect(lambda: update_display('-'))
    win.btn_add.pressed.connect(lambda: update_display('+'))
    win.btn_pow.pressed.connect(lambda: update_display('**'))
    win.btn_sqrt.pressed.connect(lambda: update_display('sqrt(x)'))
    win.btn_brackets.pressed.connect(lambda: update_display('(x+y)'))
    win.btn_ac.pressed.connect(lambda: update_display())
    win.btn_equals.pressed.connect(exec_calc)


def connect_conv(win: Ui_MainWindow):
    curr_conv = CurrencyConverter()
    dist_conv = DistanceConverter()
    speed_conv = SpeedConverter()

    curr_a, curr_b = win.cmb_curr_a, win.cmb_curr_b
    curr_av, curr_bv = win.le_curr_a, win.le_curr_b
    dist_a, dist_b = win.cmb_dist_a, win.cmb_dist_b
    dist_av, dist_bv = win.le_dist_a, win.le_dist_b
    speed_a, speed_b = win.cmb_speed_a, win.cmb_speed_b
    speed_av, speed_bv = win.le_speed_a, win.le_speed_b
    currencies = list(
        ['{0}, {1} ({2})'.format(k.ljust(4), v['Country'], v['Symbol']) for k, v in
         curr_conv.get_supported().items()]
    )
    distances = list(['{0} ({1})'.format(k.ljust(4), v['Name'])
                      for k, v in dist_conv.get_supported().items()])
    speeds = list(['{0} ({1})'.format(k.ljust(4), v['Name'])
                   for k, v in speed_conv.get_supported().items()])

    curr_a.addItems(currencies)
    curr_a.setCurrentIndex(0)
    curr_b.addItems(currencies)
    curr_b.setCurrentIndex(1)

    dist_a.addItems(distances)
    dist_a.setCurrentIndex(0)
    dist_b.addItems(distances)
    dist_b.setCurrentIndex(1)

    speed_a.addItems(speeds)
    speed_a.setCurrentIndex(0)
    speed_b.addItems(speeds)
    speed_b.setCurrentIndex(1)

    def ltr_convert(cmb_a, cmb_b, le_a, le_b, converter: ConverterBase):
        unit_a = cmb_a.currentText().split(' ', 1)[0]
        unit_b = cmb_b.currentText().split(' ', 1)[0]
        try:
            value = float(le_a.text())
            le_b.setText(str(round(converter.convert(unit_a, unit_b, value), 4)))
        except ValueError as e:
            print(e)

    def rtl_convert(cmb_a, cmb_b, le_a, le_b, converter: ConverterBase):
        unit_a = cmb_a.currentText().split(' ', 1)[0]
        unit_b = cmb_b.currentText().split(' ', 1)[0]
        try:
            value = float(le_b.text())
            le_a.setText(str(round(converter.convert(unit_b, unit_a, value), 4)))
        except ValueError as e:
            print(e)

    def l_curr_cmb_ch(converter: ConverterBase):
        unit_a = curr_a.currentText()[0:3]
        unit_b = curr_b.currentText()[0:3]
        try:
            win.le_exchange.setText(str(round(converter.conversion_rate(unit_a, unit_b), 4)))
        except ValueError:
            pass

    def r_curr_cmb_ch(converter: ConverterBase):
        unit_a = curr_a.currentText()[0:3]
        unit_b = curr_b.currentText()[0:3]
        try:
            win.le_exchange.setText(str(round(converter.conversion_rate(unit_b, unit_a), 4)))
        except ValueError:
            pass

    l_curr_cmb_ch(curr_conv)
    curr_a.currentIndexChanged.connect(lambda e: l_curr_cmb_ch(curr_conv))
    curr_b.currentIndexChanged.connect(lambda e: r_curr_cmb_ch(curr_conv))
    curr_av.textEdited.connect(lambda e: ltr_convert(curr_a, curr_b, curr_av, curr_bv, curr_conv))
    curr_bv.textEdited.connect(lambda e: rtl_convert(curr_a, curr_b, curr_av, curr_bv, curr_conv))
    win.btn_convert.pressed.connect(lambda: ltr_convert(curr_a, curr_b, curr_av, curr_bv, curr_conv))
    win.btn_refresh.pressed.connect(lambda: curr_conv.try_update_exchange())

    dist_a.currentIndexChanged.connect(lambda e: ltr_convert(dist_a, dist_b, dist_av, dist_bv, dist_conv))
    dist_b.currentIndexChanged.connect(lambda e: ltr_convert(dist_a, dist_b, dist_av, dist_bv, dist_conv))
    dist_av.textEdited.connect(lambda e: ltr_convert(dist_a, dist_b, dist_av, dist_bv, dist_conv))
    dist_bv.textEdited.connect(lambda e: rtl_convert(dist_a, dist_b, dist_av, dist_bv, dist_conv))

    speed_a.currentIndexChanged.connect(lambda e: ltr_convert(speed_a, speed_b, speed_av, speed_bv, speed_conv))
    speed_b.currentIndexChanged.connect(lambda e: ltr_convert(speed_a, speed_b, speed_av, speed_bv, speed_conv))
    speed_av.textEdited.connect(lambda e: ltr_convert(speed_a, speed_b, speed_av, speed_bv, speed_conv))
    speed_bv.textEdited.connect(lambda e: rtl_convert(speed_a, speed_b, speed_av, speed_bv, speed_conv))


def move_center(win):
    frm_gm = win.frameGeometry()
    center_point = QDesktopWidget().availableGeometry().center()
    frm_gm.moveCenter(center_point)
    win.move(frm_gm.topLeft())


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    ui.actionCalculator.triggered.connect(
        lambda e: swap_widgets(MainWindow, ui, 'calc'))
    ui.actionConverter.triggered.connect(
        lambda e: swap_widgets(MainWindow, ui, 'conv'))
    connect_calc(ui)
    connect_conv(ui)

    MainWindow.setMinimumSize(380, 286)
    MainWindow.resize(380, 286)
    move_center(MainWindow)

    MainWindow.show()
    sys.exit(app.exec_())
