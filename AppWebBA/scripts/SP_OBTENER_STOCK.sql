SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
IF (OBJECT_ID('SP_OBTENER_STOCK', 'P') IS NOT NULL) DROP PROCEDURE SP_OBTENER_STOCK
GO
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
GO