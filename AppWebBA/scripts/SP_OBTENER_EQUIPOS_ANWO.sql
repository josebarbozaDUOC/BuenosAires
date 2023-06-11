SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
IF (OBJECT_ID('SP_OBTENER_EQUIPOS_ANWO', 'P') IS NOT NULL) DROP PROCEDURE SP_OBTENER_EQUIPOS_ANWO
GO
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
GO