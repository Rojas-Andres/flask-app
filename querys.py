class Query():
    def valida_user_int(self,username):
        query = f"""
        select count(*) 
	    from usuario us inner join intentos 
        inte on us.id=inte.username_id where us.username='{username}';	
        """
        return query
    def intentos(self,username):
        query=f"""
        select
            case
                when u.cant_intentos = i.intentos_act then 1
                else 0
            end
		from
			usuario u
		inner join intentos i on
			u.id = i.username_id where u.username='{username}';
        """
        return query
    def insertar_user_intentos(self,us):
        query=f"""
        insert into intentos(username_id,intentos_act)
		select us.id , 1 from usuario us where us.username = '{us}' ;
        """
        return query
    def devuelve_id_usuario(self,username):
        query = f"""
        select id from usuario where username='{username}'
        """
        return query
    def actualiza_intentos(self,us_id):
        query=f"""
        update intentos set intentos_act = intentos_act+1 where username_id={us_id}
        """
        return query
    def update_password(self,username,password):
        query=f"""
            update usuario set password='{password}' where username='{username}'
        """
        return query
    def actualizar_intentos(self,username_id):
        query=f"""
            update intentos set intentos_act=0
            where username_id={username_id}
        """
        return query
    def insertar_contra_guardadas(self,username_id,password):
        query=f"""
            INSERT INTO "contrasGuardadas"(username_id,password)
            values
            ({username_id},'{password}')
        """ 
        return query
    def obtener_todas_pass_user(self,username_id):
        query=f"""
            select password from "contrasGuardadas" where username_id ='{username_id}'
        """
        return query