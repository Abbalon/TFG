#!venv/bin/python3
# -*- code: utf-8 -*-
from sqlalchemy import UniqueConstraint
from werkzeug.security import generate_password_hash, check_password_hash

from PiHome import db
from PiHome.dataBase import BaseDB


class User(BaseDB):
    """
        Modelo de datos del usuario
    """

    #: Nombre de tabla
    __tablename__ = 'users'
    __table_args__ = (
        UniqueConstraint("name", "email"),
    )

    group_Id = db.Column(
        db.Integer,
        db.ForeignKey('groups.id'),
        nullable=False)
    name = db.Column(
        db.String(25))
    label = db.Column(
        db.String(25))
    email = db.Column(
        db.String(56),
        unique=True)
    password = db.Column(
        db.String(255),
        nullable=False)
    validated = db.Column(
        db.Boolean,
        default=False,
        nullable=False)

    #: Establece la relación con la tabla 'groups'
    group = db.relationship(
        'Group',
        lazy='select',
        backref='User')

    def __init__(self, name, email, password, label=None, group_id=1, validated=False, **kwargs):
        """
            Inicializa un usuario

            Por defecto:
                - Tiene que contener los datos requeridos del formulario 'log_in':
                    - Nombre
                    - Email
                    - Password
                - No tiene ningún 'label' asignado
                - Pertenece al grupo 'Estandar'
        """

        super(User, self).__init__(**kwargs)

        _hash_str = self.__hash_pwd(password)

        self.group_Id = group_id
        self.name = name
        self.label = label
        self.password = _hash_str
        self.validated = validated
        self.email = email

    @staticmethod
    def __hash_pwd(password):
        """
            Metodo privado para generar el 'hash' del usuario
        """
        return generate_password_hash(password)

    def verificar_hash(self, password):
        """
            Metodo público para contrastar los 'hash´s' de las pwd
        """
        return check_password_hash(self.password, password)

    @staticmethod
    def get_mails_of_groups(id_groups: []):
        """Recupera una lista de los emaiĺ de los usuarios que pertenezcan a los grupos indicados por parámetro

        ---
        :param id_groups: Lista con los grupos de los que se desea obtener los mail de los usuarios
        :return: list: Lista de los mail de los usuarios que pertenecen a ese grupo

        """
        users = User.query.filter(User.group_Id.in_(id_groups)).all()
        mails = []
        for user in users:
            mails.append(user.email)

        return mails

    @staticmethod
    def is_validated(id_user):
        """Informa si el usuario con la id informada por parámetro, está validado

        ---

        :return:
            - True, si el usuario está validado;
            - False, si no está validado;
            - None, si no existe el usuario
        :param id_user: Id del usuario del que se desea conocer si está validado
        """

        response = None
        try:
            response = User.query.filter(User.id == id_user).first()
        except :
            pass

        return response

    @staticmethod
    def get_by_id(id_user):
        return User.query.filter_by(id=id_user).first()
