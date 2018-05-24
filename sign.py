# Signs are graphical represenation of things like safety and traffic signs.
# Copyright (C) 2013-2018 Marcel van der Boom <marcel@hsdev.com> HS-Development BV
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from openerp import models, fields, api

import logging
logger = logging.getLogger(__name__)

# Signs are images / pictograms which can be linked to other object,
# typically products. Although the focus in this module will be on
# safety signs, the module is generally applicable.

# Signs are given a type. A sign can only be designated one type. The
# purpose of this field is to allow other modules to quickly select
# and process signs based on their type.
class sign_type(models.Model):
  _name        = 'sign.type'
  _description = ' Sign types'

  # Fields for sign types
  name         = fields.Char(required=True)
  description  = fields.Text()
  regulated    = fields.Boolean(default=False)
  active       = fields.Boolean(default=True)

  _sql_constraints = [
    ('name', 'UNIQUE(name)', 'Names for sign types must be unique')
  ]

# Sign object definition
class sign_sign(models.Model):
  _name        = "sign.sign"
  _description = "Signs"

  # Define fields
  desc = fields.Char(size=256, required=True, translate=True)
  name = fields.Char(string = 'Code', size=8, required=True)

  type_id  = fields.Many2one(string = 'Type', comodel_name = 'sign.type', required=True,
                             help ='Type designation is ISO/DIN terminology')
  image       = fields.Binary(help="The default rendering of the pictogram.")

  # Mostly for future features (like rendering on labels -> black and white)
  default_rendering = fields.Selection( [   ('asis',  "Unchanged from source"),
                                            ('bw'  , "In black and white")],
                                        default = 'asis',
                                        string = 'Default rendering',
                                        required=True, help="How should the sign be rendered by default?")
  regulated = fields.Boolean(default=True, help="Is this sign defined in regulation? (For example: EC/1272/2008)")
  reference = fields.Char(help="Given a legislated sign, where is it defined. Typically a standard or law identifcation.")
  active    = fields.Boolean(default = True)
  notes     = fields.Text()

  _defaults = {
    # This default is a 300x300 png image transparent, decreased in size by pngcrush
    'image' : lambda *a: 'iVBORw0KGgoAAAANSUhEUgAAASwAAAEsAQMAAABDsxw2AAAABlBMVEUAAAAAAAClZ7nPAAAAAXRS\nTlMAQObYZgAAABl0RVh0U29mdHdhcmUAQWRvYmUgSW1hZ2VSZWFkeXHJZTwAAAAiSURBVHja7cEx\nAQAAAMKg9U9tCj+gAAAAAAAAAAAAAAB4GS20AAEBlVMEAAAAAElFTkSuQmCC\n',
    #'image' : lambda *a: 'iVBORw0KGgoAAAANSUhEUgAAASwAAAEsCAMAAABOo35HAAAABlBMVEX///8AAABVwtN+AAAAAXRS\nTlMAQObYZgAAABl0RVh0U29mdHdhcmUAQWRvYmUgSW1hZ2VSZWFkeXHJZTwAAABtSURBVHja7cEB\nAQAAAIIg/69uSEABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADwbmDLAAEQxsW9AAAAAElF\nTkSuQmCC\n'
  }
  # Note: sql constraint may not be updated automatically on change!
  _sql_constraints = [
    ('name', 'UNIQUE(name)', ('Each code for a sign must be unique.'))
  ]

# We provide the product integration integrally. Split this into a
# Define the link model
class product_signinfo(models.Model):
  _name = 'product.signinfo'
  _description = 'Sign information for products'

  # Link to the product and the sign
  product_tmpl_id = fields.Many2one('product.template', string = 'Product', required=True, ondelete='cascade')
  sign_id  = fields.Many2one('sign.sign', string = 'Sign', required=True)

  # Allow reordering per product.
  sequence   = fields.Integer(default = 1)

  # For form design, we include these related fields
  type       = fields.Char(related = 'sign_id.type_id.name')
  image      = fields.Binary(related = 'sign_id.image')
  desc       = fields.Char(related = 'sign_id.desc')

  # Get the product code in here for sorting and identification
  product_code = fields.Char(related = 'product_tmpl_id.default_code', store=True)

  # By default, sort by priority (only relavant from products point of view)
  _order = 'sequence'

# Access from the product object to signs
class product_signs(models.Model):
   _name = 'product.template'
   _inherit = 'product.template'

   # Make sure we can link to signs from products.
   sign_ids = fields.One2many(comodel_name = 'product.signinfo',
                              inverse_name = 'product_tmpl_id', string='Signs')
