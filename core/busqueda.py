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
		self.InitUI()
		self.busqueda['statusbar'].text = u'gui2py Search demo'
		self.armagrilla()
		self.busqueda.show(modal=True)
		
	def InitUI(self):
		with gui.Window(name='busqueda', title=u'gui2py Search demo', resizable=True, 
				height='250px', left='580', top='24', 
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
		registros = self.db().select(self.db[self.tabla].ALL, orderby='detalle')
		panel = self.busqueda['panel']
		with panel['panelgrid']:
			gui.Label(name='label_140_130', sizer_align='center', sizer_border=4, 
						width='100%', text=u'Grilla', )
			with gui.GridView(name='gridview', height='50%', left='0', 
								top='0', width='100%', ):
				for x in self.tabla.as_dict()['fields']:
					gui.GridColumn(name=x['fieldname'], 
								text=x['fieldname'], 
								type='string', 
								width=x['length']*13, )
			gui.Button(label=u'Cerrar', name='close', sizer_border=4, onclick=self.on_cierra)
			gui.Button(label=u'Seleccionar', name='close', sizer_border=4, onclick=self.on_select)
		gv = panel['panelgrid']['gridview']
		gv.items.clear()
		
		for registro in registros:
			gv.items.insert(0,[registro[x] for x in self.tabla.fields()])
			
		gv.ongridselectcell = self.SeleccionaGrilla
		
	def SeleccionaGrilla(self, evt):
		gv = self.busqueda['panel']['panelgrid']['gridview']
		
		row, col = evt.GetRow(), evt.GetCol()
		self.ValorRetorno = gv.GetValue(1, 0)
		print self.ValorRetorno
