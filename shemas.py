from marshmallow import Schema, fields, validate

class TrainersSchema(Schema):
    idtrainer = fields.Integer(required = True)
    name = fields.String(required = True, validate = validate.Length(max = 45))
    size = fields.Float(required = True)
    price = fields.Float(required = True)
    img_urls = fields.List(fields.String(required = True), required = True, validate = validate.Length(max = 500))


class OrderSchema(Schema):
    idorder = fields.Integer(required = True)
    delivery_adress = fields.String(required = True, validate = validate.Length(max = 45))
    status = fields.String(required = True, validate = validate.OneOf(["confirmation", "shipping", "completed"]))
    user_id = fields.Integer(required = True)


class UserSchema(Schema):
    iduser = fields.Integer(required = True)
    username = fields.String(required = True, validate = validate.Length(max = 45))
    full_name = fields.String(required = True, validate = validate.Length(max = 45))
    phone_number = fields.String(required = True, validate = validate.Length(max = 45))
    email = fields.Email(required = True, validate = validate.Length(max = 45))
    password = fields.String(required = True, validate = validate.Length(max = 100))
