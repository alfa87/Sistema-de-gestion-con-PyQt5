from Conexion.conexionTransacciones import ConexionTransacciones
from Modelo.cliente import Cliente
from Modelo.proveedor import Proveedor
from Modelo.producto import Producto
from PyQt5.QtWidgets import QRadioButton
from Componentes.tableModel import MyTableModel
from PyQt5.QtWidgets import QAbstractItemView
import datetime
from PyQt5.Qt import QTextDocument, QPrinter, QPrintDialog
from PyQt5.QtWidgets import QMessageBox, QDialog
from PyQt5.Qt import QDesktopServices, QUrl



class PestaniaTransacciones():


    def __init__(self, winPrincipal):
        self.conexionTransacciones = ConexionTransacciones()
        self.winPrincipal = winPrincipal
        self.cliente = Cliente()
        self.proveedor = Proveedor()
        self.producto = Producto()
        self.tipoTransaccion = "VENTA"
        self.configInit()
        self.total = 0


    def configInit(self):
        self.winPrincipal.rbVenta_t.clicked.connect(self.onClickVenta)
        self.winPrincipal.rbCompra_t.clicked.connect(self.onClickCompra)

        self.winPrincipal.btnSumarProducto_t.clicked.connect(self.agregarTransaccion)

        self.winPrincipal.btnAceptar_t.clicked.connect(self.onClickAceptar)
        self.winPrincipal.btnCancelar_t.clicked.connect(self.onClickCancelar)

        self.cargarTablaProductos()

        self.winPrincipal.tvClientes_t.setSortingEnabled(True)
        self.winPrincipal.tvClientes_t.setMouseTracking(True)
        self.winPrincipal.tvClientes_t.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.winPrincipal.tvProductos_t.setSortingEnabled(True)
        self.winPrincipal.tvProductos_t.setMouseTracking(True)
        self.winPrincipal.tvProductos_t.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.winPrincipal.tvDetalleTransaccion_t.setSortingEnabled(True)
        self.winPrincipal.tvDetalleTransaccion_t.setMouseTracking(True)
        self.winPrincipal.tvDetalleTransaccion_t.setSelectionBehavior(QAbstractItemView.SelectRows)


    def onClickAceptar(self):

        listTransaccion = list(self.winPrincipal.tvDetalleTransaccion_t.model().mylist).copy()
        subNom = ""
        numRecibo = 0
        if(self.tipoTransaccion == "VENTA"):
            numRecibo = self.conexionTransacciones.cargarTransaccionVenta(listTransaccion, self.cliente)
            subNom = 'VNT'
        elif(self.tipoTransaccion == "COMPRA"):
            numRecibo = self.conexionTransacciones.cargarTransaccionCompra(listTransaccion, self.proveedor)
            subNom = 'CMP'

        alert = QDialog()
        confirm = QMessageBox.question(alert, "Mensaje", "¿ Desea generar factura ?", QMessageBox.Yes, QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.createFactura(listTransaccion, subNom, numRecibo)


        self.limpiarCampos()

    def createFactura(self, listTransaccion, subNom, idRecibo):
        hoy = str(datetime.datetime.now().year) + str(datetime.datetime.now().month) + str(datetime.datetime.now().day) + str(datetime.datetime.now().hour) + str(datetime.datetime.now().minute) + str(datetime.datetime.now().second)

        nombrePdf = '../archivos/' + str(hoy + subNom) + '.pdf'
        listTransaccionTable = ""
        for transaccion in listTransaccion:
            listTransaccionTable += """
                                        <tr height="80">
                                            <td width="10%" align="center" >
                                            <br>""" + str(transaccion[1])  + """<br>
                                            </td>
                                            <td width="20%" >
                                                <br> &nbsp;&nbsp;""" + str(transaccion[3])  + """<br>
                                            </td>
                                            <td width="50%" >
                                               <br>&nbsp;&nbsp; """ + str(transaccion[4])  + """<br>
                                            </td>
                                            <td width="10%" align="right" >
                                              <br>  $ """ + str(transaccion[5])  + """&nbsp;&nbsp;<br>
                                            </td>
                                            <td width="10%" align="right" >
                                              <br>  $ """ + str( int(transaccion[1]) * float(transaccion[5]))  + """&nbsp;&nbsp;<br>
                                            </td>
                                        </tr>
                                   """
        nombre = ""
        apellido = ""

        if(self.tipoTransaccion == "VENTA"):
            nombre = self.cliente.getNombre()
            apellido = self.cliente.getApellido()
        elif(self.tipoTransaccion == "COMPRA"):
            nombre = self.proveedor.getNombre()
            apellido = self.proveedor.getDescripcion()


        total = self.winPrincipal.lblTotal.text()
        fecha = str(datetime.datetime.now())
        html =  """
                     <table width="600">
                        <tr width="600" color="#000000">
                            <td width="80%">
                               Perfumeria La que vende perfumes <br>
                               LABOULAYE, CORDOBA, ARGENTINA <br>
                               TEL: 0351-111111  <br>
                               MAIL: MAIL@MAIL.COM  <br>
                            </td>
                            <td width="20%" align="right">
                                <IMG SRC="kde1.png">
                            </td>
                        </tr>

                    </table>
                _______________________________________________________________________________________________________
                    <p>
                        DATOS DEL CLIENTE:
                    </p>
                    <br>
                    <table>

                        <tr>
                            <td>
                                NOMBRE:   """+ nombre +"""  <br>
                                APELLIDO: """ + apellido + """ <br>

                            </td>
                            <td>
                            </td>
                        </tr>
                    </table>

                    <br>
                    _______________________________________________________________________________________________________
                    <br>
                    <p>
                        DETALLES DE LA COMPRA:
                    </p>
                    <br>
                    <table width="600" height="0" style="border-color: black; border-width: 0.5px; border-spacing: 0;">
                      <tr  style=" background-color: gray; border-style: inset;">
                        <td width="10%"  align="center" valign="middle">
                            <b>
                            CANT
                            </b>
                        </td>
                        <td width="20%"  align="center" valign="middle">
                            <b>
                                PRODUCTO
                            </b>
                        </td>
                        <td width="50%"  align="center" valign="middle">
                            <b>
                            DESCRIPCION
                            </b>
                        </td>
                        <td width="10%"  align="center" valign="middle">
                            <b>
                            PREC <br>UNIT
                            </b>
                        </td>
                        <td width="10%"  align="center" valign="middle">
                            <b>
                            PREC <br>TOT
                            </b>
                        </td>
                      </tr>
                  </table>

                  <br>
                  <br>
                  <br>
                  <br>

                  <table  height="350" width="600" style="border-color: gray; border-width: .4px; border-collapse: collapse;">
                      """ + listTransaccionTable + """
                  </table>
                    <br>
                    <br>
                    <table width="600" border="0.5" height="0" style="border-color: black; border-width: 0.5px; border-spacing: 0;">
                        <tr >
                            <td width="90%" align="right">
                                <br>
                                TOTAL..................................................................................................................
                                <br>
                            </td>
                            <td width="10%" align="center">
                              <br> $ """ + total + """<br>
                            </td>
                        </tr>
                    </table>

                    <br>
                    <br>
                    <br>
                    <p width="600" align="center" style=" font-size: 10; " >
                    Por cualquier consulta, sobre este recibo, dirigirse al local que se encuentra ubicado en la calle
                    independencia 450. <br> O Comunicarse a los telefonos 03382-123123123 / 4231231
                    </p>
                    <br>
                    <br>
                    <br>
                    <br>
                    <br>
                    _______________________________________________________________________________________________________
                    <br>
                    <table width="600">
                        <tr>
                            <td align="right" width="80%">
                            FECHA/HORA : """+ fecha + """
                            </td>
                            <td align="right">
                            N° : """+ str(idRecibo) +"""
                            </td>
                        </tr>
                    </table>
                    _______________________________________________________________________________________________________
                """

        doc = QTextDocument()
        doc.setHtml(html)
        #doc.setDefaultStyleSheet(style)
        printer = QPrinter()
        printer.setOutputFileName(nombrePdf)

        printer.setOutputFormat(QPrinter.PdfFormat)
        doc.print(printer)
        printer.newPage()
        url = QUrl
        url = QUrl(nombrePdf)
        QDesktopServices.openUrl(url)

        """
        printPdf = QPrinter()
        printPdf.setOutputFormat(QPrinter.NativeFormat)

        questionPrint = QPrintDialog(printPdf, self.winPrincipal)

        if questionPrint.exec() == QPrintDialog.accept(printPdf):
            doc.print(printPdf)


        alert = QDialog()
        confirm = QMessageBox.question(alert, "Mensaje", "¿ Desea generar factura ?", QMessageBox.Yes, QMessageBox.No)
        if confirm == QMessageBox.Yes:

            #openPdf = QPrintDialog(printPdf, self.winPrincipal)
            #openPdf.setWindowTitle("Recibo")
        """


    def limpiarCampos(self):
        self.winPrincipal.tvClientes_t.setModel(None)
        self.winPrincipal.tvDetalleTransaccion_t.setModel(None)
        self.winPrincipal.tvProductos_t.setModel(None)
        self.winPrincipal.lblTotal.setText('')
        self.winPrincipal.sbCantidadProducto_t.setValue(0)



    def onClickCancelar(self):
        self.limpiarCampos()

    def cargarTablaClientes(self):
        if self.winPrincipal.cbFilterCliente_t.currentText() == 'Apellido':
            tipoParametro = 'c.apellido'
        elif self.winPrincipal.cbFilterCliente_t.currentText() == 'Email':
            tipoParametro = 'p.email'

        parametro = self.winPrincipal.txtFilterCliente_t.text()

        listaClientes = self.conexionTransacciones.selectClientes(tipoParametro, parametro)

        header = ['ID','Apellido','Nombre','Email']
        tablaModel = MyTableModel(self.winPrincipal.tvClientes_t, listaClientes, header)
        self.winPrincipal.tvClientes_t.setModel(tablaModel)
        self.winPrincipal.tvClientes_t.selectionModel().currentChanged.connect(self.changeSelectedTable)


        self.winPrincipal.tvClientes_t.setColumnHidden(0, True)
        self.winPrincipal.tvClientes_t.setColumnWidth(1, 130)
        self.winPrincipal.tvClientes_t.setColumnWidth(2, 130)
        self.winPrincipal.tvClientes_t.setColumnWidth(3, 150)


    def cargarTablaProveedores(self):
        if self.winPrincipal.cbFilterCliente_t.currentText() == 'Apellido':
            tipoParametro = 'c.apellido'
        elif self.winPrincipal.cbFilterCliente_t.currentText() == 'Email':
            tipoParametro = 'p.email'

        parametro = self.winPrincipal.txtFilterCliente_t.text()

        listProveedores = self.conexionTransacciones.selectProveedores(tipoParametro, parametro)

        header = ['ID', 'Descripcion', 'Nombre', 'Email']
        tableModel = MyTableModel(self.winPrincipal.tvClientes_t, listProveedores, header)
        self.winPrincipal.tvClientes_t.setModel(tableModel)
        self.winPrincipal.tvClientes_t.selectionModel().currentChanged.connect(self.changeSelectedTable)

        self.winPrincipal.tvClientes_t.setColumnHidden(0, True)
        self.winPrincipal.tvClientes_t.setColumnWidth(1, 130)
        self.winPrincipal.tvClientes_t.setColumnWidth(2, 130)
        self.winPrincipal.tvClientes_t.setColumnWidth(3, 150)



    def changeSelectedTable(self, selected, deselected):

        listPersonas = selected.model().mylist
        personaSelected = ()
        personaSelected = tuple(listPersonas[selected.row()])

        self.personaSelectedRow = selected.row()

        if(self.tipoTransaccion == "VENTA"):
            self.cliente = Cliente()
            self.cliente.setIdCliente(int(personaSelected[0]))
            self.cliente.setApellido(str(personaSelected[1]))
            self.cliente.setNombre(str(personaSelected[2]))
            self.cliente.setEmail(str(personaSelected[3]))

        elif(self.tipoTransaccion == "COMPRA"):
            self.proveedor = Proveedor()
            self.proveedor.setIdProveedor(int(personaSelected[0]))
            self.proveedor.setDescripcion(str(personaSelected[1]))
            self.proveedor.setNombre(str(personaSelected[2]))
            self.proveedor.setEmail(str(personaSelected[3]))



    def cargarTablaProductos(self):
        listProducto = self.conexionTransacciones.selectProductos()

        header = ['ID', 'Nombre', 'Descripcion', 'Cant', 'P.Compra', 'P.Venta', 'Marca']

        tableModel = MyTableModel(self.winPrincipal.tvProductos_t, listProducto, header)
        self.winPrincipal.tvProductos_t.setModel(tableModel)
        self.winPrincipal.tvProductos_t.selectionModel().currentChanged.connect(self.changeSelectedTableProducto)



        self.winPrincipal.tvProductos_t.setColumnHidden(0, True)
        self.winPrincipal.tvProductos_t.setColumnWidth(1, 150)
        self.winPrincipal.tvProductos_t.setColumnWidth(2, 200)
        self.winPrincipal.tvProductos_t.setColumnWidth(3, 50)
        self.winPrincipal.tvProductos_t.setColumnWidth(4, 80)
        self.winPrincipal.tvProductos_t.setColumnWidth(5, 80)
        self.winPrincipal.tvProductos_t.setColumnWidth(6, 100)

        #tvProductos_t

    def changeSelectedTableProducto(self, selected, deselected):
        listProductos = selected.model().mylist
        productoSelected = ()
        productoSelected = tuple(listProductos[selected.row()])

        self.productoSelected = selected.row()

        self.producto = Producto()
        self.producto.setIdProducto(int(productoSelected[0]))
        self.producto.setNombre(str(productoSelected[1]))
        self.producto.setDescripcion(str(productoSelected[2]))
        self.producto.setCantidad(int(productoSelected[3]))
        self.producto.setPrecioCompra(float(productoSelected[4]))
        self.producto.setPrecioVenta(float(productoSelected[5]))




    def agregarTransaccion(self):
        #tvDetalleTransaccion_t
        #btnSumarProducto_t
        cantProducto = int(self.winPrincipal.sbCantidadProducto_t.value())

        modelListTransaccion = self.winPrincipal.tvDetalleTransaccion_t.model()
        header = ['ID', 'Cantidad','idProducto' ,'Producto', 'Descripcion', 'precio_unitario' ]

        precio_unitario = 0
        if(self.tipoTransaccion == "VENTA"):
            precio_unitario = float(self.producto.getPrecioVenta())

        elif(self.tipoTransaccion == "COMPRA"):
            precio_unitario = float(self.producto.getPrecioCompra())

        if modelListTransaccion is not None:
            listTabPro = list(self.winPrincipal.tvDetalleTransaccion_t.model().mylist)

            if len(listTabPro) > 0 or listTabPro is not None:
                tuplaProd = ('0', str(cantProducto), str(self.producto.getIdProducto()), str(self.producto.getNombre()),
                            str(self.producto.getDescripcion()), str(precio_unitario)
                            )

                listTabPro.append(tuplaProd)
                tupleTable = tuple(listTabPro)

                tableModel = MyTableModel(self.winPrincipal, tupleTable , header)
                self.winPrincipal.tvDetalleTransaccion_t.setModel(tableModel)
                #self.winPrincipal.tvDetalleTransaccion_t.selectionModel().currentChanged.connect(self.changeSelectedTableTransaccion)
        else:
            lista = []
            tuplaProd = ('0', str(cantProducto), str(self.producto.getIdProducto()), str(self.producto.getNombre()),
                           str(self.producto.getDescripcion()), str(precio_unitario)
                            )
            lista.append(tuplaProd)

            tableModel = MyTableModel(self.winPrincipal, lista , header)
            self.winPrincipal.tvDetalleTransaccion_t.setModel(tableModel)
            #self.winPrincipal.tvDetalleTransaccion_t.selectionModel().currentChanged.connect(self.changeSelectedTableTel)
            self.winPrincipal.tvDetalleTransaccion_t.setColumnHidden(0, True)
            self.winPrincipal.tvDetalleTransaccion_t.setColumnWidth(1, 80)
            self.winPrincipal.tvDetalleTransaccion_t.setColumnHidden(2, True)
            self.winPrincipal.tvDetalleTransaccion_t.setColumnWidth(3, 200)
            self.winPrincipal.tvDetalleTransaccion_t.setColumnWidth(4, 300)


        self.total = (cantProducto * self.producto.getPrecioVenta()) + self.total

        self.winPrincipal.lblTotal.setText(str(self.total))

        self.winPrincipal.tvClientes_t.setEnabled(False)

    def changeSelectedTableTransaccion(self, selected, deselected):
        pass

    def onClickVenta(self):
        self.winPrincipal.label2_t.setText('Cliente')
        self.cargarTablaClientes()
        self.tipoTransaccion = "VENTA"

    def onClickCompra(self):
        self.winPrincipal.label2_t.setText('Proovedor')
        self.cargarTablaProveedores()
        self.tipoTransaccion = "COMPRA"


    def selecClientes(self):
        if self.winPrincipal.cbFilterCliente_t.currentText() == 'Apellido':
            tipoParametro = 'c.apellido'
        elif self.winPrincipal.cbFilterCliente_t.currentText() == 'Email':
            tipoParametro = 'p.email'

        parametro = self.winPrincipal.txtFilterCliente_t.text()

        self.conexionTransacciones.selectClientes(tipoParametro, parametro)