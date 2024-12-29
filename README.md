El propósito de este proyecto es desarrollar una arquitectura en AWS que permita recolectar información sobre la calidad del aire mediante técnicas de web scraping. Utilizaremos el sitio web [troposfera.es](https://troposfera.es/datos/dev-albacete/#/dashboard) como nuestra principal fuente de datos. Con la información obtenida, podremos realizar un monitoreo en tiempo real de la calidad del aire en Albacete y generaremos un documento con los valores obtenidos en los distintos puntos de la ciudad. 
Este proyecto puede ser aplicable a múltiples casos de uso tales como un Sistema de Transporte Inteligente con el fin de minimizar el tráfico o el tránsito de personas en áreas de la ciudad con alta contaminación atmosférica.

![AWS Architecture here](https://github.com/mbrazalez/aws-airquality-monitior/blob/main/diagrama.png)

- **Paso 1:** Definiremos cada cuánto queremos que se ejecute la lambda que se encargará del web scraping usando un schedule event.
- **Paso 2:** Utilizaremos el servicio de AWS EventBridge con el schedule previamente configurado, para programar la ejecución de la función lambda que contiene el código para realizar el web scraping que se encargará de recopilar los datos de la página web mencionada anteriormente.
- **Paso 3:** Los datos recopilados se almacenarán en una base de datos NoSQL de AWS DynamoDB.
- **Paso 4:** Cuando se almacenen nuevos datos en la DynamoDB se disparará una lambda encargada de generar reportes con estos datos
- **Paso 5** Los reportes generados por la lambda se almacenan como PDF en un bucket S3
- **Paso 6** Los PDFs pueden ser consultados por un usuario accediendo al bucket
- **Paso 7:** Al añadir un nuevo pdf al S3, se disparará una lambda encargada de enviar una notificación a un usuario a través del servicio de mensajería SNS.
- **Paso 8:** La función lambda se encarga de enviar la notificación al tópico de SNS, para que los usuarios suscritos reciban un email indicando que se ha almacenado en la base de datos nueva información relacionada con la calidad del aire.
- **Paso 9** El usuario recibe un email indicándole que se ha generado un nuevo PDF en el S3 Bucket.
