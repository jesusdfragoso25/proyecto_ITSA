from MySQLdb.cursors import Cursor
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask.wrappers import Request
from flask_mysqldb import MySQL
from datetime import date, datetime
import re



app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'reporte'
mysql = MySQL(app)

app.secret_key = "mysecretkey"

#<--Redirección a las paginas-->
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/link_registro')
def p_register():
    datos=['','','','','','','','']
    return render_template('register.html', datos=datos)

@app.route('/link_login')
def p_login():
    return render_template('login.html')

@app.route('/link_reportes')
def p_reportes():
    return render_template('reportes.html')

@app.route('/link_verperfil')
def ver_pe():
    return render_template('perfil.html')

@app.route('/link_editar')
def a_zar():
    return render_template('editperfil.html')

@app.route('/link_busqueda')
def p_buscar():
    busquedas = " "
    return render_template('busqueda.html', busquedas=busquedas)

@app.route('/link_cambiarcontrasena')
def cambiar():
    return render_template('cambiarcon.html')

@app.route('/link_olv_pass')
def olv_pass():
    return render_template('olvido_pass.html')

@app.route('/link_formulario pqr')
def for_pqr():
    return render_template('form_pqr.html')

@app.route('/link_pqr')
def pqr():
    return render_template('pqr.html')

@app.route('/link_transparencia')
def p_transparencia():
    return render_template('ley_transparencia.html')

@app.route('/crear_patrulla')
def pt_lla():
    return render_template('patrulla.html')

@app.route('/link_tratamiento')
def p_tratamiento():
    return render_template('tratamiento_datos.html')
#<--Fin de la redirección(solo redireccionan)-->

#Formulario de registro
@app.route('/register', methods=['POST'])
def register():
    msg=''
    if  request.method == 'POST':
        nombre = request.form['nombre']
        documento = request.form['documento']
        telefono = request.form['telefono']
        fecha_nac = request.form['fecha_nac']
        pais = request.form['pais']
        ciudad = request.form['ciudad']
        email = request.form['email']
        password = request.form['password']
        conf_password = request.form['conf_password']
        datos = [nombre,documento,telefono,fecha_nac,ciudad,email]
        
        #Comprobar si el email existe
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM usuario WHERE email = %s', [str(email)])
        emails = cursor.fetchone()
        cursor.close()
        if emails:
            msg="Ya existe un usuario registrado con el correo indicado"
            return render_template('register.html', datos=datos, msg=msg)

        #Comprobación de contraseñas
        if(password==conf_password):
            if len(password)<8:
                msg="La contraseña no cumple con la longitud requerida (8 caracteres como mínimo)"
                return render_template('register.html', datos=datos, msg=msg)
            elif re.search('[0-9]',password) is None:
                msg = "La contraseña debe contener al menos un caracter númerico"
                return render_template('register.html', datos=datos, msg=msg)
            elif re.search('[A-Z]',password) is None:
                msg = "La contraseña debe contar con al menos un Caracter en Mayúscula"
                return render_template('register.html', datos=datos, msg=msg)
        else:
            msg = "Las contraseñas no coinciden"
            return render_template('register.html', datos=datos, msg=msg)

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO usuario (nombre, documento, telefono, fecha_nac, pais, ciudad, email, password, id_rol) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
        (nombre,documento,telefono,fecha_nac,pais,ciudad,email,password,1))
        mysql.connection.commit()
        msg = 'Se ha creado la cuenta correctamente'
        return render_template('login.html', msg=msg)

#Formulario de inicio de sesion
@app.route('/login', methods=['POST'])
def login():
    msg=''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM usuario WHERE email = %s AND password = %s', (email, password))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['id'] = user[0]
            session['documento'] = user[1]
            session['nombre'] = user[2]
            session['telefono'] = user[3]
            session['fecha_nac'] = user[4].isoformat()
            session['pais'] = user[5]
            session['ciudad'] = user[6]
            session['email'] = user[7]
            session['id_rol'] = user[9]
            return redirect(url_for('index'))
        else:
            # cuenta no existe
            msg = 'Usuario / Contraseña incorrecto!'

    return render_template('login.html', msg=msg)

#Cumple con la funcion de modificar los datos personales del usuario.
@app.route('/actualizar/<id>', methods=['POST'])
def edit_pe(id):
    msg=''
    if request.method == 'POST':
        nombre=request.form['nombre']
        telefono=request.form['telefono']
        fecha_nac=request.form['fecha_nac']
        pais=request.form['pais']
        ciudad=request.form['ciudad']
        email=request.form['email']
        cur= mysql.connection.cursor()
        cur.execute('UPDATE usuario SET nombre=%s,telefono=%s, fecha_nac=%s,pais=%s,ciudad=%s,email=%s WHERE id_usuario=%s',(nombre,telefono,fecha_nac,pais,ciudad,email, str(id)))
        mysql.connection.commit()
        session['nombre'] = nombre
        session['telefono'] = telefono
        session['fecha_nac'] = fecha_nac
        session['pais'] = pais
        session['ciudad'] = ciudad
        session['email'] = email
        msg = 'Se ha actualizado la información correctamente '
        return render_template('perfil.html', msg=msg)

#Cerrar sesion
@app.route('/logout')
def logout():
    # removemos los datos de la sesión para cerrar sesión
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('nombre', None)
    session.pop('documento', None)
    session.pop('telefono', None)
    session.pop('fecha_nac', None)
    session.pop('pais', None)
    session.pop('ciudad', None)
    session.pop('email', None)
    session.pop('id_rol', None)
    # Redirige a la pagina de login
    return redirect(url_for('p_login'))

#Almacena la informacion con respecto al reporte.
@app.route('/reporte', methods=['POST'])
def reporte():
    msg=''
    if  request.method == 'POST':
        fecha_reporte = datetime.now()
        id_usuario = session['id']
        documento = request.form['documento']
        poliza = request.form['poliza']
        barrio = request.form['barrio']
        direccion_rep = request.form['direccion_rep']
        id_basura = request.form['id_basura']
        descripcion = request.form['descripcion']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO reporte (documento, poliza, barrio, direccion_rep, fecha_reporte, descripcion, estado, id_usuario, id_basura,id_patrulla) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
        (documento, poliza, barrio, direccion_rep, fecha_reporte, descripcion,"Pendiente", id_usuario, id_basura,1))
        mysql.connection.commit()
        msg = 'Se ha generado el reporte correctamente'
        return render_template('reportes.html', msg=msg)

#Almacena la informacion con respecto a las patrullas
@app.route('/patrulla', methods=['POST'])
def patrulla():
    msg=''
    if  request.method == 'POST':
        nombre = request.form['nombre']
        placa = request.form['placa']
        id_basura = request.form['id_basura']
        cur= mysql.connection.cursor()
        cur.execute('SELECT placa_patrulla FROM patrulla WHERE placa_patrulla=%s',[str(placa)])
        data = cur.fetchone()
        cur.close()
        if data:
            msg = 'Este camion ya se encuentra registrado'
            return render_template('patrulla.html', msg=msg)
        else:
            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO patrulla (nombre, placa_patrulla, id_basura) VALUES (%s, %s, %s)',
            (nombre, placa, id_basura))
            mysql.connection.commit()
            msg = 'Se ha agregado la patrulla'
            return render_template('patrulla.html', msg=msg)

#Visualizacion de una tabla que contiene los reporte generados por el usuario.
@app.route('/linkhistorial')
def h_ry():
    cur= mysql.connection.cursor()
    cur.execute('SELECT * FROM reporte WHERE id_usuario = %s order by fecha_reporte Desc',[str(session['id'])])
    data = cur.fetchall()
    return render_template('historial.html', reporte = data)

#Modulo que permite ver más información con respecto a un reporte.
@app.route('/verdetalles/<id>')
def det_es(id):
    cur= mysql.connection.cursor()
    cur.execute('SELECT u.nombre, u.documento,u.telefono,u.email,r.poliza,r.barrio, r.direccion_rep, t.tipo_basura, r.descripcion, p.id_patrulla, r.estado, r.codigo_reporte from usuario u, reporte r, tipo_basura t, patrulla p WHERE u.id_usuario = r.id_usuario and r.codigo_reporte = %s and t.id_basura=r.id_basura and p.id_patrulla=r.id_patrulla;',[str(id)])
    data1 = cur.fetchone()
    cur.close()

    cur= mysql.connection.cursor()
    cur.execute('SELECT DISTINCT p.id_patrulla, p.nombre from reporte r, patrulla p WHERE p.id_basura=r.id_basura and r.id_basura = (SELECT id_basura from reporte WHERE codigo_reporte= %s)', [str(id)])
    data2 = cur.fetchall()
    cur.close()
    return render_template('detalles.html', detalles=data1, patrullas=data2)

#El administrador puede realizar los cambios y actualizarlos en la base de datos.
@app.route('/guardar_detalles/<id>', methods=['POST'])
def guardar_detalles(id):
    if request.method == 'POST':
        id_patrulla = request.form['id_patrulla']
        estado = request.form['estado']
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE reporte SET id_patrulla=%s,estado=%s where codigo_reporte = %s', (id_patrulla,estado,id))
        mysql.connection.commit()
        msg = 'Se ha actualizado el reporte correctamente'
        return redirect(url_for('rep_t'))

@app.route('/frormulariopqr', methods=['POST'])
def f_pqr():
    msg=''
    msg = 'formulario PQR enviado correctamente'
    return render_template('pqr.html', msg=msg)

#Le permite modificar la contraseña
@app.route('/cambiar_contrasena/<id>', methods=['POST'])
def ca_biar(id):
    msg=''
    if request.method == 'POST':
        password_act=request.form['password_act']
        password=request.form['password']
        confpassword=request.form['conf_password']

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT password FROM usuario WHERE id_usuario=%s',([str(id)]))
        passwd=cursor.fetchone()
        cursor.close()


        if password_act==passwd[0]:#si la contraseña actual es igual a la colocada en el cuadro de texto entonces pasara a verificar
            if password==confpassword: #si la contraseña que ingreso no coincide con la de confirmacion 
                if len(password)<8:#Debe contener al menos 8 caracteres , sino le mandara un mensaje de advertencia
                    msg="La contraseña no cumple con la longitud requerida (8 caracteres como mínimo)"
                    return render_template('cambiarcon.html', msg=msg)
                elif re.search('[0-9]',password) is None:#Debe contener al menos un numero , sino le mandara un mensaje de advertencia
                    msg = "La contraseña debe contener al menos un caracter númerico"
                    return render_template('cambiarcon.html', msg=msg)
                elif re.search('[A-Z]',password) is None:#Debe contener al menos una mayuscula, sino le mandara un mensaje de advertencia
                    msg = "La contraseña debe contar con al menos un Caracter en Mayúscula"
                    return render_template('cambiarcon.html', msg=msg)
            else:
                msg = 'Las contraseñas no coinciden' 
                return render_template('cambiarcon.html', msg=msg)
        else:
            msg = 'La contraseña actual no es correcta'
            return render_template('cambiarcon.html', msg=msg)
    cur= mysql.connection.cursor()
    cur.execute('UPDATE usuario SET password=%s WHERE id_usuario=%s',(password, str(id)))#Actualizara la contraseña basada en la ID del usuario
    mysql.connection.commit()
    msg = 'La contraseña se ha actualizado satisfactoriamente'
    return render_template('perfil.html', msg=msg)

#Modulo - ¿Olvido su contraseña?
@app.route('/link_conf_datos', methods=['POST'] )
def conf_pss():
    msg=''
    
    if request.method == 'POST':
        email = request.form['email']
        documento = request.form['documento']
        password=request.form['password']
        confpassword=request.form['conf_password']
        datos=[email,documento]
        
        cur= mysql.connection.cursor()
        cur.execute('SELECT email, documento FROM usuario WHERE email=%s AND documento=%s', (email,documento))
        data = cur.fetchall()
        print (data)
        if data:
            if(password==confpassword):
                if len(password)<8:
                    msg="La contraseña no cumple con la longitud requerida (8 caracteres como mínimo)"
                    return render_template('olvido_pass.html', datos=datos, msg=msg)
                elif re.search('[0-9]',password) is None:
                    msg = "La contraseña debe contener al menos un caracter númerico"
                    return render_template('olvido_pass.html', datos=datos, msg=msg)
                elif re.search('[A-Z]',password) is None:
                    msg = "La contraseña debe contar con al menos un Caracter en Mayúscula"
                    return render_template('olvido_pass.html', datos=datos, msg=msg)
            else:
                msg = "Las contraseñas no coinciden"
                return render_template('olvido_pass.html', datos=datos, msg=msg)
        else:
            msg = "El email o el documento no coinciden"
            return render_template('olvido_pass.html', datos=datos, msg=msg)

    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE usuario SET password=%s WHERE documento=%s',(password, documento))
    mysql.connection.commit()
    msg = 'Contraseña actualizada correctamente'
    return render_template('login.html', msg=msg)

#Busqueda especifica - Permite buscar cierto tipo de datos ya sea (Documento,codigo_reporte o email).
@app.route('/busqueda_esp', methods=['POST'])
def bus_esp():
 if request.method == 'POST':
    cuadro=request.form['buscar_es']
    seleccion=request.form['bus_es']
    cur= mysql.connection.cursor()

    if seleccion == 'documento':
        cur.execute('SELECT * FROM reporte where documento = %s order by fecha_reporte Desc',([str(cuadro)]))
        data = cur.fetchall()
        cur.close()
        cur= mysql.connection.cursor()
        cur.execute('SELECT count(*) FROM reporte where documento = %s GROUP BY documento ',([str(cuadro)]))
        data1= cur.fetchone()
        cur.close()

    if seleccion == 'codigo_reporte':
        cur.execute('SELECT * FROM reporte where codigo_reporte = %s order by fecha_reporte Desc ',([str(cuadro)]))
        data = cur.fetchall()
        cur.close()
        cur= mysql.connection.cursor()
        cur.execute('SELECT count(*) FROM reporte where codigo_reporte = %s  GROUP BY codigo_reporte ',([str(cuadro)]))
        data1= cur.fetchone()
        cur.close()

    if seleccion == 'email':
        cur.execute('SELECT * FROM reporte r, usuario u where u.id_usuario = r.id_usuario AND email = %s order by r.fecha_reporte Desc',([str(cuadro)]))
        data = cur.fetchall()
        cur.close()
        cur= mysql.connection.cursor()
        cur.execute('SELECT count(*) FROM reporte r, usuario u where u.id_usuario = r.id_usuario AND email = %s GROUP BY r.id_usuario',([str(cuadro)]))
        data1= cur.fetchone()
        cur.close()
    return render_template('busqueda.html', reporte = data, busquedas=data1)

#Busqueda General - Permite observar de forma mas general algun reporte filtrando atravez de barrio,fecha incio o fin y estado.
@app.route('/busqueda_gen', methods=['POST'])
def bus_gen():
    if request.method == 'POST':
        barrio=request.form['barrio']
        estado=request.form['estado']
        fecha_start=request.form['fecha_start']
        fecha_end=request.form['fecha_end']
        if fecha_start == "": # Si no se especifica la fecha de inicio se toma una fecha antigua donde no existan reportes 
            fecha_start = '2015/01/01'
        else: #si se especificó se le agrega la hora, minuto y segundo para que busque desde el inicio de ese dia
            fecha_start = fecha_start + " 00:00:00"

        if fecha_end == "": # Si no se especifica fecha final, se toma la hora actual para tener como limite esta fecha
            fecha_end = datetime.now()
        else: #Si se especifica la fecha final, se le agrega la hora, minuto y segundo, del final del dia para tomar todos los reportes
            fecha_end = fecha_end + " 23:59:59"
        
        cur= mysql.connection.cursor() #Busqueda sin especificar "Estado"
        if (estado==""):

            #Busqueda para añadir datos a la tabla
            cur.execute('SELECT * FROM reporte where barrio = %s AND fecha_reporte between %s and %s order by fecha_reporte Desc', (barrio, fecha_start, fecha_end))
            data = cur.fetchall()
            cur.close()

            #Busqueda para obtener el numero de reportes encontrados
            cur= mysql.connection.cursor()
            cur.execute('SELECT count(*) FROM reporte where barrio = %s AND fecha_reporte between %s and %s', (barrio, fecha_start, fecha_end))
            data1=cur.fetchone()
            cur.close()
            
            #Busqueda para obtener el numero de reportes encontrados por cada tipo de estado
            cur= mysql.connection.cursor()
            cur.execute('SELECT estado, count(*) FROM reporte where barrio = %s AND fecha_reporte between %s and %s group by estado', (barrio, fecha_start, fecha_end))
            data2=cur.fetchall()
            cur.close()

        else: #Busqueda especificando "Estado"
            #Busqueda para añadir datos a la tabla
            cur.execute('SELECT * FROM reporte where barrio = %s AND estado = %s AND fecha_reporte between %s and %s order by fecha_reporte Desc', (barrio, estado, fecha_start, fecha_end))
            data = cur.fetchall()
            cur.close()

            #Busqueda para obtener el numero de reportes encontrados.
            cur= mysql.connection.cursor()
            cur.execute('SELECT count(*) FROM reporte where barrio = %s AND estado = %s AND fecha_reporte between %s and %s', (barrio, estado, fecha_start, fecha_end))
            data1=cur.fetchone()
            cur.close()

            #Busqueda para obtener el numero de reportes encontrados por el estado escogido.
            cur= mysql.connection.cursor()
            cur.execute('SELECT estado, count(*) FROM reporte where barrio = %s AND estado = %s AND fecha_reporte between %s and %s group by estado', (barrio, estado, fecha_start, fecha_end))
            data2=cur.fetchall()
            cur.close()
        return render_template('busqueda.html', reporte = data, busquedas=data1, estados=data2)

#Pestaña que permite visualizar aquellos reportes que se encuentren en estado pendiente.
@app.route('/reportes_pendiente')
def rep_p():
    estado = "Pendiente"
    cur= mysql.connection.cursor()
    cur.execute('SELECT * FROM reporte WHERE estado = %s order by fecha_reporte Desc', [str(estado)])
    data = cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute('SELECT estado ,count(*) FROM reporte WHERE estado = %s GROUP BY %s', ([str(estado)],[str(estado)]))
    data1 = cur.fetchall()
    cur.close()
    return render_template('reporte_gen.html', reporte = data, estados=data1, n_estado=estado)

#Pestaña que permite visualizar aquellos reportes que se encuentren en estado de "en proceso".
@app.route('/reportes_enproceso')
def rep_ep():
    estado = "En proceso"
    cur= mysql.connection.cursor()
    cur.execute('SELECT * FROM reporte WHERE estado = %s  order by fecha_reporte Desc', [str(estado)])
    data = cur.fetchall()
    cur.close()
    cur = mysql.connection.cursor()
    cur.execute('SELECT estado ,count(*) FROM reporte WHERE estado = %s GROUP BY %s', ([str(estado)],[str(estado)]))
    data1 = cur.fetchall()
    cur.close()
    return render_template('reporte_gen.html', reporte = data, estados=data1, n_estado=estado)

#Pestaña que permite visualizar aquellos reportes que se encuentren recolectados.
@app.route('/reportes_recolectado')
def rep_re():
    estado = "Recolectado"
    cur= mysql.connection.cursor()
    cur.execute('SELECT * FROM reporte WHERE estado = %s  order by fecha_reporte Desc', [str(estado)])
    data = cur.fetchall()
    cur.close()
    cur = mysql.connection.cursor()
    cur.execute('SELECT estado ,count(*) FROM reporte WHERE estado = %s GROUP BY %s', ([str(estado)],[str(estado)]))
    data1 = cur.fetchall()
    cur.close()
    return render_template('reporte_gen.html', reporte = data, estados=data1, n_estado=estado)

#Pestaña que permite visualizar aquellos reportes que se hayan cancelado por algun motivo.
@app.route('/reportes_cancelado')
def rep_ca():
    estado = "Cancelado"
    cur= mysql.connection.cursor()
    cur.execute('SELECT * FROM reporte WHERE estado = %s  order by fecha_reporte Desc', [str(estado)])
    data = cur.fetchall()
    cur.close()
    cur = mysql.connection.cursor()
    cur.execute('SELECT estado ,count(*) FROM reporte WHERE estado = %s GROUP BY %s', ([str(estado)],[str(estado)]))
    data1 = cur.fetchall()
    print(data1)
    cur.close()
    return render_template('reporte_gen.html', reporte = data, estados=data1, n_estado=estado)

#Pestaña que permite visualizar todos los reporte sin importar su estado.
@app.route('/reportes_todos')
def rep_t():
    cur= mysql.connection.cursor()
    cur.execute('SELECT * FROM reporte  order by fecha_reporte Desc')
    data = cur.fetchall()
    cur.close()
    cur = mysql.connection.cursor()
    cur.execute('SELECT estado ,count(*) FROM reporte GROUP BY estado')
    data1 = cur.fetchall()
    cur.close()
    cur = mysql.connection.cursor()
    cur.execute('SELECT count(*) FROM reporte')
    data2 = cur.fetchone()
    cur.close()
    return render_template('reportes_t.html', reporte = data, estados=data1, total=data2)


if __name__ == '__main__':
    app.run(port = 3000, debug = True)
