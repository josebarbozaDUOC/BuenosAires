# BuenosAires
 IntegracionPlataformasDuoc_G4

Aplicación de Escritorio: VentaBA

- Login (permite sólo a actores Vendedor y Administrador)
- Consume el web service (api rest) ws.validar_login_escritorio, el cual comprueba las credenciales en conjunto a su tipo de usuario.
![image](https://github.com/josebarbozaDUOC/BuenosAires/assets/101838235/a2148bb3-58ea-4724-b406-8cac92072e0b)

- Ventana Principal (Muestra todos los productos en la Bodega de Buenos Aires en conjunto a su Estado de disponibilidad)
- Consume el web service (api rest) ws.obtener_productos_en_bodega, el cual ejecuta un procedimiento almacenado el cual devuelve la query.
![image](https://github.com/josebarbozaDUOC/BuenosAires/assets/101838235/a25a7e66-d343-4239-99d3-3846aaa68096)


Aplicación de Escritorio: BodegaBA

- Login (permite sólo a actores Bodeguero y Administrador)
- Consume el web service (api rest) ws.validar_login_escritorio, el cual comprueba las credenciales en conjunto a su tipo de usuario.
![image](https://github.com/josebarbozaDUOC/BuenosAires/assets/101838235/ae0735b9-cd19-4b65-9edc-af981ba5f5ff)

- Ventana Principal (menú)
![image](https://github.com/josebarbozaDUOC/BuenosAires/assets/101838235/612bfb40-0ce4-4d35-8b8f-90115f9ec9a7)

- Ventana Guías de despacho (Muestra todas las guías de despacho de Buenos Aires, se puede modificar su estado presionando un botón del apartado opciones)
- Consume el web service (api rest) ws.obtener_guias_de_despacho, el cual ejecuta un procedimiento almacenado el cual devuelve la query.
- Consume el web service (api rest) ws.modificar_estado_guia_de_despacho, el cual ejecuta un procedimiento almacenado con parámetros, haciendo un update en la base de datos correspondiente a nrogd y estadogd.
![image](https://github.com/josebarbozaDUOC/BuenosAires/assets/101838235/78c52312-72dd-4e90-988e-fafb9edb96ed)

- Imprimir la guía de despacho
![image](https://github.com/josebarbozaDUOC/BuenosAires/assets/101838235/7b309b75-ea94-4a7a-b073-7e9938270b11)

- Ventana Adm Bodega (Muestra todos los productos en la Bodega de Buenos Aires en conjunto a su Estado de disponibilidad)
- Consume el web service (api rest) ws.obtener_productos_en_bodega, el cual ejecuta un procedimiento almacenado el cual devuelve la query.
![image](https://github.com/josebarbozaDUOC/BuenosAires/assets/101838235/97240858-354d-4c1f-84e3-61e7e791466d)

- Ventana Equipos ANWO (Muestra todas los equipos del proveedor ANWO, se puede reservar presionando un botón del apartado opciones)
- Consume el web service (SOAP) ws.obtener_equipos_anwo, el cual viaja por las diferentes capas, hasta la capa de datos y ejecuta un procedimiento almacenado el cual devuelve la query, se agrega a respuesta el cual viaja verticalmente hasta la capa de presentación en un formato XML.
- Consume el web service (SOAP) ws.reservar_equipo_anwo, el cual viaja por las diferentes capas, hasta la capa de datos y ejecuta un procedimiento almacenado con parámetros, haciendo un update en la base de datos correspondiente a nroserie y reservado.
![image](https://github.com/josebarbozaDUOC/BuenosAires/assets/101838235/acf18e30-262d-44fa-9146-a99aea19b99a)
