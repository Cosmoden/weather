import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtChart import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from csv import DictWriter
import sqlite3

num_days = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
backgrounds = {"Облака": "background1.jpg", "Капли дождя": "background2.jpg", "Снег": "background3.jpg"}


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("weather.ui", self)
        self.setWindowTitle("Календарь погоды")
        self.setGeometry(100, 100, 1060, 620)
        self.background = "background1.jpg"
        self.font = QFont("Corbel", 10)

        self.spinBox.setMinimum(-80)
        self.spinBox.setMaximum(80)
        self.spinBox_2.setMinimum(655)
        self.spinBox_2.setMaximum(815)
        self.spinBox_2.setValue(760)
        self.spinBox_3.setMinimum(0)
        self.spinBox_3.setMaximum(1600)

        self.pushButton.clicked.connect(self.save_data)
        self.pushButton_2.clicked.connect(self.view_month_stats)
        self.pushButton_3.clicked.connect(self.view_year_stats)
        self.pushButton_4.clicked.connect(self.change_background)
        self.pushButton_5.clicked.connect(self.change_font)

    def resizeEvent(self, event):
        palette = QPalette()
        img = QImage(self.background)
        scaled = img.scaled(self.size(), Qt.KeepAspectRatioByExpanding, transformMode=Qt.SmoothTransformation)
        palette.setBrush(QPalette.Window, QBrush(scaled))
        self.setPalette(palette)
        self.label.setFont(self.font)
        self.label_2.setFont(self.font)
        self.label_3.setFont(self.font)
        self.label_4.setFont(self.font)
        self.label_5.setFont(self.font)
        self.label_6.setFont(self.font)
        self.radioButton.setFont(self.font)
        self.radioButton_2.setFont(self.font)
        self.radioButton_3.setFont(self.font)
        self.radioButton_4.setFont(self.font)
        self.radioButton_5.setFont(self.font)
        self.radioButton_6.setFont(self.font)
        self.radioButton_7.setFont(self.font)
        self.radioButton_8.setFont(self.font)
        self.pushButton.setFont(self.font)
        self.pushButton_2.setFont(self.font)
        self.pushButton_3.setFont(self.font)
        self.pushButton_4.setFont(self.font)
        self.pushButton_5.setFont(self.font)

    def change_background(self):
        background, ok = QInputDialog.getItem(
            self, "Выбор фона", "Выберите фон",
            ("Облака", "Капли дождя", "Снег"), 1, False)
        if ok:
            self.background = backgrounds[background]
        self.resize(1060, 621)
        self.resize(1060, 620)

    def change_font(self):
        font, ok = QFontDialog.getFont(self.font, self)
        if ok:
            self.font = font
        self.resize(1060, 621)
        self.resize(1060, 620)

    def error(self, message):
        self.label_6.setText(message)
        self.label_6.setStyleSheet("background-color: red")

    def save_data(self):
        self.label_6.setText("")
        self.label_6.setStyleSheet("background-color: transparent")
        c = sqlite3.connect("data.sqlite")
        cur = c.cursor()
        date = self.calendarWidget.selectedDate().day()
        temperature = self.spinBox.value()
        pressure = self.spinBox_2.value()
        precip_amount = self.spinBox_3.value()

        if not self.radioButton.isChecked() \
                and not self.radioButton_2.isChecked() \
                and not self.radioButton_3.isChecked():
            self.error("Не выбрана облачность")
            return
        if self.radioButton.isChecked():
            cloud_type = 1
        elif self.radioButton_2.isChecked():
            cloud_type = 2
        elif self.radioButton_3.isChecked():
            cloud_type = 3

        if not self.radioButton_4.isChecked() \
                and not self.radioButton_5.isChecked() \
                and not self.radioButton_6.isChecked() \
                and not self.radioButton_7.isChecked() \
                and not self.radioButton_8.isChecked():
            self.error("Не выбран тип осадков")
            return
        if self.radioButton_4.isChecked():
            precip_type = 1
        elif self.radioButton_5.isChecked():
            precip_type = 2
        elif self.radioButton_6.isChecked():
            precip_type = 3
        elif self.radioButton_7.isChecked():
            precip_type = 4
        elif self.radioButton_8.isChecked():
            precip_type = 5
        cmd0 = f"""SELECT * 
                  FROM Days
                  WHERE date_number = '{date}' """
        if cur.execute(cmd0).fetchall():
            cmd = f"""UPDATE Days
                      SET temperature = {temperature},
                          atmo_pressure = {pressure},
                          cloud_cover = {cloud_type},
                          precipation_type = {precip_type},
                          precipation_amount = {precip_amount}
                      WHERE date_number = {date} AND month_id = {self.calendarWidget.monthShown()}"""
        else:
            cmd = f"""INSERT INTO Days (date_number, 
                                   temperature, 
                                   atmo_pressure, 
                                   cloud_cover, 
                                   precipation_type, 
                                   precipation_amount, 
                                   month_id)
                     VALUES ({date}, {temperature}, {pressure}, {cloud_type}, 
                     {precip_type}, {precip_amount}, {self.calendarWidget.monthShown()})"""
        cur.execute(cmd)
        c.commit()
        c.close()

    def view_month_stats(self):
        self.statWindow = StatWindow()
        self.current_stat_range = 1
        set1 = QBarSet("")
        c = sqlite3.connect("data.sqlite")
        cur = c.cursor()
        month = self.calendarWidget.monthShown()
        cmd = f"""SELECT precipation_amount 
                 FROM Days
                 WHERE month_id = {month}"""
        precip = cur.execute(cmd).fetchall()
        values1 = []
        for p in precip:
            set1.append(int(p[0]))
            values1.append(int(p[0]))
        series1 = QBarSeries()
        series1.append(set1)
        chart1 = QChart()
        chart1.addSeries(series1)
        x_axis1 = QBarCategoryAxis()
        x_axis1.append([str(i) for i in range(1, num_days[self.calendarWidget.monthShown() - 1] + 1)])
        y_axis1 = QValueAxis()
        y_axis1.setRange(min(set1), max(set1))
        chart1.setAxisX(x_axis1, series1)
        chart1.setAxisY(y_axis1, series1)
        chart1.legend().setVisible(False)
        self.statWindow.graphicsView.setChart(chart1)

        series2 = QLineSeries(self)
        cmd = f"""SELECT date_number, atmo_pressure
                  FROM Days
                  WHERE month_id = {month}"""
        pressure = cur.execute(cmd).fetchall()
        for t in pressure:
            series2.append(t[0], int(t[1]))
        chart2 = QChart()
        chart2.addSeries(series2)
        x_axis2 = QBarCategoryAxis()
        x_axis2.append([str(i) for i in range(1, num_days[self.calendarWidget.monthShown() - 1] + 1)])
        y_axis2 = QValueAxis()
        values2 = [int(i[1]) for i in pressure]
        y_axis2.setRange(min(values2) - 1, max(values2) + 1)
        chart2.setAxisX(x_axis2, series2)
        chart2.setAxisY(y_axis2, series2)
        chart2.legend().setVisible(False)
        self.statWindow.graphicsView_2.setChart(chart2)

        series3 = QSplineSeries(self)
        cmd = f"""SELECT date_number, temperature
                 FROM Days
                 WHERE month_id = {month}"""
        temp = cur.execute(cmd).fetchall()
        for t in temp:
            series3.append(t[0], int(t[1]))
        chart3 = QChart()
        chart3.addSeries(series3)
        x_axis3 = QBarCategoryAxis()
        x_axis3.append([str(i) for i in range(1, num_days[self.calendarWidget.monthShown() - 1] + 1)])
        y_axis3 = QValueAxis()
        values3 = [int(i[1]) for i in temp]
        y_axis3.setRange(min(values3) - 4, max(values3) + 4)
        chart3.setAxisX(x_axis3, series3)
        chart3.setAxisY(y_axis3, series3)
        chart3.legend().setVisible(False)
        self.statWindow.graphicsView_3.setChart(chart3)

        average_temp = str("%.2f" % (sum(values3) / len(values3)))
        average_precip = str("%.2f" % (sum(values1) / len(values1)))
        average_pressure = str("%.2f" % (sum(values2) / len(values2)))
        self.statWindow.label_7.setText(average_temp)
        self.statWindow.label_9.setText(average_precip)
        self.statWindow.label_11.setText(average_pressure)

        min_temp = str(min(values3))
        max_temp = str(max(values3))
        min_precip = str(min(values1))
        max_precip = str(max(values1))
        min_pressure = str(min(values2))
        max_pressure = str(max(values2))
        self.statWindow.label_14.setText(min_temp)
        self.statWindow.label_16.setText(max_temp)
        self.statWindow.label_18.setText(min_precip)
        self.statWindow.label_20.setText(max_precip)
        self.statWindow.label_22.setText(min_pressure)
        self.statWindow.label_24.setText(max_pressure)

        cmd = f"""SELECT *
                 FROM Days
                 WHERE precipation_type = 5 AND month_id = {month}"""
        precip_days = cur.execute(cmd).fetchall()
        precip_count = str(len(precip_days))
        self.statWindow.label_26.setText(precip_count)

        cmd = f"""SELECT *
                 FROM Days
                 WHERE (precipation_type = 1 OR precipation_type = 3) AND month_id = {month}"""
        rainy_days = cur.execute(cmd).fetchall()
        rainy_count = str(len(rainy_days))
        self.statWindow.label_27.setText(rainy_count)

        cmd = f"""SELECT *
                 FROM Days
                 WHERE (precipation_type = 2 OR precipation_type = 3) AND month_id = {month}"""
        snowy_days = cur.execute(cmd).fetchall()
        snowy_count = str(len(snowy_days))
        self.statWindow.label_29.setText(snowy_count)

        cmd = f"""SELECT *
                 FROM Days
                 WHERE precipation_type = 4 AND month_id = {month}"""
        hail_days = cur.execute(cmd).fetchall()
        hail_count = str(len(hail_days))
        self.statWindow.label_31.setText(hail_count)

        self.statWindow.show()

    def view_year_stats(self):
        self.statWindow = StatWindow()
        self.current_stat_range = 2
        set1 = QBarSet("")
        c = sqlite3.connect("data.sqlite")
        cur = c.cursor()
        values1 = []
        for month in range(1, 13):
            cmd = f"""SELECT precipation_amount 
                     FROM Days
                     WHERE month_id = {month}"""
            precip = cur.execute(cmd).fetchall()
            values = []
            for p in precip:
                values.append(int(p[0]))
            set1.append(sum(values) / len(values) if values else 0)
            values1.append(sum(values) / len(values) if values else 0)
        series1 = QBarSeries()
        series1.append(set1)
        chart1 = QChart()
        chart1.addSeries(series1)
        x_axis1 = QBarCategoryAxis()
        x_axis1.append([str(i) for i in range(1, 13)])
        y_axis1 = QValueAxis()
        y_axis1.setRange(min(set1), max(set1))
        chart1.setAxisX(x_axis1, series1)
        chart1.setAxisY(y_axis1, series1)
        chart1.legend().setVisible(False)
        self.statWindow.graphicsView.setChart(chart1)

        series2 = QLineSeries(self)
        values2 = []
        for month in range(1, 13):
            cmd = f"""SELECT atmo_pressure
                     FROM Days
                     WHERE month_id = {month}"""
            temp = cur.execute(cmd).fetchall()
            values = []
            for t in temp:
                values.append(t[0])
            series2.append(month, sum(values) / len(values) if values else 0)
            values2.append(sum(values) / len(values))
        chart2 = QChart()
        chart2.addSeries(series2)
        x_axis2 = QBarCategoryAxis()
        x_axis2.append([str(i) for i in range(1, 13)])
        y_axis2 = QValueAxis()
        y_axis2.setRange(min(values2) - 1, max(values2) + 1)
        chart2.setAxisX(x_axis2, series2)
        chart2.setAxisY(y_axis2, series2)
        chart2.legend().setVisible(False)
        self.statWindow.graphicsView_2.setChart(chart2)

        series3 = QSplineSeries(self)
        values3 = []
        for month in range(1, 13):
            cmd = f"""SELECT temperature
                     FROM Days
                     WHERE month_id = {month}"""
            pressure = cur.execute(cmd).fetchall()
            values = []
            for t in pressure:
                values.append(t[0])
            series3.append(month, sum(values) / len(values) if values else 0)
            values3.append(sum(values) / len(values))
        chart3 = QChart()
        chart3.addSeries(series3)
        x_axis3 = QBarCategoryAxis()
        x_axis3.append([str(i) for i in range(1, 13)])
        y_axis3 = QValueAxis()
        y_axis3.setRange(min(values3) - 4, max(values3) + 4)
        chart3.setAxisX(x_axis3, series3)
        chart3.setAxisY(y_axis3, series3)
        chart3.legend().setVisible(False)
        self.statWindow.graphicsView_3.setChart(chart3)

        average_temp = str("%.2f" % (sum(values3) / len(values3)))
        average_precip = str("%.2f" % (sum(values1) / len(values1)))
        average_pressure = str("%.2f" % (sum(values2) / len(values2)))
        self.statWindow.label_7.setText(average_temp)
        self.statWindow.label_9.setText(average_precip)
        self.statWindow.label_11.setText(average_pressure)
        min_temp = str(min(values3))
        max_temp = str(max(values3))
        min_precip = str(min(values1))
        max_precip = str(max(values1))
        min_pressure = str(min(values2))
        max_pressure = str(max(values2))
        self.statWindow.label_14.setText(min_temp)
        self.statWindow.label_16.setText(max_temp)
        self.statWindow.label_18.setText(min_precip)
        self.statWindow.label_20.setText(max_precip)
        self.statWindow.label_22.setText(min_pressure)
        self.statWindow.label_24.setText(max_pressure)

        cmd = """SELECT * 
                 FROM Days
                 WHERE precipation_type = 5"""
        precip_days = cur.execute(cmd).fetchall()
        precip_count = str(len(precip_days))
        self.statWindow.label_26.setText(precip_count)

        cmd = """SELECT *
                 FROM Days
                 WHERE precipation_type = 1 OR precipation_type = 3"""
        rainy_days = cur.execute(cmd).fetchall()
        rainy_count = str(len(rainy_days))
        self.statWindow.label_27.setText(rainy_count)

        cmd = """SELECT *
                 FROM Days
                 WHERE precipation_type = 2 OR precipation_type = 3"""
        snowy_days = cur.execute(cmd).fetchall()
        snowy_count = str(len(snowy_days))
        self.statWindow.label_29.setText(snowy_count)

        cmd = """SELECT *
                 FROM Days
                 WHERE precipation_type = 4"""
        hail_days = cur.execute(cmd).fetchall()
        hail_count = str(len(hail_days))
        self.statWindow.label_31.setText(hail_count)

        self.statWindow.show()

    def save_file(self):
        dialog = QFileDialog()
        if dialog.exec_():
            filename = dialog.getSaveFileName(self, "Сохранить статистику", "c:\\", "CSV file (*.csv)")[0]
        else:
            return
        c = sqlite3.connect("data.sqlite")
        cur = c.cursor()
        writer = DictWriter(open(filename, 'w', newline=''),
                            fieldnames=['Дата', 'Температура', 'Атмосферное давление', 'Облачность', 'Осадки',
                                        'Количество осадков'], delimiter=';')
        writer.writeheader()
        if self.current_stat_range == 1:
            year = self.calendarWidget.yearShown()
            month = self.calendarWidget.monthShown()
            days = cur.execute(f"""SELECT date_number 
                                  FROM Days
                                  WHERE month_id = {month}""").fetchall()
            for day in [d[0] for d in days]:
                date = f"{day}.{month}.{year}"
                res = cur.execute(f"""SELECT temperature, atmo_pressure, cloud_cover, 
                                      precipation_type, precipation_amount
                                      FROM Days
                                      WHERE date_number = {day} AND month_id = {month} """).fetchall()
                temp, pressure, cloud_cover, precip_type, precip_amount = map(str, res[0])
                cloud_cover = cur.execute(f"""SELECT description
                                              FROM CloudCover
                                              WHERE id = {int(cloud_cover)}""").fetchall()[0][0]
                precip_type = cur.execute(f"""SELECT description
                                              FROM Precipation
                                              WHERE id = {int(precip_type)}""").fetchall()[0][0]
                writer.writerow({"Дата": date,
                                 "Температура": temp,
                                 "Атмосферное давление": pressure,
                                 "Облачность": cloud_cover,
                                 "Осадки": precip_type,
                                 "Количество осадков": precip_amount})
        elif self.current_stat_range == 2:
            dates = cur.execute("""SELECT date_number, month_id 
                                   FROM Days""").fetchall()
            year = self.calendarWidget.yearShown()
            for month in set([d[1] for d in dates]):
                for day in [d[0] for d in dates if d[1] == month]:
                    date = f"{day}.{month}.{year}"
                    res = cur.execute(f"""SELECT temperature, atmo_pressure, cloud_cover, 
                                                 precipation_type, precipation_amount
                                          FROM Days
                                          WHERE date_number = {day} AND month_id = {month}""").fetchall()
                    try:
                        temp, pressure, cloud_cover, precip_type, precip_amount = map(str, res[0])
                    except IndexError:
                        print(date)
                    cloud_cover = cur.execute(f"""SELECT description
                                                  FROM CloudCover
                                                  WHERE id = {int(cloud_cover)}""").fetchall()[0][0]
                    precip_type = cur.execute(f"""SELECT description
                                                  FROM Precipation
                                                  WHERE id = {int(precip_type)}""").fetchall()[0][0]
                    writer.writerow({"Дата": date,
                                     "Температура": temp,
                                     "Атмосферное давление": pressure,
                                     "Облачность": cloud_cover,
                                     "Осадки": precip_type,
                                     "Количество осадков": precip_amount})


class StatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("weather_stat.ui", self)
        self.setWindowTitle("Календарь погоды: статистика")
        self.pushButton.clicked.connect(lambda: MainWindow.save_file(self=ex))

    def resizeEvent(self, event):
        palette = QPalette()
        img = QImage(ex.background)
        scaled = img.scaled(self.size(), Qt.KeepAspectRatioByExpanding, transformMode=Qt.SmoothTransformation)
        palette.setBrush(QPalette.Window, QBrush(scaled))
        self.setPalette(palette)
        self.pushButton.setFont(ex.font)
        self.label.setFont(ex.font)
        self.label_2.setFont(ex.font)
        self.label_3.setFont(ex.font)
        self.label_4.setFont(ex.font)
        self.label_5.setFont(ex.font)
        self.label_6.setFont(ex.font)
        self.label_7.setFont(ex.font)
        self.label_8.setFont(ex.font)
        self.label_9.setFont(ex.font)
        self.label_10.setFont(ex.font)
        self.label_11.setFont(ex.font)
        self.label_12.setFont(ex.font)
        self.label_13.setFont(ex.font)
        self.label_14.setFont(ex.font)
        self.label_15.setFont(ex.font)
        self.label_16.setFont(ex.font)
        self.label_17.setFont(ex.font)
        self.label_18.setFont(ex.font)
        self.label_19.setFont(ex.font)
        self.label_20.setFont(ex.font)
        self.label_21.setFont(ex.font)
        self.label_22.setFont(ex.font)
        self.label_23.setFont(ex.font)
        self.label_24.setFont(ex.font)
        self.label_25.setFont(ex.font)
        self.label_26.setFont(ex.font)
        self.label_27.setFont(ex.font)
        self.label_28.setFont(ex.font)
        self.label_29.setFont(ex.font)
        self.label_30.setFont(ex.font)
        self.label_31.setFont(ex.font)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
