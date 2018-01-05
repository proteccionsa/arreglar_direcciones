
import re
traducciones = [\
            ('.', ''),

            ('K ' , 'Cra. '),\
            ('CR ', 'Cra. '),\
            ('CRA ','Cra. '),\
            ('CARRERA', 'Cra.'),\

            ('CL ', 'Cl. '),\
            ('C ' , 'Cl. '),\
            ('CALLE ', 'Cl. '),\
            ('CALL ', 'Cl. '),\

            ('TR ', 'Tv. '),\

            ('AV ', 'Av. '),\

            ('CQ ', 'Cq.'),\

            ('DIAGONAL ', 'Dg. '),\

            (' N° ', ' '),\
            (' NRO ', ' '),
            (' NR ', ' '),
            (' NO ', ' '),
            (' Ñ ', ' '),
            ('#', ' '),
            
            ('  ', ' '),
                
            ('AA', 'A'),
            ('BB', 'B'),
            ('CC', 'C'),
            ('DD', 'D'),
            ('EE', 'E'),
            ('FF', 'F'),
                
            ('-', ' ')
]

class Direccion():
    def __init__(self):
        self.i = {'ppal_tipo' : None,
            'ppal_numero' : None,
            'ppal_letra' : None,
            'ppal_sector' : None,

            'seg_numero' : None,
            'seg_letra' : None,
            'seg_sector' : None,

            'nd' : None,}
    
    def isvalid(self):
        return  self.i['ppal_tipo'] is not None and\
                self.i['ppal_numero'] is not None and \
                self.i['seg_numero'] is not None
            
            
    def txt(self):
        txt = '{ppal_tipo} {ppal_numero}{ppal_letra} {ppal_sector} # {seg_numero}{seg_letra} {seg_sector}-{nd}'\
                .format(**{k: v if v is not None else '' for k, v in self.i.items()})
        while txt.find('  ') >= 0:
            txt = txt.replace('  ', ' ')
        return txt

    
separa_numeros = re.compile(r'([1-9])([a-zA-Z])', re.IGNORECASE)
separa_letra_sector = re.compile(r'([A-F])([NS])', re.IGNORECASE)

def arreglar_direccion(dire):
    if dire == "":
        return None
    
    dire = dire.upper()
    dire = separa_numeros.sub(r'\1 \2', dire)
    dire = separa_letra_sector.sub(r'\1 \2', dire)
    
    for mala_palabra, traduccion in traducciones:
        while dire.find(mala_palabra) >= 0:
            dire = dire.replace(mala_palabra, traduccion)
    
    d = Direccion()
    
    for parte in dire.split(' '):
        '''print('--', parte)
        
        for k in d.i:
            if d.i[k] is not None:
                print('  ', k, ' -> ', d.i[k])
                print(d.i['ppal_tipo'] is not None and d.i['ppal_numero'] is None and d.i['seg_numero'] is None)
                print(parte.isnumeric())
        '''
        if d.i['ppal_tipo'] is None and d.i['ppal_numero'] is None:
            if parte in {'Cra.', 'Cl.', 'Cq.', 'Dg.', 'Tv.', 'Av.'}:
                d.i['ppal_tipo'] = parte
        elif d.i['ppal_tipo'] is not None and d.i['ppal_numero'] is None and d.i['seg_numero'] is None:
            if parte.isnumeric():
                d.i['ppal_numero'] = parte
        elif d.i['ppal_tipo'] is not None and d.i['ppal_numero'] is not None and d.i['seg_numero'] is None:
            if not parte.isnumeric():
                if parte in {'A', 'B', 'C', 'D', 'E', 'F'}:
                    d.i['ppal_letra'] = parte
                elif parte in {'SUR', 'S'}:
                    d.i['ppal_sector'] = 'Sur'
                elif parte in {'NORTE', 'NTE', 'N'}:
                    d.i['ppal_sector'] = 'norte'
            else:
                d.i['seg_numero'] = parte
        elif d.i['ppal_tipo'] is not None and d.i['ppal_numero'] is not None and d.i['seg_numero'] is not None and d.i['nd'] is None:
            if not parte.isnumeric():
                if parte in {'A', 'B', 'C', 'D', 'E', 'F'}:
                    d.i['seg_letra'] = parte
                elif parte in {'SUR', 'S'}:
                    d.i['seg_sector'] = 'Sur'
                elif parte in {'NORTE', 'NTE', 'N'}:
                    d.i['seg_sector'] = 'norte'
            else:
                d.i['nd'] = parte
    
    return d.txt() if d.isvalid() else dire