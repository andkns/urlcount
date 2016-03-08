#!/Users/andkns/python/flasktest/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'andkns'


import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import gzip

from flask import send_from_directory


UPLOAD_FOLDER = '/Users/andkns/urlcount'
ALLOWED_EXTENSIONS = set(['txt', 'gz'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)    # from werkzeug.utils import secure_filename
            filename_dir = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filename_dir)

            result = count(filename_dir)

            #return redirect(url_for('uploaded_file', filename=result)) #  filename 'res.txt'
            return redirect(url_for('showresult', result=result)) # filename 'res.txt'

    return render_template('index.html')






@app.route('/result/<result>')
def showresult(result):

    return send_from_directory(app.config['UPLOAD_FOLDER'], result)
    # result1 = send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    # return render_template("result.html",result=result)


# inputfile - dir+file
# outfile -  file
# return result - массив строк
def count(inputfile):

    # если файл с расширением .gz
    if inputfile.rsplit('.', 1)[1] == 'gz':

        # открываем, распаковываем
        f = gzip.open(inputfile)
        tmp = f.read()

        # меняем расширение у имени входного файла с .gz на .txt
        inputfile = inputfile.rsplit('.', 1)[0]+'.txt'

        # открываем файл с расширением .txt на запись
        # и записываем на диск
        out = open(inputfile,'wb')
        out.write(tmp)

    outfile = 'out.txt'
    checkfile = 'check.txt'

    kns = {}

    f = open(inputfile)
    for line in f:
        # разделяем строки на слова разделенные табуляцией
        words = line.strip().split('\t')
        # приводим все строки в нижний регистр, удаляем https, http, www, разделяем на слова по "/"
        ssylka = words[1].lower().replace('https://','').replace('http://','').replace('www.','').split('/')[0]
        # заполняем словарь  kns[ключ]=значение
        if ssylka not in kns:
            kns[ssylka] = 1
        else:
            kns[ssylka] += 1
    f.close()

    # сортируем словарь по значению, получаем отсортированный кортеж knssorted
    knssorted = sorted(kns.items(), key=lambda x: x[1], reverse=True)

    #for ss in sorted(kns):
    #    g.write(ss + ' ' + str(kns[ss]) + '\n')

    g = open(os.path.join(app.config['UPLOAD_FOLDER'], outfile), 'w')
    for ss in knssorted:
         g.write(ss[0] + ' ' + str(ss[1]) + '\n')
    g.close()

    # читаем файл с с сайтами для подсчета ссылок с них (удаляем www.)
    # и записываем список в chk_words

    c = open(os.path.join(app.config['UPLOAD_FOLDER'], checkfile))
    chk_words = c.read().splitlines()
    chk_words = [sss.replace('www.','') for sss in chk_words]
    c.close()

    #result =[]
    ggg = open(os.path.join(app.config['UPLOAD_FOLDER'], "res.txt"), 'w')
    for ss in chk_words:
         if ss in kns:
            ggg.write(ss + ' --- ' + str(kns[ss]) + '\n')
            #result.append(ss + ' --- ' + str(kns[ss]))
    ggg.close()

    return 'res.txt'
    #return  result

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host='0.0.0.0')


