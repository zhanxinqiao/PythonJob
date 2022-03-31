
vote_name=[]
def counter(votes_name):
    count_dict={}
    for i in votes_name:
        if i in count_dict:
            count_dict[i]+=1
        else:
            count_dict[i]=1
    return count_dict

def sort_by_value(votes,n=None):
   print("前三名为：")
   items=votes.items()
   ba=[[v[1],v[0]] for v in items]
   ba.sort(reverse=True)
   if n:
       return ba[:n]
   else:
       return ba

def descrtbe(votes,temp=False):
    sum_votes=sum([v for v in votes.values()])
    if len(votes)==0:
        mean_votes='没有投票，无法计算平均票数'
    else:
        mean_votes=sum_votes/len(votes)
        mean_votes=float('%.2f'%mean_votes)
    if temp is True:
        print('目前总票数为:%s'%str(sum_votes))
    else:
        print('总票数为:%s'%str(sum_votes))
        print('平均票数为:%s'%mean_votes)
    fin=sort_by_value(votes,8)
    for index,i in enumerate(fin):
        if temp is True:
            print('目前投票数第%s名是%s,票数是:%s,占票数的:%.2f%%'%(str(index+1),i[1],str(i[0]),100*i[0]/sum_votes))
        else:
            print('本次投票数第%s名是%s,票数是:%s,占票数的:%.2f%%'%(str(index+1),i[1],str(i[0]),100*i[0]/sum_votes))

def vote(votes):
    votes_name=votes
    vote_name=[]
    while True:
        voting = input("投票给：")
        if voting != 'delete' and voting != 'deleteall':
            if voting in votes_name:
                a = voting
                vote_name.append(voting)
            elif voting in [str(i) for i in range(1, len(votes_name) + 1)]:
                a = int(voting) - 1
                vote_name.append(votes_name[int(voting) - 1])
            else:
                if voting != 'finish':
                    print("该候选人不存在，请给候选人进行投票")
                else:
                    break
            print(vote_name)
        if voting == 'delete':
            if int == type(a):
                vote_name.remove(votes_name[int(a)])
                print("%s删除成功！" %votes_name[int(a)])
            else:
                vote_name.remove(a)
                print("%s删除成功！" %a)

        if voting == 'deleteall':
            vote_name = []
            print("成功清空投票结果！")
    return vote_name

def candidate(votes):
    vote_list=votes
    while True:
        canndidate = input("请输入候选人姓名：")
        if canndidate == 'finish':
            if len(vote_list) != 0:
                break
            else:
                print("请先添加候选人")
        if canndidate == 'delete':
            deli = input("请输入删除人的姓名：")
            vote_list.remove(deli)
            print("%s删除成功"%deli)

        else:
            vote_list.append(canndidate)
            print("添加候选人成功。")
    print(vote_list)
    return vote_list

if __name__=='__main__':
    votes_name = []
    while True:
        print("下面进入投票系统："
              "1.候选人环节"
              "2.投票环节"
              "3.统计环节"
              "4.退出投票"
              )
        c=input("请输入对应操作：")
        if c=='1':
            votes_name=candidate(votes_name)
        if c=='2':
            votes_name=vote(votes_name)
        if c=='3':
            votes_count=counter(votes_name)
            print(votes_count)
            sa=sort_by_value(votes_count,3)
            print(sa)
            descrtbe(votes_count,10)
        if c=='4':
            break