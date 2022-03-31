# date:2019/9/20

import Service


def Mainframe():
    while True:
        print('*****************')
        print('1.管理员登录')
        print('2.教师登录')
        print('3.学生登录')
        print("*****************")
        op = input('请选择: ')
        if op == '1':
            username = input('请输入账号：')
            password = input('请输入密码: ')
            if Service.Login.login(username, password, 1) == 0:
                print('用户名或密码错误！')
                continue
            adminFrame()
        elif op == '2':
            username = input('请输入账号：')
            password = input('请输入密码: ')
            if Service.Login.login(username, password, 2) == 0:
                print('用户名或密码错误！')
                continue
            teacherFrame(username)

        elif op == '3':
            username = input('请输入账号：')
            password = input('请输入密码: ')
            if Service.Login.login(username, password, 3) == 0:
                print('用户名或密码错误！')
                continue
            stuFrame(username)
        else:
            print("无效重新输入")


def teacherFrame(teacherName):
    while True:
        print('********老师*******')
        print('1.添加学生')
        print('2.录入成绩')
        print('3.查看学生成绩')
        print('4.打印成绩')
        print('0.退出')
        op = input('请选择: ')
        if op == '1':
            Service.Teacher.addStudent(teacherName)
        elif op == '2':
            Service.Teacher.addScore(teacherName)
        elif op == '3':
            Service.Teacher.findScore(teacherName)
        elif op == '4':
            Service.Teacher.printSource(teacherName)
        elif op == '0':
            break
        else:
            print("无效重新输入")


def adminFrame():
    while True:
        print('********管理员*******')
        print('1.添加老师')
        print('2.添加班级')
        print('3.添加课程')
        print('0.退出')
        op = input('请选择: ')
        if op == '1':
            Service.Admin.addTeatcher()
        elif op == '2':
            Service.Admin.addClass()
        elif op == '3':
            Service.Admin.addCourse()
        elif op == '0':
            break
        else:
            print("无效重新输入")


def stuFrame(studentName):
    while True:
        print('********学生端*******')
        print('1.查看个人成绩')
        print('2.个人学分情况')
        print('3.选课')
        print('0.退出')
        op = input('请选择: ')
        if op == '1':
            Service.Student.selScore(studentName)
        elif op == '2':
            Service.Student.count(studentName)
        elif op == '3':
            Service.Student.selectCourse(studentName)
        elif op == '0':
            break
        else:
            print("无效重新输入")


if '__main__' == __name__:
    Mainframe()
