SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
IF (OBJECT_ID('SP_COMPRA', 'P') IS NOT NULL) DROP PROCEDURE SP_COMPRA
GO
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
GO