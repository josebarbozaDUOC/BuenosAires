from django.db import connection

SP_COMPRA = """
CREATE PROCEDURE SP_COMPRA
    @nrofac INT,
    @rutcli VARCHAR(20),
    @idprod INT,
    @descfac VARCHAR(300),
    @monto INT,
    @nrogd INT,
    @nrosol INT,
    @tiposol VARCHAR(50),
    @fechavisita DATE,
    @ruttec VARCHAR(20),
    @descsol VARCHAR(200)
AS
BEGIN
	SET @nrofac		= (SELECT (MAX(nrofac)+1) FROM Factura)
	SET @nrogd		= (SELECT (MAX(nrogd)+11) FROM GuiaDespacho)
	SET @nrosol		= (SELECT (MAX(nrosol)+111) FROM SolicitudServicio)
	SET @ruttec		= (SELECT TOP 1 ruttec FROM SolicitudServicio GROUP BY ruttec ORDER BY COUNT(*) ASC)

	-- IF @tiposol = 'Instalación' SET @monto += 25000

	-- Si la solicitud es instalación...
	IF @tiposol = 'Instalación' SET @descfac = (SELECT nomprod FROM Producto WHERE idprod = @idprod)
	ELSE SET @descfac = @tiposol

    -- Insertar datos en la tabla Factura
    INSERT INTO Factura (nrofac, rutcli, idprod, fechafac, descfac, monto)
    VALUES (@nrofac, @rutcli, @idprod, GETDATE(), @descfac, @monto)

	-- Insertar datos en la tabla GuiaDespacho
	IF @tiposol = 'Instalación'
		INSERT INTO GuiaDespacho (nrogd, nrofac, idprod, estadogd)
		VALUES (@nrogd, @nrofac, @idprod, 'En bodega')

	-- Si la solicitud es instalación...else, tomo de parámetros
	IF @tiposol = 'Instalación' SET @descsol = 'Instalar equipo' SET @fechavisita = DATEADD(day, 1, GETDATE())

    -- Insertar datos en la tabla SolicitudServicio
    INSERT INTO SolicitudServicio (nrosol, nrofac, tiposol, fechavisita, ruttec, descsol, estadosol)
    VALUES (@nrosol, @nrofac, @tiposol, @fechavisita, @ruttec, @descsol, 'Aceptada')
END
"""


SP_OBTENER_FACTURAS = """
CREATE PROCEDURE SP_OBTENER_FACTURAS
    @tipousu VARCHAR(50),
    @rut     VARCHAR(50)
AS
BEGIN
	SET NOCOUNT ON;

	IF (@tipousu = 'Cliente')
	select * from Factura
		where Factura.rutcli = @rut
		ORDER BY 
			Factura.fechafac;

	
	IF (@tipousu = 'Administrador')
		select * from Factura
		ORDER BY 
			Factura.fechafac;
END
"""

SP_OBTENER_STOCK = """
CREATE PROCEDURE SP_OBTENER_STOCK
AS
BEGIN
	SET NOCOUNT ON;

    SELECT
		s.idstock, p.idprod, p.nomprod, p.descprod,p.precio,p.imagen, f.nrofac, 
		CASE 
			WHEN f.nrofac IS NOT NULL 
			THEN 'Vendido'
			ELSE 'En bodega'
		END AS 'estado'
	FROM 
		StockProducto s 
		INNER JOIN Producto p ON s.idprod = p.idprod
		LEFT OUTER JOIN Factura  f ON s.nrofac = f.nrofac
END
"""

SP_OBTENER_EQUIPOS_ANWO = """
CREATE PROCEDURE SP_OBTENER_EQUIPOS_ANWO
AS
BEGIN
	SET NOCOUNT ON;

    Select a.nroserieanwo AS 'Nro Serie',
		a.nomprodanwo AS 'Producto',
		FORMAT(a.precioanwo, 'C0') AS 'Precio',
		CASE
			WHEN a.reservadoba = 'S'
			THEN 'Si'
			ELSE 'No'
			END AS 'Reservado'
    from AnwoListaProducto a;
END
"""

SP_RESERVAR_EQUIPO_ANWO = """
CREATE PROCEDURE SP_RESERVAR_EQUIPO_ANWO
    @nroserie VARCHAR(50)
AS
BEGIN
	SET NOCOUNT ON;

    Update AnwoListaProducto
    Set reservadoba = CASE WHEN reservadoba = 'N' THEN 'S' ELSE 'N' END
    where nroserieanwo = @nroserie;
END
"""

SP_OBTENER_GUIAS_DE_DESPACHO = """
CREATE PROCEDURE SP_OBTENER_GUIAS_DE_DESPACHO
AS
BEGIN
	SET NOCOUNT ON;

    Select g.nrogd AS 'Nro GD', 
        p.nomprod AS Producto, 
        FORMAT (f.fechafac, 'dd/MM/yyyy ') AS 'Fecha GD',  
        g.estadogd AS 'Estado GD', 
        g.nrofac AS 'Nro Fac', 
        u.first_name+' ' +u.last_name AS Cliente
    from GuiaDespacho g 
    LEFT JOIN producto p ON g.idprod = p.idprod
    LEFT JOIN factura f ON g.nrofac = f.nrofac
    JOIN PerfilUsuario pu ON f.rutcli = pu.rut
    JOIN auth_user u ON pu.user_id = u.id;
END
"""

SP_MODIFICAR_ESTADO_GUIA_DE_DESPACHO = """
CREATE PROCEDURE SP_MODIFICAR_ESTADO_GUIA_DE_DESPACHO
    @nro VARCHAR(50),
    @estado VARCHAR(50)
AS
BEGIN
	SET NOCOUNT ON;

    Update GuiaDespacho
    Set estadogd = @estado
    where nrogd = @nro;
END
"""

SP_OBTENER_EQUIPOS_EN_BODEGA = """
CREATE PROCEDURE SP_OBTENER_EQUIPOS_EN_BODEGA
AS
BEGIN
	SET NOCOUNT ON;

    SELECT
		s.idstock, p.idprod, p.nomprod, f.nrofac, 
		CASE 
			WHEN f.nrofac IS NOT NULL 
			THEN 'Vendido'
			ELSE 'En bodega'
		END AS 'estado'
	FROM 
		StockProducto s 
		INNER JOIN Producto p ON s.idprod = p.idprod
		LEFT OUTER JOIN Factura  f ON s.nrofac = f.nrofac
END
"""

SP_OBTENER_PRODUCTOS = """
CREATE PROCEDURE SP_OBTENER_PRODUCTOS 
AS
BEGIN
	SET NOCOUNT ON;

	SELECT * FROM Producto

END
"""

SP_OBTENER_SOLICITUDES_DE_SERVICIO = """
CREATE PROCEDURE SP_OBTENER_SOLICITUDES_DE_SERVICIO
	@tipousu VARCHAR(50),
	@rut     VARCHAR(50)
AS
BEGIN
	/*
		Ejemplos de ejecución del procedimiento:
		EXEC SP_OBTENER_SOLICITUDES_DE_SERVICIO 'Técnico', '6666-6'
		EXEC SP_OBTENER_SOLICITUDES_DE_SERVICIO 'Técnico', '7777-7'
		EXEC SP_OBTENER_SOLICITUDES_DE_SERVICIO 'Técnico', '8888-8'
		EXEC SP_OBTENER_SOLICITUDES_DE_SERVICIO 'Cliente', '1111-1'
		EXEC SP_OBTENER_SOLICITUDES_DE_SERVICIO 'Todos', ''
	*/

	IF (@tipousu = 'Técnico')
		SELECT 
			sol.nrosol, 
			usucli.first_name + ' '  + usucli.last_name AS nomcli, 
			sol.tiposol,
			sol.fechavisita, 
			'10:00:00'                                  AS hora,
			usutec.first_name + ' '  + usutec.last_name AS nomtec,
			sol.descsol       + ': ' + fac.descfac      AS descser,
			sol.estadosol
		FROM 
			SolicitudServicio sol 
			INNER JOIN Factura       fac    ON sol.nrofac     = fac.nrofac
			INNER JOIN PerfilUsuario percli ON fac.rutcli     = percli.rut
			INNER JOIN PerfilUsuario pertec ON sol.ruttec     = pertec.rut
			INNER JOIN auth_user     usucli ON percli.user_id =  usucli.id
			INNER JOIN auth_user     usutec ON pertec.user_id =  usutec.id
		WHERE
			pertec.rut = @rut
		ORDER BY 
			usucli.first_name

	IF (@tipousu = 'Cliente')
		SELECT 
			sol.nrosol, 
			usucli.first_name + ' '  + usucli.last_name AS nomcli, 
			sol.tiposol,
			sol.fechavisita, 
			'10:00:00'                                  AS hora,
			usutec.first_name + ' '  + usutec.last_name AS nomtec,
			sol.descsol       + ': ' + fac.descfac      AS descser,
			sol.estadosol
		FROM 
			SolicitudServicio sol 
			INNER JOIN Factura       fac    ON sol.nrofac     = fac.nrofac
			INNER JOIN PerfilUsuario percli ON fac.rutcli     = percli.rut
			INNER JOIN PerfilUsuario pertec ON sol.ruttec     = pertec.rut
			INNER JOIN auth_user     usucli ON percli.user_id =  usucli.id
			INNER JOIN auth_user     usutec ON pertec.user_id =  usutec.id
		WHERE
			percli.rut = @rut
		ORDER BY 
			usutec.first_name

	IF (@tipousu = 'Todos')
		SELECT 
			sol.nrosol, 
			usucli.first_name + ' '  + usucli.last_name AS nomcli, 
			sol.tiposol,
			sol.fechavisita, 
			'10:00:00'                                  AS hora,
			usutec.first_name + ' '  + usutec.last_name AS nomtec,
			sol.descsol       + ': ' + fac.descfac      AS descser,
			sol.estadosol
		FROM 
			SolicitudServicio sol 
			INNER JOIN Factura       fac    ON sol.nrofac     = fac.nrofac
			INNER JOIN PerfilUsuario percli ON fac.rutcli     = percli.rut
			INNER JOIN PerfilUsuario pertec ON sol.ruttec     = pertec.rut
			INNER JOIN auth_user     usucli ON percli.user_id =  usucli.id
			INNER JOIN auth_user     usutec ON pertec.user_id =  usutec.id
		ORDER BY
			usucli.first_name,
			usutec.first_name
END
"""

SP_OBTENER_TODOS_LOS_USUARIOS = """
CREATE PROCEDURE SP_OBTENER_TODOS_LOS_USUARIOS
AS
BEGIN
	SELECT 
		*
	FROM 
	PerfilUsuario per
	INNER JOIN auth_user usu ON per.user_id = usu.id
END
"""

def exec_sql(query):
    with connection.cursor() as cursor:
        cursor.execute(query)

def run():

    # Poblar tabla Producto

    exec_sql("INSERT INTO dbo.Producto (idprod, nomprod, descprod, precio, imagen) VALUES (1,N'Aire Wifi 9000 btu',  N'Enfría 9-16 m2',     299990,'images/0001.png');")
    exec_sql("INSERT INTO dbo.Producto (idprod, nomprod, descprod, precio, imagen) VALUES (2,N'Split Inv 12000 btu', N'Frío/Calor AR12',    450000,'images/0002.png');")
    exec_sql("INSERT INTO dbo.Producto (idprod, nomprod, descprod, precio, imagen) VALUES (3,N'Anwo VP',             N'9000 Virus Protect', 288990,'images/0003.png');")
    exec_sql("INSERT INTO dbo.Producto (idprod, nomprod, descprod, precio, imagen) VALUES (4,N'Anwo Portátil',       N'12000 btu f/c',      131990,'images/0004.png');")
    exec_sql("INSERT INTO dbo.Producto (idprod, nomprod, descprod, precio, imagen) VALUES (5,N'GPORT-14',            N'Anwo 14000 btu',     399990,'images/0005.png');")
    exec_sql("INSERT INTO dbo.Producto (idprod, nomprod, descprod, precio, imagen) VALUES (6,N'Kendal 12000',        N'Climat 22-24 m2',    335990,'images/0006.png');")
    exec_sql("INSERT INTO dbo.Producto (idprod, nomprod, descprod, precio, imagen) VALUES (7,N'Kendal Wifi 4000',    N'Climat 32-34 m2',    335990,'images/0006.png');")
    exec_sql("INSERT INTO dbo.Producto (idprod, nomprod, descprod, precio, imagen) VALUES (8,N'Anwo 12000',          N'Climat 42-44 m2',    335990,'images/0006.png');")

    # Poblar tabla PerfilUsuario

    exec_sql("INSERT INTO dbo.PerfilUsuario (rut, tipousu, dirusu, user_id) VALUES (N'1234-5',  N'Superusuario',  N'La Florida',  1);")
    exec_sql("INSERT INTO dbo.PerfilUsuario (rut, tipousu, dirusu, user_id) VALUES (N'1111-1',  N'Cliente',       N'La Florida',  2);")
    exec_sql("INSERT INTO dbo.PerfilUsuario (rut, tipousu, dirusu, user_id) VALUES (N'2222-2',  N'Cliente',       N'Santiago',    3);")
    exec_sql("INSERT INTO dbo.PerfilUsuario (rut, tipousu, dirusu, user_id) VALUES (N'3333-3',  N'Cliente',       N'Providencia', 4);")
    exec_sql("INSERT INTO dbo.PerfilUsuario (rut, tipousu, dirusu, user_id) VALUES (N'4444-4',  N'Cliente',       N'Las Condes',  5);")
    exec_sql("INSERT INTO dbo.PerfilUsuario (rut, tipousu, dirusu, user_id) VALUES (N'5555-5',  N'Cliente',       N'Maipú',       6);")
    exec_sql("INSERT INTO dbo.PerfilUsuario (rut, tipousu, dirusu, user_id) VALUES (N'6666-6',  N'Técnico',       N'Cerro Navia', 7);")
    exec_sql("INSERT INTO dbo.PerfilUsuario (rut, tipousu, dirusu, user_id) VALUES (N'7777-7',  N'Técnico',       N'Peñalolén',   8);")
    exec_sql("INSERT INTO dbo.PerfilUsuario (rut, tipousu, dirusu, user_id) VALUES (N'8888-8',  N'Técnico',       N'La Reina',    9);")
    exec_sql("INSERT INTO dbo.PerfilUsuario (rut, tipousu, dirusu, user_id) VALUES (N'9999-9',  N'Bodeguero',     N'La Florida',  10);")
    exec_sql("INSERT INTO dbo.PerfilUsuario (rut, tipousu, dirusu, user_id) VALUES (N'0000-0',  N'Administrador', N'La Reina',    11);")

    # Poblar tabla Factura

    exec_sql("INSERT INTO dbo.Factura (nrofac, rutcli, idprod, fechafac, descfac, monto) VALUES (1, N'1111-1', 1, CAST('20220223' AS datetime), N'Aire Wifi 9000 btu',  25000);")
    exec_sql("INSERT INTO dbo.Factura (nrofac, rutcli, idprod, fechafac, descfac, monto) VALUES (2, N'2222-2', 2, CAST('20220224' AS datetime), N'Split Inv 12000 btu', 450000);")
    exec_sql("INSERT INTO dbo.Factura (nrofac, rutcli, idprod, fechafac, descfac, monto) VALUES (3, N'3333-3', 4, CAST('20220303' AS datetime), N'Anwo Portátil',       25000);")
    exec_sql("INSERT INTO dbo.Factura (nrofac, rutcli, idprod, fechafac, descfac, monto) VALUES (4, N'4444-4', 4, CAST('20220308' AS datetime), N'Anwo Portátil',       25000);")
    exec_sql("INSERT INTO dbo.Factura (nrofac, rutcli, idprod, fechafac, descfac, monto) VALUES (5, N'5555-5', 4, CAST('20220315' AS datetime), N'Anwo Portátil',       25000);")
    exec_sql("INSERT INTO dbo.Factura (nrofac, rutcli, idprod, fechafac, descfac, monto) VALUES (6, N'1111-1', 5, CAST('20220327' AS datetime), N'Mantención',          25000);")
    exec_sql("INSERT INTO dbo.Factura (nrofac, rutcli, idprod, fechafac, descfac, monto) VALUES (7, N'1111-1', 5, CAST('20220403' AS datetime), N'GPORT-14',            25000);")
    exec_sql("INSERT INTO dbo.Factura (nrofac, rutcli, idprod, fechafac, descfac, monto) VALUES (8, N'1111-1', 3, CAST('20220408' AS datetime), N'Anwo VP',             25000);")
    exec_sql("INSERT INTO dbo.Factura (nrofac, rutcli, idprod, fechafac, descfac, monto) VALUES (9, N'1111-1', 5, CAST('20220415' AS datetime), N'GPORT-14',            25000);")

    # Poblar tabla GuiaDespacho

    exec_sql("INSERT INTO dbo.GuiaDespacho (nrogd, nrofac, idprod, estadogd) VALUES (11, 1, 1, N'Entregado');")
    exec_sql("INSERT INTO dbo.GuiaDespacho (nrogd, nrofac, idprod, estadogd) VALUES (22, 2, 2, N'Despachado');")
    exec_sql("INSERT INTO dbo.GuiaDespacho (nrogd, nrofac, idprod, estadogd) VALUES (88, 8, 3, N'EnBodega');")

    # Poblar tabla SolicitudServicio

    exec_sql("INSERT INTO dbo.SolicitudServicio (nrosol, nrofac, tiposol, fechavisita, ruttec, descsol, estadosol) VALUES (111, 1, N'Instalación', CAST('20220302 09:00' AS datetime), N'6666-6', N'Instalar equipo', N'Cerrada');")
    exec_sql("INSERT INTO dbo.SolicitudServicio (nrosol, nrofac, tiposol, fechavisita, ruttec, descsol, estadosol) VALUES (222, 2, N'Instalación', CAST('20220303 10:00' AS datetime), N'6666-6', N'Instalar equipo', N'Aceptada');")
    exec_sql("INSERT INTO dbo.SolicitudServicio (nrosol, nrofac, tiposol, fechavisita, ruttec, descsol, estadosol) VALUES (333, 3, N'Mantención',  CAST('20220310 15:00' AS datetime), N'6666-6', N'Cambiar enchufe', N'Aceptada');")
    exec_sql("INSERT INTO dbo.SolicitudServicio (nrosol, nrofac, tiposol, fechavisita, ruttec, descsol, estadosol) VALUES (444, 4, N'Mantención',  CAST('20220315 09:00' AS datetime), N'6666-6', N'Limpiar filtro',  N'Aceptada');")
    exec_sql("INSERT INTO dbo.SolicitudServicio (nrosol, nrofac, tiposol, fechavisita, ruttec, descsol, estadosol) VALUES (555, 5, N'Reparación',  CAST('20220322 17:00' AS datetime), N'6666-6', N'Reparar equipo',  N'Aceptada');")
    exec_sql("INSERT INTO dbo.SolicitudServicio (nrosol, nrofac, tiposol, fechavisita, ruttec, descsol, estadosol) VALUES (666, 6, N'Mantención',  CAST('20220403 11:00' AS datetime), N'7777-7', N'Limpiar filtro',  N'Cerrada');")
    exec_sql("INSERT INTO dbo.SolicitudServicio (nrosol, nrofac, tiposol, fechavisita, ruttec, descsol, estadosol) VALUES (777, 7, N'Reparación',  CAST('20220410 16:00' AS datetime), N'6666-6', N'Reparar aire',    N'Modificada');")
    exec_sql("INSERT INTO dbo.SolicitudServicio (nrosol, nrofac, tiposol, fechavisita, ruttec, descsol, estadosol) VALUES (888, 8, N'Instalación', CAST('20220415 10:00' AS datetime), N'7777-7', N'Instalar equipo', N'Modificada');")
    exec_sql("INSERT INTO dbo.SolicitudServicio (nrosol, nrofac, tiposol, fechavisita, ruttec, descsol, estadosol) VALUES (999, 9, N'Reparación',  CAST('20220422 18:00' AS datetime), N'8888-8', N'Enchufe quemado', N'Aceptada');")

    # Poblar tabla StockProducto

    exec_sql("INSERT INTO dbo.StockProducto (idstock, idprod, nrofac) VALUES (11111, 1, 1);")
    exec_sql("INSERT INTO dbo.StockProducto (idstock, idprod, nrofac) VALUES (22222, 2, 2);")
    exec_sql("INSERT INTO dbo.StockProducto (idstock, idprod, nrofac) VALUES (88888, 3, 8);")
    exec_sql("INSERT INTO dbo.StockProducto (idstock, idprod, nrofac) VALUES (90001, 1, null);")
    exec_sql("INSERT INTO dbo.StockProducto (idstock, idprod, nrofac) VALUES (90002, 3, null);")
    exec_sql("INSERT INTO dbo.StockProducto (idstock, idprod, nrofac) VALUES (90003, 4, null);")
    exec_sql("INSERT INTO dbo.StockProducto (idstock, idprod, nrofac) VALUES (90004, 6, null);")
    exec_sql("INSERT INTO dbo.StockProducto (idstock, idprod, nrofac) VALUES (90005, 1, null);")
    exec_sql("INSERT INTO dbo.StockProducto (idstock, idprod, nrofac) VALUES (90006, 3, null);")
    exec_sql("INSERT INTO dbo.StockProducto (idstock, idprod, nrofac) VALUES (90007, 4, null);")

    # Poblar tabla ANWOLISTAPRODUCTO

    exec_sql("INSERT INTO dbo.ANWOLISTAPRODUCTO (NROSERIEANWO, NOMPRODANWO, PRECIOANWO, RESERVADOBA) VALUES ('A1', 'Aire Anwo 111',  '500000', 'N');")
    exec_sql("INSERT INTO dbo.ANWOLISTAPRODUCTO (NROSERIEANWO, NOMPRODANWO, PRECIOANWO, RESERVADOBA) VALUES ('A2', 'Aire Anwo 222',  '400000', 'N');")
    exec_sql("INSERT INTO dbo.ANWOLISTAPRODUCTO (NROSERIEANWO, NOMPRODANWO, PRECIOANWO, RESERVADOBA) VALUES ('A3', 'Aire Anwo 333',  '300000', 'S');")
    exec_sql("INSERT INTO dbo.ANWOLISTAPRODUCTO (NROSERIEANWO, NOMPRODANWO, PRECIOANWO, RESERVADOBA) VALUES ('A4', 'Aire Anwo 444',  '200000', 'S');")
    exec_sql("INSERT INTO dbo.ANWOLISTAPRODUCTO (NROSERIEANWO, NOMPRODANWO, PRECIOANWO, RESERVADOBA) VALUES ('A5', 'Aire Anwo 555',  '500000', 'N');")
    exec_sql("INSERT INTO dbo.ANWOLISTAPRODUCTO (NROSERIEANWO, NOMPRODANWO, PRECIOANWO, RESERVADOBA) VALUES ('A6', 'Aire Anwo 666',  '400000', 'N');")
    exec_sql("INSERT INTO dbo.ANWOLISTAPRODUCTO (NROSERIEANWO, NOMPRODANWO, PRECIOANWO, RESERVADOBA) VALUES ('A7', 'Aire Anwo 777',  '300000', 'S');")
    exec_sql("INSERT INTO dbo.ANWOLISTAPRODUCTO (NROSERIEANWO, NOMPRODANWO, PRECIOANWO, RESERVADOBA) VALUES ('A8', 'Aire Anwo 888',  '200000', 'S');")
    exec_sql("INSERT INTO dbo.ANWOLISTAPRODUCTO (NROSERIEANWO, NOMPRODANWO, PRECIOANWO, RESERVADOBA) VALUES ('A9', 'Aire Anwo 999',  '500000', 'N');")

    try:
        exec_sql(SP_COMPRA)
    except:
        pass

    try:
        exec_sql(SP_OBTENER_FACTURAS)
    except:
        pass
    
    try:
        exec_sql(SP_OBTENER_STOCK)
    except:
        pass
    
    try:
        exec_sql(SP_OBTENER_EQUIPOS_ANWO)
    except:
        pass
    
    try:
        exec_sql(SP_RESERVAR_EQUIPO_ANWO)
    except:
        pass

    try:
        exec_sql(SP_OBTENER_GUIAS_DE_DESPACHO)
    except:
        pass

    try:
        exec_sql(SP_MODIFICAR_ESTADO_GUIA_DE_DESPACHO)
    except:
        pass

    try:
        exec_sql(SP_OBTENER_EQUIPOS_EN_BODEGA)
    except:
        pass

    try:
        exec_sql(SP_OBTENER_PRODUCTOS)
    except:
        pass

    try:
        exec_sql(SP_OBTENER_SOLICITUDES_DE_SERVICIO)
    except:
        pass
    
try:
    exec_sql(SP_OBTENER_TODOS_LOS_USUARIOS)
except:
    pass

    
