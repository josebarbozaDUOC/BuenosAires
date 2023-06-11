SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
IF (OBJECT_ID('SP_OBTENER_FACTURAS', 'P') IS NOT NULL) DROP PROCEDURE SP_OBTENER_FACTURAS
GO
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
GO