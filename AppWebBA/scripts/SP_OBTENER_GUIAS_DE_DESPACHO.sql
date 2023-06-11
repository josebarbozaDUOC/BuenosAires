SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
IF (OBJECT_ID('SP_OBTENER_GUIAS_DE_DESPACHO', 'P') IS NOT NULL) DROP PROCEDURE SP_OBTENER_GUIAS_DE_DESPACHO
GO
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
GO