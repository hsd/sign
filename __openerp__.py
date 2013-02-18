# (c) Copyright 2008-today Marcel van der Boom. All Rights Reserved. 
# 
# Meta information about the signs module
{
    "name"       : "Signs",
    "version"    : "1.0",
    "author"     : "HSD",
    "category"   : "Generic",
    "website"    : "http://www.hsdev.com",
    "url"        : "http://www.hsdev.com",
    "sequence"   : 2,
    'description': """
Electronic signs, to be linked to other objects 
===============================================
Create a model for electronic signs to be attached to other objects.
    
Typical usage:
--------------
* legislative labeling products
* safety and warnings signs for substances

Envisioned functionality:
-------------------------
* dynamic image generation
* image manipulation depending on object linkage
    """,
    "depends"    : ["base","product"],
    "init_xml"   : [],                      
    "update_xml" : [
        "sign_view.xml",
        "security/ir.model.access.csv"
    ],
    "images" : [],
    "qweb" : [],
    "js" : [],
    "css" : [],
    "active"     : False,
    "installable": True
}
