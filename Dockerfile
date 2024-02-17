# Usar una imagen oficial de Python como imagen base
FROM python:3.10-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /usr/src/app

# Copiar el contenido del directorio actual en el contenedor en /usr/src/app
COPY . .

# Instalar cualquier otro paquete necesario especificado en requirements.txt
# Se usa --no-cache-dir para no almacenar los archivos de caché de pip, reduciendo el tamaño de la imagen
RUN pip install --no-cache-dir -r requirements.txt

# Hacer disponible el puerto 8000 al mundo exterior a este contenedor
# Esto no publica el puerto, solo indica que el puerto está destinado a ser publicado
EXPOSE 8081

# Ejecutar app.py cuando se inicie el contenedor
# uvicorn se usa como servidor ASGI para ejecutar la aplicación FastAPI
CMD ["streamlit", "run", "app.py", "--server.port", "8081", "--server.address=0.0.0.0"]
