from gluon.fileutils import read_file

response.menu = [['Register Person', False, URL('register_person')],
                 ['Register Dog', False, URL('register_dog')],
                 ['Register Product', False, URL('register_product')],
                 ['Buy product', False, URL('buy')]]


def register_person():
    """ simple person registration form with validation and database.insert()
        also lists all records currently in the table"""

    def get_manuall_id(request):
        last_id = db.dog.id.max()
        request.vars.id = 55

    # create an insert form from the table
    form = SQLFORM(db.person)

    # if form correct perform the insert
    if form.process(onvalidation=get_manuall_id).accepted:
        response.flash = 'new record inserted'

    # and get a list of all persons
    records = SQLTABLE(db().select(db.person.ALL),headers='fieldname:capitalize')

    return dict(form=form, records=records)

def register_crud_person():
    def get_manuall_id(form):
        last_id = db.dog.id.max()
        form.vars.id = last_id
        print last_id

def person_report():

    response.title = "web2py sample listing"
    
    # define header and footers:
    head = THEAD(TR(TH("No",_width="5%"), 
                    TH("Header 2",_width="30%"),
                    TH("Header 3",_width="20%"), 
                    _bgcolor="#A0A0A0"))
    #foot = TFOOT(TR(TH("Footer 1",_width="5%"), 
    #                TH("Footer 2",_width="30%"),
    #                TH("Footer 3",_width="20%"),
    #                _bgcolor="#E0E0E0"))
    
    # create several rows:
    rows = []
    for i in range(1000):
        col = i % 2 and "#F0F0F0" or "#FFFFFF"
        rows.append(TR(TD("Row %s" %i),
                       TD("something", _align="center"),
                       TD("%s" % i, _align="right"),
                       _bgcolor=col)) 

    # make the table object
    body = TBODY(*rows)
    table = TABLE(*[head, body], 
                  _border="1", _align="center", _width="100%")
    pdf = MyFPDF()
    pdf.add_page()
    pdf.write_html(str(XML(table,sanitize=False)))
    response.headers['Content-Type'] = 'application/pdf'
    return pdf.output(dest='S')

def register_dog():
    """ simple person registration form with validation and database.insert()
        also lists all records currently in the table"""

    form = SQLFORM(db.dog)
    if form.process().accepted:
        response.flash = 'new record inserted'
    download = URL('download')  # to see the picture
    records = SQLTABLE(db().select(db.dog.ALL), upload=download,
                       headers='fieldname:capitalize')
    return dict(form=form, records=records)


def register_product():
    """ simple person registration form with validation and database.insert()
        also lists all records currently in the table"""

    form = SQLFORM(db.product)
    if form.process().accepted:
        response.flash = 'new record inserted'
    records = SQLTABLE(db().select(db.product.ALL),
                       headers='fieldname:capitalize')
    return dict(form=form, records=records)


def buy():
    """ uses a form to query who is buying what. validates form and
        updates existing record or inserts new record in purchases """

    form = SQLFORM.factory(
        Field('buyer_id',requires=IS_IN_DB(db,db.person.id,'%(name)s')),
        Field('product_id',requires=IS_IN_DB(db,db.product.id,'%(name)s')),
        Field('quantity','integer',requires=IS_INT_IN_RANGE(1,100)))
    if form.process().accepted:
        # get previous purchese
        purchase = db((db.purchase.buyer_id == form.vars.buyer_id)&
            (db.purchase.product_id==form.vars.product_id)).select().first()

        if purchase:
            # if list contains a record, update that record
            purchase.update_record(
                quantity = purchase.quantity+form.vars.quantity)
        else:
            # self insert a new record in table
            db.purchase.insert(buyer_id=form.vars.buyer_id,
                               product_id=form.vars.product_id,
                               quantity=form.vars.quantity)
        response.flash = 'product purchased!'
    elif form.errors:
        response.flash = 'invalid values in form!'

    # now get a list of all purchases
    records = SQLTABLE(db(purchased).select(),headers='fieldname:capitalize')
    return dict(form=form, records=records)


def delete_purchased():
    """ delete all records in purchases """
    db(db.purchase.id > 0).delete()
    redirect(URL('buy'))

def download():
    """ used to download uploaded files """
    return response.download(request,db)

