# app.py

from flask import Flask, render_template, request, redirect, url_for, flash, Response
from models import db, Movilidad, Convenios, ConveniosInstituciones, Extension, ExtensionAnos, ProyectosInvestigacion, Innovaciones, GruposInvestigacion
from config import Config
import csv

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Inicializar la base de datos
    db.init_app(app)
    
    # Crear todas las tablas en la base de datos (solo la primera vez)
    with app.app_context():
        db.create_all()
    
    # Definir rutas dentro de create_app
    @app.route("/")
    def index():
        return render_template("index.html")
    
    # Ruta para Movilidad
    @app.route('/movilidad', methods=['GET', 'POST'])
    def movilidad():
        if request.method == 'POST':
            # Obtener los datos del formulario para añadir movilidad
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            identificacion = request.form['identificacion']
            tipo_persona = request.form['tipo_persona']
            institucion_destino = request.form['institucion_destino']
            pais = request.form['pais']
            tipo_estadia = request.form['tipo_estadia']
            fecha_inicio = request.form['fecha_inicio']
            fecha_fin = request.form['fecha_fin']
            movilidad_tipo = request.form['movilidad_tipo']
            
            # Crear nuevo registro de movilidad
            nueva_movilidad = Movilidad(
                nombre=nombre,
                apellido=apellido,
                identificacion=identificacion,
                tipo_persona=tipo_persona,
                institucion_destino=institucion_destino,
                pais=pais,
                tipo_estadia=tipo_estadia,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                movilidad_tipo=movilidad_tipo
            )
            
            db.session.add(nueva_movilidad)
            db.session.commit()
            flash("Registro de movilidad añadido exitosamente.")
            return redirect(url_for('movilidad'))
    
        # Obtener el filtro desde la solicitud GET
        tipo_persona = request.args.get('tipo_persona')
    
        # Aplicar el filtro a los registros de movilidad
        if tipo_persona in ['estudiante', 'profesor']:
            movilidades = Movilidad.query.filter_by(tipo_persona=tipo_persona).all()
        else:
            movilidades = Movilidad.query.all()  # Sin filtro (todos los registros)
    
        return render_template('movilidad.html', movilidades=movilidades, tipo_persona=tipo_persona)
    
    # Ruta para Convenios
    @app.route("/convenios", methods=["GET", "POST"])
    def convenios():
        if request.method == "POST":
            tipo_convenio = request.form["tipo_convenio"]
            objeto = request.form["objeto"]
            resultado = request.form["resultado"]
            detalles_vigencia = request.form["detalles_vigencia"]
            institucion_id = request.form["institucion_id"]
            fecha_inicio = request.form["fecha_inicio"]
            fecha_fin = request.form["fecha_fin"]
    
            nuevo_convenio = Convenios(
                tipo_convenio=tipo_convenio,
                objeto=objeto,
                resultado=resultado,
                detalles_vigencia=detalles_vigencia,
                institucion_id=institucion_id,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin
            )
            db.session.add(nuevo_convenio)
            db.session.commit()
            flash("Convenio añadido correctamente.")
            return redirect(url_for("convenios"))
    
        registros = Convenios.query.all()
        instituciones = ConveniosInstituciones.query.all()  # Para seleccionar instituciones en el formulario
        return render_template("convenios.html", convenios=registros, instituciones=instituciones)
    
    # Ruta para Convenios_Instituciones
    @app.route("/convenios_instituciones", methods=["GET", "POST"])
    def convenios_instituciones():
        if request.method == "POST":
            nombre_institucion = request.form["nombre_institucion"]
            pais = request.form["pais"]
    
            nueva_institucion = ConveniosInstituciones(
                nombre_institucion=nombre_institucion,
                pais=pais
            )
            db.session.add(nueva_institucion)
            db.session.commit()
            flash("Institución añadida correctamente.")
            return redirect(url_for("convenios_instituciones"))
    
        registros = ConveniosInstituciones.query.all()
        return render_template("convenios_instituciones.html", convenios_instituciones=registros)
    
    # Ruta para Extensión
    @app.route("/extension", methods=["GET", "POST"])
    def extension():
        if request.method == "POST":
            nombre = request.form["nombre"]
            objeto = request.form["objeto"]
            extension_anual_id = request.form["extension_anual_id"]
    
            nueva_extension = Extension(
                nombre=nombre,
                objeto=objeto,
                extension_anual_id=extension_anual_id
            )
            db.session.add(nueva_extension)
            db.session.commit()
            flash("Extensión añadida correctamente.")
            return redirect(url_for("extension"))
    
        registros = Extension.query.all()
        extension_anos = ExtensionAnos.query.all()
        return render_template("extension.html", extension=registros, extension_anos=extension_anos)
    
    # Ruta para Extensión_Años
    @app.route("/extension_anos", methods=["GET", "POST"])
    def extension_anos():
        if request.method == "POST":
            ano = request.form["ano"]
            num_profesores = request.form["num_profesores"]
            num_estudiantes = request.form["num_estudiantes"]
            poblacion_atendida = request.form["poblacion_atendida"]
    
            nueva_extension_ano = ExtensionAnos(
                ano=ano,
                num_profesores=num_profesores,
                num_estudiantes=num_estudiantes,
                poblacion_atendida=poblacion_atendida
            )
            db.session.add(nueva_extension_ano)
            db.session.commit()
            flash("Año de Extensión añadido correctamente.")
            return redirect(url_for("extension_anos"))
    
        registros = ExtensionAnos.query.all()
        return render_template("extension_anos.html", extension_anos=registros)
    
    # Ruta para Proyectos de Investigación
    @app.route("/proyectos_investigacion", methods=["GET", "POST"])
    def proyectos_investigacion():
        if request.method == "POST":
            proyecto_nombre = request.form["proyecto_nombre"]
            ano_inicio = request.form["ano_inicio"]
            estado = request.form["estado"]
            fecha_finalizacion = request.form["fecha_finalizacion"]
            publicaciones = request.form["publicaciones"]
            aplicaciones_derivadas = request.form["aplicaciones_derivadas"]
            entidad_financiadora = request.form["entidad_financiadora"]
            investigador_principal = request.form["investigador_principal"]
            autores = request.form["autores"]
            tipo_fuente_financiacion = request.form["tipo_fuente_financiacion"]
            fuente_financiacion = request.form["fuente_financiacion"]
            observaciones = request.form["observaciones"]
    
            nuevo_proyecto = ProyectosInvestigacion(
                proyecto_nombre=proyecto_nombre,
                ano_inicio=ano_inicio,
                estado=estado,
                fecha_finalizacion=fecha_finalizacion,
                publicaciones=publicaciones,
                aplicaciones_derivadas=aplicaciones_derivadas,
                entidad_financiadora=entidad_financiadora,
                investigador_principal=investigador_principal,
                autores=autores,
                tipo_fuente_financiacion=tipo_fuente_financiacion,
                fuente_financiacion=fuente_financiacion,
                observaciones=observaciones
            )
            db.session.add(nuevo_proyecto)
            db.session.commit()
            flash("Proyecto de Investigación añadido correctamente.")
            return redirect(url_for("proyectos_investigacion"))
    
        registros = ProyectosInvestigacion.query.all()
        return render_template("proyectos_investigacion.html", proyectos=registros)
    
    # Ruta para Innovaciones
    @app.route("/innovaciones", methods=["GET", "POST"])
    def innovaciones():
        if request.method == "POST":
            autores = request.form["autores"]
            innovacion = request.form["innovacion"]
            beneficiarios = request.form["beneficiarios"]
            aplicacion_efectiva = request.form["aplicacion_efectiva"]
            ano = request.form["ano"]
    
            nueva_innovacion = Innovaciones(
                autores=autores,
                innovacion=innovacion,
                beneficiarios=beneficiarios,
                aplicacion_efectiva=aplicacion_efectiva,
                ano=ano
            )
            db.session.add(nueva_innovacion)
            db.session.commit()
            flash("Innovación añadida correctamente.")
            return redirect(url_for("innovaciones"))
    
        registros = Innovaciones.query.all()
        return render_template("innovaciones.html", innovaciones=registros)
    
    # Ruta para Grupos de Investigación
    @app.route("/grupos_investigacion", methods=["GET", "POST"])
    def grupos_investigacion():
        if request.method == "POST":
            nombre_grupo = request.form["nombre_grupo"]
            clasificacion = request.form["clasificacion"]
            codigo = request.form["codigo"]
            lineas_investigacion = request.form["lineas_investigacion"]
            proyectos_recursos_publicos = request.form["proyectos_recursos_publicos"]
            proyectos_recursos_privados = request.form["proyectos_recursos_privados"]
            articulos_revistas_indexadas = request.form["articulos_revistas_indexadas"]
            articulos_revistas_no_indexadas = request.form["articulos_revistas_no_indexadas"]
            libros_capitulos = request.form["libros_capitulos"]
            patentes = request.form["patentes"]
            productos_creacion = request.form["productos_creacion"]
            productos_totales = request.form["productos_totales"]
            estudiantes_vinculados = request.form["estudiantes_vinculados"]
            profesores_vinculados = request.form["profesores_vinculados"]
    
            nuevo_grupo = GruposInvestigacion(
                nombre_grupo=nombre_grupo,
                clasificacion=clasificacion,
                codigo=codigo,
                lineas_investigacion=lineas_investigacion,
                proyectos_recursos_publicos=proyectos_recursos_publicos,
                proyectos_recursos_privados=proyectos_recursos_privados,
                articulos_revistas_indexadas=articulos_revistas_indexadas,
                articulos_revistas_no_indexadas=articulos_revistas_no_indexadas,
                libros_capitulos=libros_capitulos,
                patentes=patentes,
                productos_creacion=productos_creacion,
                productos_totales=productos_totales,
                estudiantes_vinculados=estudiantes_vinculados,
                profesores_vinculados=profesores_vinculados
            )
            db.session.add(nuevo_grupo)
            db.session.commit()
            flash("Grupo de Investigación añadido correctamente.")
            return redirect(url_for("grupos_investigacion"))
    
        registros = GruposInvestigacion.query.all()
        return render_template("grupos_investigacion.html", grupos=registros)
    
    
    ##########################################
    ##### Implementación de descarga CSV #####
    ##########################################
    
    
    # Lista de modelos y sus atributos que queremos exportar
    MODELOS = {
        "movilidad": (Movilidad, ["nombre", "apellido", "identificacion", "tipo_persona", "institucion_destino", "pais", "tipo_estadia", "fecha_inicio", "fecha_fin", "movilidad_tipo"]),
        "convenios": (Convenios, ["tipo_convenio", "objeto", "resultado", "detalles_vigencia", "institucion_id", "fecha_inicio", "fecha_fin"]),
        "convenios_instituciones": (ConveniosInstituciones, ["nombre_institucion", "pais"]),
        "extension": (Extension, ["nombre", "objeto", "extension_anual_id"]),
        "extension_anos": (ExtensionAnos, ["ano", "num_profesores", "num_estudiantes", "poblacion_atendida"]),
        "proyectos_investigacion": (ProyectosInvestigacion, ["proyecto_nombre", "ano_inicio", "estado", "fecha_finalizacion", "publicaciones", "aplicaciones_derivadas", "entidad_financiadora", "investigador_principal", "autores", "tipo_fuente_financiacion", "fuente_financiacion", "observaciones"]),
        "innovaciones": (Innovaciones, ["autores", "innovacion", "beneficiarios", "aplicacion_efectiva", "ano"]),
        "grupos_investigacion": (GruposInvestigacion, ["nombre_grupo", "clasificacion", "codigo", "lineas_investigacion", "proyectos_recursos_publicos", "proyectos_recursos_privados", "articulos_revistas_indexadas", "articulos_revistas_no_indexadas", "libros_capitulos", "patentes", "productos_creacion", "productos_totales", "estudiantes_vinculados", "profesores_vinculados"])
    }
    
    @app.route("/descargar/<tabla>")
    def descargar_csv(tabla):
        if tabla not in MODELOS:
            flash("Tabla no encontrada.")
            return redirect(url_for("index"))
    
        modelo, campos = MODELOS[tabla]
    
        registros = modelo.query.all()
    
        # Crear la respuesta CSV
        def generar():
            # Escribir el encabezado
            datos = [",".join(campos) + "\n"]
            # Escribir los registros
            for registro in registros:
                valores = [str(getattr(registro, campo)) for campo in campos]
                datos.append(",".join(valores) + "\n")
            return "".join(datos)
    
        response = Response(generar(), mimetype='text/csv')
        response.headers.set("Content-Disposition", f"attachment; filename={tabla}.csv")
        return response
    
    
    ###############################################
    ##### Implementación de descarga Filtrado #####
    ###############################################
    
    @app.route('/descargar_csv_filtrado')
    def descargar_csv_filtrado():
        tipo_persona = request.args.get('tipo_persona')
        
        # Filtra los registros según el tipo de persona si se especifica, o todos si no hay filtro
        if tipo_persona in ['estudiante', 'profesor']:
            registros = Movilidad.query.filter_by(tipo_persona=tipo_persona).all()
        else:
            registros = Movilidad.query.all()  # Recuperar todos los registros desde la base de datos
    
        # Genera el CSV a partir de todos los registros filtrados en la base de datos
        def generar_csv():
            campos = [
                "nombre", "apellido", "identificacion", "tipo_persona", 
                "institucion_destino", "pais", "tipo_estadia", 
                "fecha_inicio", "fecha_fin", "movilidad_tipo"
            ]
            yield ",".join(campos) + "\n"
            for registro in registros:
                valores = [str(getattr(registro, campo)) for campo in campos]
                yield ",".join(valores) + "\n"
    
        nombre_archivo = f"{tipo_persona if tipo_persona else 'todos'}_movilidad.csv"
        response = Response(generar_csv(), mimetype='text/csv')
        response.headers.set("Content-Disposition", f"attachment; filename={nombre_archivo}")
        return response
    
    return app

# Opcional: Ejecutar la aplicación localmente
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
