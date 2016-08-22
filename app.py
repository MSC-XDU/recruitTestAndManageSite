# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from flask import Flask,request,make_response,redirect,abort
from flask import render_template
from datetime import datetime,timedelta
import leancloud
from leancloud.errors import LeanCloudError
import os
app = Flask(__name__)

APP_ID = os.environ['LC_APP_ID']
MASTER_KEY = os.environ['LC_APP_MASTER_KEY']

leancloud.init(APP_ID,master_key=MASTER_KEY)

def checkUserWeb(u):
    w = u.get('webpointer')
    if not w:
        W = leancloud.Object.extend('weblog')
        w = W()
        w.set('passNum',0);w.set('3',False);w.set('4',False)
        w.save()
        u.set("webpointer",w)
        u.save()
        return w
    q = leancloud.Query('weblog')
    return q.get(w.id)

def hashconvert(s):
    value = 0
    for i in s:
        value = value * 10 + ord(i)
        value %= 1000000007
    return value


@app.route('/')
def index():
    token = request.cookies.get('token')
    if not token:
        return render_template('login.html',message=[])
    try:
        u = leancloud.User()
        u.become(token)
    except LeanCloudError as e:
        message = ['text-danger',]
        if e.code == 210:
            message.append('用户名/密码 错误')
            return render_template('login.html',message=message)
        if e.code == 211:
            message.append('不存在的用户')
            return render_template('login.html',message=message)
    return redirect('/rockaroll')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return redirect('/')
    u = leancloud.User()
    username = request.form.get('email')
    password = request.form.get('pass')
    try:
        u.login(username,password)
    except LeanCloudError as e:
        message = ['text-danger',]
        if e.code == 210:
            message.append("用户名/密码 错误")
        if e.code == 211:
            message.append("不存在的用户")
        return render_template('login.html',message=message)
    r = redirect('/rockaroll')
    response = make_response(r)
    response.set_cookie('token',value=u._session_token,expires=datetime.now()+timedelta(hours=6))
    return response

@app.route('/rockaroll',methods=['GET','POST'])
def rock():
    token = request.cookies.get('token')
    if not token:
        return redirect('/')
    u = leancloud.User()
    try:
        u.become(token)
    except LeanCloudError as e:
        if e.code == 211:
            return redirect('/')
    u.login()
    email = u.get('email')

    q1 = leancloud.Query('tyLog')
    q2 = leancloud.Query('acmLog')
    q3 = leancloud.Query('appLog')
    q4 = leancloud.Query('gameLog')
    q5 = leancloud.Query('hipsLog')
    ty = {};acm = {};app = {};game={};hips = {}
    langList = ['C','C++','Java']

    try:
        TY = q1.equal_to('email',email).find()[0]
        ty['ty1'] = ty['ty2'] = ty['ty3'] = ty['ty31'] = ty['ty32'] = ty['ty4'] = ty['ty5'] = None
        for i in ty.keys():
            ty[i] = TY.get(i)
    except LeanCloudError:
        pass
    except IndexError:
        pass
    try:
        ACM = q2.equal_to('email',email).find()[0]
        lang = ACM.get('acmlanguage')
        if not lang:
            try:
                langList.remove(lang)
                langList = [lang,]+langList
            except ValueError:
                pass
        acm['acm1'] = acm['acm2'] = acm['acm3'] = None
        for i in acm.keys():
            if ACM.get(i):
                acm[i] = True
    except LeanCloudError:
        # network error
        pass
    except IndexError:
        pass

    try:
        APP = q3.equal_to('email',email).find()[0]
        app['app1'] = app['app2'] = app['app3'] = None
        for i in app.keys():
            app[i] = APP.get(i)
    except LeanCloudError:
        pass
    except IndexError:
        pass
    try:
        GAME = q4.equal_to('email',email).find()[0]
        game['game1'] = game['game2'] = game['game3'] = None
        for i in game.keys():
            game[i] = GAME.get(i)
    except LeanCloudError:
        pass
    except IndexError:
        pass
    try:
        HIPS = q5.equal_to('email',email).find()[0]
        hips['hips1'] = hips['hips2'] = hips['hips3'] = hips['hips4'] = hips['hips5'] = hips['hips21'] = hips['hips22'] = hips['hips51'] = hips['hips52'] =  None
        for i in hips.keys():
            hips[i] = HIPS.get(i)
    except LeanCloudError:
        pass
    except IndexError:
        pass

    return render_template('index.html',ty=ty,acm=acm,langList=langList,app=app,game=game,hips=hips,email=email)

@app.route('/web/<num>',methods=['GET','POST'])
def webtest(num):
    token = request.cookies.get('token')
    if not token:
        return redirect('/')
    u = leancloud.User()
    try:
        u.become(token)
    except LeanCloudError as e:
        if e.code == 211:
            return redirect('/')
    u.login()
    w = checkUserWeb(u)
    schedule = w.get('passNum')
    if request.method == 'GET':
        num = int(num)
        if num == schedule+1 or schedule == 4:
            if num == 1:
                return render_template('web/web1.html',answer=u.id[-6:-2])
            elif num == 2:
                return render_template('web/web2.html',answer=u.id[-4:])
            elif num == 3:
                subtitle = request.args.get('subtitle')
                if subtitle == '2':
                    return render_template('web/web4.html')
                else:
                    return render_template('web/web3.html')
            elif num == 4:
                return render_template('web/web5.html')
        else:
            return redirect('web/%d'%(schedule+1))
    else:
        if num == '1' or num == '2':
            answer = request.form.get('answer')
            if num == '1':
                if u.id[-6:-2] == answer:
                    if schedule != 4:
                        w.set('passNum',1)
                        w.save()
                    return redirect('/web/2')
            if num == '2':
                if u.id[-4:] == answer:
                    if schedule != 4:
                        w.set('passNum',2)
                        w.save()
                    return redirect('/web/3')
        elif num == '3':
                if schedule != 4:
                    w.set('passNum',3)
                    w.save()
                return """nice jobs,now you can go next.""",200
        else:
            try:
                return render_template('web/web%s.html'%num,error=1)
            except:
                abort(404)

@app.route('/submit',methods=['POST'])
def submit():
    token = request.cookies.get('token')
    if not token:
        return redirect('/')
    u = leancloud.User()
    try:
        u.become(token)
    except LeanCloudError as e:
        if e.code == 211:
            return redirect('/')
    u.login()

    tyList = ['ty1','ty2','ty4','ty31','ty32','ty5']
    acmList = ['acm%d'%i for i in range(1,4)]
    appList = ['app%d'%i for i in range(1,4)]
    gameList = ['game%d'%i for i in range(1,4)]
    hipsList = ['hips%d'%i for i in range(1,5)]+['hips21','hips22','hips5']

    # 通用题解决方案
    try:
        TY = leancloud.Query('tyLog')
        ty = TY.equal_to('user',u).find()[0]
    except IndexError:
        TY = leancloud.Object.extend('tyLog')
        ty = TY()
    for t in tyList:
        ty.set(t,request.form.get(t))
    if request.form.get('ty31') and request.form.get('ty32'):
        ty.set('ty3',hashconvert(request.form.get('ty31')) == hashconvert(request.form.get('ty32')))
    ty.set('user',u)
    ty.set('email',u.get('email'))
    ty.save()

    # ACM 解决方案
    try:
        ACM = leancloud.Query('acmLog')
        acm = ACM.equal_to('user',u).find()[0]
    except IndexError:
        ACM = leancloud.Object.extend('acmLog')
        acm = ACM()
    if request.form.get('acmlanguage'):
        acm.set('language',request.form.get('acmlanguage'))
    for a in acmList:
        code = request.files[a].read()
        if code:
            acm.set(a,code)
    acm.set('user',u)
    acm.set('email',u.get('email'))
    acm.save()

    #APP 解决方案
    try:
        APP = leancloud.Query('appLog')
        app = APP.equal_to('user',u).find()[0]
    except IndexError:
        APP = leancloud.Object.extend('appLog')
        app = APP()
    for a in appList:
        if a == 'app2':
            if request.form.get(a) == 'on':
                app.set(a,True)
            else:
                app.set(a,False)
        elif request.form.get(a):
            app.set(a,request.form.get(a))
    app.set('user',u)
    app.set('email',u.get('email'))
    app.save()

    #GAME 解决方案
    try:
        G = leancloud.Query('gameLog')
        g = G.equal_to('user',u).find()[0]
    except IndexError:
        G = leancloud.Object.extend('gameLog')
        g = G()
    if request.form.get(gameList[0]) == 'on':
        g.set('game1',True)
    else:
        g.set('game1',False)
    for i in gameList[1:]:
        if request.form.get(i):
            g.set(i,request.form.get(i))
    g.set('user',u)
    g.set('email',u.get('email'))
    g.save()

    #HIPS 解决方案
    try:
        hips = leancloud.Query('hipsLog')
        h = hips.equal_to('user',u).find()[0]
    except IndexError:
        hips = leancloud.Object.extend('hipsLog')
        h = hips()
    for i in hipsList:
        h.set(i,request.form.get(i))
    h.set('user',u)
    h.set('email',u.get('email'))
    h.save()

    return redirect('/rockaroll')

@app.route('/final',methods=['POST'])
def final():
    token = request.cookies.get('token')
    if not token:
        return """为什么不尝试登陆呢?""",400
    u = leancloud.User()
    try:
        u.become(token)
    except LeanCloudError as e:
        if e.code == 211:
            return redirect('/')
    u.login()
    code = request.args.get('code')
    if code == '2713':
        Q = leancloud.Query('weblog')
        w = Q.get(u.get('webpointer').id)
        w.set('passNum',4)
        w.save()
        return """恭喜你!突破Web所有关卡!\n你可以浏览全部题目\nWeb Mentor 邮箱:a@dlmyb.com""",200
    return """error code""",400

@app.route('/lost',methods=['GET','POST'])
def lost():
    url = request.args.get('redirect')
    if request.method == 'POST':
        email = request.form.get('email')
        try:
            leancloud.User().request_password_reset(email)
        except LeanCloudError as e:
            message = ['text-danger',]
            if e.code == 205:
                message.append('错误的注册邮箱')
                return render_template('lost.html',message=message)
        if url:
            return redirect(url)
        message = ['text-success','申请重置密码成功！请检查你的邮箱...']
        return render_template('login.html',message=message)
    else:
        return render_template('lost.html',message=[],url=url)

if __name__ == '__main__':
    app.run(debug=True)