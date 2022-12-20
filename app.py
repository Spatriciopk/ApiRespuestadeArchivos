from flask import Flask, render_template, request,redirect,url_for,flash,jsonify,send_file,send_from_directory
import main as m

import os
from fpdf import FPDF
from os import remove,getcwd
from datetime import datetime
PATH_FILE = getcwd()+"/files/"

app = Flask(__name__)
listClients=[]
datalist = []
informacion =   {
        'numContrato' :  "",
        'strNombre' :  "",
        'strStatus' :  "",
        'strTipoPlan' :  "",
        'strCedula' :  ""
        }
datalist=[informacion]

def cargarDatos():
    data = m.connection()
    global listClients
    global datalist
    listClients=[] 
    for x in data:
        cliente ={
    'intContrato':x[0],
    'strNombre':x[1].rstrip(),
    'strIdplan':x[3],
    'strStatus':x[2]
    }
        listClients.append(cliente)


@app.route('/')
def index():
    global listClients
    cargarDatos()
    return render_template('index.html', dicData=listClients,contrato=datalist)


@app.route('/modal/<id>')
def modal(id):
    global listClients
    global datalist
    data = m.searchdata(id)
    cedulaAfiliado = data[0][5]
    dataAfiliado = m.searchAfilicado(cedulaAfiliado)

    informacion =   {
        'numContrato' :  data[0][0],
        'strNombre' :  data[0][1],
        'strStatus' :  data[0][2],
        'strTipoPlan' :  data[0][4],
        'strCedula' :  data[0][5],
        'idPlan' : data[0][3],
        'nombreAfiliado':dataAfiliado[0][0],
        'edadAfiliado':dataAfiliado[0][1]
        }
    datalist=[informacion]
    cargarDatos()
    return render_template('modal.html', dicData=listClients,contrato=datalist)


@app.route('/enviar' ,methods=['POST'])
def submit():
    global listClients
    if request.method == 'POST':
        name = request.form['plan']
        listData = name.split("|");
        m.newvalue(listData[1],listData[0]);
    return redirect('/')

@app.route('/api/v1/info/<id>', methods=['GET'])
def get_users(id):
    global listClients
    global datalist
    for f in os.listdir(PATH_FILE):
        os.remove(os.path.join(PATH_FILE, f))
  
    data = m.searchdata(id)
    cedulaAfiliado = data[0][5]
    dataAfiliado = m.searchAfilicado(cedulaAfiliado)
    dataProducto = m.searchProuct(data[0][6])
    informacion =   {
        'numContrato' :  data[0][0],
        'strNombre' :  data[0][1],
        'strStatus' :  data[0][2],
        'strTipoPlan' :  data[0][4],
        'strCedula' :  data[0][5],
        'idPlan' : data[0][3],
        'nombreAfiliado':dataAfiliado[0][0],
        'edadAfiliado':dataAfiliado[0][1]
        }
   
  

    listData = [["N° Contrato:",str(data[0][0])],
            ["Nombre del titular:",data[0][1]],
            ["Cédula del afiliado:",data[0][5]],
            ["Status de revisión:",data[0][2]],
            ["Id del plan:",data[0][3]],
            ["Nombre del plan:",data[0][4]],
            ["Nombre del afiliado:",dataAfiliado[0][0]],
            ["Edad del afiliado:",str(dataAfiliado[0][1])],
            ["Nombre del producto:",dataProducto[0][0]]]


    listTabla1 =[["Tipo de plan","Modalidad","Nombre del Plan o Producto"],
                [data[0][4],"Cerrada",dataProducto[0][0]],]

    pdf=FPDF('P', 'mm', 'A4')
    pdf.alias_nb_pages()
    pdf.add_page()
            # Logo
        # Arial bold 15
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(110,173,255)
        # Move to the right
    pdf.cell(90)
        # Title
    pdf.cell(100, 30, 'CONTRATO N°: ContSeg'+str(data[0][0]))
   
    pdf.image('static/images/salusa.png', 190, 20, 10,10)
    pdf.ln(20)
    line_height = pdf.font_size * 2
    col_width = 190/3
    pdf.ln(line_height)
    for row in range (len(listTabla1)):
        for colum in range(len(listTabla1[0])):
            if(row == 0):
                pdf.set_font('Arial','B', 11)
                pdf.set_text_color(255,255,255)
                pdf.set_fill_color(27,150,190)
            else:
                pdf.set_font('Arial','', 11)
                pdf.set_text_color(60,60,60)
                pdf.set_fill_color(223,229,245)

            pdf.cell(col_width,line_height,listTabla1[row][colum],border=1,align='C',fill=True)
           
        pdf.ln(line_height)

    
    pdf.set_text_color(27,65,129)
    pdf.set_font('Arial', 'B', 14)
        # Move to the right
    pdf.cell(60)
        # Title
    pdf.cell(100, 30, 'FORMULARIO DE SUSCRIPCIÓN')
        # Line break
    pdf.ln(8)
    pdf.set_text_color(19,108,180)
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(100, 30, 'Suscripción del Contrato')

    pdf.ln(8)
    pdf.set_text_color(60,60,60)
    pdf.set_font('Arial', '', 11)
    pdf.cell(70, 30, 'Titular: '+data[0][1])
   
    pdf.cell(13, 30, 'Lugar: ')
    pdf.set_font('Arial', 'U', 11)
    pdf.cell(70, 30, "Quito - E1-291")
    pdf.ln(8)
    pdf.cell(70)
    now = datetime.now()
    pdf.set_font('Arial', '', 11)
    fecha = str(now.day)+"-"+str(now.month)+"-"+str(now.year)
    pdf.cell(100, 30, 'Fecha de suscripción / Inicio de vigencia: '+fecha)


    pdf.ln(8)
    pdf.set_text_color(19,108,180)
    pdf.set_font('Arial', 'B', 16)

    pdf.cell(100, 30, 'Contratantes:')
    pdf.ln(8)
    pdf.set_text_color(19,108,180)
    pdf.set_font('Arial', '', 15)
    pdf.cell(100, 30, 'A. Compañia de servicios de atención integral de salud prepagada.')   
    pdf.ln(8)
    pdf.set_text_color(60,60,60)
    pdf.set_font('Arial', '', 11)
    pdf.cell(100, 30, 'Saludsa Sistema de Medicina Prepagada del Ecuador S.A. (SALUDSA)')   
    pdf.ln(8)
    pdf.set_text_color(19,108,180)
    pdf.set_font('Arial', '', 15)
    pdf.cell(100, 30, 'B. Datos del titular / contratante')   
    pdf.ln(8)
    pdf.set_text_color(60,60,60)
    pdf.set_font('Arial', '', 11)
    nomCompleto = data[0][1].split(' ')
    pdf.cell(100, 30, 'Nombres: '+nomCompleto[0])   
    pdf.ln(8)
    pdf.cell(100, 30, 'Apellido: '+nomCompleto[1])
    pdf.ln(8)
    pdf.cell(70, 30, 'Cédula | Pasaporte: '+data[0][5])    
    pdf.cell(23, 30, 'Estado civil: ')  
    pdf.set_font('Arial', 'U', 11)
    pdf.cell(50, 30, 'casado')  


    pdf.ln(8)
    pdf.set_text_color(19,108,180)
    pdf.set_font('Arial', '', 15)
    pdf.cell(100, 30, 'Notificaciones Titular / Contratante') 
    pdf.ln(8)
    pdf.set_text_color(60,60,60)
    pdf.set_font('Arial', '', 11)
    pdf.cell(13, 30, 'E-mail:') 
    pdf.set_font('Arial', 'U', 11)
    pdf.cell(80, 30, 'paul.omar.penafiel@gmail.com') 
    pdf.set_font('Arial', '', 11)
    pdf.cell(32, 30, 'E-mail de trabajo:') 
    pdf.cell(50, 30, 'paul.penafiel@bayteq.com') 
    pdf.ln(8)
    pdf.cell(27, 30, 'Calle principal:')
    pdf.set_font('Arial', 'U', 11) 
    pdf.cell(66, 30, 'Av. Turubamba')
    pdf.set_font('Arial', '', 11)
    pdf.cell(23, 30, 'Número: 291')
    pdf.ln(8)
    pdf.cell(31, 30, 'Calle transversal:')
    pdf.set_font('Arial', 'U', 11)
    pdf.cell(28, 30, 'Carlos Rubira')
    pdf.ln(8)
    pdf.set_font('Arial', '', 11)
    pdf.cell(18, 30, 'Provincia:')
    pdf.set_font('Arial', 'U', 11)
    pdf.cell(75, 30, 'Pichincha')
    pdf.set_font('Arial', '', 11)
    pdf.cell(14, 30, 'Ciudad')
    pdf.set_font('Arial', 'U', 11)
    pdf.cell(28, 30, 'Quito - E1-291')
    pdf.ln(8)
    pdf.set_font('Arial', '', 11)
    pdf.cell(18, 30, 'Teléfono:')
    pdf.set_font('Arial', 'U', 11)
    pdf.cell(28, 30, '0998307269')
    pdf.ln(8)
    pdf.set_font('Arial', '', 9)
    pdf.cell(28, 30, '    *Autorizo a recibir de Saludsa todo tipo de notificaciones en la información de contacto proporcionada.')


    pdf.ln(8)
    pdf.set_text_color(19,108,180)
    pdf.set_font('Arial', '', 15)
    pdf.cell(40, 30, 'Forma de Pago:') 
    pdf.set_text_color(60,60,60)
    pdf.set_font('Arial', 'U', 11)
    pdf.cell(53, 30, 'débito Corriente') 
    pdf.set_text_color(19,108,180)
    pdf.set_font('Arial', '', 15)
    pdf.cell(39, 30, 'Perido de Pago:') 
    pdf.set_text_color(60,60,60)
    pdf.set_font('Arial', 'U', 11)
    pdf.cell(13, 30, 'Q1') 

    pdf.ln(8)
    pdf.set_text_color(19,108,180)
    pdf.set_font('Arial', '', 15)
    pdf.cell(56, 30, '   Reembolso de gastos ') 
    pdf.set_font('Arial', '', 12)
    pdf.cell(40, 30, '(datos de banco para transferencia / pago inteligente del titular)(*)') 
    pdf.ln(5)
    pdf.set_font('Arial', '', 9)
    pdf.cell(40, 30, '     (*) Acepto que el reembolso de gastos con pago inteligente, serán realizados única y exclusivamente a la cuenta del titular.') 

    pdf.ln(8)
    pdf.set_text_color(60,60,60)
    pdf.set_font('Arial', '', 11)
    pdf.cell(95, 30, 'Nombre del Banco: inn_reembolso_nombrebanco') 
    pdf.cell(13, 30, 'N°. de cuenta: inn_reembolso_numerocuenta')
    pdf.ln(8)
    pdf.cell(13, 30, 'Tipo de Cuenta: inn_reembolso_nombretipocuenta') 
    pdf.ln(8)
    pdf.cell(13, 30, 'Nombre del vendedor: inn_vendedorbusqueda')
    pdf.ln(8)
    pdf.cell(95, 30, 'Código del vendedor: inn_codigovendedorcontrato')
    pdf.cell(13, 30, 'Firma director: salud_directorname')
    pdf.set_text_color(105,110,111)
    pdf.ln(22)
        # Select Arial italic 8
    pdf.set_font('Arial', 'I', 8)
        # Print centered page number
    pdf.cell(13, 10, 'N° Contrato: '+ str(data[0][0]), 0, 0, 'C')
  


    pdf.ln(30)
    pdf.set_text_color(19,108,180)
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(100, 30, 'Usuarios')
    pdf.image('static/images/salusa.png', 190, 20, 10,10)

    listTable2 = [[" ","Nombre Completo"," ","Sin Maternidad","Tarjeta Adicional","Sexo","Parentesco código","Cuota"],
                    [data[0][5],nomCompleto[0],nomCompleto[1]," "," ","Masculino","2","109"]]
    pdf.ln(20)
    line_height = pdf.font_size * 2
    col_width = 195/8
    pdf.ln(line_height)
    for row in range (len(listTable2)):
        for colum in range(len(listTable2[0])):
            if(row == 0):
                pdf.set_font('Arial','B', 7)
                pdf.set_text_color(255,255,255)
                pdf.set_fill_color(27,150,190)
            else:
                pdf.set_font('Arial','', 8)
                pdf.set_text_color(60,60,60)
                pdf.set_fill_color(223,229,245)

            if (row == 0 and colum <3):
                pdf.cell(col_width,line_height,listTable2[row][colum],border=0,align='C',fill=True)
            else:
                pdf.cell(col_width,line_height,listTable2[row][colum],border=1,align='C',fill=True)
           
        pdf.ln(line_height)


    pdf.ln(5)
    line_height = pdf.font_size * 4
    col_width = 50
    #pdf.ln(line_height)
    pdf.cell(95)
    listTable3 = ["1.PRECIO COTIZADO","109"]
    for colum in range (len(listTable3)):
        if(colum == 0):
                pdf.set_font('Arial','B', 11)
                pdf.set_text_color(255,255,255)
                pdf.set_fill_color(47,84,150)
                pdf.cell(col_width,line_height,listTable3[colum],border=1,align='C',fill=True)
        else:
                pdf.set_font('Arial','B', 11)
                pdf.set_text_color(255,255,255)
                pdf.set_fill_color(166,186,227)
                pdf.cell(col_width,line_height,listTable3[colum],border=1,align='C',fill=True)


    pdf.ln(5)
    pdf.set_text_color(60,60,60)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(24, 30, 'Parentesco: 1.') 
    pdf.set_font('Arial', '', 10)
    pdf.cell(38, 30, 'Cónyuge | Conviviente ')
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(4, 30, '2.')  
    pdf.set_font('Arial', '', 10)
    pdf.cell(10, 30, 'Hijos ')
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(4, 30, '3.')
    pdf.set_font('Arial', '', 10)
    pdf.cell(25, 30, 'Padres')   
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(16, 30, '4. Otros ')  
    pdf.set_font('Arial', '', 10)
    pdf.cell(95, 30, '(hasta el cuarto grado de consaguinidad o segundo de afinidad)') 
    pdf.ln(5)
    pdf.set_font('Arial', '', 10)
    pdf.cell(95, 30, '*El Contratante al escoger la opción de sin mateernidad, respecto de uno o más Beneficiarios, declara que está consciente')
    pdf.ln(5)
    pdf.cell(95,30,"que dichos Beneficiarios no tendrán el Financiamiento ni coberturas por maternidad (Embarazo normal, embarazo ectópico,")
    pdf.ln(5)
    pdf.cell(95,30,"aborto no provocado), inclusive las relacionadas con Terifa Cero.")


    pdf.ln(20)
    pdf.set_text_color(19,108,180)
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(100, 30, 'Cotización')


    listTable3 =[["PRECIOS COTIZADOS","109"],
                ["TOTAL CONDICIONES ESPECIALES","0"],
                ["SUBTOTAL","109"],
                ["DESCUENTO inn_descuentoformapago\n % POR FORMA DE PAGO **","0"],
                ["GASTO ADMINISTRATIVO","0"],
                ["SEGURO CAMPESINO","0"],
                ["TOTAL CUOTA MENSUAL","109"],
                ["GASTO DE EMISIÓN",""],
                ["SEGURO CAMPESINO POR GASTOS DE EMISIÓN",""],
                ["TOTAL PRIMERA CUOTA","109"],
                ["DESCUENTO inn_descuentoprimeracuota % PRIMERA CUOTA",""]]
    pdf.ln(20)
    line_height = pdf.font_size 
    col_width = 185/2
    
    pdf.set_fill_color(242,242,242)
    for row in range (len(listTable3)):
        for colum in range(len(listTable3[0])):
            
            if ( row == 2 or row == 6 or row ==9):
                 pdf.set_fill_color(173,184,202)
            else:
                 pdf.set_fill_color(242,242,242)
            if( colum == 0):
                pdf.cell(40)
                pdf.set_font('Arial','B', 8)
                pdf.set_text_color(90,90,90)
                pdf.cell(col_width,line_height,listTable3[row][colum],border=1,fill=True)
             
            else:
                pdf.set_font('Arial','', 8)
                pdf.set_text_color(6,6,6)
                pdf.cell(20,line_height,listTable3[row][colum],border=1,align='C',fill=True)
        pdf.ln(line_height)

    pdf.set_font('Arial','I', 10)
    pdf.set_text_color(6,6,6)
    pdf.cell(100, 30, '**El descuento otorgado será aplicado mientras se cumplan las condiciones acordadas.')

    pdf.set_text_color(105,110,111)
    pdf.ln(71)
        # Select Arial italic 8
    pdf.set_font('Arial', 'I', 8)
        # Print centered page number
    pdf.cell(13, 10, 'N° Contrato: '+ str(data[0][0]), 0, 0, 'C')
   
   
    pdf.output(PATH_FILE+'contrato_'+str(id)+'_'+data[0][5]+'.pdf', 'F')
   

  
   
    
    return send_from_directory(PATH_FILE,path='contrato_'+str(id)+'_'+data[0][5]+'.pdf',as_attachment=True)
 

if __name__== '__main__':
    app.run(debug=True)
