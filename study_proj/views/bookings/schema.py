import colander


class BookingPost(colander.MappingSchema):
    book_ref = colander.SchemaNode(colander.String(),
                                   validator=colander.Length(6))
    book_date = colander.SchemaNode(colander.DateTime())
    total_amount = colander.SchemaNode(colander.Decimal())


class BookingPut(colander.MappingSchema):
    book_date = colander.SchemaNode(colander.DateTime(), missing=colander.drop)
    total_amount = colander.SchemaNode(colander.Decimal(), validator=colander.Range(min=0), missing=colander.drop)
