#!/usr/bin/python
# -*- coding: utf-8 -*-

"Experimental CRUD sample gui2py application demo"
import gui
import sqlite3
import sys
from os.path import join, abspath

DEBUG = True

def on_cierra(evt):
    mywin.close()

with gui.Window(name='ppal', title=u'gui2py CRUD demo', resizable=True, 
		height='250px', left='580', top='24', 
		width='580px', bgcolor=u'#E0E0E0', image='', tiled=True, ):
	with gui.Panel(name='panel',  sizer='wrap', width="100%", height="100%"):
		gui.Label(name='label_140_120', sizer_align='center', sizer_border=4, 
				  width='100%', text=u'Registros', )
		gui.Panel(label=u'', name='record', width='100%', 
					   image='', sizer_border=5)
		gui.Button(label=u'Crear', name='create', sizer_border=4, )
		gui.Button(label=u'Actualizar', name='update', sizer_border=4, )
		gui.Button(label=u'Borrar', name='delete', sizer_border=4, )
		gui.Button(label=u'Buscar', name='search', sizer_border=4, )
		gui.Button(label=u'Cerrar', name='close', sizer_border=4, onclick=on_cierra)
		

mywin = gui.get("ppal")
panel = mywin['panel']


class crud():
	
	def __init__(self, *args, **kwargs):
		base = ''

		if kwargs.has_key('basedatos'):
			if sys.platform.startswith('win32'):
				ruta = kwargs['basedatos'].split('/')
				for r in ruta:
					base += join(r)
			elif sys.platform.startswith('linux'):
				ruta = kwargs['basedatos'].split('\\')
				for r in ruta:
					base += join(r)
			
			self.DB = abspath(base)
		else:
			self.DB = abspath(join('modelos','test.db'))
			
		self.con = self.conectar()
		self.con.row_factory = sqlite3.Row
		print self.con
		if kwargs.has_key('tabla'):
			self.tabla = kwargs['tabla']
			if not self.existe_tabla():
				gui.alert("No se encuentra la tabla en la base de datos", "Sistema")
		else:
			gui.alert("No se especifico tabla para el CRUD", "Sistema")

		if kwargs.has_key('formato'):
			self.formato = kwargs['formato']
		else:
			self.formato = {}
			
		self.InitUI()
		panel['create'].onclick = self.button_press_create
		panel['update'].onclick = self.button_press_update
		panel['delete'].onclick = self.button_press_delete
		panel['search'].onclick = self.button_press_search
		
		mywin.show()
		gui.main_loop()
	
	def InitUI(self):
		cur = self.con.cursor()
		cur.execute("select * from " + self.tabla)
		formato = self.formato
		self.controls = {}
		with panel['record']:
			nTop = '10'
			datos = cur.fetchone()
			fila = 0
			for x in cur.description:
				if formato.has_key(x[0]):
					gui.Label(name='lbl'+x[0], 
						top=nTop, 
						text=formato[x[0]]['text'] if formato[x[0]].has_key('text') else x[0].capitalize(),)
					gui.TextBox(name='txt'+x[0], 
						top=nTop, 
						left='130', 
						mask=formato[x[0]].get('mask', ''),
						width=formato[x[0]].get('width', '100'),
						)
				else:
					gui.Label(name='lbl'+x[0], top=nTop, text=x[0].replace('_',' ').capitalize() )
					gui.TextBox(name='txt'+x[0], top=nTop, left='130', )
				self.controls['txt'+x[0]] = {'name':'txt'+x[0], 'field':x[0]}
				nTop = str(int(nTop)+30)
				fila += 1
				if formato.has_key(x[0]):
					if formato[x[0]].has_key('id') and formato[x[0]]['id']:
						panel['record']['txt'+x[0]].onblur = self.on_id_change
						self.controls['id'] = {'name':'txt'+x[0], 'field':x[0]}
		
		nTop = str(int(nTop)+80)
		mywin.height = nTop    
		
	def button_press_create(self, evt):
		for x in self.controls.itervalues():
			ctrl = panel['record'][x['name']]
			if type(ctrl.value) == float:
				ctrl.value = 0.00
			else:
				ctrl.value = ""
			if DEBUG:
				print "Tipo {} nombre {} mascara {}".format(type(ctrl.value), ctrl.name, ctrl.mask)

	
	def button_press_update(self, evt):
		if self.nuevo:
			sql = 'insert into ' + self.tabla + '('
			sql += ','.join(d for d in self.controls.itervalues())
			sql += ') values('
			sql += ',%s'.join('' for d in self.controls.itervalues())
			sql += ')'
			params = [d for d in self.controls.itervalues()]
		else:
			query = 'update ' + self.tabla + ' set '
			query += ', '.join(d['field'] + ' = ?' \
				for d in self.controls.itervalues() \
				if d['field'] != self.controls['id']['field'])
			params = [panel['record'][d['name']].value \
				for d in self.controls.itervalues() \
				if d['field'] != self.controls['id']['field']]
			query += ' where ' + self.controls['id']['field'] + ' = ?'
			params.append(panel['record'][self.controls['id']['name']].value)

		if DEBUG:
			print query, params
		cur = self.con.cursor()
		cur.execute(query, params)
		self.con.commit()
		gui.alert("Datos actualizados", "Sistema")

	def button_press_delete(self, evt):
		gui.alert("Borrar")
	
	def button_press_search(self, evt):
		gui.alert("Busqueda")
	
	def conectar(self, basedatos=""):
		try:
			db = sqlite3.connect(self.DB)
		except sqlite3.Error, e:
			print "Error %s:" % e.args[0]
			sys.exit(1)
		return db
	
	def on_id_change(self, evt):
		ctrl = panel['record'][self.controls['id']['name']]
		sql = ("select * from " + self.tabla + 
				" where " + self.controls['id']['field'] +
				" = '" + ctrl.value + "'")
		cur = self.con.cursor()
		cur.execute(sql)
		datos = cur.fetchone()
		if datos is None:
			self.nuevo = True
		else:
			self.nuevo = False
			for x in self.controls.itervalues():
				ctrl = panel['record'][x['name']]
				ctrl.value = datos[x['field']]
		
	def existe_tabla(self):
		cur = self.con.cursor()
		try:
			cur.execute("select * from " + self.tabla)
			return True
		except:
			return False
