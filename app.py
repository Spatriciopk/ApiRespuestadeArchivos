from flask import Flask, render_template, request,redirect,url_for,flash,jsonify,send_file
import main as m
import wget
import os
from fpdf import FPDF
from os import remove
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
    remove("contrato.pdf")
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

    pdf=FPDF('P', 'mm', 'A4')
    pdf.alias_nb_pages()
    pdf.add_page()
            # Logo
    pdf.image('static/images/bayteq.png', 10, 8, 30,30)
        # Arial bold 15
    pdf.set_font('Arial', 'B', 20)
        # Move to the right
    pdf.cell(70)
        # Title
    pdf.cell(100, 30, 'Información del contrato')
        # Line break
    pdf.ln(30)
    pdf.set_font('Arial','B', 14)
    pdf.cell(30, 10, 'N° contrato:', 0)
    pdf.cell(19)
    pdf.set_font('Arial','', 14)
    pdf.cell(40, 10, str(informacion['numContrato']), 0)

    pdf.ln(6)
    pdf.set_font('Arial','B', 14)
    pdf.cell(30, 10, 'Nombre del titular:', 0)
    pdf.set_font('Arial','', 14)
    pdf.cell(19)
    pdf.cell(30, 10, str(informacion['strNombre']), 0)

    pdf.ln(6)
    pdf.set_font('Arial','B', 14)
    pdf.cell(30, 10, 'Cédula del afilidado:', 0)
    pdf.set_font('Arial','', 14)
    pdf.cell(19)
    pdf.cell(30, 10, str(informacion['strCedula']), 0)

    pdf.ln(6)
    pdf.set_font('Arial','B', 14)
    pdf.cell(30, 10, 'Status de revisión:', 0)
    pdf.set_font('Arial','', 14)
    pdf.cell(19)
    pdf.cell(30, 10, str(informacion['strStatus']), 0)

    pdf.ln(6)
    pdf.set_font('Arial','B', 14)
    pdf.cell(30, 10, 'Id del plan:', 0)
    pdf.set_font('Arial','', 14)
    pdf.cell(19)
    pdf.cell(30, 10, str(informacion['idPlan']), 0)

    pdf.ln(6)
    pdf.set_font('Arial','B', 14)
    pdf.cell(30, 10, 'Nombre del plan:', 0)
    pdf.set_font('Arial','', 14)
    pdf.cell(19)
    pdf.cell(30, 10, str(informacion['strTipoPlan']), 0)

    pdf.ln(6)
    pdf.set_font('Arial','B', 14)
    pdf.cell(30, 10, 'Nombre del afiliado:', 0)
    pdf.set_font('Arial','', 14)
    pdf.cell(19)
    pdf.cell(30, 10, str(informacion['nombreAfiliado']), 0)

    pdf.output('contrato.pdf', 'F')


    datalist=[informacion]
    response = {'message': datalist}
  
    PATH ='contrato.pdf'
   
    #path_desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Downloads')
    #path_desktop = path_desktop
    #url = "https://github.com/Spatriciopk/ApiRespuestadeArchivos/blob/main/contrato.pdf"
    #wget.download(url,path_desktop)
    return send_file(PATH,as_attachment=False)

if __name__== '__main__':
    app.run(debug=True)
