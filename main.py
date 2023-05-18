from flask import Flask, render_template, request, redirect, session

from datetime import date
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = "abz"
app.config['UPLOAD_FOLDER '] = "static/Student_img"

main = None


@app.route('/')
def home():
    session['student_login'] = "logout"
    session['only_student_login'] = "logout"
    session['only_laibrary_login'] = "logout"
    session['st_id'] = "bal"
    return render_template('Home_page.html')


@app.route('/login')
def login():
    valu = session['only_student_login']
    valu2 = session['only_laibrary_login']
    if valu != "logout":
        return redirect('/student_index')
    elif valu2 != "logout":
        return redirect('/index_l')
    else:
        return render_template('login.html')


@app.route('/logout_lib', methods=['POST', 'GET'])
def logout():
    session['Email'] = 1
    session['only_student_login'] = "logout"
    session['only_student_login'] = "logout"
    session['student_login'] = "logout"
    return render_template('login.html')


@app.route('/logindo', methods=['POST', 'GET'])
def logindo():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="university_project"
    )
    mycursor = mydb.cursor()
    if request.method == 'POST':
        result = request.form
        error = None
        email = request.form.get('email')
        password = request.form.get('stpass')

        session['email'] = email

        mycursor.execute("select * from student_table where Email ='" + email + "' and pass='" + password + "'")
        Emaildata = mycursor.fetchall()
        if len(Emaildata) > 0:
            session['student_login'] = email
            session['only_student_login'] = 1
            x = email
            session['only_laibrary_login'] = "logout"
            mycursor.execute('')
            mydb.commit()
            mycursor.close()
            return redirect('/student_index')
        else:
            error = "Email or Password Incorrect "
            return render_template('login.html', error=error)


@app.route('/loginl', methods=['POST', 'GET'])
def loginl():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="university_project"
    )
    mycursor = mydb.cursor()
    if request.method == 'POST':
        result = request.form
        error = None
        email = request.form.get('lemail')
        password = request.form.get('lpass')
        mycursor.execute("select * from l_table where Email='" + email + "' and pass='" + password + "'")
        Emaildata = mycursor.fetchall()
        session['Email'] = email

        if len(Emaildata) > 0:
            mycursor.execute("select * from l_table where Email='" + email + "'")
            user_data = mycursor.fetchone()
            userid = user_data[7]
            session['user_ID'] = userid
            session['only_laibrary_login'] = 1
            session['student_login'] = "logout"
            mydb.commit()
            mycursor.close()
            return redirect('index_l')

        else:
            error = "Email or Password Incorrect "
            return render_template('login.html', error=error)


@app.route('/signup')
def signup():
    valu = session['only_student_login']
    valu2 = session['only_laibrary_login']
    return render_template('registration.html', valu=valu, valu2=valu2)


@app.route('/signupdo', methods=['POST', 'GET'])
def signupdo():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="university_project"
    )
    mycursor = mydb.cursor()
    if request.method == 'POST':
        result = request.form
        error = None
        sname = request.form['sname']
        slname = request.form['slname']
        semail = request.form['semail']
        sid = request.form['sid']
        sphn = request.form['sphn']
        spass = request.form['spass']
        scpass = request.form['scpass']
        sb_day = request.form['sbd']
        sphoto = request.files['sphoto']
        sbt = request.form['sbt']
        sdp = request.form['sdp']

        if sphoto == '':
            er = "Import Your Image"
            return render_template('registration.html', er=er)
        else:
            filep = os.path.join(app.config['UPLOAD_FOLDER '], '1CE' + sphoto.filename)
            sphoto.save(filep)
            photoname = '1CE' + sphoto.filename

        mycursor.execute("""SELECT * FROM `student_table`  WHERE `Email` LIKE '{}' """
                         .format(semail))
        Emaildata = mycursor.fetchall()

        mycursor.execute("select * from student_table where st_id ='" + sid + "'")
        studentid = mycursor.fetchall()

        if len(Emaildata) > 0:
            error = "Email  Already  Used"
            return render_template('registration.html', error=error)
        if len(studentid) > 0:
            studenterror = "This Id is already added"
            return render_template('registration.html', studenterror=studenterror)

        elif spass != scpass:
            errorr = "Password Not Match , Try agin"
            return render_template('registration.html', errorr=errorr)
        elif len(spass) < 8:
            errorr = "password at least 8 characters"
            return render_template('registration.html', errorr=errorr)
        else:
            mycursor.execute(
                "insert into student_table (Fstname,Sndname,Email,st_id,phone,pass,birth_day,photo,Batch,Depertment)value(%s,%s,%s,%s,"
                "%s,%s,%s,%s,%s,%s)",
                (sname, slname, semail, sid, sphn, spass, sb_day, photoname, sbt, sdp))
            mydb.commit()
            mycursor.close()
            return redirect('login')


@app.route('/singnupl', methods=['POST', 'GET'])
def signupl():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="university_project"
    )
    mycursor = mydb.cursor()
    if request.method == 'POST':
        sname = request.form['lname']
        slname = request.form['llname']
        semail = request.form['lemail']
        sphn = request.form['lphn']
        spass = request.form['lpass']
        scpass = request.form['lcpass']
        sb_day = request.form['lbd']
        sphoto = request.files['lphoto']

        if sphoto.filename == '':
            err = "Import Your Image"
            return render_template('registration.html', err=err)
        else:
            filep = os.path.join(app.config['UPLOAD_FOLDER '], '2C' + sphoto.filename)
            sphoto.save(filep)

            photoname = '2C' + sphoto.filename

        mycursor.execute("""SELECT * FROM `l_table`  WHERE `Email` LIKE '{}' """
                         .format(semail))
        Emaildata = mycursor.fetchall()
        if len(Emaildata) > 0:
            error = "Email  Already  Used"
            return render_template('registration.html', error=error)
        elif spass != scpass:
            errorr = "Password Not Match , Try agin"
            return render_template('registration.html', errorr=errorr)
        elif len(spass) < 8:
            errorr = "password at least 8 characters"
            return render_template('registration.html', errorr=errorr)
        else:
            mycursor.execute(
                "insert into l_table (Fname,Sname,Email,phone,pass,birth_day,photo)value(%s,%s,%s,%s,%s,%s,%s)",
                (sname, slname, semail, sphn, spass, sb_day, photoname))
            mydb.commit()
            mycursor.close()
            return render_template("login.html")


@app.route('/index_l', methods=['POST', 'GET'])
def index_l():
    global cvalu
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="university_project"
    )
    mycursor = mydb.cursor()

    valu = session['Email']
    if valu == 1:
        return render_template("login.html")
    mycursor.execute(

        "SELECT * FROM l_table WHERE Email='" + valu + "'")

    valu_of_login = mycursor.fetchone()
    filename = 'Student_img/' + valu_of_login[6]

    mycursor.execute("SELECT SUM(qty)  FROM books")
    qty = mycursor.fetchone()
    inr = int(qty[0])

    if len(valu_of_login) > 0:
        mycursor.execute("SELECT * FROM l_table")
        valu = mycursor.fetchall()
        cvalu = len(valu)
    mycursor.execute("SELECT * FROM student_table")
    valu2 = mycursor.fetchall()
    mycursor.execute("select * from  books")
    books = mycursor.fetchall()
    valu_books = len(books)
    dvalu = len(valu2)

    name = valu_of_login[0]
    name2 = valu_of_login[1]
    session['user_first_name'] = valu_of_login[1]
    mydb.commit()
    mycursor.close()

    return render_template('index.html', name=name, name2=name2, filename=filename, cvalu=cvalu, dvalu=dvalu,
                           student=valu2, valu2=valu2, valu_books=valu_books, qty=inr)


@app.route('/add_cata', methods=['POST', 'GET'])
def add_cata():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="university_project"
    )
    valu = session['Email']
    if valu == 1:
        return render_template("login.html")
    mycursor = mydb.cursor()
    id = str(session['user_ID'])
    mycursor.execute("select  * from l_table where id ='" + id + "'")
    main_data = mycursor.fetchone()
    name = main_data[0]
    name2 = main_data[1]
    filename = 'Student_img/' + main_data[6]
    mydb.commit()
    mycursor.close()
    return render_template('add-cata.html', name=name, name2=name2, filename=filename)


@app.route('/mange_book', methods=['POST', 'GET'])
def mange_book():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="university_project"
    )
    valu = session['Email']
    if valu == 1:
        return render_template("login.html")

    zero = "0"
    z_sts = "Active"
    z_sts2 = "Inactive"
    mycursor = mydb.cursor()
    mycursor.execute("select * from books where qty='" + zero + "' and status='" + z_sts + "'")
    Book_name = mycursor.fetchone()
    mycursor.execute("select * from books where qty='" + zero + "' and status='" + z_sts + "'")
    Book_name_g = mycursor.fetchall()
    if len(Book_name_g) > 0:
        upd_sts = str(Book_name[0])
        mycursor.execute("update books set status ='" + z_sts2 + "' where Id='" + upd_sts + "'")

    mycursor.execute("select * from books where qty>'" + zero + "' and status='" + z_sts2 + "'")
    Book_name = mycursor.fetchone()
    mycursor.execute("select * from books where qty>'" + zero + "' and status='" + z_sts2 + "'")
    Book_name_g = mycursor.fetchall()
    if len(Book_name_g) > 0:
        upd_sts = str(Book_name[0])
        mycursor.execute("update books set status ='" + z_sts + "' where Id='" + upd_sts + "'")
    mycursor.execute("select * from books")
    book_data = mycursor.fetchall()
    id = str(session['user_ID'])
    mycursor.execute("select  * from l_table where id ='" + id + "'")
    main_data = mycursor.fetchone()
    name = main_data[0]
    name2 = main_data[1]
    filename = 'Student_img/' + main_data[6]
    mydb.commit()
    mycursor.close()
    return render_template('manage-books.html', book_datas=book_data, name=name, name2=name2, filename=filename)


# add category list on form page

@app.route('/add_book', methods=['POST', 'GET'])
def add_book():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="university_project"
    )
    valu = session['Email']
    if valu == 1:
        return render_template("login.html")
    mycursor = mydb.cursor()
    mycursor.execute("select * from categories where ctg_sts ='Active'")

    all_categorys = mycursor.fetchall()
    id = str(session['user_ID'])
    mycursor.execute("select  * from l_table where id ='" + id + "'")
    main_data = mycursor.fetchone()
    name = main_data[0]
    name2 = main_data[1]
    filename = 'Student_img/' + main_data[6]
    mydb.commit()
    mycursor.close()

    return render_template('add-book.html', category=all_categorys, all_categorys=all_categorys, name=name, name2=name2,
                           filename=filename)


# add book on database
@app.route('/Add_book', methods=['POST', 'GET'])
def Add_book():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="university_project"
    )
    valu = session['Email']
    if valu == 1:
        return render_template("login.html")
    mycursor = mydb.cursor()
    if request.method == 'POST':
        Book_name = request.form['Bn']
        Book_edition = request.form['Be']
        author_name = request.form['An']
        book_self = request.form['Bsn']
        qty = request.form['Qt']
        category = request.form['ctg']
        status = request.form['flexR']
        mycursor.execute("select * from categories where ctg_sts ='Active'")
        all_categorys = mycursor.fetchall()
        mycursor.execute(
            "select * from books where Book_name='" + Book_name + "' and Book_edition='" + Book_edition + "' "
                                                                                                          "and  Author_name = '" + author_name + "' and self_no= '" + book_self + "' and qty ='" + qty + "' and "
                                                                                                                                                                                                         "Category"
                                                                                                                                                                                                         " ='" + category + "' and status ='" + status + "' ")
        data_book = mycursor.fetchall()
        if Book_name == '' or Book_edition == '' or author_name == '' or book_self == '' or qty == '' or category == '':
            mess = "Enter your input again , Somewhere your Input is empty"
            id = str(session['user_ID'])
            mycursor.execute("select  * from l_table where id ='" + id + "'")
            main_data = mycursor.fetchone()
            name = main_data[0]
            name2 = main_data[1]
            filename = 'Student_img/' + main_data[6]

            mydb.commit()
            mycursor.close()
            return render_template('add-book.html', category=all_categorys, all_categorys=all_categorys, mess=mess,
                                   name=name, name2=name2, filename=filename)
        if len(data_book) > 0:
            mess = "This Book is all ready Added"
            id = str(session['user_ID'])
            mycursor.execute("select  * from l_table where id ='" + id + "'")
            main_data = mycursor.fetchone()
            name = main_data[0]
            name2 = main_data[1]
            filename = 'Student_img/' + main_data[6]
            mydb.commit()
            mycursor.close()
            return render_template('add-book.html', category=all_categorys, all_categorys=all_categorys, mess=mess,
                                   name=name, name2=name2, filename=filename)
        else:
            mycursor.execute("insert into books (Book_name,Book_edition,Author_name,self_no,qty,Category,"
                             "status)value(%s, "
                             "%s,%s,%s,%s,%s,%s)",
                             (Book_name, Book_edition, author_name, book_self, qty, category, status))
            mydb.commit()
            mycursor.close()
            return redirect('/mange_book')


# delete  Books
@app.route('/book_delete/<id>', methods=['POST', 'GET'])
def book_delete(id):
    dle = id
    session['dle'] = dle
    return ('', 204)


@app.route('/book_delete_conferm')
def book_delete_conferm():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="university_project"
    )
    valu = session['Email']
    if valu == 1:
        return render_template("login.html")
    mycursor = mydb.cursor()
    data_del = session['dle']
    mycursor.execute("DELETE FROM books WHERE Id='" + data_del + "' ")
    mydb.commit()
    mycursor.close()
    return redirect('mange_book')


@app.route('/add-issu', methods=['POST', 'GET'])
def addiss():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="university_project"
    )
    valu = session['Email']
    if valu == 1:
        return render_template("login.html")
    mycursor = mydb.cursor()
    id = str(session['user_ID'])
    mycursor.execute("select  * from l_table where id ='" + id + "'")
    main_data = mycursor.fetchone()
    name = main_data[0]
    name2 = main_data[1]
    filename = 'Student_img/' + main_data[6]
    mydb.commit()
    mycursor.close()
    return render_template('add-issu-books.html', name=name, name2=name2, filename=filename)


@app.route('/manage_iss_book', methods=['POST', 'GET'])
def iss_book():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="university_project"
    )
    valu = session['Email']
    if valu == 1:
        return render_template("login.html")
    mycursor = mydb.cursor()

    mycursor.execute("select * from issue")
    all_issuedata = mycursor.fetchall()
    i = 0
    size = len(all_issuedata)
    while i < size:
        mycursor = mydb.cursor()
        single = all_issuedata[i]
        ID = str(single[3])
        book_pass_id = str(single[5])
        issu_date_f = date.today()
        issue_last_date_year = int(single[8].year)
        issue_last_date_month = int(single[8].month)
        issue_last_date_day = int(single[8].day)
        user_birthday = date(issue_last_date_year, issue_last_date_month, issue_last_date_day)
        todayd = date(issu_date_f.year, issu_date_f.month, issu_date_f.day)
        delta = user_birthday - todayd
        age = str(delta.days)
        mycursor.execute(
            "UPDATE issue SET age='" + age + "' WHERE student_id ='" + ID + "' and book_pass_id='" + book_pass_id + "'")
        i = i + 1

    mycursor.execute("select * from issue")
    issu_data = mycursor.fetchall()
    id = str(session['user_ID'])
    mycursor.execute("select  * from l_table where id ='" + id + "'")
    main_data = mycursor.fetchone()
    name = main_data[0]
    name2 = main_data[1]
    filename = 'Student_img/' + main_data[6]
    mydb.commit()
    mycursor.close()
    return render_template('manage-issu-books.html', all_issu=issu_data, issu_data=issu_data, name=name, name2=name2,
                           filename=filename)


@app.route('/issu_book_id_pass/<Id>')
def issu_book(Id):
    id = Id
    session['issue_delete'] = id
    return ('', 204)


@app.route('/delete_issu')
def delete_issue():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="university_project"
    )
    valu = session['Email']
    if valu == 1:
        return render_template("login.html")
    mycursor = mydb.cursor()

    a = session['issue_delete']
    mycursor.execute("delete from issue where issue_id='" + a + "'")

    mycursor.execute("select * from issue")
    all_issuedata = mycursor.fetchall()
    i = 0
    size = len(all_issuedata)
    while i < size:
        mycursor = mydb.cursor()
        single = all_issuedata[i]
        ID = str(single[3])
        book_pass_id = str(single[5])
        issu_date_f = date.today()
        issue_last_date_year = int(single[8].year)
        issue_last_date_month = int(single[8].month)
        issue_last_date_day = int(single[8].day)
        user_birthday = date(issue_last_date_year, issue_last_date_month, issue_last_date_day)
        todayd = date(issu_date_f.year, issu_date_f.month, issu_date_f.day)
        delta = user_birthday - todayd
        age = str(delta.days)
        mycursor.execute(
            "UPDATE issue SET age='" + age + "' WHERE student_id ='" + ID + "' and book_pass_id='" + book_pass_id + "'")
        i = i + 1

    mydb.commit()
    mycursor.close()
    return redirect('/manage_iss_book')


@app.route('/issu-add', methods=['POST', 'GET'])
def issu_add():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="university_project"
    )
    valu = session['Email']
    if valu == 1:
        return render_template("login.html")

    if request.method == 'POST':
        mycursor = mydb.cursor()
        studet_id = request.form['st_id']
        book_id = request.form['book_id']
        issu_date_f = date.today()
        issu_date_l = request.form['ilf_d']

        mycursor.execute("select * from student_table where st_id = '" + studet_id + "'")
        studet_id_data = mycursor.fetchone()
        mycursor.execute("select * from student_table where st_id = '" + studet_id + "'")
        studet_id_data_a = mycursor.fetchall()
        mycursor.execute("select  * from books where Id='" + book_id + "' ")
        book_id_data = mycursor.fetchone()
        mycursor.execute("select  * from books where Id='" + book_id + "' ")
        book_id_data_a = mycursor.fetchall()

        issue_last_date_year = int(issu_date_l[0] + issu_date_l[1] + issu_date_l[2] + issu_date_l[3])
        issue_last_date_month = int(issu_date_l[5] + issu_date_l[6])
        issue_last_date_day = int(issu_date_l[8] + issu_date_l[9])
        user_birthday = date(issue_last_date_year, issue_last_date_month, issue_last_date_day)
        todayd = date(issu_date_f.year, issu_date_f.month, issu_date_f.day)
        delta = user_birthday - todayd
        age = delta.days

        if studet_id == '' or book_id == '' or issu_date_f == '' or issu_date_l == '':
            valu = session['Email']
            if valu == 1:
                return render_template("login.html")
            id = str(session['user_ID'])
            mycursor.execute("select  * from l_table where id ='" + id + "'")
            main_data = mycursor.fetchone()
            name = main_data[0]
            name2 = main_data[1]
            filename = 'Student_img/' + main_data[6]
            mydb.commit()
            mycursor.close()
            Error_blank = "Enter input again , somewhere your input is  empty"
            return render_template('add-issu-books.html', Error_blank=Error_blank, name2=name2, filename=filename,
                                   studet_id=studet_id, book_id=book_id)
        if len(studet_id_data_a) == 0:
            valu = session['Email']
            if valu == 1:
                return render_template("login.html")
            id = str(session['user_ID'])
            mycursor.execute("select  * from l_table where id ='" + id + "'")
            main_data = mycursor.fetchone()
            name = main_data[0]
            name2 = main_data[1]
            filename = 'Student_img/' + main_data[6]
            mydb.commit()
            mycursor.close()
            Error_blank = "Student id not found"
            return render_template('add-issu-books.html', Error_blank=Error_blank, name2=name2, name=name,
                                   filename=filename, studet_id=studet_id, book_id=book_id)
        if age < 0:
            valu = session['Email']
            if valu == 1:
                return render_template("login.html")
            id = str(session['user_ID'])
            mycursor.execute("select  * from l_table where id ='" + id + "'")
            main_data = mycursor.fetchone()
            name = main_data[0]
            name2 = main_data[1]
            filename = 'Student_img/' + main_data[6]
            mydb.commit()
            mycursor.close()
            Error_blank = "Enter issue date correctly"
            return render_template('add-issu-books.html', age_error=Error_blank, name2=name2, name=name,
                                   filename=filename, studet_id=studet_id, book_id=book_id)

        if len(book_id_data_a) == 0:
            valu = session['Email']
            if valu == 1:
                return render_template("login.html")
            id = str(session['user_ID'])
            mycursor.execute("select  * from l_table where id ='" + id + "'")
            main_data = mycursor.fetchone()
            name = main_data[0]
            name2 = main_data[1]
            filename = 'Student_img/' + main_data[6]
            mydb.commit()
            mycursor.close()
            Error_blank_st = "Student id not found"
            return render_template('add-issu-books.html', Error_blank_st=Error_blank_st, filename=filename, name=name,
                                   name2=name2, studet_id=studet_id, book_id=book_id)
        if book_id_data[5] < 1:
            valu = session['Email']
            if valu == 1:
                return render_template("login.html")
            id = str(session['user_ID'])
            mycursor.execute("select  * from l_table where id ='" + id + "'")
            main_data = mycursor.fetchone()
            name = main_data[0]
            name2 = main_data[1]
            filename = 'Student_img/' + main_data[6]
            mydb.commit()
            mycursor.close()
            Error_blank_qt = "This book  is not available now"
            return render_template('add-issu-books.html', Error_blank_qt=Error_blank_qt, name2=name2, name=name,
                                   filename=filename, studet_id=studet_id, book_id=book_id)
        else:
            valu = session['Email']
            if valu == 1:
                return render_template("login.html")
            st_name_f = studet_id_data[0]
            st_name_s = studet_id_data[1]
            st_id = studet_id
            sts = "Inactive"
            book_i = book_id_data[0]
            book_j = str(book_i)
            book_n = book_id_data[1]
            book_e = book_id_data[2]
            mycursor.execute("insert into  issue (student_name,student_l_name,student_id,book_name,book_pass_id,"
                             "book_edition, "
                             "issue_date,issue_last_date,age)value(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                             (st_name_f, st_name_s, st_id, book_n, book_i, book_e, issu_date_f, issu_date_l, age))
            n = book_id_data[5]
            Book_name = int(n) - 1
            if Book_name == 0:
                mycursor.execute("update books set status ='" + sts + "' where Id ='" + book_j + "'")
            strm = str(Book_name)
            mycursor.execute("UPDATE books SET qty ='" + strm + "' WHERE Id ='" + book_j + "'")

            mycursor.execute("select * from issue")
            all_issuedata = mycursor.fetchall()
            i = 0
            size = len(all_issuedata)
            while i < size:
                mycursor = mydb.cursor()
                single = all_issuedata[i]
                ID = str(single[3])
                book_pass_id = str(single[5])
                issu_date_f = date.today()
                issue_last_date_year = int(single[8].year)
                issue_last_date_month = int(single[8].month)
                issue_last_date_day = int(single[8].day)
                user_birthday = date(issue_last_date_year, issue_last_date_month, issue_last_date_day)
                todayd = date(issu_date_f.year, issu_date_f.month, issu_date_f.day)
                delta = user_birthday - todayd
                age = str(delta.days)
                mycursor.execute(
                    "UPDATE issue SET age='" + age + "' WHERE student_id ='" + ID + "' and book_pass_id='" + book_pass_id + "'")
                i = i + 1

            mydb.commit()
            mycursor.close()
            return redirect('/manage_iss_book')


@app.route('/Change_password', methods=['POST', 'GET'])
def Change_password():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="university_project"
    )
    mycursor = mydb.cursor()
    if request.method == 'POST':

        oldpass = request.form['password']
        change_pass = request.form['newpassword']
        Conferm_oldpass = request.form['renewpassword']

        email = session['Email']
        mycursor.execute("select * from l_table where Email ='" + email + "'")
        oldpassword = mycursor.fetchone()

        if oldpassword[4] != oldpass:
            id = session['user_ID']
            Id = str(id)
            mycursor.execute("select * from l_table where id='" + Id + "'")
            about = mycursor.fetchone()
            name = about[0]
            name2 = about[1]
            filename = 'Student_img/' + about[6]
            email = about[2]
            phone = about[3]
            country = about[8]
            address = about[9]
            us_about = about[10]
            text = "Sorry your password is not match"
            mydb.commit()
            mycursor.close()
            return render_template('users-profile.html', name=name, filename=filename, name2=name2, email=email,
                                   phone=phone,
                                   country=country, address=address, us_about=us_about, text=text)
        if change_pass != Conferm_oldpass:
            id = session['user_ID']
            Id = str(id)
            mycursor.execute("select * from l_table where id='" + Id + "'")
            about = mycursor.fetchone()
            name = about[0]
            name2 = about[1]
            filename = 'Student_img/' + about[6]
            email = about[2]
            phone = about[3]
            country = about[8]
            address = about[9]
            us_about = about[10]
            text = "Sorry your conform password is not match"
            mydb.commit()
            mycursor.close()
            return render_template('users-profile.html', name=name, filename=filename, name2=name2, email=email,
                                   phone=phone,
                                   country=country, address=address, us_about=us_about, text=text)

        if len(change_pass) < 8 or len(Conferm_oldpass) < 8:
            id = session['user_ID']
            Id = str(id)
            mycursor.execute("select * from l_table where id='" + Id + "'")
            about = mycursor.fetchone()
            name = about[0]
            name2 = about[1]
            filename = 'Student_img/' + about[6]
            email = about[2]
            phone = about[3]
            country = about[8]
            address = about[9]
            us_about = about[10]
            text = "Your password is too short"
            mydb.commit()
            mycursor.close()
            return render_template('users-profile.html', name=name, filename=filename, name2=name2, email=email,
                                   phone=phone,
                                   country=country, address=address, us_about=us_about, text=text)

        else:
            mycursor.execute("UPDATE l_table SET pass ='" + Conferm_oldpass + "' WHERE Email ='" + email + "'")
            id = session['user_ID']
            Id = str(id)
            mycursor.execute("select * from l_table where id='" + Id + "'")
            about = mycursor.fetchone()
            name = about[0]
            name2 = about[1]
            filename = 'Student_img/' + about[6]
            email = about[2]
            phone = about[3]
            country = about[8]
            address = about[9]
            us_about = about[10]
            text = "Successfully Changed"
            mydb.commit()
            mycursor.close()
            return render_template('users-profile.html', name=name, filename=filename, name2=name2, email=email,
                                   phone=phone,
                                   country=country, address=address, us_about=us_about, textr=text)


@app.route('/user_profile', methods=['POST', 'GET'])
def user_profile():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="university_project"
    )

    valu = session['Email']

    if valu == 1:
        return render_template("login.html")
    mycursor = mydb.cursor()
    # filename = session['user_profile_pic']

    id = session['user_ID']
    Id = str(id)
    mycursor.execute("select * from l_table where id='" + Id + "'")
    about = mycursor.fetchone()
    name = about[0]
    name2 = about[1]
    filename = 'Student_img/' + about[6]
    email = about[2]
    phone = about[3]
    country = about[8]
    address = about[9]
    us_about = about[10]
    mydb.commit()
    mycursor.close()
    return render_template('users-profile.html', name=name, filename=filename, name2=name2, email=email, phone=phone,
                           country=country, address=address, us_about=us_about)


@app.route('/addcata', methods=['POST', 'GET'])
def addcata():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="university_project"
    )
    valu = session['Email']
    if valu == 1:
        return render_template("login.html")
    mycursor = mydb.cursor()
    if request.method == 'POST':

        ctgname = request.form['cat']
        st = request.form['flex']
        mycursor.execute("""SELECT * FROM `categories`  WHERE `ctg_name` LIKE '{}'  """
                         .format(ctgname))
        alr = mycursor.fetchall()
        if len(alr) > 0:
            valu = session['Email']
            if valu == 1:
                return render_template("login.html")
            m = "This categorie is  already added"
            id = str(session['user_ID'])
            mycursor.execute("select  * from l_table where id ='" + id + "'")
            main_data = mycursor.fetchone()
            name = main_data[0]
            name2 = main_data[1]
            filename = 'Student_img/' + main_data[6]
            mydb.commit()
            mycursor.close()
            return render_template('add-cata.html', m=m, name=name, name2=name2, filename=filename)
        if ctgname == '':
            valu = session['Email']
            if valu == 1:
                return render_template("login.html")
            m = "Enter category name"
            id = str(session['user_ID'])
            mycursor.execute("select  * from l_table where id ='" + id + "'")
            main_data = mycursor.fetchone()
            name = main_data[0]
            name2 = main_data[1]
            filename = 'Student_img/' + main_data[6]
            mydb.commit()
            mycursor.close()
            return render_template('add-cata.html', m=m, name=name, name2=name2, filename=filename)
        else:
            valu = session['Email']
            if valu == 1:
                return render_template("login.html")
            mycursor.execute(
                "insert into categories (ctg_name,ctg_sts)value(%s,%s)",
                (ctgname, st))
            mydb.commit()
            mycursor.close()
            return redirect('mange_cata')


@app.route('/mange_cata', methods=['POST', 'GET'])
def mange_cata():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="university_project"
    )
    valu = session['Email']
    if valu == 1:
        return render_template("login.html")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM categories")

    catgory = mycursor.fetchall()
    length = len(catgory)
    id = str(session['user_ID'])
    mycursor.execute("select  * from l_table where id ='" + id + "'")
    main_data = mycursor.fetchone()
    name = main_data[0]
    name2 = main_data[1]
    session['li_name'] = name + name2
    filename = 'Student_img/' + main_data[6]
    session['li_img'] = filename
    mydb.commit()
    mycursor.close()

    return render_template('manage-cata.html', catgorys=catgory, catgory=catgory, length=length, name=name, name2=name2,
                           filename=filename)


@app.route('/delete/<catgorys>', methods=['POST', 'GET'])
def delete(catgorys):
    a = catgorys
    session['Ac'] = a
    return ('', 204)


@app.route('/delet', methods=['POST', 'GET'])
def delt():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="university_project"
    )
    valu = session['Email']
    if valu == 1:
        return render_template("login.html")
    delet_data = session['Ac']
    mycursor = mydb.cursor()
    mycursor.execute("DELETE FROM categories WHERE ctg_name='" + delet_data + "' ")
    mydb.commit()
    mycursor.close()
    return redirect('mange_cata')


# edit catagory
@app.route('/edit_category', methods=['POST', 'GET'])
def edit_category():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="university_project"
    )
    valu = session['Email']
    if valu == 1:
        return render_template("login.html")
    mycursor = mydb.cursor()
    if request.method == 'POST':
        status_chake = request.form['flexRadioDefault']

        back_name = request.form['edit_value']
        mycursor.execute("UPDATE categories SET ctg_sts ='" + status_chake + "' WHERE ctg_name ='" + back_name + "'")
        mydb.commit()
        mycursor.close()
        return redirect('mange_cata')


@app.route('/edit_books', methods=['POST', 'GET'])
def edit_books():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="university_project"
    )
    valu = session['Email']
    if valu == 1:
        return render_template("login.html")
    mycursor = mydb.cursor()
    if request.method == 'POST':
        book_id = request.form['book_id']
        book_name = request.form['book_name']
        book_edition = request.form['book_e']
        book_author = request.form['book_a']
        book_qty = request.form['book_q']
        book_self = request.form['book_s']
        book_status = request.form['fl']
        mycursor.execute(
            "update books set  Book_name='" + book_name + "' , Book_edition ='" + book_edition + "' , Author_name='" + book_author + "' , self_no ='" + book_self + "' , qty='" + book_qty + "' , status ='" + book_status + "' where Id='" + book_id + "'")
        mydb.commit()
        mycursor.close()
        return redirect('mange_book')


@app.route('/issue_update', methods=['POST', 'GET'])
def issue_update():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="university_project"
    )
    valu = session['Email']
    if valu == 1:
        return render_template("login.html")
    mycursor = mydb.cursor()
    if request.method == 'POST':
        st_id = request.form['issue_up_id']
        issue_lastdate = request.form['issue_up']
        today = date.today()
        issue_last_date_year = int(issue_lastdate[0] + issue_lastdate[1] + issue_lastdate[2] + issue_lastdate[3])
        issue_last_date_month = int(issue_lastdate[5] + issue_lastdate[6])
        issue_last_date_day = int(issue_lastdate[8] + issue_lastdate[9])
        user_birthday = date(issue_last_date_year, issue_last_date_month, issue_last_date_day)
        todayd = date(today.year, today.month, today.day)
        delta = user_birthday - todayd
        age = delta.days
        if age < 0:
            return redirect('/manage_iss_book')
        else:

            mycursor.execute(
                "UPDATE issue SET issue_last_date ='" + issue_lastdate + "' and age='" + age + "' WHERE student_id ='" + st_id + "'")

            mycursor.execute("select * from issue")
            all_issuedata = mycursor.fetchall()
            i = 0
            size = len(all_issuedata)
            while i < size:
                mycursor = mydb.cursor()
                single = all_issuedata[i]
                ID = str(single[3])
                book_pass_id = str(single[5])
                issu_date_f = date.today()
                issue_last_date_year = int(single[8].year)
                issue_last_date_month = int(single[8].month)
                issue_last_date_day = int(single[8].day)
                user_birthday = date(issue_last_date_year, issue_last_date_month, issue_last_date_day)
                todayd = date(issu_date_f.year, issu_date_f.month, issu_date_f.day)
                delta = user_birthday - todayd
                age = str(delta.days)
                mycursor.execute(
                    "UPDATE issue SET age='" + age + "' WHERE student_id ='" + ID + "' and book_pass_id='" + book_pass_id + "'")
                i = i + 1

            mydb.commit()
            mycursor.close()
            return redirect('/manage_iss_book')


@app.route('/Edite_user_name', methods=['POST', 'GET'])
def Edite_user_name():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="university_project"
    )
    valu = session['Email']
    if valu == 1:
        return render_template("login.html")
    mycursor = mydb.cursor()
    if request.method == 'POST':
        first_name = request.form['first_name']
        second_name = request.form['second_name']
        email = request.form['email']
        phone = request.form['phone']
        about = request.form['about']
        country = request.form['country']
        address = request.form['address']
        mycursor.execute(
            "update l_table set Fname='" + first_name + "' , Sname='" + second_name + "' ,	phone='" + phone + "' , country='" + country + "' , address='" + address + "', About='" + about + "'   where    	Email='" + email + "' ")
        mydb.commit()
        mycursor.close()
        return redirect('/user_profile')


@app.route('/student_index')
def student_index():
    notshow = session['student_login']
    if notshow == "logout":
        return redirect('/login')

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="university_project"
    )
    email = session['student_login']
    mycursor = mydb.cursor()

    mycursor.execute("select * from issue")
    all_issuedata = mycursor.fetchall()
    i = 0
    size = len(all_issuedata)
    while i < size:
        mycursor = mydb.cursor()
        single = all_issuedata[i]
        ID = str(single[3])
        book_pass_id = str(single[5])
        issu_date_f = date.today()
        issue_last_date_year = int(single[8].year)
        issue_last_date_month = int(single[8].month)
        issue_last_date_day = int(single[8].day)
        user_birthday = date(issue_last_date_year, issue_last_date_month, issue_last_date_day)
        todayd = date(issu_date_f.year, issu_date_f.month, issu_date_f.day)
        delta = user_birthday - todayd
        age = str(delta.days)
        mycursor.execute(
            "UPDATE issue SET age='" + age + "' WHERE student_id ='" + ID + "' and book_pass_id='" + book_pass_id + "'")
        i = i + 1

    mycursor.execute("select * from student_table where Email = '" + email + "'")
    student_details = mycursor.fetchone()
    student_name = student_details[0] + " " + student_details[1]
    student_img = student_details[7]
    student_id = student_details[3]
    session['st_name'] = student_name
    session['st_img'] = student_img
    session['st_id'] = student_details[3]
    mycursor.execute("select * from student_table")
    total_student = mycursor.fetchall()
    mycursor.execute("select * from books")
    total_books = mycursor.fetchall()
    mycursor.execute("SELECT COUNT(student_id) FROM issue where student_id = '" + student_id + "'")
    total_issue = mycursor.fetchone()
    mydb.commit()
    mycursor.close()
    return render_template('student-index.html', student_name=student_name, total_student=len(total_student),
                           total_books=len(total_books), student_img=student_img, total_issue=total_issue[0])


@app.route('/student_books', methods=['POST', 'GET'])
def student_books():
    notshow = session['student_login']
    if notshow == "logout":
        return redirect('/login')

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="university_project"
    )

    mycursor = mydb.cursor()
    mycursor.execute("select * from books")
    totla_book = mycursor.fetchall()
    mydb.commit()
    mycursor.close()
    student_name = session['st_name']
    student_img = session['st_img']
    return render_template("student-books.html", totla_books=totla_book, student_img=student_img,
                           student_name=student_name)


@app.route('/student_issue_books', methods=['POST', 'GET'])
def student_issue_books():
    notshow = session['student_login']
    if notshow == "logout":
        return redirect('/login')
    today = date.today()
    student_email = session['student_login']
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="university_project"
    )
    mycursor = mydb.cursor()
    mycursor.execute("select * from student_table where Email='" + student_email + "'")
    student_ids = mycursor.fetchone()
    student_id = student_ids[3]
    if request.method == 'POST':
        notshow = session['student_login']
        if notshow == "logout":
            return redirect('/login')
        id = request.form['student_id']
        issue_last_date = request.form['issue_last_date']
        if issue_last_date == "" or id == "":
            notshow = session['student_login']
            if notshow == "logout":
                return redirect('/login')
            mycursor.execute("select * from books")
            totla_book = mycursor.fetchall()
            mydb.commit()
            mycursor.close()
            student_name = session['st_name']
            student_img = session['st_img']
            text = "Enter your inputs correctly"
            return render_template("student-books.html", totla_books=totla_book, student_img=student_img,
                                   student_name=student_name, text=text)
        issue_last_date_year = int(issue_last_date[0] + issue_last_date[1] + issue_last_date[2] + issue_last_date[3])
        issue_last_date_month = int(issue_last_date[5] + issue_last_date[6])
        issue_last_date_day = int(issue_last_date[8] + issue_last_date[9])
        user_birthday = date(issue_last_date_year, issue_last_date_month, issue_last_date_day)
        todayd = date(today.year, today.month, today.day)
        delta = user_birthday - todayd
        age = delta.days


        mycursor.execute("select * from issue where student_id ='"+student_id+"' and book_pass_id='"+id+"'")
        orac=mycursor.fetchall()

        mycursor.execute("select * from request_table where student_id ='" + student_id + "' and book_pass_id='" + id + "'")
        request_chake = mycursor.fetchall()

        if  len(request_chake)>0:
            notshow = session['student_login']
            if notshow == "logout":
                return redirect('/login')
            mycursor.execute("select * from books")
            totla_book = mycursor.fetchall()
            mydb.commit()
            mycursor.close()
            student_name = session['st_name']
            student_img = session['st_img']
            text = "You  already send request for  that book . Please wait for accept   request"
            return render_template("student-books.html", totla_books=totla_book, student_img=student_img,
                                   student_name=student_name, text=text)
        elif len(orac)>0:
            notshow = session['student_login']
            if notshow == "logout":
                return redirect('/login')
            mycursor.execute("select * from books")
            totla_book = mycursor.fetchall()
            mydb.commit()
            mycursor.close()
            student_name = session['st_name']
            student_img = session['st_img']
            text = "You  already issued that book"
            return render_template("student-books.html", totla_books=totla_book, student_img=student_img,
                                   student_name=student_name, text=text)

        elif age >= 0:
            notshow = session['student_login']
            if notshow == "logout":
                return redirect('/login')
            mycursor.execute("select * from books where Id='" + id + "'")
            book_details = mycursor.fetchone()
            student_name = session['st_name']
            student_l_name = ""
            book_name = book_details[1]
            book_id = id
            book_edition = book_details[2]
            issue_date = today
            mycursor.execute(
                "insert into request_table (student_name,student_l_name,student_id,book_name,book_pass_id,book_edition,issue_date,issue_last_date,age)value(%s,%s,%s,"
                "%s,%s,%s,%s,%s,%s)",
                (
                    student_name, student_l_name, student_id, book_name, book_id, book_edition, issue_date,
                    issue_last_date,
                    age))
            mycursor.execute("select * from books")
            totla_book = mycursor.fetchall()
            mydb.commit()
            mycursor.close()
            student_name = session['st_name']
            student_img = session['st_img']
            text = "Successfully send request"
            return render_template("student-books.html", totla_books=totla_book, student_img=student_img,
                                   student_name=student_name, textr=text)
        else:
            notshow = session['student_login']
            if notshow == "logout":
                return redirect('/login')
            mycursor.execute("select * from books")
            totla_book = mycursor.fetchall()
            mydb.commit()
            mycursor.close()
            student_name = session['st_name']
            student_img = session['st_img']
            text = "Enter your issue Date correctly . At last one day you  need to issue"
            return render_template("student-books.html", totla_books=totla_book, student_img=student_img,
                                   student_name=student_name, text=text)


@app.route('/Request', methods=['POST', 'GET'])
def Request():
    valu = session['Email']
    if valu == 1:
        return render_template("login.html")
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="university_project"
    )
    email = session['Email']
    mycursor = mydb.cursor()
    mycursor.execute("select * from request_table")
    allrequest = mycursor.fetchall()

    mycursor.execute("select * from l_table where Email ='" + email + "' ")

    student_data = mycursor.fetchone()
    filename = 'Student_img/' + student_data[6]
    mydb.commit()
    mycursor.close()
    return render_template("Request.html", allrequests=allrequest, name=student_data[0], name2=student_data[1],
                           filename=filename)


@app.route('/warning', methods=['POST', 'GET'])
def warning():
    valu = session['Email']
    if valu == 1:
        return render_template("login.html")
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="university_project"
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM issue WHERE age<3")
    warning_value = mycursor.fetchall()
    email = session['Email']
    mycursor.execute("select * from l_table where Email ='" + email + "' ")

    student_data = mycursor.fetchone()
    filename = 'Student_img/' + student_data[6]
    mydb.commit()
    mycursor.close()
    return render_template("warning.html", warning_values=warning_value, name=student_data[0], name2=student_data[1],
                           filename=filename)


@app.route('/student_users_profile', methods=['POST', 'GET'])
def student_users_profile():
    notshow = session['student_login']
    if notshow == "logout":
        return redirect('/login')
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="university_project"
    )
    mycursor = mydb.cursor()
    email = session['student_login']
    mycursor.execute("select * from student_table where Email='" + email + "'")
    student_data = mycursor.fetchone()
    name = student_data[0] + student_data[1]
    Email = student_data[2]
    st_id = student_data[3]
    phone = student_data[4]
    birthday = student_data[6]
    photo = 'Student_img/' + student_data[7]
    Batch = student_data[8]
    Department = student_data[9]
    country = student_data[10]
    address = student_data[11]
    about = student_data[12]
    mydb.commit()
    mycursor.close()
    return render_template("student-users-profile.html", name=name, Email=Email, st_id=st_id, phone=phone,
                           birthday=birthday, photo=photo, Batch=Batch, Department=Department, country=country,
                           address=address, about=about)


@app.route('/change', methods=['POST', 'GET'])
def change():
    notshow = session['student_login']
    if notshow == "logout":
        return redirect('/login')
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="university_project"
    )
    mycursor = mydb.cursor()
    if request.method == 'POST':
        name = request.form.get('name')
        about = request.form.get('about')
        student_id = request.form.get('id')
        batch = request.form.get('batch')
        dep = request.form.get('dep')
        country = request.form.get('country')
        add = request.form.get('add')
        phone = request.form.get('phone')
        email = session['student_login']
        send_name = ""
        mycursor.execute(
            "update student_table set Fstname ='" + name + "',Sndname='" + send_name + "'  ,st_id='" + student_id + "' , 	phone='" + phone + "' ,Batch='" + batch + "' ,Depertment='" + dep + "' ,country='" + country + "' , address='" + add + "' ,about='" + about + "' where Email='" + email + "' ")
        mydb.commit()
        mycursor.close()
        return redirect('student_users_profile')


@app.route('/test', methods=['POST', 'GET'])
def change_st_pass():
    notshow = session['student_login']
    if notshow == "logout":
        return redirect('/login')
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="university_project"
    )

    mycursor = mydb.cursor()
    if request.method == 'POST':
        password = request.form['password']
        new_password = request.form['newpassword']
        re_password = request.form['renewpassword']
        email = session['student_login']
        mycursor.execute("select pass from student_table where Email='" + email + "'")
        oldpass = mycursor.fetchone()

        if password != oldpass[0]:
            notshow = session['student_login']
            if notshow == "logout":
                return redirect('/login')
            mycursor.execute("select * from student_table where Email='" + email + "'")
            student_data = mycursor.fetchone()
            name = student_data[0] + student_data[1]
            Email = student_data[2]
            st_id = student_data[3]
            phone = student_data[4]
            birthday = student_data[6]
            photo = 'Student_img/' + student_data[7]
            Batch = student_data[8]
            Department = student_data[9]
            country = student_data[10]
            address = student_data[11]
            about = student_data[12]
            text = "Password incorrect"
            mydb.commit()
            mycursor.close()
            return render_template("student-users-profile.html", name=name, Email=Email, st_id=st_id, phone=phone,
                                   birthday=birthday, photo=photo, Batch=Batch, Department=Department, country=country,
                                   address=address, about=about, text=text)
        elif new_password != re_password:
            notshow = session['student_login']
            if notshow == "logout":
                return redirect('/login')
            mycursor.execute("select * from student_table where Email='" + email + "'")
            student_data = mycursor.fetchone()
            name = student_data[0] + student_data[1]
            Email = student_data[2]
            st_id = student_data[3]
            phone = student_data[4]
            birthday = student_data[6]
            photo = 'Student_img/' + student_data[7]
            Batch = student_data[8]
            Department = student_data[9]
            country = student_data[10]
            address = student_data[11]
            about = student_data[12]
            text = "Password not match"
            mydb.commit()
            mycursor.close()
            return render_template("student-users-profile.html", name=name, Email=Email, st_id=st_id, phone=phone,
                                   birthday=birthday, photo=photo, Batch=Batch, Department=Department, country=country,
                                   address=address, about=about, text=text)
        elif len(new_password) < 8:
            notshow = session['student_login']
            if notshow == "logout":
                return redirect('/login')
            mycursor.execute("select * from student_table where Email='" + email + "'")
            student_data = mycursor.fetchone()
            name = student_data[0] + student_data[1]
            Email = student_data[2]
            st_id = student_data[3]
            phone = student_data[4]
            birthday = student_data[6]
            photo = 'Student_img/' + student_data[7]
            Batch = student_data[8]
            Department = student_data[9]
            country = student_data[10]
            address = student_data[11]
            about = student_data[12]
            text = "Password is too short"
            mydb.commit()
            mycursor.close()
            return render_template("student-users-profile.html", name=name, Email=Email, st_id=st_id, phone=phone,
                                   birthday=birthday, photo=photo, Batch=Batch, Department=Department, country=country,
                                   address=address, about=about, text=text)
        else:
            notshow = session['student_login']
            if notshow == "logout":
                return redirect('/login')
            mycursor.execute("UPDATE student_table SET pass ='" + new_password + "' WHERE Email ='" + email + "'")
            mydb.commit()
            mycursor.close()
            return redirect("student_users_profile")


@app.route('/reqest_acept/<id>', methods=['POST', 'GET'])
def reqest_acept(id):
    valu = session['Email']
    if valu == 1:
        return render_template("login.html")
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="university_project"
    )
    a = id
    mycursor = mydb.cursor()
    mycursor.execute("select * from request_table where student_id='" + a + "'")
    information = mycursor.fetchone()

    mycursor.execute("select * from issue")
    all_issuedata = mycursor.fetchall()
    i = 0
    size = len(all_issuedata)
    while i < size:
        mycursor = mydb.cursor()
        single = all_issuedata[i]
        ID = str(single[3])
        book_pass_id = str(single[5])
        issu_date_f = date.today()
        issue_last_date_year = int(single[8].year)
        issue_last_date_month = int(single[8].month)
        issue_last_date_day = int(single[8].day)
        user_birthday = date(issue_last_date_year, issue_last_date_month, issue_last_date_day)
        todayd = date(issu_date_f.year, issu_date_f.month, issu_date_f.day)
        delta = user_birthday - todayd
        age = str(delta.days)
        mycursor.execute(
            "UPDATE issue SET age='" + age + "' WHERE student_id ='" + ID + "' and book_pass_id='" + book_pass_id + "'")
        i = i + 1

    student_name = information[1]
    student_l_name = information[2]
    student_id = information[3]
    book_name = information[4]
    book_pass_id = information[5]
    book_edition = information[6]
    issue_date = information[7]
    issue_last_date = information[8]
    age = information[9]
    mycursor.execute("insert into  issue (student_name,student_l_name,student_id,book_name,book_pass_id,"
                     "book_edition, "
                     "issue_date,issue_last_date,age)value(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                     (student_name, student_l_name, student_id, book_name, book_pass_id, book_edition, issue_date,
                      issue_last_date, age))
    mycursor.execute("DELETE FROM request_table WHERE student_id ='" + a + "' ")
    book_pass_id=str(book_pass_id)
    mycursor.execute("select * from books where Id='"+book_pass_id+"'")
    book_information=mycursor.fetchone()
    book_qty=str(book_information[5]-1)
    mycursor.execute(
        "UPDATE books SET qty='" + book_qty + "' WHERE Id='"+book_pass_id+"'")
    mydb.commit()
    mycursor.close()
    return redirect('/Request')


@app.route('/reqest_delete/<id>', methods=['POST', 'GET'])
def reqest_delete(id):
    valu = session['Email']
    if valu == 1:
        return render_template("login.html")
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="university_project"
    )
    a = id
    mycursor = mydb.cursor()
    mycursor.execute("DELETE FROM request_table WHERE student_id ='" + a + "' ")
    mydb.commit()
    mycursor.close()
    return redirect('/Request')


@app.route('/Your_Issue_book', methods=['POST', 'GET'])
def Your_Issue_book():
    notshow = session['student_login']
    if notshow == "logout":
        return redirect('/login')
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="university_project"
    )
    email = session['student_login']
    mycursor = mydb.cursor()

    mycursor.execute("select * from issue")
    all_issuedata = mycursor.fetchall()
    i = 0
    size = len(all_issuedata)
    while i < size:
        mycursor = mydb.cursor()
        single = all_issuedata[i]
        ID = str(single[3])
        book_pass_id = str(single[5])
        issu_date_f = date.today()
        issue_last_date_year = int(single[8].year)
        issue_last_date_month = int(single[8].month)
        issue_last_date_day = int(single[8].day)
        user_birthday = date(issue_last_date_year, issue_last_date_month, issue_last_date_day)
        todayd = date(issu_date_f.year, issu_date_f.month, issu_date_f.day)
        delta = user_birthday - todayd
        age = str(delta.days)
        mycursor.execute(
            "UPDATE issue SET age='" + age + "' WHERE student_id ='" + ID + "' and book_pass_id='" + book_pass_id + "'")
        i = i + 1

    mycursor.execute("select  * from student_table where Email='" + email + "'")
    iformation = mycursor.fetchone()
    name = iformation[0] + iformation[1]
    photo = 'Student_img/' + iformation[7]
    id = iformation[3]

    mycursor.execute("select * from issue where student_id ='" + id + "'")
    issue_information = mycursor.fetchall()
    mydb.commit()
    mycursor.close()
    return render_template('yourissuebook.html', name=name, photo=photo, issue_informations=issue_information)
    # return render_template('userint.html',age=iformation)




@app.route('/received', methods=['POST', 'GET'])
def received():
    valu = session['Email']
    if valu == 1:
        return render_template("login.html")
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="university_project"
    )
    mycursor = mydb.cursor()
    email = session['Email']
    mycursor.execute("select * from l_table where  Email='" + email + "'")
    information = mycursor.fetchone()
    name = information[0] + information[1]
    filename = 'Student_img/' + information[6]
    mydb.commit()
    mycursor.close()
    return render_template('received.html', name=name, filename=filename)


@app.route('/manage_received', methods=['POST', 'GET'])
def manage_received():
    valu = session['Email']
    if valu == 1:
        return render_template("login.html")
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="university_project"
    )
    mycursor = mydb.cursor()
    email = session['Email']
    if request.method == 'POST':
        issue_id=request.form['issue_id']

        mycursor.execute("select * from issue where issue_id='"+issue_id+"' ")
        information_issue=mycursor.fetchone()

        mycursor.execute("select * from issue where issue_id='" + issue_id + "' ")
        information_issuee = mycursor.fetchall()

        if len(information_issuee)==0:
            email = session['Email']
            mycursor.execute("select * from l_table where  Email='" + email + "'")
            information = mycursor.fetchone()
            name = information[0] + information[1]
            filename = 'Student_img/' + information[6]
            error="This issue id is not found "
            mydb.commit()
            mycursor.close()
            return render_template('received.html', name=name, filename=filename,error=error)

        issue_id=information_issue[0]
        st_name=information_issue[1]
        st_n_name=information_issue[2]
        st_id=information_issue[3]
        book_name=information_issue[4]
        book_id=information_issue[5]
        book_edition=information_issue[6]
        issue_date=information_issue[7]
        issue_last=date.today()
        mycursor.execute(
            "insert into receved (issue_id,student_name,student_l_name,student_id,book_name,book_pass_id,book_edition,issue_date,issue_last_date)value(%s,%s,%s,%s,"
            "%s,%s,%s,%s,%s)",
            (issue_id,st_name,st_n_name,st_id,book_name,book_id,book_edition,issue_date,issue_last))
        issue_id=str(issue_id)
        mycursor.execute("DELETE FROM issue WHERE issue_id='" + issue_id + "' ")
        mydb.commit()
        mycursor.close()
        return redirect('received')



@app.route('/History', methods=['POST', 'GET'])
def history():
    valu = session['Email']
    if valu == 1:
        return render_template("login.html")
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="university_project"
    )
    mycursor = mydb.cursor()
    email = session['Email']
    mycursor.execute("select * from l_table where  Email='" + email + "'")
    information = mycursor.fetchone()
    name = information[0] + information[1]
    filename = 'Student_img/' + information[6]
    mycursor.execute("select * from receved")
    information_re=mycursor.fetchall()
    mydb.commit()
    mycursor.close()
    return render_template('issue_History.html',name=name,filename=filename,information_res=information_re)

@app.route('/Notification', methods=['POST', 'GET'])
def Notification():
    notshow = session['student_login']
    if notshow == "logout":
        return redirect('/login')
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="university_project"
    )
    mycursor = mydb.cursor()
    email = session['student_login']
    mycursor.execute("select * from student_table where Email='"+email+"'")
    student_information=mycursor.fetchone()
    st_id=student_information[3]
    name=student_information[0] + student_information[1]
    filename = 'Student_img/' + student_information[7]
    mycursor.execute("select * from issue where student_id ='"+st_id+"' and age <3")
    issue_information=mycursor.fetchall()
    mydb.commit()
    mycursor.close()
    return render_template('Notification.Html' ,all=issue_information,name=name,filename=filename)




app.debug = True
app.run(host='0.0.0.0', port=8000)
