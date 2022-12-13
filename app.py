from flask import Flask, render_template, url_for, redirect, request, flash, jsonify, json
import mysql.connector

#connect to MySQL
def getMySqlConnection():
    return mysql.connector.connect(
        host="localhost",
        database="sekolah2",
        user="root",
        password="",
    )

# cursor.execute
def curExecGet(query, dictParam=False):
    db = getMySqlConnection()

    cur = db.cursor(dictionary=dictParam)
    cur.execute(query)

    data = cur.fetchall()
    cur.close()

    return data

def curExecPost(query):
    db = getMySqlConnection()

    cur = db.cursor()
    cur.execute(query)

    db.commit()
    cur.close()

# Fetch datas from database
def getDataSiswa():
    db = getMySqlConnection()
    cur = db.cursor()
    cur.execute("SELECT * from siswa")
    data_siswa = cur.fetchall()
    cur.close()
    return data_siswa


def getDataSiswaById(id):
    db = getMySqlConnection()
    cur = db.cursor()
    cur.execute("SELECT * from siswa WHERE nis={}".format(id))
    data_siswa = cur.fetchall()
    cur.close()
    return data_siswa


def getDataOrtu():
    db = getMySqlConnection()
    cur = db.cursor()
    cur.execute("SELECT * from orang_tua")
    data_ortu = cur.fetchall()
    cur.close()
    return data_ortu


def getDataOrtuById(id):
    db = getMySqlConnection()
    cur = db.cursor()
    cur.execute("SELECT * from orang_tua WHERE kode_ortu='{}'".format(id))
    data_ortu = cur.fetchall()
    cur.close()
    return data_ortu


def getDataGuru():
    db = getMySqlConnection()
    cur = db.cursor()
    cur.execute("SELECT * from guru")
    data_guru = cur.fetchall()
    cur.close()
    return data_guru


def getDataGuruById(id):
    db = getMySqlConnection()
    cur = db.cursor()
    cur.execute("SELECT * from guru WHERE nip='{}'".format(id))
    data_guru = cur.fetchall()
    cur.close()
    return data_guru


def getDataMapel():
    db = getMySqlConnection()
    cur = db.cursor()
    cur.execute("SELECT * from mapel")
    data_mapel = cur.fetchall()
    cur.close()
    return data_mapel


def getDataMapelById(id):
    db = getMySqlConnection()
    cur = db.cursor()
    cur.execute("SELECT * from mapel WHERE id_mapel={}".format(id))
    data_mapel = cur.fetchall()
    cur.close()
    return data_mapel


def getDataKelas():
    db = getMySqlConnection()
    cur = db.cursor()
    cur.execute("SELECT * from kelas")
    data_kelas = cur.fetchall()
    cur.close()
    return data_kelas


def getDataKelasById(id):
    db = getMySqlConnection()
    cur = db.cursor()
    cur.execute("SELECT * from kelas WHERE id_kelas='{}'".format(id))
    data_kelas = cur.fetchall()
    cur.close()
    return data_kelas


def getDataUser():
    db = getMySqlConnection()
    cur = db.cursor()
    cur.execute("SELECT * from pengguna")
    data_user = cur.fetchall()
    cur.close()
    return data_user


def getDataMengajar():
    db = getMySqlConnection()
    cur = db.cursor()
    cur.execute("SELECT * from mengajar")
    data_mengajar = cur.fetchall()
    cur.close()
    return data_mengajar


app = Flask(__name__)
app.secret_key = "ytta"


@app.route("/")
@app.route("/index")
def index():
    return render_template("landing/index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("index.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    db = getMySqlConnection()
    cur = db.cursor()

    if request.method == 'POST':
        user = request.form.get('user_form')
        email = request.form.get('email_form')
        password = request.form.get('pass_form')
        password2 = request.form.get('pass2_form')

        cur.execute("SELECT * FROM pengguna")
        data = cur.fetchall()
        print("data pada pengguna", data)
        cur.close()

        if data == []:
            if password == password2:
                db = getMySqlConnection()
                cur = db.cursor()

                query = '''INSERT INTO pengguna VALUES('{0}','{1}','{2}')'''
                cur.execute(query.format(user, email, password))
                db.commit()
                cur.close()
                flash("Registrasi berhasil! Silahkan login", "success")
            else:
                flash("Registrasi gagal! Kedua password tidak sama")
        else:
            db = getMySqlConnection()
            cur = db.cursor()

            cur.execute(
                "SELECT * FROM pengguna WHERE username='{}'".format(user))
            row = cur.fetchone()
            # print(row)
            cur.close()

            if row != None:
                flash('Username telah terdaftar! Gunakan username lain', 'error')
            else:
                db = getMySqlConnection()
                cur = db.cursor()

                cur.execute("SELECT email FROM pengguna")
                dataEmail = cur.fetchall()
                print(dataEmail)
                print("----")
                cur.close()

                emailArray = []
                for dataEmail2 in dataEmail:
                    for dataEmail3 in dataEmail2:
                        emailArray.append(dataEmail3)

                if not email in emailArray:
                    if password == password2:
                        db = getMySqlConnection()
                        cur = db.cursor()

                        query = '''INSERT INTO pengguna VALUES('{0}','{1}','{2}')'''
                        cur.execute(query.format(user, email, password))
                        db.commit()
                        cur.close()
                        flash("Registrasi berhasil! Silahkan login", "success")

                    else:
                        flash("Registrasi gagal! Kedua password tidak sama", "error")

                else:
                    flash("Email telah terdaftar! Gunakan email lain", "error")

    return render_template("account/register.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    db = getMySqlConnection()
    cur = db.cursor()

    if request.method == 'POST':
        user = request.form.get('user_form')
        password = request.form.get('pass_form')

        userQuery = "SELECT * FROM pengguna WHERE username=%s"
        cur.execute(userQuery, (user,))
        row = cur.fetchone()
        # print(row[1])
        cur.close()

        if row != None:
            if password == row[2]:
                return redirect(url_for("dashboard"))
            else:
                flash("Password yang Anda masukkan salah!")
        else:
            flash("Username tidak ditemukan!")

    return render_template("account/login.html")


@app.route("/guru")
def guru():
    
    data = curExecGet("SELECT * FROM guru", False)
    return render_template("guru.html", data=data)


@app.route("/insertGuru", methods=['POST'])
def insertGuru():

    nip = request.form.get('nip_form')
    nama = request.form.get('name_form')
    alamat = request.form.get('alamat_form')
    tempat = request.form.get('tempat_form')
    tanggalLahir = request.form.get('date_form')
    gender = request.form.get('gender_form')
    agama = request.form.get('agama_form')
    telepon = request.form.get('telepon_form')
    pendidikan = request.form.get('pendidikan_form')
    status = request.form.get('status_form')

    if 'add_button' in request.form:
        insertQuery = '''INSERT INTO guru VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}')'''
        curExecPost(insertQuery.format(nip, nama, alamat, tempat,
                                       tanggalLahir, gender, agama, telepon, pendidikan, status))

    elif 'edit_button' in request.form:
        updateQuery = "UPDATE guru SET nip='{0}',nama='{1}',alamat='{2}',tmp_lahir='{3}',tgl_lahir='{4}',gender='{5}',agama='{6}',telp='{7}',pendidikan='{8}',status='{9}' WHERE nip='{0}'"

        curExecPost(updateQuery.format(nip, nama, alamat, tempat,
                    tanggalLahir, gender, agama, telepon, pendidikan, status))

    return redirect(url_for("guru"))


@app.route("/hapusGuru/<int:nip>")
def hapusGuru(nip):

    curExecPost('''DELETE FROM guru WHERE nip={}'''.format(nip))

    return redirect(url_for("guru"))


@app.route("/siswa")
def siswa():

    queryKdOrtu = '''SELECT kode_ortu, nama_ortu FROM orang_tua'''
    queryIdKelas = '''SELECT id_kelas, nama_kelas FROM kelas'''
    queryData = '''SELECT * FROM siswa'''
    queryOrtuKelas = "SELECT * FROM siswa INNER JOIN orang_tua ON orang_tua.kode_ortu = siswa.kode_ortu INNER JOIN kelas ON kelas.id_kelas = siswa.id_kelas"

    kode_ortu=curExecGet(queryKdOrtu, True)
    data = curExecGet(queryData, True)
    OrtuKelas = curExecGet(queryOrtuKelas, True)
    # print(OrtuKelas)
    id_kelas = curExecGet(queryIdKelas, True)

    # print("+++++")
    # print(kode_ortu)

    return render_template("siswa.html", kode_ortu=kode_ortu, data=data, OrtuKelas=OrtuKelas, id_kelas=id_kelas)


@app.route("/insertSiswa", methods=['GET', 'POST'])
def insertSiswa():
    db = getMySqlConnection()
    cur = db.cursor()

    nis = request.form.get('nis_form')
    nama = request.form.get('name_form')
    alamat = request.form.get('alamat_form')
    tempat_lahir = request.form.get('tempat_form')
    tanggal_lahir = request.form.get('date_form')
    gender = request.form.get('gender_form')
    agama = request.form.get('agama_form')
    id_kelas = request.form.get('idkelas_form')
    kodeortu = request.form.get('kodeortu_form')
    daftar = request.form.get('daftar_form')

    if 'add_button' in request.form:
        insertQuery = "INSERT INTO siswa VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}')"
        curExecPost(insertQuery.format(nis, nama, alamat, tempat_lahir,
                    tanggal_lahir, gender, agama, id_kelas, kodeortu, daftar))
        # print(nis, nama, alamat, tempat_lahir, tanggal_lahir, gender, agama, id_kelas, kodeortu, daftar)

    elif 'edit_button' in request.form:
        # print(nis, nama, alamat, tempat_lahir, tanggal_lahir, gender, agama, id_kelas, kodeortu, daftar)
        insertQuery = "UPDATE siswa SET nama_siswa='{1}', alamat='{2}', tmp_lahir='{3}', tgl_lahir='{4}', gender='{5}', agama='{6}', id_kelas='{7}', kode_ortu='{8}', tgl_daftar='{9}' WHERE nis='{0}'"
        curExecPost(insertQuery.format(nis, nama, alamat, tempat_lahir,
                    tanggal_lahir, gender, agama, id_kelas, kodeortu, daftar))

    return redirect(url_for("siswa"))


@app.route("/hapusSiswa/<int:nis>")
def hapusSiswa(nis):

    curExecPost('''DELETE FROM siswa WHERE nis={}'''.format(nis))

    return redirect(url_for("siswa"))


@app.route("/orangtua")
def orangtua():

    data = curExecGet("SELECT * FROM orang_tua")

    return render_template("orangtua.html", data=data)


@app.route("/insertOrangtua", methods=['POST'])
def insertOrangtua():

    kodeortu = request.form.get('kodeortu_form')
    nama = request.form.get('name_form')
    alamat = request.form.get('alamat_form')
    telepon = request.form.get('telepon_form')
    pekerjaan = request.form.get('pekerjaan_form')
    agama = request.form.get('agama_form')
    status = request.form.get('status_form')

    if 'add_button' in request.form:
        insertQuery = '''INSERT INTO orang_tua VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}')'''
        curExecPost(insertQuery.format(kodeortu, nama, alamat,
                    telepon, pekerjaan, agama, status))

    elif 'edit_button' in request.form:

        updateQuery = "UPDATE orang_tua SET nama_ortu='{1}',alamat='{2}',telp='{3}', pekerjaan='{4}', agama='{5}', status='{6}' WHERE kode_ortu='{0}'"

        curExecPost(updateQuery.format(kodeortu, nama, alamat,
                    telepon, pekerjaan, agama, status))

    return redirect(url_for("orangtua"))


@app.route("/hapusOrangtua/<int:kode_ortu>")
def hapusOrangtua(kode_ortu):

    curExecPost('''DELETE FROM orang_tua WHERE kode_ortu={}'''.format(kode_ortu))

    return redirect(url_for("orangtua"))


@app.route("/mapel")
def mapel():

    data = curExecGet("SELECT * FROM mapel")

    return render_template("mapel.html", data=data)


@app.route("/insertMapel", methods=['POST'])
def insertMapel():
    id_mapel = request.form.get('idMapel_form')
    data_mapel = request.form.get('mapel_form')

    if 'add_button' in request.form:
        insertQuery = '''INSERT INTO mapel VALUES('{0}','{1}')'''.format(
            id_mapel, data_mapel)
        curExecPost(insertQuery)
    elif 'edit_button' in request.form:
        updateQuery = "UPDATE mapel SET nama_mapel='{1}' WHERE id_mapel='{0}'".format(
            id_mapel, data_mapel)
        curExecPost(updateQuery)

    return redirect(url_for("mapel"))


@app.route("/hapusMapel/<int:id_mapel>")
def hapusMapel(id_mapel):

    curExecPost('''DELETE FROM mapel WHERE id_mapel={}'''.format(id_mapel))

    return redirect(url_for("mapel"))


@app.route("/mengajar")
def mengajar():

    queryDataGuru = "SELECT * FROM mengajar INNER JOIN guru ON mengajar.nip=guru.nip INNER JOIN mapel ON mengajar.id_mapel=mapel.id_mapel"
    data_guru = curExecGet(queryDataGuru, True)

    return render_template("mengajar.html", data_guru=data_guru)


@app.route("/kelas")
def kelas():
    queryData = "SELECT * FROM kelas INNER JOIN guru ON kelas.nip=guru.nip"
    data = curExecGet(queryData, True)

    queryDataGuru = "SELECT * from guru"
    dataGuru = curExecGet(queryDataGuru, True)

    # print(data)

    return render_template("kelas.html", data=data, dataGuru=dataGuru)


@app.route("/insertKelas/", methods=['GET', 'POST'])
def insertKelas():
    id_kelas = request.form.get('idKelas_form')
    nama_kelas = request.form.get('namaKelas_form')
    nama_guru = request.form.get('guru_form')

    if 'add_button' in request.form:
        insertQuery = "INSERT INTO kelas VALUES ('{0}','{1}','{2}')"

        curExecPost(insertQuery.format(id_kelas, nama_kelas, nama_guru))

    elif 'edit_button' in request.form:
        updateQuery = "UPDATE kelas SET nama_kelas='{1}', nip='{2}' WHERE id_kelas='{0}'"

        curExecPost(updateQuery.format(id_kelas, nama_kelas, nama_guru))

    # print("+========++=========",id_kelas, nama_kelas, nama_guru)

    return redirect(url_for("kelas"))


@app.route('/api/')
def api():
    return render_template("api.html")


@app.route("/api/insertGuru", methods=['POST'])
def api_insertGuru():

    nip = request.form.get('nip_form')
    nama = request.form.get('name_form')
    alamat = request.form.get('alamat_form')
    tempat = request.form.get('tempat_form')
    tanggalLahir = request.form.get('date_form')
    gender = request.form.get('gender_form')
    agama = request.form.get('agama_form')
    telepon = request.form.get('telepon_form')
    pendidikan = request.form.get('pendidikan_form')
    status = request.form.get('status_form')

    insertQuery = '''INSERT INTO guru VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}')'''
    curExecPost(insertQuery.format(nip, nama, alamat, tempat,
                                   tanggalLahir, gender, agama, telepon, pendidikan, status))

    return jsonify({"msg": "Data berhasil dimasukkan",
                    "kode": "666"})


@app.route("/api/insertSiswa", methods=['POST'])
def api_insertSiswa():

    nis = request.form.get('nis_form')
    nama = request.form.get('name_form')
    alamat = request.form.get('alamat_form')
    tempat_lahir = request.form.get('tempat_form')
    tanggal_lahir = request.form.get('date_form')
    gender = request.form.get('gender_form')
    agama = request.form.get('agama_form')
    id_kelas = request.form.get('idkelas_form')
    kodeortu = request.form.get('kodeortu_form')
    daftar = request.form.get('daftar_form')

    insertQuery = "INSERT INTO siswa VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}')"
    curExecPost(insertQuery.format(nis, nama, alamat, tempat_lahir,
                                   tanggal_lahir, gender, agama, id_kelas, kodeortu, daftar))

    return jsonify({"msg": "Data berhasil dimasukkan",
                    "kode": "666"})


@app.route("/api/insertOrangtua", methods=['POST'])
def api_insertOrangtua():

    kodeortu = request.form.get('kodeortu_form')
    nama = request.form.get('name_form')
    alamat = request.form.get('alamat_form')
    telepon = request.form.get('telepon_form')
    pekerjaan = request.form.get('pekerjaan_form')
    agama = request.form.get('agama_form')
    status = request.form.get('status_form')

    insertQuery = '''INSERT INTO orang_tua VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}')'''
    curExecPost(insertQuery.format(kodeortu, nama, alamat,
                                   telepon, pekerjaan, agama, status))

    return jsonify({"msg": "Data berhasil dimasukkan",
                    "kode": "666"})


@app.route("/api/insertMapel", methods=['POST'])
def api_insertMapel():

    id_mapel = request.form.get('idMapel_form')
    data_mapel = request.form.get('mapel_form')

    insertQuery = '''INSERT INTO mapel VALUES('{0}','{1}')'''.format(
        id_mapel, data_mapel)
    curExecPost(insertQuery)

    return jsonify({"msg": "Data berhasil dimasukkan",
                    "kode": "666"})


@app.route("/api/insertKelas/", methods=['POST'])
def api_insertKelas():

    id_kelas = request.form.get('idKelas_form')
    nama_kelas = request.form.get('namaKelas_form')
    nama_guru = request.form.get('guru_form')

    insertQuery = "INSERT INTO kelas VALUES ('{0}','{1}','{2}')"

    curExecPost(insertQuery.format(id_kelas, nama_kelas, nama_guru))

    return jsonify({"msg": "Data berhasil dimasukkan",
                    "kode": "666"})


@app.route('/api/kelas')
def api_kelas():
    data_kelas = getDataKelas()

    kelas = {}
    kelas['data_kelas'] = []
    for row in data_kelas:
        content = {"kelas": row[1], "nip": row[2]}
        kelas['data_kelas'].append(content)

    return jsonify(kelas)


@app.route('/api/kelasById/<int:id>')
def api_kelasById(id):
    data_kelas = getDataKelasById(id)

    kelas = {}
    kelas['data_kelas'] = []
    for row in data_kelas:
        content = {"kelas": row[1], "nip": row[2]}
        kelas['data_kelas'].append(content)

    return jsonify(kelas)


@app.route('/api/orang_tua')
def api_ortu():
    data_ortu = getDataOrtu()

    orangtua = {}
    orangtua['data_orangtua'] = []
    for row in data_ortu:
        content = {"nama": row[1], "alamat": row[2], "telp": row[3],
                   "pekerjaan": row[4], "agama": row[5], "status": row[6]}
        orangtua['data_orangtua'].append(content)

    return jsonify(orangtua)


@app.route('/api/orang_tuaById/<int:id>')
def api_ortuById(id):
    data_ortu = getDataOrtuById(id)

    orangtua = {}
    orangtua['data_orangtua'] = []
    for row in data_ortu:
        content = {"nama": row[1], "alamat": row[2], "telp": row[3],
                   "pekerjaan": row[4], "agama": row[5], "status": row[6]}
        orangtua['data_orangtua'].append(content)

    return jsonify(orangtua)


@app.route('/api/guru')
def api_guru():
    data_guru = getDataGuru()

    guru = {}
    guru['data_guru'] = []
    for row in data_guru:
        content = {"nama": row[1], "alamat": row[2], "tmp_lahir": row[3], "tgl_lahir": str(
            row[4]), "gender": row[5], "agama": row[6], "telp": row[7], "pendidikan": row[8], "status": row[9]}
        guru['data_guru'].append(content)

    return jsonify(guru)


@app.route('/api/guruById/<int:id>')
def api_guruById(id):
    data_guru = getDataGuruById(id)

    guru = {}
    guru['data_guru'] = []
    for row in data_guru:
        content = {"nama": row[1], "alamat": row[2], "tmp_lahir": row[3], "tgl_lahir": str(
            row[4]), "gender": row[5], "agama": row[6], "telp": row[7], "pendidikan": row[8], "status": row[9]}
        guru['data_guru'].append(content)

    return jsonify(guru)


@app.route('/api/siswa')
def api_siswa():
    data_siswa = getDataSiswa()

    siswa = {}
    siswa['data_siswa'] = []
    for row in data_siswa:
        content = {"nama": row[1], "alamat": row[2], "tmp_lahir": row[3], "tgl_lahir": str(
            row[4]), "gender": row[5], "agama": row[6], "id_kelas": row[7], "kd_ortu": row[8], "tgl_daftar": str(row[9])}
        siswa['data_siswa'].append(content)

    return jsonify(siswa)


@app.route('/api/siswaById/<int:id>')
def api_siswaById(id):
    data_siswa = getDataSiswaById(id)

    siswa = {}
    siswa['data_siswa'] = []
    for row in data_siswa:
        content = {"nama": row[1], "alamat": row[2], "tmp_lahir": row[3], "tgl_lahir": str(
            row[4]), "gender": row[5], "agama": row[6], "id_kelas": row[7], "kd_ortu": row[8], "tgl_daftar": str(row[9])}
        siswa['data_siswa'].append(content)

    return jsonify(siswa)


@app.route('/api/mapel')
def api_mapel():
    data_mapel = getDataMapel()

    mapel = {}
    mapel['data_mapel'] = []
    for row in data_mapel:
        content = {"mapel": row[1]}
        mapel['data_mapel'].append(content)

    return jsonify(mapel)


@app.route('/api/mapelById/<int:id>')
def api_mapelById(id):
    data_mapel = getDataMapelById(id)

    mapel = {}
    mapel['data_mapel'] = []
    for row in data_mapel:
        content = {"mapel": row[1]}
        mapel['data_mapel'].append(content)

    return jsonify(mapel)


@app.route('/api/mengajar')
def api_mengajar():
    data_mengajar = getDataMengajar()

    mengajar = {}
    mengajar['data_mengajar'] = []
    for row in data_mengajar:
        content = {"id_mapel": row[1]}
        mengajar['data_mengajar'].append(content)

    return jsonify(mengajar)


if __name__ == '__main__':
    app.run(debug=True)
