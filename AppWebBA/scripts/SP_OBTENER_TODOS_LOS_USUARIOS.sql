CREATE PROCEDURE SP_OBTENER_TODOS_LOS_USUARIOS
AS
BEGIN
	SELECT 
		*
	FROM 
	PerfilUsuario per
	INNER JOIN auth_user usu ON per.user_id = usu.id
END