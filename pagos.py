#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from core.crud import crud
from pydal import DAL, Field

##db = DAL('mysql://root:fasca@192.168.0.200/fasa', migrate=False)

db = DAL('sqlite://'+os.path.join('modelos','pyfactura.db'), migrate=False)

db.define_table('pagos',
	Field('pago', 'string', length=2, required=True,),
	Field('detalle', 'string', length=40, required=True,),
	Field('dia', 'date', length=8),
	Field('des1', 'decimal(12,2)', length=10),
	primarykey=['pago'],
)

formato = {'pago':{'width':30, 'text':'Pagos', 'id':True},
}

def main():
	abm = crud(tabla=db.pagos, 
		basedatos=db,
		formato=formato,
        )

if __name__ == '__main__':
	main()
	
