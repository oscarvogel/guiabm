#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from core.crud import crud

formato = {
	'cuit':{'width':100, 'text':'CUIT', 'mask':'##-########-#', 'id':True},
	'denominacion':{'width':300, 'text':u'Denominación'},
}

def main():
	abm = crud(tabla='clientes', 
		basedatos=os.path.join('modelos','pyfactura.db'),
		formato=formato)

if __name__ == '__main__':
	main()
	
