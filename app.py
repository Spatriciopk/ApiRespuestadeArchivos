from flask import Flask, render_template, request,redirect,url_for,flash,jsonify,send_file,send_from_directory
import main as m
import wget
import os
from fpdf import FPDF, HTMLMixin
from os import remove,getcwd

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
    remove(PATH_FILE+"contrato.pdf")
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
    pdf.ln(5)
    pdf.set_line_width(1)
    pdf.line(10, 45, 200, 45)
    pdf.set_line_width(0)
    #SetLineWidth(float width)
        # Line break
    pdf.ln(30)
  
    line_height = pdf.font_size * 2
    col_width = 190/2
    listData = [["N° Contrato:",str(data[0][0])],
            ["Nombre del titular:",data[0][1]],
            ["Cédula del afiliado:",data[0][5]],
            ["Status de revisión:",data[0][2]],
            ["Id del plan:",data[0][3]],
            ["Nombre del plan:",data[0][4]],
            ["Nombre del afiliado:",dataAfiliado[0][0]],
            ["Edad del afiliado:",str(dataAfiliado[0][1])]]
    pdf.ln(line_height)
    for row in range (len(listData)):
        for colum in range(len(listData[0])):
            if(colum == 0):
                pdf.set_font('Arial','B', 14)
            else:
                pdf.set_font('Arial','', 14)
            pdf.cell(col_width,line_height,listData[row][colum],border=1)
        pdf.ln(line_height)
    

    pdf.line(15, 240, 85, 240)
    pdf.line(115, 240, 185, 240)
    pdf.ln(60)
    pdf.set_font('Arial', '', 14)
        # Move to the right


    pdf.cell(20)
    pdf.cell(100, 30, data[0][1])
    pdf.cell(2)
    pdf.cell(100, 30, dataAfiliado[0][0])
    
        
    pdf.ln(10)
    pdf.cell(20)
        # Title
    pdf.cell(100, 30, 'Firma del titular')
    pdf.cell(2)
    pdf.cell(100, 30, "Firma del afiliado")
   
    pdf.output(PATH_FILE+'contrato.pdf', 'F')
   

    datalist=[informacion]
    response = {'message': datalist}
  
    PATH =PATH_FILE+'contrato.pdf'
   
    #path_desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Downloads')
    #path_desktop = path_desktop
    #url = "https://github.com/Spatriciopk/ApiRespuestadeArchivos/blob/main/contrato.pdf"
    #url = "https://www.python.org/static/img/python-logo@2x.png";
    #wget.download(url,path_desktop)
    return send_from_directory(PATH_FILE,path="contrato.pdf",as_attachment=True)
    #return send_file(PATH,as_attachment=False)

if __name__== '__main__':
    app.run(debug=True)
