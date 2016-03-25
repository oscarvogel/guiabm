#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  pagos.py
#  
#  Copyright 2016 Jose Oscar Vogel <oscarvogel@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

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
	
