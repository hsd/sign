#(c) Copyright 2008 Marcel van der Boom. All Rights Reserved. 
from osv import osv, fields

#
# Like products and partners we slice signs in categories
# @todo I tried inheriting, but it didnt make things clearer IMO
class sign_category(osv.osv):
  # @todo: cant we inherit this from the res.partner.category class?
  def name_get(self, cr, uid, ids, context={}):
    # do we have anything to do?
    if not len(ids):
      return []
    # if so, read em
    reads = self.read(cr, uid, ids, ['name','parent_id'], context)
    res = []
    # start by the name and prepend the parents
    for record in reads:
      name = record['name']
      if record['parent_id']:
        name = record['parent_id'][1]+' / '+name
      res.append((record['id'], name))
    return res
    
  # This is the functional field
  # @todo: cant we inherit this from the res.partner.category class?
  def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, unknow_dict):
    res = self.name_get(cr, uid, ids)
    return dict(res)
    
  # We need to overide this method as the SQL is slightly different here.
  def _check_recursion(self, cr, uid, ids):
    level = 100
    while len(ids):
      cr.execute('select distinct parent_id from sign_category where id in ('+','.join(map(str,ids))+')')
      ids = filter(None, map(lambda x:x[0], cr.fetchall()))
      if not level:
        return False
      level -= 1
    return True    
  _name        = 'sign.category'
  _description = 'Sign Categories'
  _columns = {
    'name': fields.char('Category Name', required=True, size=64, translate=True),
    'parent_id': fields.many2one('sign.category', 'Parent Category', select=True),
    'child_ids': fields.one2many('sign.category', 'parent_id', 'Childs Category'),
    'complete_name': fields.function(_name_get_fnc, method=True, type="char", string='Name'),
    'active' : fields.boolean('Active')
  }
  _constraints = [
    (_check_recursion, 'Error ! You can not create recursive categories.', ['parent_id'])
  ]
  _defaults = {
    'active' : lambda *a: 1
  }
  _order = 'parent_id,name'
sign_category()

#
# Sign object definition
class sign_sign(osv.osv):
  _name = "sign.sign"
  _description = "Signs"
  _columns = {
    'name'     : fields.char('Name', size=256, required=True,select=1, translate=True),
    'code'     : fields.char('Code', size=8, select=1),
    'type'     : fields.selection( [
            ('fire', "Fire fighting"),
            ('informational','Informational'),
            ('mandatory','Mandatory'), 
            ('warning','Warning'), 
            ('prohibition','Prohibition'), 
            ('safe', 'Safety routing'),
            ('transport', 'Transport')
        ], 'Sign Type', translate=True),
    'category_id': fields.many2many('sign.category', 'sign_category_rel', 'sign_id', 'category_id', 'Categories'),
    'image'    : fields.binary('Image'),
    'regulated'  : fields.boolean('Regulated', required=True),
    'active' : fields.boolean('Active'),
    'notes': fields.text('Notes')
  }
  _defaults = {
    # This default is a 300x300 png image transparaent, decreased in size by pngcrush 
    'image' : lambda *a: 'iVBORw0KGgoAAAANSUhEUgAAASwAAAEsAQMAAABDsxw2AAAABlBMVEUAAAAAAAClZ7nPAAAAAXRS\nTlMAQObYZgAAABl0RVh0U29mdHdhcmUAQWRvYmUgSW1hZ2VSZWFkeXHJZTwAAAAiSURBVHja7cEx\nAQAAAMKg9U9tCj+gAAAAAAAAAAAAAAB4GS20AAEBlVMEAAAAAElFTkSuQmCC\n',
    #'image' : lambda *a: 'iVBORw0KGgoAAAANSUhEUgAAASwAAAEsCAMAAABOo35HAAAABlBMVEX///8AAABVwtN+AAAAAXRS\nTlMAQObYZgAAABl0RVh0U29mdHdhcmUAQWRvYmUgSW1hZ2VSZWFkeXHJZTwAAABtSURBVHja7cEB\nAQAAAIIg/69uSEABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADwbmDLAAEQxsW9AAAAAElF\nTkSuQmCC\n'
    'regulated' : lambda *a: True,
    'active'    : lambda *a: True
  }
  # Note: sql constraint may not be updated automatically on change!
  _sql_constraints = [
    ('ident', 'UNIQUE(name)', 'The name of the symbol must be unique')
  ]
sign_sign()