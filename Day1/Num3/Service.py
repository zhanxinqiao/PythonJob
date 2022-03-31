# date:2019/9/20
import pymysql

import Utils


class Login:

    @staticmethod
    def login(username, passwrod, role):
        conn = Utils.SqlUtils.getConn()
        cursor = conn.cursor()
        sql = 'select * from user where name=%s and password=%s and role=%s'
        res = cursor.execute(sql, (username, passwrod, role))
        return res


#### 管理员添加老师
class Admin:
    @staticmethod
    def addTeatcher():
        list = []
        conn = Utils.SqlUtils.getConn()
        cursor = conn.cursor()
        while True:
            teacherName = input("请输入老师名字：")
            teacherSex = input('请输入老师性别:')
            teacherPasswd = input('请输入教师登录密码:')
            list.append((teacherName, teacherSex, teacherPasswd, 2))
            op = input("是否继续输入Y/y? ")
            if op != 'Y' or op != 'y':
                break
        sql = 'insert into user (name,sex,password,role)values (%s,%s,%s,%s)'
        res = cursor.executemany(sql, list)
        if res >= 1:
            print("添加老师成功!")
            conn.commit()
            Utils.SqlUtils.close(cursor, conn)

    ### 管理员添加课程
    @staticmethod
    def addCourse():
        list = []
        conn = Utils.SqlUtils.getConn()
        cursor = conn.cursor()
        while True:
            courseName = input('请输入课程名字：')
            courseScore = input('请输入课程学分：')
            courTeacher = input('请输入任课老师: ')
            sql = 'select userid from user where name = %s and role = 2'
            res = cursor.execute(sql, courTeacher)
            if res == 0:
                print('该老师不存在请重新输入！')
                continue

            list.append((courseName, courseScore, cursor.fetchone()[0]))

            op = input("是否继续添加Y/y? ")
            if op != 'Y' and op != 'y':
                break

        sql = 'insert into course (coursename,coursescore,teacher)values (%s,%s,%s)'
        res = cursor.executemany(sql, list)
        if res >= 1:
            print('添课程成功！')
            conn.commit()
            Utils.SqlUtils.close(cursor, conn)

    ##管理员添加班级
    @staticmethod
    def addClass():
        list = []
        conn = Utils.SqlUtils.getConn()
        cursor = conn.cursor()
        while True:
            className = input('请输入班级名字：')
            classTeacher = input('请输入班主任: ')
            sql = 'select userid from user where name = %s and role = 2'
            res = cursor.execute(sql, classTeacher)
            if res == 0:
                print('该老师不存在请重新输入！')
                continue

            list.append((className, cursor.fetchone()[0]))

            op = input("是否继续添加Y/y? ")
            if op != 'Y' and op != 'y':
                break

        sql = 'insert into classes (classname,classteacher)values (%s,%s)'
        res = cursor.executemany(sql, list)
        if res >= 1:
            print('添课班级成功！')
            conn.commit()
            Utils.SqlUtils.close(cursor, conn)


class Teacher:

    # 根据老师名字查找班级
    # @staticmethod
    # def findClassIdByTeacherName(teacherName):
    #     conn = Utils.SqlUtils.getConn()
    #     cursor = conn.cursor()
    #     sql ='select classid from  classes , user where user.name=%s and user.userid=classes.classteacher'
    #     res = cursor.execute(sql,teacherName)
    #     Utils.SqlUtils.close(cursor,conn)
    #     if res!=0:
    #         return  cursor.fetchone()[0]
    #     else: return 0

    # 根据班级查学生
    @staticmethod
    def findStudentByClass(classid):
        conn = Utils.SqlUtils.getConn()
        cursor = conn.cursor()
        sql = 'select studentid from  student where studentclass=%s'
        res = cursor.execute(sql, classid)
        Utils.SqlUtils.close(cursor, conn)
        if res != 0:
            return cursor.fetchall()
        else:
            return 0

    @staticmethod
    def findCourseByTeahcerName(teahcerName):
        conn = Utils.SqlUtils.getConn()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        sql = 'select courseid,coursename from course,user where user.userid=course.teacher and user.name=%s'
        res = cursor.execute(sql, teahcerName)
        Utils.SqlUtils.close(cursor, conn)
        if res != 0:
            return cursor.fetchall()
        else:
            return 0

    # 添加学生
    @staticmethod
    def addStudent(teachername):
        conn = Utils.SqlUtils.getConn()
        cursor = conn.cursor()
        while True:
            stuName = input("请输入学生名字：")
            stuSex = input('请输入学生性别:')
            stuPasswd = input('请输入学生登录密码:')

            sqlUser = 'insert into user (name,sex,password,role)values (%s,%s,%s,%s)'  # 往user表中插入学生
            res1 = cursor.execute(sqlUser, (stuName, stuSex, stuPasswd, 3))
            studentid = cursor.lastrowid  # user表中stu的id
            sqlstu = 'insert into student (studentid,studentclass)values (%s,%s)'  # 往stu表中插入
            classid = Teacher.findClassIdByTeacherName(teachername)  # 班级id
            res2 = cursor.execute(sqlstu, (studentid, classid))

            if res1 >= 1 and res2 >= 1:
                print("添加学生成功!")

            op = input("是否继续添加Y/y? ")
            if op != 'Y' and op != 'y':
                break

        conn.commit()
        Utils.SqlUtils.close(cursor, conn)

    # # 选课
    #     @staticmethod
    #     def selectCourse(teachername):
    #         conn = Utils.SqlUtils.getConn()
    #         cursor = conn.cursor()
    #         classid = Teacher.findClassIdByTeacherName(teachername)  # 该老师带的班级id
    #         student = Teacher.findStudentByClass(classid)#该班级的所有学生
    #         while True:
    #             courseName = input("请输入要选的课程: ")
    #             sqlCourse = 'select courseid from course where coursename=%s'
    #             res = cursor.execute(sqlCourse,courseName)
    #             if res==0:
    #                 print("课程名不存在，请重新输入！")
    #                 continue
    #             courseid = cursor.fetchone()[0]  # 要选的课程id
    #             for stuItem in student:  #为该班的所有学生选课
    #                 sqlSelCourse = 'insert into socre (userid,courseid ,score)values (%s,%s,%s)'
    #                 res = cursor.execute(sqlSelCourse,(stuItem,courseid,0))
    #                 if res>=1:
    #                     conn.commit()
    #             op = input("选课完成！是否继续添加Y/y? ")
    #             if op != 'Y' and op != 'y':
    #                 break
    #         Utils.SqlUtils.close(cursor,conn)

    # 给成绩
    @staticmethod
    def addScore(teachername):
        course = Teacher.findCourseByTeahcerName(teachername)  # 该老师带的所有课程
        conn = Utils.SqlUtils.getConn()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        for item in course:  # 该老师带的一门课
            sql = 'select user.name,user.userid from user,socre where user.userid=socre.userid and socre.courseid=%s'
            res = cursor.execute(sql, item['courseid'])
            if res != 0:
                student = cursor.fetchall()  # 这门课的所有学生
                for stu in student:  # 一个学生
                    score = input('%s的%s成绩为：' % (stu['name'], item['coursename']))
                    sql = 'update socre SET score=%s where userid=%s and courseid=%s'
                    res = cursor.execute(sql, (score, stu['userid'], item['courseid']))
                    if res >= 1:
                        conn.commit()
        Utils.SqlUtils.close(cursor, conn)
        print("成绩录入成功")

    # 任课老师查看学生成绩
    @staticmethod
    def findScore(teachername):
        course = Teacher.findCourseByTeahcerName(teachername)  # 该老师带的所有课程
        conn = Utils.SqlUtils.getConn()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        print('***********************')
        for item in course:  # 该老师带的一门课
            sql = 'select user.name,socre.score  from user,socre where user.userid=socre.userid and socre.courseid=%s'
            res = cursor.execute(sql, item['courseid'])
            if res != 0:
                student = cursor.fetchall()  # 这门课的所有学生
                for stu in student:  # 一个学生
                    print('%s的%s成绩为：%s' % (stu['name'], item['coursename'], stu['score']))
        print("*******************")
        Utils.SqlUtils.close(cursor, conn)

    @staticmethod
    def printSource(teacherName):
        conn = Utils.SqlUtils.getConn()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        file = open('Source.csv', mode='w', encoding='utf-8')
        file.write("姓名\t课程名\t成绩\n")
        sql = '''select distinct name,a.coursename,score 
                from user,socre,course,  
                (select courseid,coursename  
                 from course 
                 where course.teacher=(select user.userid from user where name=%s)) as a 
                where a.courseid=socre.courseid 
                and socre.userid=user.userid'''
        res = cursor.execute(sql, teacherName)
        if res!=0:
            lists=cursor.fetchall()
            for list in lists:
                print(list)
                file.write(list['name']+"\t"+list['coursename']+"\t"+str(list['score'])+"\n")
        file.close()


class Student:

    @staticmethod  #
    def selScore(studentname):
        conn = Utils.SqlUtils.getConn()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        sql = 'SELECT user.name,socre.score,course.coursename from user,socre ,course where user.userid=socre.userid and user.name =%s and course.courseid = socre.courseid'
        res = cursor.execute(sql, studentname)
        if res > 0:
            scores = cursor.fetchall()
            print('*******%s 的成绩如下*******' % studentname)
            for item in scores:
                print('%s的成绩为：%s' % (item['coursename'], item['score']))
        print("*******************")
        Utils.SqlUtils.close(cursor, conn)

    @staticmethod
    def count(studentname):
        conn = Utils.SqlUtils.getConn()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        sql = 'SELECT sum(course.coursescore) as score from user,socre ,course where user.userid=socre.userid and user.name =%s and course.courseid = socre.courseid and socre.score>=60'
        res = cursor.execute(sql, studentname)
        if res > 0:
            scores = cursor.fetchone()
            print('*******%s 的累计学分为%s分*******' % (studentname, scores['score']))
        sql = 'SELECT user.name,socre.score,course.coursename from user,socre ,course where user.userid=socre.userid and user.name =%s and course.courseid = socre.courseid and socre.score<=60 ;'
        res = cursor.execute(sql, studentname)
        if res > 0:
            print('*******%s未通过的课程如下********' % studentname)
            nopass = cursor.fetchall()
            for item in nopass:
                print('%s的成绩为：%s' % (item['coursename'], item['score']))
        Utils.SqlUtils.close(cursor, conn)

        # 选课

    @staticmethod
    def selectCourse(studentName):
        conn = Utils.SqlUtils.getConn()
        cursor = conn.cursor()
        # classid = Teacher.findClassIdByTeacherName(studentName)  # 该老师带的班级id
        # student = Teacher.findStudentByClass(classid)  # 该班级的所有学生
        while True:
            courseName = input("请输入要选的课程: ")
            sqlCourse = 'select courseid from course where coursename=%s'
            res = cursor.execute(sqlCourse, courseName)
            if res == 0:
                print("课程名不存在，请重新输入！")
                continue
            courseid = cursor.fetchone()[0]  # 要选的课程id
            sqlstuid = 'select userid from user where name=%s'
            rr = cursor.execute(sqlstuid, studentName)
            if rr == 0:
                print("用户不存在，请重新输入！")
                continue
            userid = cursor.fetchone()[0]  # 要选的课程id
            sqlSelCourse = 'insert into socre (userid,courseid ,score)values (%s,%s,%s)'
            res = cursor.execute(sqlSelCourse, (userid, courseid, 0))
            if res >= 1:
                conn.commit()
            op = input("选课完成！是否继续添加Y/y? ")
            if op != 'Y' and op != 'y':
                break
        Utils.SqlUtils.close(cursor, conn)


if '__main__' == __name__:
    print(Login.login('stu1', 'stu1', 3))
