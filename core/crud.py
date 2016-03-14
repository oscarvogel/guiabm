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
	
	nuevo = False
	
	def __init__(self, *args, **kwargs):
		base = ''
		self.tabla = kwargs['tabla']
		if kwargs.has_key('basedatos'):
			self.db = kwargs['basedatos']
		
		#print self.tabla.as_dict()
		for x in self.tabla.as_dict()['fields']:
			print x['label'], x['length'], x['fieldname']
		
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
		formato = self.formato
		self.controls = {}
		with panel['record']:
			nTop = '10'
			fila = 0
			for x in self.tabla.as_dict()['fields']:
				print x['type']
				mask = ''
				if x['type'] == 'date':
					mask = 'date'
				elif x['type'] in ('double'):
					mask = '##############.####'
				elif x['type'].startswith('decimal'):
					mask = '#########.##'
					
				if formato.has_key(x['fieldname']):
					gui.Label(name='lbl'+x['fieldname'], 
						top=nTop, 
						text=formato[x['fieldname']]['text'] 
							if formato[x['fieldname']].has_key('text') 
							else x['fieldname'].capitalize(),)
					gui.TextBox(name='txt'+x['fieldname'], 
						top=nTop, 
						left='130', 
						mask=formato[x['fieldname']].get('mask', ''),
						width=formato[x['fieldname']].get('width', '100'),
						)
				else:
					gui.Label(name='lbl'+x['fieldname'], top=nTop, 
						text=x['fieldname'].replace('_',' ').capitalize())
					gui.TextBox(name='txt'+x['fieldname'], top=nTop, 
						left='130', 
						width=x['length']*13,
						mask=mask
						)
				self.controls['txt'+x['fieldname']] = \
					{'name':'txt'+x['fieldname'], 'field':x['fieldname']}
				nTop = str(int(nTop)+30)
				fila += 1
				if formato.has_key(x['fieldname']):
					if formato[x['fieldname']].has_key('id') \
							and formato[x['fieldname']]['id']:
						panel['record']['txt'+x['fieldname']].onblur = \
							self.on_id_change
						self.controls['id'] = \
							{'name':'txt'+x['fieldname'], 'field':x['fieldname']}

	def button_press_create(self, evt):
		pass

	
	def button_press_update(self, evt):
		param = {}
		controles = self.controls
		for d in controles.iterkeys():
			ctrl = panel['record'][controles[d]['name']]
			if d != 'id':
				param[controles[d]['field']] = ctrl.value
			else:
				valorid = ctrl.value
		
		if not self.nuevo:
			self.db(self.db[self.tabla]._id==valorid).update(**param)
		else:
			self.db[self.tabla].insert(**param)
		
		self.db.commit()
		gui.alert("Datos grabados correctamente")
		if DEBUG:
			print self.db._lastsql
		

	def button_press_delete(self, evt):
		if gui.confirm("Desea borrar el registro seleccionado?", "Sistema"):
			ctrl = panel['record'][self.controls['id']['name']]
			self.db(self.db[self.tabla]._id == ctrl.value).delete()
			if DEBUG:
				print self.db._lastsql
			self.db.commit()
		
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
		miregistro = self.tabla[ctrl.value]
		
		if miregistro is None:
			self.nuevo = True
		else:
			for x in self.controls.itervalues():
				ctrl = panel['record'][x['name']]
				ctrl.value = miregistro[x['field']]
			self.nuevo = False
		
	def existe_tabla(self):
		cur = self.con.cursor()
		try:
			cur.execute("select * from " + self.tabla)
			return True
		except:
			return False
