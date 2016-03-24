#!/usr/bin/python
# -*- coding: utf-8 -*-

import gui


class busqueda():
	
	ValorRetorno = "Valor"
	tabla = ""
	
	def __init__(self, *args, **kwargs):
		self.db = kwargs['db']
		self.tabla = kwargs['tabla']
		if kwargs.has_key('campos'):
			self.campos = kwargs['campos']
		else:
			self.campos = '*'
		if kwargs.has_key('orden'):
			self.orden = kwargs['orden']
		else:
			self.orden = ''
		self.InitUI()
		self.busqueda['statusbar'].text = u'gui2py Search demo'
		self.armagrilla()
		self.busqueda.show(modal=True)
		
	def InitUI(self):
		with gui.Window(name='busqueda', title=u'gui2py Search demo', resizable=True, 
				height='450px', left='580', top='24', 
				width='580px', bgcolor=u'#E0E0E0', image='', tiled=True, 
				modal = True):
			with gui.Panel(name='panel',  sizer='wrap', width="100%", height="100%"):
				gui.Label(name='label_140_120', sizer_align='center', sizer_border=4, 
							width='100%', text=u'Registros', )
				gui.Panel(name='panelgrid', sizer='wrap', width='100%', 
						height='100%', sizer_border=5)
				
			gui.StatusBar(name='statusbar', )
	
		self.busqueda = gui.get("busqueda")
	
	def on_cierra(self, evt):
		self.busqueda.close()

	def on_select(self, evt):
		self.busqueda.close()
		
	def __str__(self):
		return self.ValorRetorno

	def armagrilla(self):
		panel = self.busqueda['panel']
		with panel['panelgrid']:
			gui.Label(name='label_140_130', sizer_align='center', sizer_border=4, 
						width='20%', text=u'Busqueda', )
			gui.TextBox(name='txtBusqueda', 
						left='130', 
						width='70%',)
			with gui.GridView(name='gridview', height='60%', left='0', 
								top='0', width='100%', ):
				for x in self.tabla.as_dict()['fields']:
					gui.GridColumn(name=x['fieldname'], 
								text=x['fieldname'], 
								type='string', 
								width=x['length']*13, )
			gui.Button(label=u'Cerrar', name='close', sizer_border=4, onclick=self.on_cierra)
			gui.Button(label=u'Seleccionar', name='close', sizer_border=4, onclick=self.on_select)
		
		b = panel['panelgrid']['txtBusqueda']
		b.onchange = self.OnChangeBusqueda
		
		self.CargaRegistros()
	
	def CargaRegistros(self):
		panel = self.busqueda['panel']
		b = panel['panelgrid']['txtBusqueda']
		gv = panel['panelgrid']['gridview']
		gv.items.clear()
		
		if b.value != '' and self.orden != '':
			registros = self.db(self.db[self.tabla][self.orden].like(
					'%' + b.value + '%')).select( orderby=self.orden)
			print self.db._lastsql
		else:
			registros = self.db().select(self.db[self.tabla].ALL, 
				orderby=self.orden)
		
		i = 0
		for registro in registros:
			gv.items.insert(i,[registro[x] for x in self.tabla.fields()])
			i += 1
			
		gv.ongridmouseclick = self.SeleccionaGrilla
		
	def SeleccionaGrilla(self, evt):
		gv = self.busqueda['panel']['panelgrid']['gridview']
		selected_rows = gv.actualrow
		print evt.GetRow()
		self.ValorRetorno = evt.GetRow(selected_rows, 0)
		print self.ValorRetorno
	
	def OnChangeBusqueda(self,evt):
		panel = self.busqueda['panel']
		b = panel['panelgrid']['txtBusqueda']
		print b.value
		self.CargaRegistros()
