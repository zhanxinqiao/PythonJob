#程序功能：用户登录
#程序分析：管理员登录，普通用户登录
#    判断是否是首次使用，是：初始化，否：用户类型选择
#    管理员 直接登录
#    普通用户 是否需要注册
import re
import os
ptuser_name='普通用户文件夹'
def login(): #程序的入口。判断是否为首次使用这个系统
    biaoz=open('test','r')
    word=biaoz.read()
    biaoz.close()
    if word =='0':
        print('首次启动。')
        change_biaoz()
        init()
        print_login_menu()
        user_select()
    elif word =='1':
        print('欢迎回来！')
        print_login_menu()
        user_select()
    else:
        print('参数错误！')
def change_biaoz(): #改变标志位
    f=open('test','w')
    f.write('1')
    f.close()
def init(): #信息初始化,创建管理员账户，普通用户文件
    f=open('u_root','w') #创建管理员账户文件，并打开
    root={'name':'root','pwd':'123456'} #创建一个字典并保存管理员账户信息
    f.write(str(root))   #写入管理员账户信息
    f.close()
    if not os.path.exists(ptuser_name):
        os.mkdir(ptuser_name)
def print_login_menu(): #输出登录菜单
    print('---------用户选择----------')
    print('1-管理员登录')
    print('2-普通用户登录')
    print('---------------------------')
def user_select(): #用户类型选择
    while True:
        user_type=input('请选择用户类型:')
        if user_type == '1':
            print('管理登录')
            root_login()
            break
        elif user_type == '2':
            print('普通用户登录')
            while True:
                sel = input('是否需要注册？（y/n）：')
                if sel == 'y' or sel == 'Y':
                    print('用户注册')
                    print('用户名规则为：长度为 6-10 个字符、以汉字、字母或下划线开头；')
                    print('密码规则为：长度为 6-10 个字符、必须以字母开头、包含字母、数字、其他字符。')
                    user_regidter()
                    ptuser_login()
                    break
                elif sel == 'n' or sel == 'N':
                    print('用户登录')
                    ptuser_login()
                    break
                else:
                    print('输入有误')
            break
        else:
            print('输入有误，请重新选择！')
def root_login(): #管理员登录
    while True:
        root_name = input('请输入账号名：')
        root_pwd = input('请输入密码：')
        f_root = open('u_root', 'r')
        root = eval(f_root.read())
        f_root.close()
        if root_name == root['name'] and root_pwd == root['pwd']:
            print('登录成功！')
            break
        else:
            print('登陆失败！')

def user_regidter(): #普通用户注册
    while True:
        user_id = input('请输入账号名：')
        if 6 <= len(user_id) <= 10:
            if re.match('[0-9]', user_id):
                print('请以数字、字母、汉字、下划线开头！')
                continue
            elif re.match('[a-zA-Z_\u4e00-\u9fa5]', user_id):
                break
        else:
            print('长度不到6位或超过10位！')
    while True:
        user_pwd = input('请输入密码：')
        if 6 <= len(user_pwd) <= 10:
            if re.match('^[a-zA-Z]', user_pwd):
                if re.search('[0-9]', user_pwd) and re.search('[_]', user_pwd):
                    break
                else:
                    print('密码必须包含字母、数字、下划线！')
                    continue
            else:
                print('请以字母开头！')
                continue
        else:
            print('长度不到6位或超过10位！')
    user = {'u_id': user_id, 'u_pwd': user_pwd}
    user_path = ptuser_name + '/' + user_id
    f_user = open(user_path, 'w')
    f_user.write(str(user))
    f_user.close()

def ptuser_login(): #普通用户登录
    print('-----用户登录-----')
    user_id = input('请输入账号名：')
    user_pwd = input('请输入密码：')
    user_list=os.listdir(ptuser_name)
    if user_id in user_list:
        print('登录中。。。')
        user_path = ptuser_name + '/' + user_id
        f_user = open(user_path)
        if user_pwd==eval(f_user.read())['u_pwd']:
            print('登录成功！')
        else:
            print('登录失败！')
    else:
        print('无此用户，请先注册！')
if __name__ == '__main__':
    login()