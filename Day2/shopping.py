print('1.会员','2.非会员')

while True:
    sf = input('请选择身份：')
    if sf == '1':
        while True:
            je = input('请输入消费的金额：')
            if je.isdigit() is True:
                if je >= '200':
                    print('会员消费', je, '元，打折后', int(je) * 0.75, '元')
                    break
                elif '0' <= je < '200':
                    print('会员消费', je, '元，打折后', int(je) * 0.9, '元')
                    break
                else:
                    print('输入有误，请重新输入！')
                    break
            else:
                print('输入有误，请重新输入！')
    elif sf == '2':
        while True:
            je = input('请输入消费的金额：')
            if je.isdigit() is True:
                if je >= '200':
                    print('非会员消费', je, '元，打折后', int(je) * 0.9, '元')
                    break
                elif '0' <= je < '200':
                    print('非会员消费', je, '元，无折扣')
                    break
                else:
                    print('输入有误，请重新输入！')
                    break
            else:
                print('输入有误，请重新输入！')
    else:
        print('输入有误，请重新输入！')

