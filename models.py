from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Tabla: Convenios_Instituciones
class ConveniosInstituciones(db.Model):
    __tablename__ = 'convenios_instituciones'
    id = db.Column(db.Integer, primary_key=True)
    nombre_institucion = db.Column(db.String(200), nullable=False)
    pais = db.Column(db.String(100), nullable=False)

# Tabla: Convenios
class Convenios(db.Model):
    __tablename__ = 'convenios'
    id = db.Column(db.Integer, primary_key=True)
    tipo_convenio = db.Column(db.String(100))
    objeto = db.Column(db.Text)
    resultado = db.Column(db.Text)
    detalles_vigencia = db.Column(db.Text)
    institucion_id = db.Column(db.Integer, db.ForeignKey('convenios_instituciones.id', ondelete="CASCADE"))
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)

    institucion = db.relationship("ConveniosInstituciones", backref="convenios")

# Tabla: Extensión_Años
class ExtensionAnos(db.Model):
    __tablename__ = 'extension_anos'
    id = db.Column(db.Integer, primary_key=True)
    ano = db.Column(db.Integer, nullable=False)
    num_profesores = db.Column(db.Integer)
    num_estudiantes = db.Column(db.Integer)
    poblacion_atendida = db.Column(db.Integer)

# Tabla: Extensión
class Extension(db.Model):
    __tablename__ = 'extension'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    objeto = db.Column(db.Text)
    extension_anual_id = db.Column(db.Integer, db.ForeignKey('extension_anos.id', ondelete="CASCADE"))

    extension_ano = db.relationship("ExtensionAnos", backref="extensiones")

# Tabla: Movilidad
class Movilidad(db.Model):
    __tablename__ = 'movilidad'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    apellido = db.Column(db.String(100))
    identificacion = db.Column(db.String(50), unique=True)
    tipo_identificacion = db.Column(db.String(50))
    tipo_persona = db.Column(db.String(50))  # Estudiante o Profesor
    institucion_destino = db.Column(db.String(200))
    pais = db.Column(db.String(50))
    tipo_estadia = db.Column(db.String(50))
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    tiempo_estadia = db.Column(db.Integer)
    movilidad_tipo = db.Column(db.String(50))  # Entrante o Saliente

# Tabla: Proyectos de Investigación
class ProyectosInvestigacion(db.Model):
    __tablename__ = 'proyectos_investigacion'
    id = db.Column(db.Integer, primary_key=True)
    proyecto_nombre = db.Column(db.String(200), nullable=False)
    ano_inicio = db.Column(db.Integer)
    estado = db.Column(db.String(50))
    fecha_finalizacion = db.Column(db.Date)
    publicaciones = db.Column(db.Text)
    aplicaciones_derivadas = db.Column(db.Text)
    entidad_financiadora = db.Column(db.String(200))
    investigador_principal = db.Column(db.String(100))
    autores = db.Column(db.Text)  # Lista de autores como texto
    tipo_fuente_financiacion = db.Column(db.String(100))
    fuente_financiacion = db.Column(db.String(200))
    observaciones = db.Column(db.Text)

# Tabla: Innovaciones
class Innovaciones(db.Model):
    __tablename__ = 'innovaciones'
    id = db.Column(db.Integer, primary_key=True)
    autores = db.Column(db.Text)  # Lista de autores como texto
    innovacion = db.Column(db.Text)
    beneficiarios = db.Column(db.Text)
    aplicacion_efectiva = db.Column(db.Text)
    ano = db.Column(db.Integer)

# Tabla: Grupos de Investigación
class GruposInvestigacion(db.Model):
    __tablename__ = 'grupos_investigacion'
    id = db.Column(db.Integer, primary_key=True)
    nombre_grupo = db.Column(db.String(200), nullable=False)
    clasificacion = db.Column(db.String(50))
    codigo = db.Column(db.String(100))
    lineas_investigacion = db.Column(db.Text)
    proyectos_recursos_publicos = db.Column(db.Integer)
    proyectos_recursos_privados = db.Column(db.Integer)
    articulos_revistas_indexadas = db.Column(db.Integer)
    articulos_revistas_no_indexadas = db.Column(db.Integer)
    libros_capitulos = db.Column(db.Integer)
    patentes = db.Column(db.Integer)
    productos_creacion = db.Column(db.Integer)
    productos_totales = db.Column(db.Integer)
    estudiantes_vinculados = db.Column(db.Integer)
    profesores_vinculados = db.Column(db.Integer)
